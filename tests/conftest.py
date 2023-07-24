from typing import Generator

import numpy
import pytest

import ansys.modelcenter.workflow.grpc_modelcenter as grpcmc
from ansys.modelcenter.workflow.grpc_modelcenter.proto.engine_messages_pb2 import (
    HeartbeatRequest, HeartbeatResponse, ShutdownRequest, ShutdownResponse)

from .grpc_server_test_utils.client_creation_monkeypatch import \
    monkeypatch_client_creation


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
