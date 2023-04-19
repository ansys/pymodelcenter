"""Integration tests around Component functionality"""
import os
from typing import Collection, Mapping

import ansys.engineeringworkflow.api as ewapi

import ansys.modelcenter.workflow.api as mcapi


def test_can_get_component_properties(engine) -> None:
    """Verify getting component and its properties."""
    # Arrange
    workflow_name = "all_types.pxcz"
    workflow_path: str = os.path.join(os.getcwd(), "test_files", workflow_name)

    with engine.load_workflow(file_name=workflow_path) as workflow:
        # Act
        component: mcapi.Component = workflow.get_component("ワークフロー.all_types_コンポーネント")

        # Assert
        assert component is not None
        assert component.name == "all_types_コンポーネント"
        assert component.full_name == "ワークフロー.all_types_コンポーネント"
        assert component.element_id is not None and component.element_id
        assert component.parent_element_id is not None and component.parent_element_id
        source: str = component.get_source()  # it's a method, should be a property?
        assert source is not None and source
        assert source == ".\\all_types.pacz"
        assert component.is_connected
        assert component.pacz_url == ".\\all_types.pacz"
        assert component.control_type == "Component"
        assert component.index_in_parent == 0
        assert component.parent_assembly is not None
        assert component.groups is not None
