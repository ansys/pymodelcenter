"""Implementation of Workflow."""
import os.path
from typing import AbstractSet, Iterable, List, Mapping, Optional, Tuple, Union

import ansys.common.variableinterop as acvi
from ansys.engineeringworkflow.api import IControlStatement, IElement, WorkflowInstanceState
import grpc
from overrides import overrides

from ansys.modelcenter.workflow.api import (
    DataExplorer,
    DataMonitor,
    IComponent,
    IVariable,
    VariableLink,
)
from ansys.modelcenter.workflow.api import Workflow as IWorkflow

from .assembly import Assembly
from .component import Component
from .proto import variable_value_messages_pb2 as var_msgs
from .proto import workflow_messages_pb2 as wkfl_msgs
from .proto.element_messages_pb2 import ElementId, ElementName
from .proto.grpc_modelcenter_workflow_pb2_grpc import ModelCenterWorkflowServiceStub


class Workflow(IWorkflow):
    """Represents a Workflow in ModelCenter."""

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
        self._state = WorkflowInstanceState.UNKNOWN
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
    def _create_client(grpc_channel) -> ModelCenterWorkflowServiceStub:
        """Create a client from a grpc channel."""
        return ModelCenterWorkflowServiceStub(grpc_channel)

    @overrides
    def get_state(self) -> WorkflowInstanceState:
        # if self._instance.getHaltStatus():
        #     return WorkflowInstanceState.PAUSED
        # return self._state
        raise NotImplementedError

    @overrides
    def run(
        self,
        inputs: Mapping[str, acvi.VariableState],
        reset: bool,
        validation_ids: AbstractSet[str],
    ) -> Mapping[str, acvi.VariableState]:
        raise NotImplementedError

    @overrides
    def start_run(
        self,
        inputs: Mapping[str, acvi.VariableState],
        reset: bool,
        validation_ids: AbstractSet[str],
    ) -> str:
        raise NotImplementedError

    @overrides
    def get_root(self) -> IControlStatement:
        request = wkfl_msgs.WorkflowId(id=self._id)
        response: wkfl_msgs.WorkflowGetRootResponse = self._stub.WorkflowGetRoot(request)
        root: ElementId = response.id
        return Assembly(root)

    @overrides
    def get_element_by_id(self, element_id: str) -> IElement:
        # TODO: not on grpc api
        raise NotImplementedError

    @property  # type: ignore
    @overrides
    def workflow_directory(self) -> str:
        request = wkfl_msgs.WorkflowId(id=self._id)
        response: wkfl_msgs.WorkflowGetDirectoryResponse = self._stub.WorkflowGetDirectory(request)
        return response.workflow_dir

    @property  # type: ignore
    @overrides
    def workflow_file_name(self) -> str:
        return self._file_name

    @overrides
    def set_value(self, var_name: str, value: str) -> None:
        # if isinstance(value, acvi.IVariableValue):
        #     api_value = value.to_api_string()
        # else:
        #     api_value = str(value)
        # self._instance.setValue(var_name, api_value)
        raise NotImplementedError

    @overrides
    def get_value(self, var_name: str) -> object:
        # value = self._instance.getValue(var_name)
        # return Workflow.value_to_variable_value(value)
        raise NotImplementedError

    @overrides
    def create_link(self, variable: str, equation: str) -> None:
        request = wkfl_msgs.WorkflowCreateLinkRequest(equation=equation)
        request.target.id_string = variable
        response: wkfl_msgs.WorkflowCreateLinkResponse = self._stub.WorkflowCreateLink(request)

    @overrides
    def save_workflow(self) -> None:
        request = wkfl_msgs.WorkflowId()
        request.id = self._id
        response: wkfl_msgs.WorkflowSaveResponse = self._stub.WorkflowSave(request)

    @overrides
    def save_workflow_as(self, file_name: str) -> None:
        request = wkfl_msgs.WorkflowSaveAsRequest()
        request.target.id = self._id
        request.new_target_path = file_name
        response: wkfl_msgs.WorkflowSaveResponse = self._stub.WorkflowSaveAs(request)

    @overrides
    def close_workflow(self) -> None:
        request = wkfl_msgs.WorkflowId()
        request.id = self._id
        response: wkfl_msgs.WorkflowCloseResponse = self._stub.WorkflowClose(request)

    @overrides
    def get_variable(self, name: str) -> IVariable:
        request = ElementName(name=name)
        response: ElementId = self._stub.WorkflowGetVariableByName(request)
        type_response: var_msgs.VariableTypeResponse = self._stub.VariableGetType(response)
        # TODO: maybe use a visitor here?
        var_type: var_msgs.VariableType = type_response.var_type
        if var_type == var_msgs.VARTYPE_BOOLEAN:
            return None  # TODO: need wrapper
        elif var_type == var_msgs.VARTYPE_INTEGER:
            return None  # TODO: need wrapper
        elif var_type == var_msgs.VARTYPE_REAL:
            return None  # TODO: need wrapper
        elif var_type == var_msgs.VARTYPE_STRING:
            return None  # TODO: need wrapper
        elif var_type == var_msgs.VARTYPE_FILE:
            return None  # TODO: need wrapper
        elif var_type == var_msgs.VARTYPE_BOOLEAN_ARRAY:
            return None  # TODO: need wrapper
        elif var_type == var_msgs.VARTYPE_INTEGER_ARRAY:
            return None  # TODO: need wrapper
        elif var_type == var_msgs.VARTYPE_REAL_ARRAY:
            return None  # TODO: need wrapper
        elif var_type == var_msgs.VARTYPE_STRING_ARRAY:
            return None  # TODO: need wrapper
        elif var_type == var_msgs.VARTYPE_FILE_ARRAY:
            return None  # TODO: need wrapper
        else:
            raise ValueError("Unknown variable type.")

    @overrides
    def get_component(self, name: str) -> IComponent:
        request = ElementName(name=name)
        response: ElementId = self._stub.WorkflowGetComponentOrAssemblyByName(request)
        return Component(response.id_string)

    @overrides
    def trade_study_end(self) -> None:
        # self._instance.tradeStudyEnd()
        raise NotImplementedError

    # Skip IDispatch* createJobManager([optional]VARIANT showProgressDialog);

    @overrides
    def trade_study_start(self) -> None:
        # self._instance.tradeStudyStart()
        raise NotImplementedError

    @overrides
    def get_halt_status(self) -> bool:
        # return self._instance.getHaltStatus()
        raise NotImplementedError

    @overrides
    def get_value_absolute(self, var_name: str) -> acvi.IVariableValue:
        # value = self._instance.getValueAbsolute(var_name)
        # return Workflow.value_to_variable_value(value)
        raise NotImplementedError

    @overrides
    def set_scheduler(self, schedular: str) -> None:
        # self._instance.setScheduler(schedular)
        raise NotImplementedError

    @overrides
    def remove_component(self, name: str) -> None:
        comp: Component = self.get_component(name)
        request = wkfl_msgs.WorkflowRemoveComponentRequest()
        request.target.id_string = comp.element_id
        response: wkfl_msgs.WorkflowRemoveComponentResponse = self._stub.WorkflowRemoveComponent(
            request
        )
        if not response.existed:
            raise ValueError("Component does not exist")

    @overrides
    def break_link(self, target_id: str) -> None:
        request = wkfl_msgs.WorkflowBreakLinkRequest()
        request.target_var.id_string = target_id
        response: wkfl_msgs.WorkflowBreakLinkResponse = self._stub.WorkflowBreakLink(request)
        if not response.existed:
            raise ValueError("Target id does not exist.")

    @overrides
    def run_macro(self, macro_name: str, use_mc_object: bool = False) -> object:
        # return self._instance.runMacro(macro_name, use_mc_object)
        raise NotImplementedError

    @overrides
    def create_assembly(self, name: str, parent: str, assembly_type: Optional[str] = None):
        # return self._instance.createAssembly(name, parent, assembly_type)
        raise NotImplementedError

    @overrides
    def create_assembly_variable(
        self, name: str, type_: str, parent: str
    ) -> acvi.CommonVariableMetadata:
        # return self._convert_variable(self._instance.createAssemblyVariable(name, type_, parent))
        raise NotImplementedError

    @overrides
    def auto_link(self, src_comp: str, dest_comp: str) -> Iterable[VariableLink]:
        request = wkfl_msgs.WorkflowAutoLinkRequest()
        request.source_comp.id_string = src_comp
        request.target_comp.id_string = dest_comp
        response: wkfl_msgs.WorkflowAutoLinkResponse = self._stub.WorkflowAutoLink(request)
        links: List[VariableLink] = []
        for entry in response.created_links:
            link = VariableLink(lhs_id=entry.lhs.id_string, rhs=entry.rhs)
            links.append(link)
        return links

    @overrides
    def get_links(self, reserved: object = None) -> Iterable[VariableLink]:
        request = wkfl_msgs.WorkflowId(id=self._id)
        response: wkfl_msgs.WorkflowGetLinksResponse = self._stub.WorkflowGetLinksRequest(request)
        links: List[VariableLink] = []
        for entry in response.links:
            link = VariableLink(lhs_id=entry.lhs.id_string, rhs=entry.rhs)
            links.append(link)
        return links

    @overrides
    def get_workflow_uuid(self) -> str:
        return self._id

    @overrides
    def halt(self) -> None:
        # self._instance.halt()
        raise NotImplementedError

    @overrides
    def run_variables(self, variable_array: Optional[str]) -> None:
        # self._instance.run(variable_array or "")
        raise NotImplementedError

    @overrides
    def get_data_monitor(self, component: str, index: int) -> DataMonitor:
        # dm_object: phxmock.MockDataMonitor = self._instance.getDataMonitor(component, index)
        # return DataMonitor(dm_object)
        raise NotImplementedError

    @overrides
    def create_data_monitor(self, component: str, name: str, x: int, y: int) -> object:
        # dm_object: phxmock.MockDataMonitor = self._instance.createDataMonitor(
        #   component, name, x, y)
        # return DataMonitor(dm_object)
        raise NotImplementedError

    @overrides
    def remove_data_monitor(self, component: str, index: int) -> bool:
        # return self._instance.removeDataMonitor(component, index)
        raise NotImplementedError

    @overrides
    def get_data_explorer(self, index: int) -> Optional[DataExplorer]:
        # TODO: not on grpc api
        raise NotImplementedError

    @overrides
    def move_component(self, component: str, parent: str, index: object) -> None:
        # TODO: not on grpc api
        raise NotImplementedError

    @overrides
    def set_xml_extension(self, xml: str) -> None:
        # TODO: not on grpc api
        raise NotImplementedError

    @overrides
    def set_assembly_style(
        self, assembly_name: str, style: object, width: object = None, height: object = None
    ) -> None:
        # TODO: not on grpc api
        raise NotImplementedError

    @overrides
    def get_assembly_style(self, assembly_name: str) -> Tuple[int, int]:
        # TODO: not on grpc api
        raise NotImplementedError

    @overrides
    def get_assembly(self, name: str = None) -> object:  # IAssembly
        # if name is None or name == "":
        #     assembly = self._instance.getModel()
        # else:
        #     assembly = self._instance.getAssembly(name)
        # if assembly is None:
        #     return None
        # return Assembly(assembly)
        raise NotImplementedError

    @overrides
    def create_component(
        self,
        server_path: str,
        name: str,
        parent: str,
        init_string: Optional[str] = None,
        x_pos: Optional[int] = None,
        y_pos: Optional[int] = None,
    ) -> IComponent:
        # TODO: init_string not on grpc api
        request = wkfl_msgs.WorkflowCreateComponentRequest(
            source_path=server_path, name=name, init_str=init_string
        )
        request.parent.id_string = parent
        if x_pos is not None and y_pos is not None:
            request.coord.x_pos = x_pos
            request.coord.y_pos = y_pos
        response: wkfl_msgs.WorkflowCreateComponentResponse = self._stub.WorkflowCreateComponent(
            request
        )
        return Component(response.created.id_string)

    @overrides
    def get_macro_script(self, macro_name: str) -> str:
        # TODO: not on grpc api
        raise NotImplementedError

    @overrides
    def set_macro_script(self, macro_name: str, script: str) -> None:
        # TODO: not on grpc api
        raise NotImplementedError

    @overrides
    def get_macro_script_language(self, macro_name: str) -> str:
        # TODO: not on grpc api
        raise NotImplementedError

    @overrides
    def set_macro_script_language(self, macro_name: str, language: str) -> None:
        # TODO: not on grpc api
        raise NotImplementedError

    @overrides
    def add_new_macro(self, macro_name: str, is_app_macro: bool) -> None:
        # TODO: not on grpc api
        raise NotImplementedError

    @overrides
    def get_variable_meta_data(self, name: str) -> acvi.CommonVariableMetadata:
        metadata: acvi.CommonVariableMetadata = None
        request = ElementName(name=name)
        response: ElementId = self._stub.WorkflowGetVariableByName(request)
        type_response: var_msgs.VariableTypeResponse = self._stub.VariableGetType(response)
        var_type: var_msgs.VariableType = type_response.var_type
        if var_type == var_msgs.VARTYPE_BOOLEAN:
            metadata = acvi.BooleanMetadata()
            # TODO: description?
        elif var_type == var_msgs.VARTYPE_INTEGER:
            metadata = acvi.IntegerMetadata()
            self._set_int_metadata(response, metadata)
        elif var_type == var_msgs.VARTYPE_REAL:
            metadata = acvi.RealMetadata()
            self._set_real_metadata(response, metadata)
        elif var_type == var_msgs.VARTYPE_STRING:
            metadata = acvi.StringMetadata()
            self._set_string_metadata(response, metadata)
        elif var_type == var_msgs.VARTYPE_FILE:
            metadata = acvi.FileMetadata()
            # TODO: description?
        elif var_type == var_msgs.VARTYPE_BOOLEAN_ARRAY:
            metadata = acvi.BooleanArrayMetadata()
            # TODO: description?
        elif var_type == var_msgs.VARTYPE_INTEGER_ARRAY:
            metadata = acvi.IntegerArrayMetadata()
            self._set_int_metadata(response, metadata)
        elif var_type == var_msgs.VARTYPE_REAL_ARRAY:
            metadata = acvi.RealArrayMetadata()
            self._set_real_metadata(response, metadata)
        elif var_type == var_msgs.VARTYPE_STRING_ARRAY:
            metadata = acvi.StringArrayMetadata()
            self._set_string_metadata(response, metadata)
        elif var_type == var_msgs.VARTYPE_FILE_ARRAY:
            metadata = acvi.FileArrayMetadata()
            # TODO: description?
        else:
            raise ValueError("Unknown variable type.")
        return metadata

    def _set_real_metadata(
        self, var_id: ElementId, metadata: Union[acvi.RealMetadata, acvi.RealArrayMetadata]
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
        response: var_msgs.DoubleVariableMetadata = self._stub.DoubleVariableGetMetadata(var_id)
        # TODO: description, units, display_format?
        metadata.lower_bound = response.lower_bound
        metadata.upper_bound = response.upper_bound
        metadata.enumerated_values.extend(response.enum_values)
        metadata.enumerated_aliases.extend(response.enum_aliases)

    def _set_int_metadata(
        self, var_id: ElementId, metadata: Union[acvi.IntegerMetadata, acvi.IntegerArrayMetadata]
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
        response: var_msgs.IntegerVariableMetadata = self._stub.IntegerVariableGetMetadata(var_id)
        # TODO: description, units, display_format?
        metadata.lower_bound = response.lower_bound
        metadata.upper_bound = response.upper_bound
        metadata.enumerated_values.extend(response.enum_values)
        metadata.enumerated_aliases.extend(response.enum_aliases)

    def _set_string_metadata(
        self, var_id: ElementId, metadata: Union[acvi.StringMetadata, acvi.StringArrayMetadata]
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
        # TODO: description, units, display_format?
        response: var_msgs.StringVariableMetadata = self._stub.StringVariableGetMetadata(var_id)
        metadata.enumerated_values.extend(response.enum_values)
        metadata.enumerated_aliases.extend(response.enum_aliases)

    @overrides
    def create_data_explorer(self, trade_study_type: str, setup: str) -> DataExplorer:
        # TODO: not on grpc api
        raise NotImplementedError

    @overrides
    def get_macro_timeout(self, macro_name: str) -> float:
        # TODO: not on grpc api
        raise NotImplementedError

    @overrides
    def set_macro_timeout(self, macro_name: str, timeout: float) -> None:
        # TODO: not on grpc api
        raise NotImplementedError
