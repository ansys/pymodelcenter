import io
import subprocess
import unittest
from unittest.mock import patch

import pytest

from ansys.modelcenter.workflow.grpc_modelcenter import EngineLicensingFailedException, MCDProcess


class MockProcess:
    def __init__(self) -> None:
        self.stdout = io.BytesIO(b"garbage\r\n\r\ngrpc server listening on 0.0.0.0:50051\n")
        self.pid = 902


def mock_find_exe_location() -> str:
    return "C:\\ModelCenter.exe"


@patch(
    "ansys.modelcenter.workflow.grpc_modelcenter.mcd_process._find_exe_location",
    mock_find_exe_location,
)
def test_start(monkeypatch) -> None:
    # Setup
    sut = MCDProcess()
    mock_process = MockProcess()
    with unittest.mock.patch.object(subprocess, "Popen", return_value=mock_process) as mock_popen:
        # SUT
        result: int = sut.start()

        mock_popen.assert_called_once_with(
            ["C:\\ModelCenter.exe", "/Grpc", "/Automation", "/Heartbeat:30000:3"],
            stdout=subprocess.PIPE,
        )
        assert result == 50051


@patch(
    "ansys.modelcenter.workflow.grpc_modelcenter.mcd_process._find_exe_location",
    mock_find_exe_location,
)
def test_start_license_failure(monkeypatch) -> None:
    # Setup
    sut = MCDProcess()
    mock_process = MockProcess()
    mock_process.stdout = io.BytesIO(b"garbage\r\n\r\ngrpcmc: licensing failed\n")
    with unittest.mock.patch.object(subprocess, "Popen", return_value=mock_process) as mock_popoen:
        # SUT
        with pytest.raises(EngineLicensingFailedException):
            sut.start()


@patch(
    "ansys.modelcenter.workflow.grpc_modelcenter.mcd_process._find_exe_location",
    mock_find_exe_location,
)
def test_start_runonly(monkeypatch) -> None:
    # Setup
    sut = MCDProcess()
    mock_process = MockProcess()
    with unittest.mock.patch.object(subprocess, "Popen", return_value=mock_process) as mock_popen:
        # SUT
        result: int = sut.start(run_only=True)

        mock_popen.assert_called_once_with(
            ["C:\\ModelCenter.exe", "/Grpc", "/Automation", "/Heartbeat:30000:3", "/runonly"],
            stdout=subprocess.PIPE,
        )
        assert result == 50051


@patch(
    "ansys.modelcenter.workflow.grpc_modelcenter.mcd_process._find_exe_location",
    mock_find_exe_location,
)
def test_start_timeout(monkeypatch) -> None:
    # Setup
    sut = MCDProcess()
    mock_process = MockProcess()
    with unittest.mock.patch.object(subprocess, "Popen", return_value=mock_process) as mock_popen:
        sut._timeout = 0  # instant timeout

        # SUT
        with pytest.raises(Exception) as err:
            result: int = sut.start()

        mock_popen.assert_called_once_with(
            ["C:\\ModelCenter.exe", "/Grpc", "/Automation", "/Heartbeat:30000:3"],
            stdout=subprocess.PIPE,
        )
        assert err.value.args[0] == "Timed out waiting for ModelCenter to start."


@patch(
    "ansys.modelcenter.workflow.grpc_modelcenter.mcd_process._find_exe_location",
    mock_find_exe_location,
)
def test_get_process_id(monkeypatch) -> None:
    # Setup
    sut = MCDProcess()
    mock_process = MockProcess()
    with unittest.mock.patch.object(subprocess, "Popen", return_value=mock_process) as mock_popen:
        sut.start()

        # SUT
        result = sut.get_process_id()

        # Verification
        assert result == 902


@patch(
    "ansys.modelcenter.workflow.grpc_modelcenter.mcd_process._find_exe_location",
    mock_find_exe_location,
)
def test_get_process_id_before_start(monkeypatch) -> None:
    # Setup
    sut = MCDProcess()

    # SUT
    result = sut.get_process_id()

    # Verification
    assert result == -1
