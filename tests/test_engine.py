import multiprocessing
from typing import Any, Collection, Mapping, Optional, Union, cast
import unittest
from unittest.mock import create_autospec

from ansys.engineeringworkflow.api import WorkflowEngineInfo
import ansys.platform.instancemanagement as pypim
import grpc
import numpy
import pytest

import ansys.modelcenter.workflow.api as mcapi
import ansys.modelcenter.workflow.grpc_modelcenter as grpcapi
import ansys.modelcenter.workflow.grpc_modelcenter as grpcmc
from ansys.modelcenter.workflow.grpc_modelcenter.grpc_error_interpretation import (
    EngineDisconnectedError,
)
import ansys.modelcenter.workflow.grpc_modelcenter.proto.engine_messages_pb2 as eng_msgs  # noqa: 501
from tests.grpc_server_test_utils.mock_grpc_exception import MockGrpcError

from .grpc_server_test_utils.client_creation_monkeypatch import monkeypatch_client_creation


class MockEngineClientForEngineTest:
    def __init__(self) -> None:
        self.username: str = ""
        self.password: str = ""
        self.pref_value: Optional[Union[bool, int, float, str]] = None
        self.raise_error_on_info: Optional[grpc.StatusCode] = None
        self.raise_error_on_heartbeat: Optional[grpc.StatusCode] = None
        self.workflow_already_open = False

    def GetEngineInfo(
        self, request: eng_msgs.GetServerInfoRequest
    ) -> eng_msgs.GetServerInfoResponse:
        if self.raise_error_on_info is not None:
            raise MockGrpcError(self.raise_error_on_info, "Simulated failure to communicate.")

        response = eng_msgs.GetServerInfoResponse()
        response.version.major = 1
        response.version.minor = 2
        response.version.patch = 3
        response.is_release = True
        response.build_type = "Mock"
        response.server_type = "WorkflowCenter"
        response.directory_path = "C:\\Path\\To\\ModelCenter\\"
        return response

    def EngineSetUserName(
        self, request: eng_msgs.SetUserNameRequest
    ) -> eng_msgs.SetUserNameResponse:
        self.username = request.user_name
        return eng_msgs.SetUserNameResponse()

    def EngineSetPassword(
        self, request: eng_msgs.SetPasswordRequest
    ) -> eng_msgs.SetPasswordResponse:
        self.password = request.password
        return eng_msgs.SetPasswordResponse()

    def EngineGetPreference(
        self, request: eng_msgs.GetPreferenceRequest
    ) -> eng_msgs.GetPreferenceResponse:
        response = eng_msgs.GetPreferenceResponse()
        if request.preference_name == "a":
            response.bool_value = True
        elif request.preference_name == "b":
            response.int_value = 1
        elif request.preference_name == "c":
            response.double_value = 2.3
        elif request.preference_name == "d":
            response.str_value = "e"
        return response

    def EngineSetPreference(
        self, request: eng_msgs.SetPreferenceRequest
    ) -> eng_msgs.SetPreferenceResponse:
        attr: Optional[str] = request.WhichOneof("value")
        if attr is not None:
            self.pref_value = getattr(request, attr)
        return eng_msgs.SetPreferenceResponse()

    def EngineGetUnitCategories(
        self, request: eng_msgs.GetUnitCategoriesRequest
    ) -> eng_msgs.GetUnitCategoriesResponse:
        response = eng_msgs.GetUnitCategoriesResponse()
        response.names.append("001_empty_category")
        response.names.append("002_length")
        response.names.append("003_seconds")
        return response

    def EngineGetUnitNames(
        self, request: eng_msgs.GetUnitNamesRequest
    ) -> eng_msgs.GetUnitNamesResponse:
        response = eng_msgs.GetUnitNamesResponse()
        if request.category == "002_length":
            response.names.append("inches")
            response.names.append("feet")
            response.names.append("mm")
            response.names.append("cm")
        elif request.category == "003_seconds":
            response.names.append("seconds")
        return response

    def EngineCreateWorkflow(
        self, request: eng_msgs.NewWorkflowRequest
    ) -> eng_msgs.NewWorkflowResponse:
        if self.workflow_already_open:
            raise MockGrpcError(
                code=grpc.StatusCode.RESOURCE_EXHAUSTED, details="We've already got one!"
            )
        response = eng_msgs.NewWorkflowResponse()
        response.workflow_id = "8675309"
        return response

    def EngineLoadWorkflow(
        self, request: eng_msgs.LoadWorkflowRequest
    ) -> eng_msgs.LoadWorkflowResponse:
        if self.workflow_already_open:
            raise MockGrpcError(
                code=grpc.StatusCode.RESOURCE_EXHAUSTED, details="We've already got one!"
            )
        response = eng_msgs.LoadWorkflowResponse()
        response.workflow_id = "147258369"
        return response

    def Shutdown(self, request: eng_msgs.ShutdownRequest) -> eng_msgs.ShutdownResponse:
        return eng_msgs.ShutdownResponse()

    def Heartbeat(self, request: eng_msgs.HeartbeatRequest) -> eng_msgs.HeartbeatResponse:
        if self.raise_error_on_heartbeat:
            raise MockGrpcError(self.raise_error_on_heartbeat, "Simulated failure to communicate.")
        return eng_msgs.HeartbeatResponse()


