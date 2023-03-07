"""Implementation of Engine."""
from os import PathLike
from string import Template
from typing import Any, Union

from ansys.engineeringworkflow.api import IWorkflowInstance, WorkflowEngineInfo
import grpc
import mcd_process
from overrides import overrides
import proto.engine_messages_pb2 as engine_messages
import proto.grpc_modelcenter_pb2_grpc as mcd_grpc

from ansys.modelcenter.workflow.api import DataExplorer
from ansys.modelcenter.workflow.api import Engine as IEngine
from ansys.modelcenter.workflow.api import Format, OnConnectionErrorMode, Workflow, WorkflowType


class Engine(IEngine):
    """GRPC implementation of IEngine."""

    def __init__(self):
        """Initialize a new Engine instance."""
        self._process = mcd_process.MCDProcess()
        self._process.start()
        self._channel = grpc.insecure_channel("localhost:50051")
        self._stub = mcd_grpc.GRPCModelCenterServiceStub(self._channel)

    def __enter__(self):
        """Initialization when created in a 'with' statement."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Clean up when leaving a 'with' block."""
        self.close()

    def close(self):
        """Shuts down the grpc server and clear out all objects."""
        request: Any = engine_messages.ShutdownRequest()
        self._stub.Shutdown(request)
        self._stub = None

        self._channel.close()
        self._channel = None

        self._process = None

    @property  # type: ignore
    @overrides
    def is_interactive(self) -> bool:
        return False

    @property  # type: ignore
    @overrides
    def process_id(self) -> int:
        return self._process.get_process_id()

    @overrides
    def new_workflow(self, name: str, workflow_type: WorkflowType = WorkflowType.DATA) -> Workflow:
        # if self._instance.getModel() is not None:
        #     msg: str = i18n("Exceptions", "ERROR_WORKFLOW_ALREADY_OPEN")
        #     raise Exception(msg)
        # else:
        #     self._instance.newModel(workflow_type.value)
        #     self._instance.saveModelAs(name)
        #     return Workflow(self._instance)
        return Workflow(None)

    @overrides
    def load_workflow(self, file_name: Union[PathLike, str]) -> IWorkflowInstance:
        # return self.load_workflow_ex(str(file_name))
        return IWorkflowInstance()

    @overrides
    def load_workflow_ex(
        self, file_name: str, on_connect_error: OnConnectionErrorMode = OnConnectionErrorMode.ERROR
    ) -> Workflow:
        # if self._instance.getModel() is not None:
        #     msg: str = i18n("Exceptions", "ERROR_WORKFLOW_ALREADY_OPEN")
        #     raise Exception(msg)
        # else:
        #     self._instance.loadModel(file_name, on_connect_error.value)
        #     return Workflow(self._instance)
        return Workflow(None)

    @overrides
    def get_formatter(self, fmt: str) -> Format:
        # formatter: Format = Format(self._instance.getFormatter(fmt))
        # return formatter
        return Format(None)

    @overrides
    def set_user_name(self, user_name: str) -> None:
        # self._instance.setUserName(user_name)
        return

    @overrides
    def set_password(self, password: str) -> None:
        # self._instance.setPassword(password)
        return

    @overrides
    def get_preference(self, pref: str) -> Union[bool, int, float, str]:
        # return self._instance.getPreference(pref)
        return False

    @overrides
    def get_num_unit_categories(self) -> int:
        # return self._instance.getNumUnitCategories()
        return 0

    @overrides
    def get_unit_category_name(self, index: int) -> str:
        # return self._instance.getUnitCategoryName(index)
        return ""

    @overrides
    def get_num_units(self, category: str) -> int:
        # return self._instance.getNumUnits(category)
        return 0

    @overrides
    def get_unit_name(self, category: str, index: int) -> str:
        # return self._instance.getUnitName(category, index)
        return ""

    @overrides
    def get_run_only_mode(self) -> bool:
        # return self._instance.getRunOnlyMode()
        return False

    @overrides
    def set_run_only_mode(self, should_be_in_run_only: bool) -> None:
        # self._instance.setRunOnlyMode(should_be_in_run_only)
        return

    @overrides
    def save_trade_study(self, uri: str, data_explorer: DataExplorer) -> None:
        # self._instance.saveTradeStudy(uri, 3, data_explorer)
        return

    @overrides
    def get_server_info(self) -> WorkflowEngineInfo:
        request: Any = engine_messages.GetServerInfoRequest()
        response: Any = self._stub.GetEngineInfo(request)

        version = {
            "major": response.version.major,
            "minor": response.version.minor,
            "patch": response.version.patch,
        }
        version_str: str = Template("${major}.${minor}.${patch}").safe_substitute(version)

        info = WorkflowEngineInfo(
            release_year=version["major"],
            release_id=version["minor"],
            build=version["patch"],
            is_release_build=response.is_release,
            build_type=response.build_type,
            version_as_string=version_str,
            server_type=response.server_type,
            install_location=response.directory_path,
            base_url=None,
        )
        return info


if __name__ == "__main__":
    with Engine() as test:
        result = test.get_server_info()
        print(result)
