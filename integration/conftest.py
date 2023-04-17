"""Shared test fixtures for the integration tests."""
from typing import Generator

import pytest

import ansys.modelcenter.workflow.grpc_modelcenter as grpcmc

engine: grpcmc.Engine
"""The Engine object used for all integration tests."""


@pytest.fixture(scope="session")
def create_engine() -> Generator[grpcmc.Engine, None, None]:
    """
    Setup called before each test function in this test session to create the SUT.
    """
    global engine
    with grpcmc.Engine(is_run_only=False) as engine:
        yield engine
