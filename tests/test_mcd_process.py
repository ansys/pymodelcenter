# Copyright (C) 2022 - 2026 ANSYS, Inc. and/or its affiliates.
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
def test_start_fails_to_get_stdout(monkeypatch) -> None:
    # Setup
    sut = MCDProcess()
    mock_process = MockProcess()
    mock_process.stdout = None
    with unittest.mock.patch.object(subprocess, "Popen", return_value=mock_process) as mock_popen:
        with pytest.raises(Exception) as err:
            result: int = sut.start()

        assert err.value.args[0] == "Failed to connect to ModelCenter stdout."


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
