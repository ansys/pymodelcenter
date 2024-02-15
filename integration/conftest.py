"""Shared test fixtures for the integration tests."""
import os
from typing import Generator

import pytest

import ansys.modelcenter.workflow.grpc_modelcenter as grpcmc


@pytest.fixture(scope="session", name="engine")
def create_engine() -> Generator[grpcmc.Engine, None, None]:
    """
    Setup called before each test function in this test session to create the SUT.
    """
    with grpcmc.Engine(is_run_only=False) as engine:
        yield engine


@pytest.fixture(name="workflow")
def load_workflow(engine, request) -> Generator[grpcmc.Workflow, None, None]:
    file_name: str
    marker = request.node.get_closest_marker("workflow_name")
    if marker is None:
        file_name = "all_types.pxcz"
    else:
        file_name = marker.args[0]
    workflow_path: str = os.path.join(os.getcwd(), "test_files", file_name)
    with engine.load_workflow(file_name=workflow_path) as workflow:
        yield workflow
