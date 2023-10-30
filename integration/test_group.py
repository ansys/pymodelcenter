"""Integration tests around Group functionality"""
from typing import Mapping

import ansys.modelcenter.workflow.api as mcapi
import ansys.modelcenter.workflow.grpc_modelcenter as grpcmc


def test_can_get_group_variables(workflow) -> None:
    # Arrange
    component: grpcmc.Component = workflow.get_component("ワークフロー.all_types_コンポーネント")
    group: mcapi.IGroup = next(iter(component.get_groups().values()))

    # Act
    variables: Mapping[str, mcapi.IDatapin] = group.get_datapins()

    # Assert
    assert variables == {
        "boolIn": workflow.get_datapin("ワークフロー.all_types_コンポーネント.arrays.boolIn"),
        "realIn": workflow.get_datapin("ワークフロー.all_types_コンポーネント.arrays.realIn"),
        "intIn": workflow.get_datapin("ワークフロー.all_types_コンポーネント.arrays.intIn"),
        "strIn": workflow.get_datapin("ワークフロー.all_types_コンポーネント.arrays.strIn"),
        "boolOut": workflow.get_datapin("ワークフロー.all_types_コンポーネント.arrays.boolOut"),
        "realOut": workflow.get_datapin("ワークフロー.all_types_コンポーネント.arrays.realOut"),
        "intOut": workflow.get_datapin("ワークフロー.all_types_コンポーネント.arrays.intOut"),
        "strOut": workflow.get_datapin("ワークフロー.all_types_コンポーネント.arrays.strOut"),
    }
