# Copyright (C) 2022 - 2024 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
"""Implementation of Workflow."""
from contextlib import ExitStack
import os
from typing import TYPE_CHECKING, AbstractSet, Collection, List, Mapping, Optional, Tuple, Union

import ansys.api.modelcenter.v0.element_messages_pb2 as element_msg
import ansys.api.modelcenter.v0.grpc_modelcenter_workflow_pb2_grpc as grpc_mcd_workflow
import ansys.api.modelcenter.v0.variable_value_messages_pb2 as var_val_msg
import ansys.api.modelcenter.v0.workflow_messages_pb2 as workflow_msg
from ansys.api.modelcenter.v0.workflow_messages_pb2 import WorkflowInstanceState as WkflInstState
import ansys.engineeringworkflow.api as engapi
import ansys.tools.variableinterop as atvi
import grpc
from overrides import overrides

import ansys.modelcenter.workflow.api as wfapi

from .assembly import Assembly
from .component import Component
from .create_datapin import create_datapin
from .datapin_link import DatapinLink

if TYPE_CHECKING:
    from .engine import Engine

from .element_wrapper import create_element
from .grpc_error_interpretation import (
    WRAP_INVALID_ARG,
    WRAP_NAME_COLLISION,
    WRAP_OUT_OF_BOUNDS,
    WRAP_TARGET_NOT_FOUND,
    interpret_rpc_error,
)
from .var_value_convert import convert_grpc_value_to_atvi, convert_interop_value_to_grpc


class WorkflowRunFailedError(Exception):
    """Raised to indicate that a workflow run failed."""


