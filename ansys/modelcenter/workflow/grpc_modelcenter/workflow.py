"""Implementation of Workflow."""
import os
from typing import AbstractSet, Collection, List, Mapping, Optional, Tuple, Type, Union

import ansys.common.variableinterop as acvi
import ansys.engineeringworkflow.api as engapi
import grpc
import numpy as np
from numpy.typing import ArrayLike
from overrides import overrides

import ansys.modelcenter.workflow.api as wfapi
import ansys.modelcenter.workflow.grpc_modelcenter.proto.element_messages_pb2 as element_msg
import ansys.modelcenter.workflow.grpc_modelcenter.proto.grpc_modelcenter_workflow_pb2_grpc as grpc_mcd_workflow  # noqa: E501
import ansys.modelcenter.workflow.grpc_modelcenter.proto.variable_value_messages_pb2 as var_val_msg
import ansys.modelcenter.workflow.grpc_modelcenter.proto.workflow_messages_pb2 as workflow_msg

from ._visitors import VariableValueVisitor
from .assembly import Assembly
from .boolean_variable import BooleanVariable
from .component import Component
from .double_variable import DoubleVariable
from .integer_variable import IntegerVariable
from .string_variable import StringVariable
from .var_value_convert import convert_grpc_value_to_acvi, convert_interop_value_to_grpc
from .variable_link import VariableLink


