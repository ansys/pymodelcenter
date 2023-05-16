from typing import Generator

import pytest

import ansys.modelcenter.workflow.grpc_modelcenter as grpcmc


@pytest.fixture(name="engine")
def engine(monkeypatch) -> Generator[grpcmc.Engine, None, None]:
    def mock_start(self, run_only: bool = False):
        return 12345

    def mock_init(self):
        pass

    # mock Engine creation
    monkeypatch.setattr(grpcmc.MCDProcess, "start", mock_start)
    monkeypatch.setattr(grpcmc.MCDProcess, "__init__", mock_init)
    yield grpcmc.Engine(is_run_only=False)
