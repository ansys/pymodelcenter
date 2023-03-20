"""Implementation of Workflow."""
from typing import AbstractSet, Iterable, Mapping, Optional, Tuple, Type

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


class Workflow(wfapi.Workflow):
    """Represents a Workflow or Model in ModelCenter."""

    def __init__(self, root_element: element_msg.ElementId, workflow_id: str):
        """
        Initialize a new Workflow instance.

        Parameters
        ----------
        root_element: element_messages.ElementId
            The root element of the workflow.
        workflow_id: str
            The workflow's ID.
        """
        self._state = engapi.WorkflowInstanceState.UNKNOWN
        self._root = root_element
        self._id = workflow_id
        # (MPP): Unsure if we should pass this in from Engine
        self._channel = grpc.insecure_channel("localhost:50051")
        self._stub = grpc_mcd_workflow.ModelCenterWorkflowServiceStub(self._channel)

    @overrides
    def get_state(self) -> engapi.WorkflowInstanceState:
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
    def get_root(self) -> engapi.IControlStatement:
        request = workflow_msg.WorkflowId()
        request.id = self._id
        response: workflow_msg.WorkflowGetRootResponse = self._stub.WorkflowGetRoot(request)
        root: element_msg.ElementId = response.id
        return Assembly(root)

    @overrides
    def get_element_by_id(self, element_id: str) -> engapi.IElement:
        raise NotImplementedError

    @property  # type: ignore
    @overrides
    def workflow_directory(self) -> str:
        # TODO: readonly?
        request = workflow_msg.WorkflowId()
        request.id = self._id
        response: workflow_msg.WorkflowGetDirectoryResponse = self._stub.WorkflowGetDirectory(
            request
        )
        return response.workflow_dir

    @property  # type: ignore
    @overrides
    def workflow_file_name(self) -> str:
        # return self._instance.modelFileName
        raise NotImplementedError

    @overrides
    def get_value(self, var_name: str) -> acvi.IVariableValue:
        request = element_msg.ElementId(id_string=var_name)
        response: var_val_msg.VariableState
        try:
            response = self._stub.VariableGetState(request)
        except grpc.RpcError as e:
            # TODO: how to handle?
            raise e

        def convert(val: ArrayLike, dims: ArrayLike, val_type: Type) -> acvi.IVariableValue:
            return val_type(shape_=dims, values=np.array(val).flatten())

        value = getattr(response.value, response.value.WhichOneof("value"))
        if isinstance(value, float):
            return acvi.RealValue(value)
        elif isinstance(value, int):
            return acvi.IntegerValue(value)
        elif isinstance(value, bool):
            return acvi.BooleanValue(value)
        elif isinstance(value, str):
            return acvi.StringValue(value)
        elif isinstance(value, var_val_msg.DoubleArrayValue):
            return convert(value.values, value.dims.dims, acvi.RealArrayValue)
        elif isinstance(value, var_val_msg.IntegerArrayValue):
            return convert(value.values, value.dims.dims, acvi.IntegerArrayValue)
        elif isinstance(value, var_val_msg.BooleanArrayValue):
            return convert(value.values, value.dims.dims, acvi.BooleanArrayValue)
        elif isinstance(value, var_val_msg.StringArrayValue):
            return convert(value.values, value.dims.dims, acvi.StringArrayValue)
        else:
            # unsupported type (should be impossible)
            raise TypeError(f"Unsupported type was returned: {type(value)}")

    @overrides
    def create_component(
        self,
        server_path: str,
        name: str,
        parent: str,
        x_pos: Optional[object] = None,
        y_pos: Optional[object] = None,
    ) -> None:
        # self._instance.createComponent(server_path, name, parent, x_pos, y_pos)
        raise NotImplementedError

    @overrides
    def create_link(self, variable: str, equation: str) -> None:
        # self._instance.createLink(variable, equation)
        raise NotImplementedError

    @overrides
    def save_workflow(self) -> None:
        # self._instance.saveModel()
        raise NotImplementedError

    @overrides
    def save_workflow_as(self, file_name: str) -> None:
        # self._instance.saveModelAs(file_name)
        raise NotImplementedError

    @overrides
    def close_workflow(self) -> None:
        # self._instance.closeModel()
        raise NotImplementedError

    @overrides
    def get_variable(self, name: str) -> object:
        # return WorkflowVariable(self._instance.getVariable(name))
        raise NotImplementedError

    @overrides
    def get_component(
        self, name: str
    ) -> wfapi.IComponent:  # IComponent, IIfComponent, IScriptComponent
        # mc_i_component: mcapiIComponent = self._instance.getComponent(name)
        # if mc_i_component is None:
        #     msg: str = i18n("Exceptions", "ERROR_COMPONENT_NOT_FOUND")
        #     raise Exception(msg)
        # return IComponent(mc_i_component)
        raise NotImplementedError

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
        # self._instance.removeComponent(name)
        raise NotImplementedError

    @overrides
    def break_link(self, variable: str) -> None:
        # self._instance.breakLink(variable)
        raise NotImplementedError

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
    def auto_link(self, src_comp: str, dest_comp: str) -> None:
        # self._instance.autoLink(src_comp, dest_comp)
        raise NotImplementedError

    @overrides
    def get_links(self, reserved: object = None) -> Iterable[wfapi.VariableLink]:
        # return dotnet_links_to_iterable(self._instance.getLinks(reserved))
        raise NotImplementedError

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
    def get_data_monitor(self, component: str, index: int) -> wfapi.DataMonitor:
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
    def get_data_explorer(self, index: int) -> Optional[wfapi.DataExplorer]:
        # de_object: object = self._instance.getDataExplorer(index)
        # if de_object is None:
        #     return None
        # else:
        #     return DataExplorer(de_object)
        raise NotImplementedError

    @overrides
    def move_component(self, component: str, parent: str, index: object) -> None:
        raise NotImplementedError

    @overrides
    def set_xml_extension(self, xml: str) -> None:
        raise NotImplementedError

    @overrides
    def set_assembly_style(
        self, assembly_name: str, style: object, width: object = None, height: object = None
    ) -> None:
        raise NotImplementedError

    @overrides
    def get_assembly_style(self, assembly_name: str) -> Tuple[int, int]:
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
    def create_and_init_component(
        self,
        server_path: str,
        name: str,
        parent: str,
        init_string: str,
        x_pos: object = None,
        y_pos: object = None,
    ):
        raise NotImplementedError

    @overrides
    def get_macro_script(self, macro_name: str) -> str:
        # return self._instance.getMacroScript(macro_name)
        raise NotImplementedError

    @overrides
    def set_macro_script(self, macro_name: str, script: str) -> None:
        # self._instance.setMacroScript(macro_name, script)
        raise NotImplementedError

    @overrides
    def get_macro_script_language(self, macro_name: str) -> str:
        # return self._instance.getMacroScriptLanguage(macro_name)
        raise NotImplementedError

    @overrides
    def set_macro_script_language(self, macro_name: str, language: str) -> None:
        # self._instance.setMacroScriptLanguage(macro_name, language)
        raise NotImplementedError

    @overrides
    def add_new_macro(self, macro_name: str, is_app_macro: bool) -> None:
        # self._instance.addNewMacro(macro_name, is_app_macro)
        raise NotImplementedError

    @overrides
    def get_variable_meta_data(self, name: str) -> acvi.CommonVariableMetadata:
        # metadata: acvi.CommonVariableMetadata = None
        # variable = self._instance.getVariableMetaData(name)  # PHXDATAHISTORYLib.IDHVariable
        # is_array: bool = variable.type.endswith("[]")
        # type_: str = variable.type[:-2] if is_array else variable.type
        #
        # if type_ == "double":
        #     if is_array:
        #         metadata = acvi.RealArrayMetadata()
        #     else:
        #         metadata = acvi.RealMetadata()
        #     # TODO: Where do other metadata come from? variable.getMetaData?
        #     # metadata.description =
        #     # metadata.units =
        #     # metadata.display_format =
        #     metadata.lower_bound = variable.lowerBound
        #     metadata.upper_bound = variable.upperBound
        #     metadata.enumerated_values = acvi.RealArrayValue.from_api_string(variable.enumValues)
        #     metadata.enumerated_aliases = acvi.StringArrayValue.from_api_string(
        #         variable.enumAliases
        #     )
        #
        # elif type_ == "integer":
        #     if is_array:
        #         metadata = acvi.IntegerArrayMetadata()
        #     else:
        #         metadata = acvi.IntegerMetadata()
        #     metadata.lower_bound = variable.lowerBound
        #     metadata.upper_bound = variable.upperBound
        #     metadata.enumerated_values = acvi.IntegerArrayValue.from_api_string(
        #       variable.enumValues)
        #     metadata.enumerated_aliases = acvi.StringArrayValue.from_api_string(
        #         variable.enumAliases
        #     )
        #
        # elif type_ == "boolean":
        #     if is_array:
        #         metadata = acvi.BooleanArrayMetadata()
        #     else:
        #         metadata = acvi.BooleanMetadata()
        #
        # elif type_ == "string":
        #     if is_array:
        #         metadata = acvi.StringArrayMetadata()
        #     else:
        #         metadata = acvi.StringMetadata()
        #     metadata.enumerated_values = acvi.StringArrayValue.from_api_string(
        #       variable.enumValues)
        #     metadata.enumerated_aliases = acvi.StringArrayValue.from_api_string(
        #         variable.enumAliases
        #     )
        # else:
        #     raise NotImplementedError
        #
        # # TODO: Add remaining types.
        # if metadata is not None:
        #     # Copy custom metadata.
        #     keys = variable.getMetaDataKeys()
        #     for key in keys:
        #         metadata.custom_metadata[key] = variable.getMetaData(key)
        # return metadata
        raise NotImplementedError

    @overrides
    def create_data_explorer(self, trade_study_type: str, setup: str) -> wfapi.DataExplorer:
        # de_object: object = self._instance.createDataExplorer(trade_study_type, setup)
        # return DataExplorer(de_object)
        raise NotImplementedError

    @overrides
    def get_macro_timeout(self, macro_name: str) -> float:
        # return self._instance.getMacroTimeout(macro_name)
        raise NotImplementedError

    @overrides
    def set_macro_timeout(self, macro_name: str, timeout: float) -> None:
        # self._instance.setMacroTimeout(macro_name, timeout)
        raise NotImplementedError

    @overrides
    def set_value(self, var_name: str, value: acvi.IVariableValue) -> None:
        try:
            value.accept(VariableValueVisitor(var_name, self._stub))
        except grpc.RpcError as e:
            # How should we handle errors here?
            raise e