mock_client: MockEngineClientForEngineTest


@pytest.fixture
def setup_function(monkeypatch):
    """
    Setup called before each test function in this module.
    """

    def mock_start(
        self,
        run_only: bool = False,
        force_local: bool = False,
        heartbeat_interval: numpy.uint = 30000,
        allowed_heartbeat_misses: numpy.uint = 3,
    ):
        return 12345

    def mock_init(self):
        pass

    def mock_process_start(self):
        pass

    monkeypatch.setattr(grpcapi.MCDProcess, "start", mock_start)
    monkeypatch.setattr(grpcapi.MCDProcess, "__init__", mock_init)
    monkeypatch.setattr(multiprocessing.Process, "start", mock_process_start)
    global mock_client
    mock_client = MockEngineClientForEngineTest()
    monkeypatch_client_creation(monkeypatch, grpcapi.Engine, mock_client)


def test_get_units(setup_function) -> None:
    # Setup
    sut = grpcapi.Engine()

    # Execute
    result: Mapping[str, Collection[str]] = sut.get_units()

    # Verify
    assert len(result.keys()) == 3
    assert len(result["001_empty_category"]) == 0
    assert len(result["002_length"]) == 4
    assert len(result["003_seconds"]) == 1


def test_get_run_only_mode(setup_function) -> None:
    # Setup
    sut = grpcapi.Engine(is_run_only=True)

    # Execute
    result: bool = sut.get_run_only_mode()

    # Verify
    assert result is True


@pytest.mark.parametrize("workflow_type", [mcapi.WorkflowType.DATA, mcapi.WorkflowType.PROCESS])
def test_new_workflow(setup_function, workflow_type: mcapi.WorkflowType) -> None:
    """
    Verify that new_workflow works as expected.

    Parameters
    ----------
    workflow_type The type of workflow to create.
    """

    # Setup
    engine = grpcapi.Engine()

    # SUT
    result: grpcapi.Workflow = engine.new_workflow("workflow.pxcz", workflow_type)

    # Verification
    assert isinstance(result, grpcapi.Workflow)
    assert result._id == "8675309"


def test_new_workflow_already_loaded(setup_function) -> None:
    engine = grpcapi.Engine()

    # SUT
    engine = grpcapi.Engine()
    mock_client.workflow_already_open = True

    with pytest.raises(grpcapi.WorkflowAlreadyLoadedError, match="We've already got one"):
        engine.new_workflow("workflow.pxcz", mcapi.WorkflowType.DATA)


def test_load_workflow(setup_function) -> None:
    """
    Verify that load_workflow works as expected.
    """

    # Setup
    engine = grpcapi.Engine()

    # SUT
    result: grpcapi.Workflow = engine.load_workflow("", False)

    # Verification
    assert isinstance(result, grpcapi.Workflow)
    assert result._id == "147258369"


def test_load_workflow_already_loaded(setup_function) -> None:
    engine = grpcapi.Engine()

    # SUT
    engine = grpcapi.Engine()
    mock_client.workflow_already_open = True

    with pytest.raises(grpcapi.WorkflowAlreadyLoadedError, match="We've already got one"):
        engine.load_workflow("workflow.pxcz", False)


@pytest.mark.parametrize(
    "fmt", ["General", "0.00", "$#,##0.00", "0.00%", "# ?/?", "0.00E+00", "EpSec"]
)
def test_get_formatter(setup_function, fmt: str) -> None:
    """
    Verify that get_formatter works as expected.

    Parameters
    ----------
    fmt: str
        The format style to use in the formatter.
    """
    # Setup
    engine = grpcapi.Engine()

    # SUT
    result: grpcapi.Format = engine.get_formatter(fmt)

    # Verification
    assert result.format == fmt


@pytest.mark.parametrize("key, value", [("a", True), ("b", 1), ("c", 2.3), ("d", "e")])
def test_get_preference(setup_function, key: str, value: object) -> None:
    """
    Verify that preferences of different value types can be retrieved.

    Parameters
    ----------
    key: str
        The preference key.
    value: object
        The preference value.
    """

    # Setup
    engine = grpcapi.Engine()

    # SUT
    result: object = engine.get_preference(key)

    # Verification
    assert result == value


def test_get_preference_no_value(setup_function) -> None:
    # Setup
    engine = grpcapi.Engine()

    # SUT
    with pytest.raises(Exception) as ex:
        engine.get_preference("key")
        assert ex.value == "Server did not return a value"


