from typing import Generator

import numpy
import pytest

import ansys.modelcenter.workflow.grpc_modelcenter as grpcmc


@pytest.fixture
def anyio_backend():
    return "asyncio"


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

    # mock Engine creation
    monkeypatch.setattr(grpcmc.MCDProcess, "start", mock_start)
    monkeypatch.setattr(grpcmc.MCDProcess, "__init__", mock_init)
    yield grpcmc.Engine(is_run_only=False)