class Workflow(wfapi.IWorkflow):
    """Represents a Workflow or Model in ModelCenter."""

    def __init__(self, workflow_id: str, file_path: str):
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
        # (MPP): Unsure if we should pass this in from Engine
        self._channel = grpc.insecure_channel("localhost:50051")
        self._stub = self._create_client(self._channel)

    def __enter__(self):
        """Initialization when created in a 'with' statement."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Clean up when leaving a 'with' block."""
        self.close_workflow()

    @staticmethod
    def _create_client(grpc_channel) -> grpc_mcd_workflow.ModelCenterWorkflowServiceStub:
        """Create a client from a grpc channel."""
        return grpc_mcd_workflow.ModelCenterWorkflowServiceStub(grpc_channel)

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
        validation_ids: AbstractSet[str],
    ) -> workflow_msg.WorkflowRunRequest:
        request = workflow_msg.WorkflowRunRequest(
            target=workflow_msg.WorkflowId(id=self._id),
            reset=reset,
            validation_ids=[val_id for val_id in validation_ids],
        )

        var_id: str
        var_state: acvi.VariableState
        for var_id, var_state in inputs.items():
            request.inputs[var_id].is_valid = var_state.is_valid
            request.inputs[var_id].value.MergeFrom(convert_interop_value_to_grpc(var_state.value))

        return request

    @overrides
    def run(
        self,
        inputs: Mapping[str, acvi.VariableState],
        reset: bool,
        validation_ids: AbstractSet[str],
    ) -> Mapping[str, acvi.VariableState]:
        request: workflow_msg.WorkflowRunRequest = self._create_run_request(
            inputs, reset, validation_ids
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

    @overrides
    def start_run(
        self,
        inputs: Mapping[str, acvi.VariableState],
        reset: bool,
        validation_ids: AbstractSet[str],
    ) -> str:
        raise NotImplementedError

    @overrides
    def get_root(self) -> engapi.IControlStatement:
        request = workflow_msg.WorkflowId(id=self._id)
        response: workflow_msg.WorkflowGetRootResponse = self._stub.WorkflowGetRoot(request)
        root: element_msg.ElementId = response.id
        return Assembly(root, self._channel)

    @overrides
    def get_element_by_id(self, element_id: str) -> engapi.IElement:
        # TODO: not on grpc api
        raise NotImplementedError()

    # TODO: Should we just delete this? Should probably remove from
    #       GRPC api if so.
    @property
    def workflow_directory(self) -> str:
        """
        Get the directory the workflow is in.

        Returns
        -------
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

    @overrides
    def get_value(self, var_name: str) -> acvi.VariableState:
        var_id: element_msg.ElementId = self._stub.WorkflowGetVariableByName(
            element_msg.ElementName(name=var_name)
        )
        response: var_val_msg.VariableState
        try:
            response = self._stub.VariableGetState(var_id)
        except grpc.RpcError as e:
            # TODO: how to handle?
            raise e

        def convert(val: ArrayLike, dims: ArrayLike, val_type: Type) -> acvi.IVariableValue:
            return val_type(shape_=dims, values=np.array(val).flatten())

        value = getattr(response.value, response.value.WhichOneof("value"))
        acvi_value: acvi.IVariableValue
        if isinstance(value, float):
            acvi_value = acvi.RealValue(value)
        elif isinstance(value, int):
            acvi_value = acvi.IntegerValue(value)
        elif isinstance(value, bool):
            acvi_value = acvi.BooleanValue(value)
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

    @overrides
    def create_link(
        self, variable: Union[wfapi.IVariable, str], equation: Union[str, wfapi.IVariable]
    ) -> None:
        eq: str
        if isinstance(equation, str):
            eq = equation
        else:
            eq = equation.name
        request = workflow_msg.WorkflowCreateLinkRequest(equation=eq)
        if isinstance(variable, str):
            request.target.id_string = variable
        else:
            request.target.id_string = variable.element_id
        response: workflow_msg.WorkflowCreateLinkResponse = self._stub.WorkflowCreateLink(request)

    @overrides
    def save_workflow(self) -> None:
        request = workflow_msg.WorkflowId()
        request.id = self._id
        response: workflow_msg.WorkflowSaveResponse = self._stub.WorkflowSave(request)

    @overrides
    def save_workflow_as(self, file_name: str) -> None:
        request = workflow_msg.WorkflowSaveAsRequest()
        request.target.id = self._id
        request.new_target_path = file_name
        response: workflow_msg.WorkflowSaveResponse = self._stub.WorkflowSaveAs(request)

    @overrides
    def close_workflow(self) -> None:
        request = workflow_msg.WorkflowId()
        request.id = self._id
        response: workflow_msg.WorkflowCloseResponse = self._stub.WorkflowClose(request)

    @overrides
    def get_variable(self, name: str) -> wfapi.IVariable:
        request = element_msg.ElementName(name=name)
        response: element_msg.ElementId = self._stub.WorkflowGetVariableByName(request)
        type_response: var_val_msg.VariableTypeResponse = self._stub.VariableGetType(response)
        # TODO: maybe use a visitor here?
        var_type: var_val_msg.VariableType = type_response.var_type
        if var_type == var_val_msg.VARTYPE_BOOLEAN:
            return BooleanVariable(response, self._stub)
        elif var_type == var_val_msg.VARTYPE_INTEGER:
            return IntegerVariable(response, self._stub)
        elif var_type == var_val_msg.VARTYPE_REAL:
            return DoubleVariable(response, self._stub)
        elif var_type == var_val_msg.VARTYPE_STRING:
            return StringVariable(response, self._stub)
        elif var_type == var_val_msg.VARTYPE_FILE:
            raise NotImplementedError()
        elif var_type == var_val_msg.VARTYPE_BOOLEAN_ARRAY:
            raise NotImplementedError()
        elif var_type == var_val_msg.VARTYPE_INTEGER_ARRAY:
            raise NotImplementedError()
        elif var_type == var_val_msg.VARTYPE_REAL_ARRAY:
            raise NotImplementedError()
        elif var_type == var_val_msg.VARTYPE_STRING_ARRAY:
            raise NotImplementedError()
        elif var_type == var_val_msg.VARTYPE_FILE_ARRAY:
            raise NotImplementedError()
        else:
            raise ValueError("Unknown variable type.")

    @overrides
    def get_component(self, name: str) -> wfapi.IComponent:
        request = element_msg.ElementName(name=name)
        response: element_msg.ElementId = self._stub.WorkflowGetComponentOrAssemblyByName(request)
        return Component(response.id_string)

    @overrides
    def set_scheduler(self, schedular: str) -> None:
        raise NotImplementedError()

    @overrides
    def remove_component(self, name: str) -> None:
        comp: Component = self.get_component(name)
        request = workflow_msg.WorkflowRemoveComponentRequest()
        request.target.id_string = comp.element_id
        response: workflow_msg.WorkflowRemoveComponentResponse = self._stub.WorkflowRemoveComponent(
            request
        )
        if not response.existed:
            raise ValueError("Component does not exist")

    @overrides
    def create_assembly(
        self, name: str, parent: Union[wfapi.IAssembly, str], assembly_type: Optional[str] = None
    ):
        raise NotImplementedError()

    @overrides
    def auto_link(self, src_comp: str, dest_comp: str) -> Collection[wfapi.IVariableLink]:
        request = workflow_msg.WorkflowAutoLinkRequest()
        request.source_comp.id_string = src_comp
        request.target_comp.id_string = dest_comp
        response: workflow_msg.WorkflowAutoLinkResponse = self._stub.WorkflowAutoLink(request)
        links: List[wfapi.IVariableLink] = [
            VariableLink(self._stub, lhs_id=entry.lhs.id_string, rhs=entry.rhs)
            for entry in response.created_links
        ]
        return links

    @overrides
    def get_links(self) -> Collection[wfapi.IVariableLink]:
        request = workflow_msg.WorkflowId(id=self._id)
        response: workflow_msg.WorkflowGetLinksResponse = self._stub.WorkflowGetLinksRequest(
            request
        )
        links: List[wfapi.IVariableLink] = [
            VariableLink(self._stub, lhs_id=entry.lhs.id_string, rhs=entry.rhs)
            for entry in response.links
        ]
        return links

    @overrides
    def get_workflow_uuid(self) -> str:
        return self._id

    @overrides
    def halt(self) -> None:
        raise NotImplementedError()

    @overrides
    def get_data_monitor(
        self, component: Union[wfapi.IComponent, str], index: int
    ) -> wfapi.IDataMonitor:
        raise NotImplementedError()

    @overrides
    def create_data_monitor(
        self, component: Union[wfapi.IComponent, str], name: str, x: int, y: int
    ) -> object:
        raise NotImplementedError()

    @overrides
    def remove_data_monitor(self, component: Union[wfapi.IComponent, str], index: int) -> bool:
        raise NotImplementedError()

    @overrides
    def move_component(
        self,
        component: Union[wfapi.IComponent, str],
        parent: Union[wfapi.IAssembly, str],
        index: int = -1,
    ) -> None:
        # TODO: not on grpc api
        raise NotImplementedError()

    @overrides
    def set_xml_extension(self, xml: str) -> None:
        # TODO: not on grpc api
        raise NotImplementedError()

    @overrides
    def get_assembly(self, name: Optional[str] = None) -> wfapi.IAssembly:
        raise NotImplementedError()

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
    ) -> wfapi.IComponent:
        request = workflow_msg.WorkflowCreateComponentRequest(
            source_path=server_path, name=name, init_str=init_string
        )
        request.parent.id_string = parent
        if av_position is not None:
            request.coords.x_pos = av_position[0]
            request.coords.y_pos = av_position[1]
        elif insert_before is not None:
            if isinstance(insert_before, str):
                request.after_comp.id_string = insert_before
            else:
                request.after_comp.id_string = insert_before.element_id
        response: workflow_msg.WorkflowCreateComponentResponse = self._stub.WorkflowCreateComponent(
            request
        )
        return Component(response.created.id_string)

    @overrides
    def get_variable_meta_data(self, name: str) -> acvi.CommonVariableMetadata:
        metadata: acvi.CommonVariableMetadata = None
        request = element_msg.ElementName(name=name)
        response: element_msg.ElementId = self._stub.WorkflowGetVariableByName(request)
        type_response: var_val_msg.VariableTypeResponse = self._stub.VariableGetType(response)
        var_type: var_val_msg.VariableType = type_response.var_type
        if var_type == var_val_msg.VARTYPE_BOOLEAN:
            metadata = acvi.BooleanMetadata()
            self._set_bool_metadata(response, metadata)
        elif var_type == var_val_msg.VARTYPE_INTEGER:
            metadata = acvi.IntegerMetadata()
            self._set_int_metadata(response, metadata)
        elif var_type == var_val_msg.VARTYPE_REAL:
            metadata = acvi.RealMetadata()
            self._set_real_metadata(response, metadata)
        elif var_type == var_val_msg.VARTYPE_STRING:
            metadata = acvi.StringMetadata()
            self._set_string_metadata(response, metadata)
        elif var_type == var_val_msg.VARTYPE_FILE:
            metadata = acvi.FileMetadata()
            self._set_file_metadata(response, metadata)
        elif var_type == var_val_msg.VARTYPE_BOOLEAN_ARRAY:
            metadata = acvi.BooleanArrayMetadata()
            self._set_bool_metadata(response, metadata)
        elif var_type == var_val_msg.VARTYPE_INTEGER_ARRAY:
            metadata = acvi.IntegerArrayMetadata()
            self._set_int_metadata(response, metadata)
        elif var_type == var_val_msg.VARTYPE_REAL_ARRAY:
            metadata = acvi.RealArrayMetadata()
            self._set_real_metadata(response, metadata)
        elif var_type == var_val_msg.VARTYPE_STRING_ARRAY:
            metadata = acvi.StringArrayMetadata()
            self._set_string_metadata(response, metadata)
        elif var_type == var_val_msg.VARTYPE_FILE_ARRAY:
            metadata = acvi.FileArrayMetadata()
            self._set_file_metadata(response, metadata)
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

    @overrides
    def set_value(self, var_name: str, value: acvi.IVariableValue) -> None:
        var_id: element_msg.ElementId = self._stub.WorkflowGetVariableByName(
            element_msg.ElementName(name=var_name)
        )
        try:
            value.accept(VariableValueVisitor(var_id, self._stub))
        except grpc.RpcError as e:
            # How should we handle errors here?
            raise e