class Workflow(wfapi.IWorkflow):
    """Represents a workflow or model in ModelCenter.

    .. note::
        This class should not be directly instantiated by clients. Create an ``Engine``, and use it
        to get a valid instance of this object.
    """

    def __init__(self, workflow_id: str, file_path: str, engine: "Engine"):
        """Initialize a new ``Workflow`` instance.

        Parameters
        ----------
        workflow_id : str
            ID of the workflow.
        file_path : str
            Path to the workflow file.
        engine : Engine
            ``Engine`` creating this ``Workflow``.
        """
        self._id = workflow_id
        self._file_name = os.path.basename(file_path)
        self._engine = engine
        self._stub = self._create_client(self._engine.channel)
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
        """Create a client from a gRPC channel."""
        return grpc_mcd_workflow.ModelCenterWorkflowServiceStub(grpc_channel)

    __WORKFLOW_INSTANCE_STATE_MAP = {
        WkflInstState.WORKFLOW_INSTANCE_STATE_UNSPECIFIED: engapi.WorkflowInstanceState.UNKNOWN,
        WkflInstState.WORKFLOW_INSTANCE_STATE_INVALID: engapi.WorkflowInstanceState.INVALID,
        WkflInstState.WORKFLOW_INSTANCE_STATE_RUNNING: engapi.WorkflowInstanceState.RUNNING,
        WkflInstState.WORKFLOW_INSTANCE_STATE_PAUSED: engapi.WorkflowInstanceState.PAUSED,
        WkflInstState.WORKFLOW_INSTANCE_STATE_FAILED: engapi.WorkflowInstanceState.FAILED,
        WkflInstState.WORKFLOW_INSTANCE_STATE_SUCCESS: engapi.WorkflowInstanceState.SUCCESS,
    }

    @interpret_rpc_error(WRAP_TARGET_NOT_FOUND)
    def get_state(self) -> engapi.WorkflowInstanceState:
        """Get the state of the workflow instance.

        Returns
        -------
        WorkflowInstanceState
            Current state of the workflow instance.

        Notes
        -----
        Possible states are:

        - ``WorkflowInstanceState.UNKNOWN``:
            If any datapin validated by the last run no longer exists, or some other error occurs
            getting the state.
        - ``WorkflowInstanceState.INVALID``:
            If any datapin validated by the last run is not valid, or the workflow has never been
            run and the root assembly is invalid. Note that this can be returned by requesting a
            datapin that will not be validated even if the workflow runs successfully, such as
            a datapin in an inactive branch of an if-component.
        - ``WorkflowInstanceState.RUNNING``:
            If the workflow is currently running.
        - ``WorkflowInstanceState.FAILED``:
            If the last workflow run terminated due to a failure.
        - ``WorkflowInstanceState.SUCCESS``:
            If the workflow ran successfully and all requested datapins are valid.

        Note that ``WorkflowInstanceState.PAUSED`` is never returned.
        """
        request = workflow_msg.GetWorkflowStateRequest()
        response: workflow_msg.GetWorkflowStateResponse = self._stub.WorkflowGetState(request)
        return (
            Workflow.__WORKFLOW_INSTANCE_STATE_MAP[response.state]
            if response.state in Workflow.__WORKFLOW_INSTANCE_STATE_MAP
            else engapi.WorkflowInstanceState.UNKNOWN
        )

    def _create_run_request(
        self,
        inputs: Mapping[str, atvi.VariableState],
        reset: bool,
        validation_names: AbstractSet[str],
        collection_names: AbstractSet[str],
        local_file_content_pins: ExitStack,
    ) -> workflow_msg.WorkflowRunRequest:
        request = workflow_msg.WorkflowRunRequest(
            target=workflow_msg.WorkflowId(id=self._id),
            reset=reset,
            validation_names=[name for name in validation_names],
            collection_names=[name for name in collection_names],
        )

        var_id: str
        var_state: atvi.VariableState
        for var_id, var_state in inputs.items():
            request.inputs[var_id].is_valid = var_state.is_valid
            request.inputs[var_id].value.MergeFrom(
                convert_interop_value_to_grpc(
                    var_state.value, local_file_content_pins, self._engine.is_local
                )
            )

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
        inputs: Mapping[str, atvi.VariableState] = {},
        reset: bool = False,
        validation_names: AbstractSet[str] = set(),
        collect_names: AbstractSet[str] = set(),
    ) -> Mapping[str, atvi.VariableState]:
        with ExitStack() as local_file_content_pins:
            request: workflow_msg.WorkflowRunRequest = self._create_run_request(
                inputs, reset, validation_names, collect_names, local_file_content_pins
            )
            response = self._stub.WorkflowRun(request)
            elem_id: str
            response_var_state: var_val_msg.VariableState
            return {
                elem_id: atvi.VariableState(
                    is_valid=response_var_state.is_valid,
                    value=convert_grpc_value_to_atvi(
                        response_var_state.value, self._engine.is_local
                    ),
                )
                for elem_id, response_var_state in response.results.items()
            }
        # This line should only be reachable if one of the context managers in
        # local_file_content_pins suppress an exception, which they should not
        # be doing.
        raise engapi.EngineInternalError(
            "Reached an unexpected state. A local file content context may be suppressing an "
            "exception? Report this error to the pyModelCenter maintainers."
        )

    @interpret_rpc_error({**WRAP_TARGET_NOT_FOUND, **WRAP_INVALID_ARG, **WRAP_OUT_OF_BOUNDS})
    @overrides
    def start_run(
        self,
        inputs: Mapping[str, atvi.VariableState],
        reset: bool,
        validation_names: AbstractSet[str],
    ) -> None:
        with ExitStack() as local_file_content_pins:
            request: workflow_msg.WorkflowRunRequest = self._create_run_request(
                inputs, reset, validation_names, set(), local_file_content_pins
            )
            self._stub.WorkflowStartRun(request)
            return
        # This line should only be reachable if one of the context managers in
        # local_file_content_pins suppress an exception, which they should not
        # be doing.
        raise engapi.EngineInternalError(
            "Reached an unexpected state. A local file content context may be suppressing an "
            "exception? Report this error to the pyModelCenter maintainers."
        )

    @interpret_rpc_error(WRAP_TARGET_NOT_FOUND)
    @overrides
    def get_root(self) -> Assembly:
        request = workflow_msg.WorkflowId(id=self._id)
        response: workflow_msg.WorkflowGetRootResponse = self._stub.WorkflowGetRoot(request)
        root: element_msg.ElementId = response.id
        return Assembly(root, self._engine)

    @interpret_rpc_error({**WRAP_TARGET_NOT_FOUND, **WRAP_INVALID_ARG})
    @overrides
    def get_element_by_name(self, element_name: str) -> engapi.IElement:
        request = workflow_msg.NamedElementWorkflow(
            workflow=workflow_msg.WorkflowId(id=self._id),
            element_full_name=element_msg.ElementName(name=element_name),
        )
        response = self._stub.WorkflowGetElementByName(request)
        return create_element(response, self._engine)

    @property
    def workflow_directory(self) -> str:
        """Get the directory the workflow is in.

        Returns
        -------
        str
            Directory containing the workflow.
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
    def get_datapin_state(self, var_name: str) -> atvi.VariableState:
        request = workflow_msg.ElementIdOrName(
            target_name=workflow_msg.NamedElementWorkflow(
                element_full_name=element_msg.ElementName(name=var_name),
                workflow=workflow_msg.WorkflowId(id=self._id),
            )
        )
        response: var_val_msg.VariableState = self._stub.VariableGetState(request)
        return atvi.VariableState(
            convert_grpc_value_to_atvi(response.value, self._engine.is_local), response.is_valid
        )

    @interpret_rpc_error({**WRAP_TARGET_NOT_FOUND, **WRAP_INVALID_ARG})
    @overrides
    def create_link(
        self, datapin: Union[wfapi.IDatapin, str], equation: Union[str, wfapi.IDatapin]
    ) -> None:
        eq: str
        if isinstance(equation, str):
            eq = equation
        else:
            eq = equation.full_name
        request = workflow_msg.WorkflowCreateLinkRequest(equation=eq)
        if isinstance(datapin, str):
            request.target.id_string = self.get_element_by_name(datapin).element_id
        else:
            request.target.id_string = datapin.element_id
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
    def get_datapin(self, name: str) -> wfapi.IDatapin:
        request = workflow_msg.NamedElementWorkflow(
            workflow=workflow_msg.WorkflowId(id=self._id),
            element_full_name=element_msg.ElementName(name=name),
        )
        response: workflow_msg.ElementInfo = self._stub.WorkflowGetElementByName(request)

        if response.type != element_msg.ELEMENT_TYPE_VARIABLE:
            raise ValueError("Element is not a datapin.")

        var_type: var_val_msg.VariableType = response.var_type

        return create_datapin(
            var_value_type=var_type,
            element_id=response.id,
            engine=self._engine,
        )

    @interpret_rpc_error({**WRAP_TARGET_NOT_FOUND, **WRAP_INVALID_ARG})
    @overrides
    def get_component(self, name: str) -> Component:
        request = workflow_msg.NamedElementWorkflow(
            workflow=workflow_msg.WorkflowId(id=self._id),
            element_full_name=element_msg.ElementName(name=name),
        )
        response: workflow_msg.ElementInfo = self._stub.WorkflowGetElementByName(request)
        if response.type == element_msg.ELEMENT_TYPE_COMPONENT:
            return Component(response.id, self._engine)
        elif response.type == element_msg.ELEMENT_TYPE_DRIVERCOMPONENT:
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
        return Assembly(response.id, self._engine)

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
        parent: Union[engapi.IControlStatement, str],
        index: int = -1,
    ) -> None:
        used_component: wfapi.IComponent = (
            component if isinstance(component, wfapi.IComponent) else self.get_component(component)
        )
        used_parent: engapi.IControlStatement = (
            parent if isinstance(parent, engapi.IControlStatement) else self.get_assembly(parent)
        )
        request = workflow_msg.MoveComponentRequest(
            target=element_msg.ElementId(id_string=used_component.element_id),
            new_parent=element_msg.ElementId(id_string=used_parent.element_id),
            index_parent=index,
        )
        self._stub.WorkflowMoveComponent(request)

    @interpret_rpc_error({**WRAP_TARGET_NOT_FOUND, **WRAP_INVALID_ARG})
    @overrides
    def get_assembly(self, name: Optional[str] = None) -> wfapi.IAssembly:
        if name is None:
            return self.get_root()
        else:
            request = workflow_msg.NamedElementWorkflow(
                workflow=workflow_msg.WorkflowId(id=self._id),
                element_full_name=element_msg.ElementName(name=name),
            )
            response: workflow_msg.ElementInfo = self._stub.WorkflowGetElementByName(request)
            if response.type == element_msg.ELEMENT_TYPE_ASSEMBLY:
                return Assembly(
                    element_msg.ElementId(id_string=response.id.id_string), self._engine
                )
            else:
                raise ValueError("Element is not an assembly.")

    @interpret_rpc_error({**WRAP_TARGET_NOT_FOUND, **WRAP_INVALID_ARG, **WRAP_NAME_COLLISION})
    @overrides
    def create_component(
        self,
        server_path: str,
        name: str,
        parent: Union[engapi.IControlStatement, str],
        *,
        init_string: Optional[str] = None,
        av_position: Optional[Tuple[int, int]] = None,
        insert_before: Optional[Union[wfapi.IComponent, engapi.IControlStatement, str]] = None,
    ) -> Component:
        request = workflow_msg.WorkflowCreateComponentRequest(
            source_path=server_path, name=name, init_str=init_string
        )
        used_parent = (
            parent if isinstance(parent, engapi.IControlStatement) else self.get_assembly(parent)
        )
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
        parent_elements: workflow_msg.ElementInfoCollection = (
            self._stub.AssemblyGetAssembliesAndComponents(
                element_msg.ElementId(id_string=used_parent.element_id)
            )
        )
        one_element: workflow_msg.ElementInfo
        parent_element_by_id = {
            one_element.id.id_string: one_element for one_element in parent_elements.elements
        }
        created_element = create_element(
            parent_element_by_id[response.created.id_string], self._engine
        )
        if isinstance(created_element, Component):
            return created_element
        else:
            raise engapi.EngineInternalError(
                "A request to create a component created something that was not a component."
            )

    @interpret_rpc_error({**WRAP_TARGET_NOT_FOUND, **WRAP_INVALID_ARG})
    @overrides
    def get_datapin_meta_data(self, name: str) -> atvi.CommonVariableMetadata:
        metadata: atvi.CommonVariableMetadata
        request = workflow_msg.NamedElementWorkflow(
            workflow=workflow_msg.WorkflowId(id=self._id),
            element_full_name=element_msg.ElementName(name=name),
        )
        response: workflow_msg.ElementInfo = self._stub.WorkflowGetElementByName(request)

        if response.type != element_msg.ELEMENT_TYPE_VARIABLE:
            raise ValueError("Element is not a datapin.")
        elem_id: element_msg.ElementId = response.id
        var_type: var_val_msg.VariableType = response.var_type

        if var_type == var_val_msg.VARIABLE_TYPE_BOOLEAN:
            metadata = atvi.BooleanMetadata()
            self._set_bool_metadata(elem_id, metadata)
        elif var_type == var_val_msg.VARIABLE_TYPE_INTEGER:
            metadata = atvi.IntegerMetadata()
            self._set_int_metadata(elem_id, metadata)
        elif var_type == var_val_msg.VARIABLE_TYPE_REAL:
            metadata = atvi.RealMetadata()
            self._set_real_metadata(elem_id, metadata)
        elif var_type == var_val_msg.VARIABLE_TYPE_STRING:
            metadata = atvi.StringMetadata()
            self._set_string_metadata(elem_id, metadata)
        elif var_type == var_val_msg.VARIABLE_TYPE_FILE:
            metadata = atvi.FileMetadata()
            self._set_file_metadata(elem_id, metadata)
        elif var_type == var_val_msg.VARIABLE_TYPE_BOOLEAN_ARRAY:
            metadata = atvi.BooleanArrayMetadata()
            self._set_bool_metadata(elem_id, metadata)
        elif var_type == var_val_msg.VARIABLE_TYPE_INTEGER_ARRAY:
            metadata = atvi.IntegerArrayMetadata()
            self._set_int_metadata(elem_id, metadata)
        elif var_type == var_val_msg.VARIABLE_TYPE_REAL_ARRAY:
            metadata = atvi.RealArrayMetadata()
            self._set_real_metadata(elem_id, metadata)
        elif var_type == var_val_msg.VARIABLE_TYPE_STRING_ARRAY:
            metadata = atvi.StringArrayMetadata()
            self._set_string_metadata(elem_id, metadata)
        elif var_type == var_val_msg.VARIABLE_TYPE_FILE_ARRAY:
            metadata = atvi.FileArrayMetadata()
            self._set_file_metadata(elem_id, metadata)
        else:
            raise ValueError("Unknown datapin type.")
        return metadata

    def _set_bool_metadata(
        self,
        var_id: element_msg.ElementId,
        metadata: Union[atvi.BooleanMetadata, atvi.BooleanArrayMetadata],
    ) -> None:
        """Query gRPC for metadata for a boolean datapin, and populate the
        given metadata object.

        Parameters
        ----------
        var_id : ElementId
            ID of the datapin.
        metadata : Union[atvi.BooleanMetadata, atvi.BooleanArrayMetadata]
            Metadata object to populate.
        """
        response: var_val_msg.BooleanVariableMetadata = self._stub.BooleanVariableGetMetadata(
            var_id
        )
        metadata.description = response.base_metadata.description

    def _set_real_metadata(
        self,
        var_id: element_msg.ElementId,
        metadata: Union[atvi.RealMetadata, atvi.RealArrayMetadata],
    ) -> None:
        """Query gRPC for metadata for a real datapin, and populate the given
        metadata object.

        Parameters
        ----------
        var_id : ElementId
            ID of the datapin.
        metadata : Union[atvi.RealMetadata, atvi.RealArrayMetadata]
            Metadata object to populate.
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
        metadata: Union[atvi.IntegerMetadata, atvi.IntegerArrayMetadata],
    ) -> None:
        """Query gRPC for metadata for an integer datapin, and populate the
        given metadata object.

        Parameters
        ----------
        var_id : ElementId
            ID of the datapin.
        metadata : Union[atvi.IntegerMetadata, atvi.IntegerArrayMetadata]
            Metadata object to populate.
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
        metadata: Union[atvi.StringMetadata, atvi.StringArrayMetadata],
    ) -> None:
        """Query gRPC for metadata for a string datapin, and populate the given
        metadata object.

        Parameters
        ----------
        var_id : ElementId
            ID of the datapin.
        metadata : Union[atvi.StringMetadata, atvi.StringArrayMetadata]
            Metadata object to populate.
        """
        response: var_val_msg.StringVariableMetadata = self._stub.StringVariableGetMetadata(var_id)
        metadata.description = response.base_metadata.description
        metadata.enumerated_values.extend(response.enum_values)
        metadata.enumerated_aliases.extend(response.enum_aliases)

    def _set_file_metadata(
        self,
        var_id: element_msg.ElementId,
        metadata: Union[atvi.FileMetadata, atvi.FileArrayMetadata],
    ) -> None:
        """Query gRPC for metadata for a file datapin, and populate the given
        metadata object.

        Parameters
        ----------
        var_id : ElementId
            ID of the datapin.
        metadata : Union[atvi.FileMetadata, atvi.FileArrayMetadata]
            Metadata object to populate.
        """
        response: var_val_msg.FileVariableMetadata = self._stub.FileVariableGetMetadata(var_id)
        metadata.description = response.base_metadata.description

    @interpret_rpc_error({**WRAP_TARGET_NOT_FOUND, **WRAP_INVALID_ARG, **WRAP_OUT_OF_BOUNDS})
    @overrides
    def set_value(self, var_name: str, value: atvi.IVariableValue) -> None:
        var = self.get_datapin(var_name)
        var.set_state(atvi.VariableState(value, True))
