"""Implementation of Workflow."""
import os
from typing import AbstractSet, Any, Collection, List, Mapping, Optional, Tuple, Type, Union

import ansys.common.variableinterop as acvi
import ansys.engineeringworkflow.api as engapi
import grpc
from grpc import Channel
import numpy as np
from numpy.typing import ArrayLike
from overrides import overrides

import ansys.modelcenter.workflow.api as wfapi
import ansys.modelcenter.workflow.grpc_modelcenter.proto.element_messages_pb2 as element_msg
import ansys.modelcenter.workflow.grpc_modelcenter.proto.grpc_modelcenter_workflow_pb2_grpc as grpc_mcd_workflow  # noqa: E501
import ansys.modelcenter.workflow.grpc_modelcenter.proto.variable_value_messages_pb2 as var_val_msg
import ansys.modelcenter.workflow.grpc_modelcenter.proto.workflow_messages_pb2 as workflow_msg

from .assembly import Assembly
from .component import Component
from .create_datapin import create_datapin
from .datapin_link import DatapinLink
from .element_wrapper import create_element
from .grpc_error_interpretation import (
    WRAP_INVALID_ARG,
    WRAP_NAME_COLLISION,
    WRAP_OUT_OF_BOUNDS,
    WRAP_TARGET_NOT_FOUND,
    interpret_rpc_error,
)
from .var_value_convert import (
    convert_grpc_value_to_acvi,
    convert_interop_value_to_grpc,
    grpc_type_enum_to_interop_type,
)


class WorkflowRunFailedError(Exception):
    """Raised to indicate that a workflow run failed."""


