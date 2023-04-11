"""Implementation of Engine."""
from os import PathLike
from string import Template
from typing import Collection, Dict, List, Mapping, Optional, Union

from ansys.engineeringworkflow.api import IWorkflowInstance, WorkflowEngineInfo
import grpc
from overrides import overrides

from ansys.modelcenter.workflow.api import IEngine, IFormat, IWorkflow, WorkflowType
import ansys.modelcenter.workflow.grpc_modelcenter.proto.engine_messages_pb2 as eng_msg

from .format import Format
from .mcd_process import MCDProcess
from .proto.grpc_modelcenter_pb2_grpc import GRPCModelCenterServiceStub
from .workflow import Workflow


class Engine(IEngine):
    """GRPC implementation of IEngine."""

    def __init__(self, is_run_only: bool = False):
        """Initialize a new Engine instance."""
        self._is_run_only: bool = is_run_only
        self._process = MCDProcess()
        port: int = self._process.start(is_run_only)
        self._channel = grpc.insecure_channel("localhost:" + str(port))
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
        request = eng_msg.ShutdownRequest()
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
        return self._process.get_process_id()  # pragma: no cover

    @overrides
    def new_workflow(self, name: str, workflow_type: WorkflowType = WorkflowType.DATA) -> IWorkflow:
        request = eng_msg.NewWorkflowRequest(
            path=name,
            workflow_type=eng_msg.DATA if workflow_type is WorkflowType.DATA else eng_msg.PROCESS,
        )
        response: eng_msg.NewWorkflowResponse = self._stub.EngineCreateWorkflow(request)
        return Workflow(response.workflow_id, name)

    @overrides
    def load_workflow(
        self, file_name: Union[PathLike, str], ignore_connection_errors: Optional[bool] = None
    ) -> IWorkflowInstance:
        request = eng_msg.LoadWorkflowRequest(
            path=str(file_name),
            connect_err_mode=eng_msg.IGNORE if ignore_connection_errors else eng_msg.ERROR,
        )
        response: eng_msg.LoadWorkflowResponse = self._stub.EngineLoadWorkflow(request)
        return Workflow(response.workflow_id, request.path)

    @overrides
    def get_formatter(self, fmt: str) -> IFormat:
        formatter: Format = Format(fmt)
        return formatter

    @overrides
    def get_preference(self, pref: str) -> Union[bool, int, float, str]:
        request = eng_msg.GetPreferenceRequest(preference_name=pref)
        response: eng_msg.GetPreferenceResponse = self._stub.EngineGetPreference(request)
        attr: Optional[str] = response.WhichOneof("value")
        if attr is not None:
            return getattr(response, attr)
        else:
            raise Exception("Server did not return a value.")

    @overrides
    def set_preference(self, pref: str, value: Union[bool, int, float, str]) -> None:
        request = eng_msg.SetPreferenceRequest(preference_name=pref)
        if isinstance(value, bool):
            request.bool_value = value
        elif isinstance(value, int):
            request.int_value = value
        elif isinstance(value, float):
            request.double_value = value
        else:
            request.str_value = value
        response: eng_msg.SetPreferenceResponse = self._stub.EngineSetPreference(request)

    @overrides
    def get_units(self) -> Mapping[str, Collection[str]]:
        result: Dict[str, List[str]] = {}
        category_request = eng_msg.GetUnitCategoriesRequest()
        category_response: eng_msg.GetUnitCategoriesResponse = self._stub.EngineGetUnitCategories(
            category_request
        )
        for category in category_response.names:
            result[category] = []
            request = eng_msg.GetUnitNamesRequest()
            request.category = category
            response: eng_msg.GetUnitNamesResponse = self._stub.EngineGetUnitNames(request)
            for unit in response.names:
                result[category].append(unit)
        return result

    @overrides
    def get_run_only_mode(self) -> bool:
        return self._is_run_only

    @overrides
    def get_server_info(self) -> WorkflowEngineInfo:
        request = eng_msg.GetServerInfoRequest()
        response: eng_msg.GetServerInfoResponse = self._stub.GetEngineInfo(request)

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
