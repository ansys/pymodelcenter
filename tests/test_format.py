"""Tests for Format."""
from typing import Dict

import numpy
import pytest
from numpy import float64, int64

import ansys.modelcenter.workflow.grpc_modelcenter as mcapi
import ansys.modelcenter.workflow.grpc_modelcenter.proto.engine_messages_pb2 as engine_messages  # noqa: 501
import ansys.modelcenter.workflow.grpc_modelcenter.proto.format_messages_pb2 as format_messages  # noqa: 501

from .grpc_server_test_utils.client_creation_monkeypatch import \
    monkeypatch_client_creation


class MockEngineClientForFormatTest:
    def __init__(self) -> None:
        self._str_to_int_responses: Dict[str, int64] = {}
        self._str_to_real_responses: Dict[str, float64] = {}
        self._int_to_str_responses: Dict[int64, str] = {}
        self._real_to_str_responses: Dict[float64, str] = {}

    @property
    def str_to_int_responses(self) -> Dict[str, int64]:
        return self._str_to_int_responses

    @property
    def str_to_real_responses(self) -> Dict[str, float64]:
        return self._str_to_real_responses

    @property
    def int_to_str_responses(self) -> Dict[int64, str]:
        return self._int_to_str_responses

    @property
    def real_to_str_responses(self) -> Dict[float64, str]:
        return self._real_to_str_responses

    def FormatStringToInteger(
        self, request: format_messages.FormatFromStringRequest
    ) -> format_messages.FormatToIntegerResponse:
        key: str = request.original
        if request.format == "mockFormat":
            key = key.lstrip("ඞ")
        return format_messages.FormatToIntegerResponse(result=self._str_to_int_responses[key])

    def FormatStringToDouble(
        self, request: format_messages.FormatFromStringRequest
    ) -> format_messages.FormatToDoubleResponse:
        key: str = request.original
        if request.format == "mockFormat":
            key = key.lstrip("ඞ")
        return format_messages.FormatToDoubleResponse(result=self._str_to_real_responses[key])

    def FormatIntegerToString(
        self, request: format_messages.FormatFromIntegerRequest
    ) -> format_messages.FormatToStringResponse:
        result: str = self._int_to_str_responses[request.original]
        if request.format == "mockFormat":
            result = "ඞ" + result
        return format_messages.FormatToStringResponse(result=result)

    def FormatDoubleToString(
        self, request: format_messages.FormatFromDoubleRequest
    ) -> format_messages.FormatToStringResponse:
        result: str = self._real_to_str_responses[float64(request.original)]
        if request.format == "mockFormat":
            result = "ඞ" + result
        return format_messages.FormatToStringResponse(result=result)

    def FormatStringToString(
        self, request: format_messages.FormatFromStringRequest
    ) -> format_messages.FormatToStringResponse:
        result: str = request.original
        if request.format == "mockFormat":
            result = "ඞ" + result
        return format_messages.FormatToStringResponse(result=result)

    def FormatIntegerToEditString(
        self, request: format_messages.FormatFromIntegerRequest
    ) -> format_messages.FormatToStringResponse:
        result: str = self._int_to_str_responses[request.original]
        if request.format == "mockFormat":
            result = "ඞ" + result
        return format_messages.FormatToStringResponse(result=result)

    def FormatDoubleToEditString(
        self, request: format_messages.FormatFromDoubleRequest
    ) -> format_messages.FormatToStringResponse:
        result: str = self._real_to_str_responses[float64(request.original)]
        if request.format == "mockFormat":
            result = "ඞ" + result
        return format_messages.FormatToStringResponse(result=result)

    def Heartbeat(
        self, request: engine_messages.HeartbeatRequest
    ) -> engine_messages.HeartbeatResponse:
        return engine_messages.HeartbeatResponse


engine: mcapi.Engine
mock_client: MockEngineClientForFormatTest


@pytest.fixture
def setup_function(monkeypatch) -> None:
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
        pass

    def mock_init(self):
        pass

    monkeypatch.setattr(mcapi.MCDProcess, "start", mock_start)
    monkeypatch.setattr(mcapi.MCDProcess, "__init__", mock_init)
    global mock_client
    mock_client = MockEngineClientForFormatTest()
    monkeypatch_client_creation(monkeypatch, mcapi.Format, mock_client)

    global engine
    monkeypatch_client_creation(monkeypatch, mcapi.Engine, mock_client)
    engine = mcapi.Engine()