class Workflow(wfapi.IWorkflow):
    """
    Represents a Workflow or Model in ModelCenter.

    .. note::
        This class should not be directly instantiated by clients. Create an Engine, and use it to
        get a valid instance of this object.
    """

    def __init__(self, workflow_id: str, file_path: str, channel: Channel):
        """
        Initialize a new Workflow instance.

        Parameters
        ----------
        workflow_id: str
            The workflow's ID.
        file_path: str
            The path to the workflow file on disk.
        """
        self._state = engapi.WorkflowInstanceState.UNKNOWN
        self._id = workflow_id
        self._file_name = os.path.basename(file_path)
        self._channel = channel
        self._stub = self._create_client(self._channel)
        self._closed = False

    def __enter__(self):
        """Initialization when created in a 'with' statement."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Clean up when leaving a 'with' block."""
        if not self._closed:
            self.close_workflow()

    @staticmethod
    def _create_client(grpc_channel) -> grpc_mcd_workflow.ModelCenterWorkflowServiceStub:
        """Create a client from a grpc channel."""
        return grpc_mcd_workflow.ModelCenterWorkflowServiceStub(grpc_channel)

    @interpret_rpc_error(WRAP_TARGET_NOT_FOUND)
    @overrides
    def get_state(self) -> engapi.WorkflowInstanceState:
        # if self._instance.getHaltStatus():
        #     return WorkflowInstanceState.PAUSED
        # return self._state
        raise NotImplementedError

    def _create_run_request(
        self,
        inputs: Mapping[str, acvi.VariableState],
        reset: bool,
        validation_names: AbstractSet[str],
        collection_names: AbstractSet[str],
    ) -> workflow_msg.WorkflowRunRequest:
        request = workflow_msg.WorkflowRunRequest(
            target=workflow_msg.WorkflowId(id=self._id),
            reset=reset,
            validation_names=[name for name in validation_names],
            collection_names=[name for name in collection_names],
        )

        var_id: str
        var_state: acvi.VariableState
        for var_id, var_state in inputs.items():
            request.inputs[var_id].is_valid = var_state.is_valid
            request.inputs[var_id].value.MergeFrom(convert_interop_value_to_grpc(var_state.value))

        return request

    @interpret_rpc_error(
        {
            **WRAP_TARGET_NOT_FOUND,
            **WRAP_INVALID_ARG,
            **WRAP_OUT_OF_BOUNDS,
            grpc.StatusCode.FAILED_PRECONDITION: WorkflowRunFailedError,
        }
    )
    @overrides
    def run(
        self,
        inputs: Mapping[str, acvi.VariableState] = {},
        reset: bool = False,
        validation_names: AbstractSet[str] = set(),
        collect_names: AbstractSet[str] = set(),
    ) -> Mapping[str, acvi.VariableState]:
        request: workflow_msg.WorkflowRunRequest = self._create_run_request(
            inputs, reset, validation_names, collect_names
        )
        response = self._stub.WorkflowRun(request)
        elem_id: str
        response_var_state: var_val_msg.VariableState
        return {
            elem_id: acvi.VariableState(
                is_valid=response_var_state.is_valid,
                value=convert_grpc_value_to_acvi(response_var_state.value),
            )
            for elem_id, response_var_state in response.results.items()
        }

    @interpret_rpc_error({**WRAP_TARGET_NOT_FOUND, **WRAP_INVALID_ARG, **WRAP_OUT_OF_BOUNDS})
    @overrides
    def start_run(
        self,
        inputs: Mapping[str, acvi.VariableState],
        reset: bool,
        validation_names: AbstractSet[str],
    ) -> None:
        raise NotImplementedError

    @interpret_rpc_error(WRAP_TARGET_NOT_FOUND)
    @overrides
    def get_root(self) -> Assembly:
        request = workflow_msg.WorkflowId(id=self._id)
        response: workflow_msg.WorkflowGetRootResponse = self._stub.WorkflowGetRoot(request)
        root: element_msg.ElementId = response.id
        return Assembly(root, self._channel)

    @interpret_rpc_error({**WRAP_TARGET_NOT_FOUND, **WRAP_INVALID_ARG})
    @overrides
    def get_element_by_name(self, element_name: str) -> engapi.IElement:
        request = workflow_msg.NamedElementInWorkflow(
            workflow=workflow_msg.WorkflowId(id=self._id),
            element_full_name=element_msg.ElementName(name=element_name),
        )
        response = self._stub.WorkflowGetElementByName(request)
        return create_element(response, self._channel)

    # TODO: Should we just delete this? Should probably remove from
    #       GRPC api if so.
    @property
    def workflow_directory(self) -> str:
        """
        Get the directory the workflow is in.

        Returns
        -------
        str
            The workflow directory.
        """
        request = workflow_msg.WorkflowId(id=self._id)
        response: workflow_msg.WorkflowGetDirectoryResponse = self._stub.WorkflowGetDirectory(
            request
        )
        return response.workflow_dir

    @property  # type: ignore
    @overrides
    def workflow_file_name(self) -> str:
        return self._file_name

    @interpret_rpc_error({**WRAP_TARGET_NOT_FOUND, **WRAP_INVALID_ARG})
    @overrides
    def get_value(self, var_name: str) -> acvi.VariableState:
        request = workflow_msg.ElementIdOrName(
            target_name=workflow_msg.NamedElementInWorkflow(
                element_full_name=element_msg.ElementName(name=var_name),
                workflow=workflow_msg.WorkflowId(id=self._id),
            )
        )
        response: var_val_msg.VariableState = self._stub.VariableGetState(request)

        def convert(val: ArrayLike, dims: ArrayLike, val_type: Type) -> acvi.IVariableValue:
            return val_type(shape_=dims, values=np.array(val).flatten())

        attr: Optional[str] = response.value.WhichOneof("value")
        value: Any = None
        if attr is not None:
            value = getattr(response.value, attr)
        acvi_value: acvi.IVariableValue
        if isinstance(value, bool):
            acvi_value = acvi.BooleanValue(value)
        elif isinstance(value, float):
            acvi_value = acvi.RealValue(value)
        elif isinstance(value, int):
            acvi_value = acvi.IntegerValue(value)
        elif isinstance(value, str):
            acvi_value = acvi.StringValue(value)
        elif isinstance(value, var_val_msg.DoubleArrayValue):
            acvi_value = convert(value.values, value.dims.dims, acvi.RealArrayValue)
        elif isinstance(value, var_val_msg.IntegerArrayValue):
            acvi_value = convert(value.values, value.dims.dims, acvi.IntegerArrayValue)
        elif isinstance(value, var_val_msg.BooleanArrayValue):
            acvi_value = convert(value.values, value.dims.dims, acvi.BooleanArrayValue)
        elif isinstance(value, var_val_msg.StringArrayValue):
            acvi_value = convert(value.values, value.dims.dims, acvi.StringArrayValue)
        else:
            # unsupported type (should be impossible)
            raise TypeError(f"Unsupported type was returned: {type(value)}")
        return acvi.VariableState(acvi_value, response.is_valid)

    @interpret_rpc_error({**WRAP_TARGET_NOT_FOUND, **WRAP_INVALID_ARG})
    @overrides
    def create_link(
        self, variable: Union[wfapi.IDatapin, str], equation: Union[str, wfapi.IDatapin]
    ) -> None:
        eq: str
        if isinstance(equation, str):
            eq = equation
        else:
            eq = equation.full_name
        request = workflow_msg.WorkflowCreateLinkRequest(equation=eq)
        if isinstance(variable, str):
            request.target.id_string = self.get_element_by_name(variable).element_id
        else:
            request.target.id_string = variable.element_id
        response: workflow_msg.WorkflowCreateLinkResponse = self._stub.WorkflowCreateLink(request)

    @interpret_rpc_error(WRAP_TARGET_NOT_FOUND)
    @overrides
    def save_workflow(self) -> None:
        request = workflow_msg.WorkflowId()
        request.id = self._id
        response: workflow_msg.WorkflowSaveResponse = self._stub.WorkflowSave(request)

    @interpret_rpc_error({**WRAP_TARGET_NOT_FOUND, **WRAP_INVALID_ARG})
    @overrides
    def save_workflow_as(self, file_name: str) -> None:
        request = workflow_msg.WorkflowSaveAsRequest()
        request.target.id = self._id
        request.new_target_path = file_name
        response: workflow_msg.WorkflowSaveResponse = self._stub.WorkflowSaveAs(request)

    @interpret_rpc_error(WRAP_TARGET_NOT_FOUND)
    @overrides
    def close_workflow(self) -> None:
        request = workflow_msg.WorkflowId()
        request.id = self._id
        response: workflow_msg.WorkflowCloseResponse = self._stub.WorkflowClose(request)
        self._closed = True

    @interpret_rpc_error({**WRAP_TARGET_NOT_FOUND, **WRAP_INVALID_ARG})
    @overrides
    def get_variable(self, name: str) -> wfapi.IDatapin:
        request = workflow_msg.NamedElementInWorkflow(
            workflow=workflow_msg.WorkflowId(id=self._id),
            element_full_name=element_msg.ElementName(name=name),
        )
        response: workflow_msg.ElementInfo = self._stub.WorkflowGetElementByName(request)

        if response.type != element_msg.ELEMTYPE_VARIABLE:
            raise ValueError("Element is not a variable.")

        var_type: var_val_msg.VariableType = response.var_type

        return create_datapin(
            var_value_type=grpc_type_enum_to_interop_type(var_type),
            element_id=response.id,
            channel=self._channel,
        )

    @interpret_rpc_error({**WRAP_TARGET_NOT_FOUND, **WRAP_INVALID_ARG})
    @overrides
    def get_component(self, name: str) -> Component:
        request = workflow_msg.NamedElementInWorkflow(
            workflow=workflow_msg.WorkflowId(id=self._id),
            element_full_name=element_msg.ElementName(name=name),
        )
        response: workflow_msg.ElementInfo = self._stub.WorkflowGetElementByName(request)
        if response.type == element_msg.ELEMTYPE_COMPONENT:
            return Component(response.id, self._channel)
        elif response.type == element_msg.ELEMTYPE_IFCOMPONENT:
            # return IfComponent(response.id.id_string)
            raise NotImplementedError()
        else:
            raise ValueError("Element is not a component.")

    @interpret_rpc_error({**WRAP_TARGET_NOT_FOUND})
    @overrides
    def remove_component(self, name: str) -> None:
        comp: Component = self.get_component(name)
        request = workflow_msg.WorkflowRemoveComponentRequest()
        request.target.id_string = comp.element_id
        self._stub.WorkflowRemoveComponent(request)

    @interpret_rpc_error({**WRAP_TARGET_NOT_FOUND, **WRAP_INVALID_ARG, **WRAP_NAME_COLLISION})
    @overrides
    def create_assembly(
        self,
        name: str,
        parent: Union[wfapi.IAssembly, str],
        assembly_type: Optional[wfapi.AssemblyType] = None,
    ) -> Assembly:
        request = element_msg.AddAssemblyRequest(
            name=element_msg.ElementName(name=name),
            av_pos=None,
            assembly_type=assembly_type.value
            if assembly_type is not None
            else wfapi.AssemblyType.ASSEMBLY.value,
        )
        if parent is not None:
            if isinstance(parent, str):
                request.parent.id_string = parent
            else:
                request.parent.id_string = parent.element_id
        response: element_msg.AddAssemblyResponse = self._stub.AssemblyAddAssembly(request)
        return Assembly(response.id, self._channel)

    @interpret_rpc_error({**WRAP_TARGET_NOT_FOUND, **WRAP_INVALID_ARG})
    @overrides
    def auto_link(
        self, src_comp: Union[str, wfapi.IComponent], dest_comp: Union[str, wfapi.IComponent]
    ) -> Collection[wfapi.IDatapinLink]:
        request = workflow_msg.WorkflowAutoLinkRequest()
        src_comp_used = (
            src_comp if isinstance(src_comp, wfapi.IComponent) else self.get_component(src_comp)
        )
        dest_comp_used = (
            dest_comp if isinstance(dest_comp, wfapi.IComponent) else self.get_component(dest_comp)
        )
        request.source_comp.id_string = src_comp_used.element_id
        request.target_comp.id_string = dest_comp_used.element_id
        response: workflow_msg.WorkflowAutoLinkResponse = self._stub.WorkflowAutoLink(request)
        links: List[wfapi.IDatapinLink] = [
            DatapinLink(self._stub, lhs_id=entry.lhs.id_string, rhs=entry.rhs)
            for entry in response.created_links
        ]
        return links

    @interpret_rpc_error({**WRAP_TARGET_NOT_FOUND})
    @overrides
    def get_links(self) -> Collection[wfapi.IDatapinLink]:
        request = workflow_msg.WorkflowId(id=self._id)
        response: workflow_msg.WorkflowGetLinksResponse = self._stub.WorkflowGetLinksRequest(
            request
        )
        links: List[wfapi.IDatapinLink] = [
            DatapinLink(self._stub, lhs_id=entry.lhs.id_string, rhs=entry.rhs)
            for entry in response.links
        ]
        return links

    @overrides
    def get_workflow_uuid(self) -> str:
        return self._id

    @interpret_rpc_error({**WRAP_TARGET_NOT_FOUND})
    @overrides
    def halt(self) -> None:
        request = workflow_msg.WorkflowHaltRequest()
        response: workflow_msg.WorkflowHaltResponse = self._stub.WorkflowHalt(request)

    @interpret_rpc_error({**WRAP_TARGET_NOT_FOUND, **WRAP_INVALID_ARG})
    @overrides
    def move_component(
        self,
        component: Union[wfapi.IComponent, str],
        parent: Union[wfapi.IAssembly, str],
        index: int = -1,
    ) -> None:
        used_component: wfapi.IComponent = (
            component if isinstance(component, wfapi.IComponent) else self.get_component(component)
        )
        used_parent: wfapi.IAssembly = (
            parent if isinstance(parent, wfapi.IAssembly) else self.get_assembly(parent)
        )
        request = workflow_msg.MoveComponentRequest(
            target=element_msg.ElementId(id_string=used_component.element_id),
            new_parent=element_msg.ElementId(id_string=used_parent.element_id),
            index_in_parent=index,
        )
        self._stub.WorkflowMoveComponent(request)

    @interpret_rpc_error({**WRAP_TARGET_NOT_FOUND, **WRAP_INVALID_ARG})
    @overrides
    def get_assembly(self, name: Optional[str] = None) -> wfapi.IAssembly:
        if name is None:
            return self.get_root()
        else:
            request = workflow_msg.NamedElementInWorkflow(
                workflow=workflow_msg.WorkflowId(id=self._id),
                element_full_name=element_msg.ElementName(name=name),
            )
            response: workflow_msg.ElementInfo = self._stub.WorkflowGetElementByName(request)
            if response.type == element_msg.ELEMTYPE_ASSEMBLY:
                return Assembly(
                    element_msg.ElementId(id_string=response.id.id_string), self._channel
                )
            else:
                raise ValueError("Element is not an assembly.")

    @interpret_rpc_error({**WRAP_TARGET_NOT_FOUND, **WRAP_INVALID_ARG, **WRAP_NAME_COLLISION})
    @overrides
    def create_component(
        self,
        server_path: str,
        name: str,
        parent: Union[wfapi.IAssembly, str],
        *,
        init_string: Optional[str] = None,
        av_position: Optional[Tuple[int, int]] = None,
        insert_before: Optional[Union[wfapi.IComponent, wfapi.IAssembly, str]] = None,
    ) -> Component:
        request = workflow_msg.WorkflowCreateComponentRequest(
            source_path=server_path, name=name, init_str=init_string
        )
        used_parent = parent if isinstance(parent, wfapi.IAssembly) else self.get_assembly(parent)
        request.parent.id_string = used_parent.element_id
        if av_position is not None:
            request.coords.x_pos = av_position[0]
            request.coords.y_pos = av_position[1]
        elif insert_before is not None:
            if isinstance(insert_before, str):
                request.after_comp.id_string = self.get_element_by_name(insert_before).element_id
            else:
                request.after_comp.id_string = insert_before.element_id
        response: workflow_msg.WorkflowCreateComponentResponse = self._stub.WorkflowCreateComponent(
            request
        )
        return Component(response.created, self._channel)

    @interpret_rpc_error({**WRAP_TARGET_NOT_FOUND, **WRAP_INVALID_ARG})
    @overrides
    def get_variable_meta_data(self, name: str) -> acvi.CommonVariableMetadata:
        metadata: acvi.CommonVariableMetadata = None
        request = workflow_msg.NamedElementInWorkflow(
            workflow=workflow_msg.WorkflowId(id=self._id),
            element_full_name=element_msg.ElementName(name=name),
        )
        response: workflow_msg.ElementInfo = self._stub.WorkflowGetElementByName(request)

        if response.type != element_msg.ELEMTYPE_VARIABLE:
            raise ValueError("Element is not a variable.")
        elem_id: element_msg.ElementId = response.id
        var_type: var_val_msg.VariableType = response.var_type

        if var_type == var_val_msg.VARTYPE_BOOLEAN:
            metadata = acvi.BooleanMetadata()
            self._set_bool_metadata(elem_id, metadata)
        elif var_type == var_val_msg.VARTYPE_INTEGER:
            metadata = acvi.IntegerMetadata()
            self._set_int_metadata(elem_id, metadata)
        elif var_type == var_val_msg.VARTYPE_REAL:
            metadata = acvi.RealMetadata()
            self._set_real_metadata(elem_id, metadata)
        elif var_type == var_val_msg.VARTYPE_STRING:
            metadata = acvi.StringMetadata()
            self._set_string_metadata(elem_id, metadata)
        elif var_type == var_val_msg.VARTYPE_FILE:
            metadata = acvi.FileMetadata()
            self._set_file_metadata(elem_id, metadata)
        elif var_type == var_val_msg.VARTYPE_BOOLEAN_ARRAY:
            metadata = acvi.BooleanArrayMetadata()
            self._set_bool_metadata(elem_id, metadata)
        elif var_type == var_val_msg.VARTYPE_INTEGER_ARRAY:
            metadata = acvi.IntegerArrayMetadata()
            self._set_int_metadata(elem_id, metadata)
        elif var_type == var_val_msg.VARTYPE_REAL_ARRAY:
            metadata = acvi.RealArrayMetadata()
            self._set_real_metadata(elem_id, metadata)
        elif var_type == var_val_msg.VARTYPE_STRING_ARRAY:
            metadata = acvi.StringArrayMetadata()
            self._set_string_metadata(elem_id, metadata)
        elif var_type == var_val_msg.VARTYPE_FILE_ARRAY:
            metadata = acvi.FileArrayMetadata()
            self._set_file_metadata(elem_id, metadata)
        else:
            raise ValueError("Unknown variable type.")
        return metadata

    def _set_bool_metadata(
        self,
        var_id: element_msg.ElementId,
        metadata: Union[acvi.BooleanMetadata, acvi.BooleanArrayMetadata],
    ) -> None:
        """
        Query grpc for metadata for a boolean variable, and populate the given metadata object.

        Parameters
        ----------
        var_id: ElementId
        The id of the variable.
        metadata: Union[acvi.BooleanMetadata, acvi.BooleanArrayMetadata]
        The metadata object to populate.
        """
        response: var_val_msg.BooleanVariableMetadata = self._stub.BooleanVariableGetMetadata(
            var_id
        )
        metadata.description = response.base_metadata.description

    def _set_real_metadata(
        self,
        var_id: element_msg.ElementId,
        metadata: Union[acvi.RealMetadata, acvi.RealArrayMetadata],
    ) -> None:
        """
        Query grpc for metadata for a real variable, and populate the given metadata object.

        Parameters
        ----------
        var_id: ElementId
        The id of the variable.
        metadata: Union[acvi.RealMetadata, acvi.RealArrayMetadata]
        The metadata object to populate.
        """
        response: var_val_msg.DoubleVariableMetadata = self._stub.DoubleVariableGetMetadata(var_id)
        metadata.description = response.base_metadata.description
        metadata.units = response.numeric_metadata.units
        metadata.display_format = response.numeric_metadata.display_format
        metadata.lower_bound = response.lower_bound
        metadata.upper_bound = response.upper_bound
        metadata.enumerated_values.extend(response.enum_values)
        metadata.enumerated_aliases.extend(response.enum_aliases)

    def _set_int_metadata(
        self,
        var_id: element_msg.ElementId,
        metadata: Union[acvi.IntegerMetadata, acvi.IntegerArrayMetadata],
    ) -> None:
        """
        Query grpc for metadata for an integer variable, and populate the given metadata object.

        Parameters
        ----------
        var_id: ElementId
        The id of the variable.
        metadata: Union[acvi.IntegerMetadata, acvi.IntegerArrayMetadata]
        The metadata object to populate.
        """
        response: var_val_msg.IntegerVariableMetadata = self._stub.IntegerVariableGetMetadata(
            var_id
        )
        metadata.description = response.base_metadata.description
        metadata.units = response.numeric_metadata.units
        metadata.display_format = response.numeric_metadata.display_format
        metadata.lower_bound = response.lower_bound
        metadata.upper_bound = response.upper_bound
        metadata.enumerated_values.extend(response.enum_values)
        metadata.enumerated_aliases.extend(response.enum_aliases)

    def _set_string_metadata(
        self,
        var_id: element_msg.ElementId,
        metadata: Union[acvi.StringMetadata, acvi.StringArrayMetadata],
    ) -> None:
        """
        Query grpc for metadata for a string variable, and populate the given metadata object.

        Parameters
        ----------
        var_id: ElementId
        The id of the variable.
        metadata: Union[acvi.StringMetadata, acvi.StringArrayMetadata]
        The metadata object to populate.
        """
        response: var_val_msg.StringVariableMetadata = self._stub.StringVariableGetMetadata(var_id)
        metadata.description = response.base_metadata.description
        metadata.enumerated_values.extend(response.enum_values)
        metadata.enumerated_aliases.extend(response.enum_aliases)

    def _set_file_metadata(
        self,
        var_id: element_msg.ElementId,
        metadata: Union[acvi.FileMetadata, acvi.FileArrayMetadata],
    ) -> None:
        """
        Query grpc for metadata for a file variable, and populate the given metadata object.

        Parameters
        ----------
        var_id: ElementId
        The id of the variable.
        metadata: Union[acvi.FileMetadata, acvi.FileArrayMetadata]
        The metadata object to populate.
        """
        response: var_val_msg.FileVariableMetadata = self._stub.FileVariableGetMetadata(var_id)
        metadata.description = response.base_metadata.description

    @interpret_rpc_error({**WRAP_TARGET_NOT_FOUND, **WRAP_INVALID_ARG, **WRAP_OUT_OF_BOUNDS})
    @overrides
    def set_value(self, var_name: str, value: acvi.IVariableValue) -> None:
        var = self.get_variable(var_name)
        var.set_value(acvi.VariableState(value, True))
