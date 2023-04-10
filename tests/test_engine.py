from typing import Collection, Mapping, Optional, Union
import unittest

from ansys.engineeringworkflow.api import WorkflowEngineInfo
import pytest

import ansys.modelcenter.workflow.api as mcapi
import ansys.modelcenter.workflow.grpc_modelcenter as grpcapi
import ansys.modelcenter.workflow.grpc_modelcenter.proto.engine_messages_pb2 as eng_msgs  # noqa: 501

from .grpc_server_test_utils.client_creation_monkeypatch import monkeypatch_client_creation


class MockEngineClientForEngineTest:
    def __init__(self) -> None:
        self.username: str = ""
        self.password: str = ""
        self.pref_value: Optional[Union[bool, int, float, str]] = None

    def GetEngineInfo(
        self, request: eng_msgs.GetServerInfoRequest
    ) -> eng_msgs.GetServerInfoResponse:
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
        response = eng_msgs.NewWorkflowResponse()
        response.workflow_id = "8675309"
        return response

    def EngineLoadWorkflow(
        self, request: eng_msgs.LoadWorkflowRequest
    ) -> eng_msgs.LoadWorkflowResponse:
        response = eng_msgs.LoadWorkflowResponse()
        response.workflow_id = "147258369"
        return response

    def Shutdown(self, request: eng_msgs.ShutdownRequest) -> eng_msgs.ShutdownResponse:
        return eng_msgs.ShutdownResponse()


mock_client: MockEngineClientForEngineTest


@pytest.fixture
def setup_function(monkeypatch):
    """
    Setup called before each test function in this module.
    """

    def mock_start(self, run_only: bool = False):
        pass

    def mock_init(self):
        pass

    monkeypatch.setattr(grpcapi.MCDProcess, "start", mock_start)
    monkeypatch.setattr(grpcapi.MCDProcess, "__init__", mock_init)
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
