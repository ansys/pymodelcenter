# Copyright (C) 2022 - 2024 ANSYS, Inc. and/or its affiliates.
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

from typing import Generator

from ansys.api.modelcenter.v0.engine_messages_pb2 import (
    HeartbeatRequest,
    HeartbeatResponse,
    ShutdownRequest,
    ShutdownResponse,
)
import numpy
import pytest

import ansys.modelcenter.workflow.grpc_modelcenter as grpcmc

from .grpc_server_test_utils.client_creation_monkeypatch import monkeypatch_client_creation


class MockHeartbeatAndShutdownClient:
    def Shutdown(self, request: ShutdownRequest) -> ShutdownResponse:
        return ShutdownResponse()

    def Heartbeat(self, request: HeartbeatRequest) -> HeartbeatResponse:
        return HeartbeatResponse()


@pytest.fixture(name="engine")
def engine(monkeypatch) -> Generator[grpcmc.Engine, None, None]:
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

    # mock Engine creation
    monkeypatch.setattr(grpcmc.MCDProcess, "start", mock_start)
    monkeypatch.setattr(grpcmc.MCDProcess, "__init__", mock_init)
    monkeypatch_client_creation(monkeypatch, grpcmc.Engine, MockHeartbeatAndShutdownClient())
    with grpcmc.Engine(is_run_only=False) as engine:
        yield engine
