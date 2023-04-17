"""Integration tests for ansys.modelcenter.workflow.grpc_modelcenter.Engine."""
import os

import ansys.modelcenter.workflow.api as mcapi


def test_new_workflow(create_engine) -> None:
    # Arrange
    workflow_name = "new_workflow_test.pxcz"
    workflow_path: str = os.path.join(os.getcwd(), workflow_name)
    if os.path.isfile(workflow_path):
        os.remove(workflow_path)  # delete the file if it already exists

    # Act
    with create_engine.new_workflow(
        name=workflow_path, workflow_type=mcapi.WorkflowType.DATA
    ) as workflow:
        # Assert
        assert workflow.workflow_file_name == workflow_name
        assert os.path.isfile(workflow_name)


def test_load_workflow(create_engine) -> None:
    # Arrange
    workflow_name = "all_types.pxcz"
    workflow_path: str = os.path.join(os.getcwd(), "test_files", workflow_name)

    # Act
    with create_engine.load_workflow(file_name=workflow_path) as workflow:
        # Assert
        assert workflow.workflow_file_name == workflow_name
