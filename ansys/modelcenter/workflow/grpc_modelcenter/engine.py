"""Implementation of Engine."""
from os import PathLike
from string import Template
from typing import Collection, Dict, List, Mapping, Optional, Union

from ansys.engineeringworkflow.api import IWorkflowInstance, WorkflowEngineInfo
import grpc
from overrides import overrides

from ansys.modelcenter.workflow.api import (
    IEngine,
    IFormat,
    IWorkflow,
    OnConnectionErrorMode,
    WorkflowType,
)

from .format import Format
from .mcd_process import MCDProcess
from .proto.engine_messages_pb2 import (
    DATA,
    PROCESS,
    GetPreferenceRequest,
    GetPreferenceResponse,
    GetServerInfoRequest,
    GetServerInfoResponse,
    GetUnitCategoriesRequest,
    GetUnitCategoriesResponse,
    GetUnitNamesRequest,
    GetUnitNamesResponse,
    LoadWorkflowRequest,
    LoadWorkflowResponse,
    NewWorkflowRequest,
    NewWorkflowResponse,
    SetPasswordRequest,
    SetUserNameRequest,
    ShutdownRequest,
)
from .proto.grpc_modelcenter_pb2_grpc import GRPCModelCenterServiceStub
from .workflow import Workflow


class Engine(IEngine):
    """GRPC implementation of IEngine."""

    def __init__(self, is_run_only: bool = False):
        """Initialize a new Engine instance."""
        self._is_run_only: bool = is_run_only
        self._process = MCDProcess()
        self._process.start(is_run_only)
        self._channel = grpc.insecure_channel("localhost:50051")
        self._stub = self._create_client(self._channel)
        self._workflow_id: Optional[str] = None

    def __enter__(self):
        """Initialization when created in a 'with' statement."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Clean up when leaving a 'with' block."""
        self.close()

    def close(self):
        """Shuts down the grpc server and clear out all objects."""
        request = ShutdownRequest()
        self._stub.Shutdown(request)
        self._stub = None

        self._channel.close()
        self._channel = None

        self._process = None

    @staticmethod
    def _create_client(grpc_channel) -> GRPCModelCenterServiceStub:
        """Create a client from a grpc channel."""
        return GRPCModelCenterServiceStub(grpc_channel)

    @property
    def process_id(self) -> int:
        """Get the id of the connected process; useful for debugging."""
        # Can also get this via grpc if we want.
        return self._process.get_process_id()

    @overrides
    def new_workflow(self, name: str, workflow_type: WorkflowType = WorkflowType.DATA) -> IWorkflow:
        request = NewWorkflowRequest()
        request.path = name
        request.workflow_type = DATA if workflow_type is WorkflowType.DATA else PROCESS
        response: NewWorkflowResponse = self._stub.EngineCreateWorkflow(request)
        return Workflow(response.workflow_id, name)

    @overrides
    def load_workflow(self, file_name: Union[PathLike, str]) -> IWorkflowInstance:
        return self.load_workflow_ex(file_name)

    @overrides
    def load_workflow_ex(
        self, file_name: str, on_connect_error: OnConnectionErrorMode = OnConnectionErrorMode.ERROR
    ) -> IWorkflow:
        if on_connect_error == OnConnectionErrorMode.DIALOG:
            raise ValueError("This client does not support UI mode.")
        request = LoadWorkflowRequest()
        request.path = file_name
        response: LoadWorkflowResponse = self._stub.EngineLoadWorkflow(request)
        return Workflow(response.workflow_id, file_name)

    @overrides
    def get_formatter(self, fmt: str) -> IFormat:
        formatter: Format = Format(fmt)
        return formatter

    @overrides
    def set_user_name(self, user_name: str) -> None:
        request = SetUserNameRequest()
        request.user_name = user_name
        self._stub.EngineSetUserName(request)

    @overrides
    def set_password(self, password: str) -> None:
        request = SetPasswordRequest()
        request.password = password
        self._stub.EngineSetPassword(request)

    @overrides
    def get_preference(self, pref: str) -> Union[bool, int, float, str]:
        request = GetPreferenceRequest()
        request.preference_name = pref
        response: GetPreferenceResponse = self._stub.EngineGetPreference(request)
        attr: Optional[str] = response.WhichOneof("value")
        if attr is not None:
            return getattr(response, attr)
        else:
            raise Exception("Server did not return a value.")

    @overrides
    def get_units(self) -> Mapping[str, Collection[str]]:
        result: Dict[str, List[str]] = {}
        category_request = GetUnitCategoriesRequest()
        category_response: GetUnitCategoriesResponse = self._stub.EngineGetUnitCategories(
            category_request
        )
        for category in category_response.names:
            result[category] = []
            request = GetUnitNamesRequest()
            request.category = category
            response: GetUnitNamesResponse = self._stub.EngineGetUnitNames(request)
            for unit in response.names:
                result[category].append(unit)
        return result

    @overrides
    def get_run_only_mode(self) -> bool:
        return self._is_run_only

    @overrides
    def get_server_info(self) -> WorkflowEngineInfo:
        request = GetServerInfoRequest()
        response: GetServerInfoResponse = self._stub.GetEngineInfo(request)

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