@pytest.mark.parametrize("value", [True, 1, 2.3, "e"])
def test_set_preference(setup_function, value: Union[bool, int, float, str]) -> None:
    # Setup
    engine = grpcapi.Engine()

    # SUT
    engine.set_preference("key", value)

    # Verification
    assert mock_client.pref_value == value


def test_get_engine_info(setup_function) -> None:
    """
    Verify that get_engine_info returns the correct information.
    """

    # Setup
    engine = grpcapi.Engine()

    # SUT
    info: WorkflowEngineInfo = engine.get_server_info()

    # Verification
    assert info.release_year == 1
    assert info.release_id == 2
    assert info.build == 3
    assert info.is_release_build
    assert info.build_type == "Mock"
    assert info.version_as_string == "1.2.3"
    assert info.server_type == "WorkflowCenter"
    assert info.install_location == "C:\\Path\\To\\ModelCenter\\"
    assert info.base_url is None


def test_get_engine_info_simulated_crash(setup_function) -> None:

    # Setup
    engine = grpcapi.Engine()
    mock_client.raise_error_on_info = grpc.StatusCode.UNAVAILABLE

    # SUT
    with pytest.raises(EngineDisconnectedError):
        engine.get_server_info()


def test_close(setup_function) -> None:
    """
    Verify that close calls Shutdown.
    """

    # Setup
    with unittest.mock.patch.object(
        mock_client, "Shutdown", return_value=eng_msgs.ShutdownResponse()
    ) as mock_grpc_method:
        with grpcapi.Engine() as sut:
            # SUT
            pass

        # Verification
        mock_grpc_method.assert_called_once_with(eng_msgs.ShutdownRequest())


def test_creation_via_pypim(monkeypatch) -> None:
    # Arrange
    mock_instance = pypim.Instance(
        definition_name="definitions/fake-modelcenter-desktop",
        name="instances/fake-modelcenter-desktop",
        ready=True,
        status_message=None,
        services={"grpc": pypim.Service(uri="localhost:50052", headers={})},
    )
    pim_channel = grpc.insecure_channel("localhost:50052")
    mock_instance.wait_for_ready = create_autospec(mock_instance.wait_for_ready)
    mock_instance.build_grpc_channel = create_autospec(
        mock_instance.build_grpc_channel, return_value=pim_channel
    )
    mock_instance.delete = create_autospec(mock_instance.delete)
    mock_pypim_client = pypim.Client(channel=grpc.insecure_channel("localhost:12345"))
    mock_pypim_client.create_instance = create_autospec(
        mock_pypim_client.create_instance, return_value=mock_instance
    )
    mock_connect = create_autospec(pypim.connect, return_value=mock_pypim_client)
    mock_is_configured = create_autospec(pypim.is_configured, return_value=True)
    monkeypatch.setattr(pypim, "connect", mock_connect)
    monkeypatch.setattr(pypim, "is_configured", mock_is_configured)

    # Act
    engine = grpcmc.Engine()
    result_channel = engine.channel
    engine.close()

    # Assert
    assert mock_is_configured.called
    assert mock_connect.called
    mock_pypim_client.create_instance.assert_called_with(
        product_name="modelcenter-desktop", product_version=None
    )
    assert mock_instance.wait_for_ready.called
    assert mock_instance.build_grpc_channel.called
    assert result_channel == pim_channel
    assert mock_instance.delete.called
    assert engine.is_local is False


def test_is_local(setup_function) -> None:
    # SUT
    engine = grpcapi.Engine()

    # Verification
    assert engine.is_local is True


def test_get_channel(setup_function) -> None:
    # Setup
    engine = grpcapi.Engine()

    # SUT
    channel = engine.channel

    # Assert
    assert cast(Any, channel)._channel.target() == b"localhost:12345"


def test_heartbeat_process_should_call_the_right_method(setup_function) -> None:
    """
    Verify the right method is started in the heartbeat process.
    """
    # Arrange/Act
    sut = grpcapi.Engine()

    # Assert
    assert sut._heartbeat_process._target == grpcmc.engine._heartbeat_loop  # type: ignore


def test_heartbeat_method_sends_grpc_calls_until_released(monkeypatch, setup_function) -> None:
    # Arrange
    class MockLock:
        acquire_count = 0

        def acquire(self, block):
            self.acquire_count += 1
            return self.acquire_count > 5

    mock_client_create = lambda channel, mock_client=mock_client: mock_client
    monkeypatch.setattr(grpcmc.Engine, "_create_client", mock_client_create)

    lock = MockLock()
    with unittest.mock.patch.object(
        mock_client, "Heartbeat", return_value=eng_msgs.HeartbeatResponse()
    ) as mock_grpc_method:
        # Act
        grpcmc.engine._heartbeat_loop(lock, "0.0.0.0:5051", 1)  # type: ignore

    # Assert
    assert mock_grpc_method.call_count == 5
    mock_grpc_method.assert_called_with(eng_msgs.HeartbeatRequest())