def test_get_format(setup_function) -> None:
    """Verifies the getter of the format property."""
    # Setup
    sut: mcapi.Format = engine.get_formatter("")

    # SUT
    result: str = sut.format

    # Verification
    assert result == "General"


def test_set_format(setup_function) -> None:
    """Verifies the setter of the format property."""
    # Setup
    sut: mcapi.Format = engine.get_formatter("")

    # SUT
    sut.format = "mockFormat"
    result: str = sut.format

    # Verification
    assert result == "mockFormat"


@pytest.mark.parametrize(
    "format_, string",
    [
        pytest.param("General", "5"),
        pytest.param("mockFormat", "ඞ5"),
    ],
)
def test_string_to_integer(setup_function, format_: str, string: str) -> None:
    """Verifies the string_to_integer method."""
    # Setup
    sut: mcapi.Format = engine.get_formatter(format_)
    mock_client.str_to_int_responses["5"] = 5

    # SUT
    result: int = sut.string_to_integer(string)

    # Verification
    assert isinstance(result, int)
    assert result == 5


@pytest.mark.parametrize(
    "format_, string",
    [
        pytest.param("General", "5.5"),
        pytest.param("mockFormat", "ඞ5.5"),
    ],
)
def test_string_to_real(setup_function, format_: str, string: str) -> None:
    """Verifies the string_to_real method."""
    # Setup
    sut: mcapi.Format = engine.get_formatter(format_)
    mock_client.str_to_real_responses["5.5"] = float64(5.5)

    # SUT
    result: float = sut.string_to_real(string)

    # Verification
    assert isinstance(result, float)
    assert result == 5.5


@pytest.mark.parametrize(
    "format_, expected",
    [
        pytest.param("General", "5"),
        pytest.param("mockFormat", "ඞ5"),
    ],
)
def test_integer_to_string(setup_function, format_: str, expected: str) -> None:
    """Verifies the integer_to_string method."""
    # Setup
    sut: mcapi.Format = engine.get_formatter(format_)
    mock_client.int_to_str_responses[5] = "5"

    # SUT
    result: str = sut.integer_to_string(5)

    # Verification
    assert isinstance(result, str)
    assert result == expected


@pytest.mark.parametrize(
    "format_, expected",
    [
        pytest.param("General", "5.5"),
        pytest.param("mockFormat", "ඞ5.5"),
    ],
)
def test_real_to_string(setup_function, format_: str, expected: str) -> None:
    """Verifies the real_to_string method."""
    # Setup
    sut: mcapi.Format = engine.get_formatter(format_)
    mock_client.real_to_str_responses[float64(5.5)] = "5.5"

    # SUT
    result: str = sut.real_to_string(float64(5.5))

    # Verification
    assert isinstance(result, str)
    assert result == expected


@pytest.mark.parametrize(
    "format_, expected",
    [
        pytest.param("General", "abc"),
        pytest.param("mockFormat", "ඞabc"),
    ],
)
def test_string_to_string(setup_function, format_: str, expected: str) -> None:
    """Verifies the string_to_string method."""
    # Setup
    sut: mcapi.Format = engine.get_formatter(format_)

    # SUT
    result: str = sut.string_to_string("abc")

    # Verification
    assert isinstance(result, str)
    assert result == expected


@pytest.mark.parametrize(
    "format_, expected",
    [
        pytest.param("General", "5"),
        pytest.param("mockFormat", "ඞ5"),
    ],
)
def test_integer_to_editable_string(setup_function, format_: str, expected: str) -> None:
    """Verifies the integer_to_editable_string method."""
    # Setup
    sut: mcapi.Format = engine.get_formatter(format_)
    mock_client.int_to_str_responses[5] = "5"

    # SUT
    result: str = sut.integer_to_editable_string(5)

    # Verification
    assert isinstance(result, str)
    assert result == expected


@pytest.mark.parametrize(
    "format_, expected",
    [
        pytest.param("General", "5.5"),
        pytest.param("mockFormat", "ඞ5.5"),
    ],
)
def test_real_to_editable_string(setup_function, format_: str, expected: str) -> None:
    """Verifies the real_to_editable_string method."""
    # Setup
    sut: mcapi.Format = engine.get_formatter(format_)
    mock_client.real_to_str_responses[float64(5.5)] = "5.5"

    # SUT
    result: str = sut.real_to_editable_string(float64(5.5))

    # Verification
    assert isinstance(result, str)
    assert result == expected
