"""Integration tests around Workflow functionality."""
import os
from typing import Collection, List, Mapping, Set
import unittest

import ansys.common.variableinterop as acvi
import ansys.engineeringworkflow.api as ewapi
import pytest

import ansys.modelcenter.workflow.api as mcapi
import ansys.modelcenter.workflow.grpc_modelcenter as grpcmc


def test_getting_the_workflow_root(workflow) -> None:
    # Act
    root: grpcmc.Assembly = workflow.get_root()

    # Assert
    assert root.full_name == "ワークフロー"
    assert root.name == "ワークフロー"
    assert root.control_type == "Sequence"
    assert root.parent_element_id == ""


def test_getting_elements_by_name(workflow) -> None:
    # Act
    assembly: ewapi.IElement = workflow.get_element_by_name(element_name="ワークフロー")
    component: ewapi.IElement = workflow.get_element_by_name(
        element_name="ワークフロー.all_types_コンポーネント"
    )
    variable: ewapi.IElement = workflow.get_element_by_name(
        element_name="ワークフロー.all_types_コンポーネント.boolIn"
    )

    # Assert
    assert isinstance(assembly, grpcmc.Assembly)
    assert assembly.full_name == "ワークフロー"
    assert isinstance(component, grpcmc.Component)
    assert component.full_name == "ワークフロー.all_types_コンポーネント"
    assert isinstance(variable, grpcmc.BooleanDatapin)
    assert variable.full_name == "ワークフロー.all_types_コンポーネント.boolIn"


def test_creating_a_new_assembly(workflow) -> None:
    # Arrange
    root: grpcmc.Assembly = workflow.get_root()

    # Act
    created: grpcmc.Assembly = workflow.create_assembly(
        name="assembly_シークエンス", parent=root, assembly_type="Sequence"
    )
    retrieved: mcapi.IAssembly = workflow.get_assembly("ワークフロー.assembly_シークエンス")

    assert created == retrieved


def test_creating_a_new_component(workflow) -> None:
    # Arrange
    root: grpcmc.Assembly = workflow.get_root()

    # Act
    created: grpcmc.Component = workflow.create_component(
        server_path=".\\all_types.pacz", name="component_全型", parent=root
    )
    retrieved: grpcmc.Component = workflow.get_component(name="ワークフロー.component_全型")

    # Assert
    assert created == retrieved


def test_removing_a_component(workflow) -> None:
    # Act
    workflow.remove_component(name="ワークフロー.all_types_コンポーネント")

    # Assert
    with pytest.raises(grpcmc.InvalidInstanceError) as ex:
        workflow.get_component(name="ワークフロー.all_types_コンポーネント")
    assert ex is not None


def test_getting_and_setting_a_variable_value(workflow) -> None:
    # Arrange
    new_value: acvi.IVariableValue = acvi.RealValue(87.32498)

    # Act
    initial_state: ewapi.VariableState = workflow.get_value(
        var_name="ワークフロー.all_types_コンポーネント.realIn"
    )
    workflow.set_value(var_name="ワークフロー.all_types_コンポーネント.realIn", value=new_value)
    final_state: ewapi.VariableState = workflow.get_value(
        var_name="ワークフロー.all_types_コンポーネント.realIn"
    )

    # Assert
    assert initial_state.value == 0
    assert initial_state.is_valid is True
    assert final_state.value == 87.32498
    assert final_state.is_valid is True


def test_getting_a_variable_and_its_metadata(workflow) -> None:
    # Act
    variable: mcapi.IDatapin = workflow.get_variable(name="ワークフロー.all_types_コンポーネント.realIn")
    metadata: acvi.CommonVariableMetadata = workflow.get_variable_meta_data(
        name="ワークフロー.all_types_コンポーネント.realIn"
    )

    # Assert
    assert variable.full_name == "ワークフロー.all_types_コンポーネント.realIn"
    assert metadata.variable_type == acvi.VariableType.REAL


def test_creating_and_getting_links(workflow) -> None:
    # Act
    workflow.create_link(
        variable="ワークフロー.all_types_コンポーネント.realIn", equation="ワークフロー.all_types_コンポーネント.intIn"
    )
    links: List[mcapi.IDatapinLink] = list(workflow.get_links())

    # Assert
    assert len(links) == 1
    assert links[0].rhs == "ワークフロー.all_types_コンポーネント.intIn"


def test_auto_linking(workflow) -> None:
    case = unittest.TestCase()

    # Arrange
    root: grpcmc.Assembly = workflow.get_root()
    quad1: grpcmc.Component = workflow.create_component(
        server_path="common:\\Functions\\Quadratic", name="quad一", parent=root
    )
    quad2: grpcmc.Component = workflow.create_component(
        server_path="common:\\Functions\\Quadratic", name="quad二", parent=root
    )

    # Act
    links: List[mcapi.IDatapinLink] = list(workflow.auto_link(src_comp=quad1, dest_comp=quad2))

    # Assert
    expected_rhs_list: Collection[str] = [
        "ワークフロー.quad一.a",
        "ワークフロー.quad一.b",
        "ワークフロー.quad一.c",
        "ワークフロー.quad一.x",
    ]
    actual_rhs_list = [link.rhs for link in links]
    case.assertCountEqual(expected_rhs_list, actual_rhs_list)


def test_workflow_save(engine) -> None:
    # Arrange
    workflow_name = "workflow_save_test.pxcz"
    workflow_path: str = os.path.join(os.getcwd(), workflow_name)
    if os.path.isfile(workflow_path):
        os.remove(workflow_path)  # delete the file if it already exists

    with engine.new_workflow(name=workflow_path) as new_workflow:
        root: grpcmc.Assembly = new_workflow.get_root()
        new_workflow.create_component(
            server_path="common:\\Functions\\Quadratic", name="quad二次", parent=root
        )

        # Act
        new_workflow.save_workflow()

    # Assert
    assert os.path.isfile(workflow_path)
    with engine.load_workflow(file_name=workflow_path) as loaded_workflow:
        loaded_workflow.get_component(name="Model.quad二次")


def test_workflow_save_as(engine) -> None:
    # Arrange
    workflow_path: str = os.path.join(os.getcwd(), "test_files", "all_types.pxcz")
    new_path: str = os.path.join(os.getcwd(), "workflow_save_as_test.pxcz")
    if os.path.isfile(new_path):
        os.remove(new_path)  # delete the file if it already exists

    with engine.load_workflow(file_name=workflow_path) as workflow:
        # Act
        workflow.save_workflow_as(file_name=new_path)

    # Assert
    assert os.path.isfile(new_path)
    with engine.load_workflow(file_name=workflow_path) as loaded_workflow:
        loaded_workflow.get_component(name="ワークフロー.all_types_コンポーネント")


def test_workflow_is_not_usable_after_close(workflow) -> None:
    # Act
    workflow.close_workflow()

    # Assert
    with pytest.raises(grpcmc.UnexpectedEngineError) as ex:
        workflow.get_root()
    assert (
        ex.value.args[0]
        == "The ModelCenter engine reported an unexpected error:\n"
        + "Message:Error: No workflow is currently loaded.\nCode:StatusCode.FAILED_PRECONDITION\n"
    )


def test_running_and_getting_results(workflow) -> None:
    # Arrange
    validation_names: Set[str] = set()
    collection_names: Set[str] = {"ワークフロー.all_types_コンポーネント"}
    inputs: Mapping[str, acvi.VariableState] = {
        "ワークフロー.all_types_コンポーネント.boolIn": acvi.VariableState(
            value=acvi.BooleanValue(True), is_valid=True
        ),
        "ワークフロー.all_types_コンポーネント.realIn": acvi.VariableState(
            value=acvi.RealValue(984.65646754), is_valid=True
        ),
        "ワークフロー.all_types_コンポーネント.intIn": acvi.VariableState(
            value=acvi.IntegerValue(1431655765), is_valid=True
        ),
        "ワークフロー.all_types_コンポーネント.strIn": acvi.VariableState(
            value=acvi.StringValue("•-•• --- •••- •"), is_valid=True
        ),
        "ワークフロー.all_types_コンポーネント.arrays.boolIn": acvi.VariableState(
            value=acvi.BooleanArrayValue(values=[True, False, False, True]), is_valid=True
        ),
        "ワークフロー.all_types_コンポーネント.arrays.realIn": acvi.VariableState(
            value=acvi.RealArrayValue(values=[1.1, 2.2, 3.3, 4.4]), is_valid=True
        ),
        "ワークフロー.all_types_コンポーネント.arrays.intIn": acvi.VariableState(
            value=acvi.IntegerArrayValue(values=[9, 8, 7, 6]), is_valid=True
        ),
        "ワークフロー.all_types_コンポーネント.arrays.strIn": acvi.VariableState(
            value=acvi.StringArrayValue(values=["風", "林", "火", "山"]), is_valid=True
        ),
    }

    # Act
    result: Mapping[str, acvi.VariableState] = workflow.run(
        inputs=inputs, reset=True, validation_names=validation_names, collect_names=collection_names
    )

    # Assert
    expected_results: Mapping[str, acvi.VariableState] = {
        "ワークフロー.all_types_コンポーネント.boolOut": acvi.VariableState(
            value=acvi.BooleanValue(True), is_valid=True
        ),
        "ワークフロー.all_types_コンポーネント.realOut": acvi.VariableState(
            value=acvi.RealValue(984.65646754), is_valid=True
        ),
        "ワークフロー.all_types_コンポーネント.intOut": acvi.VariableState(
            value=acvi.IntegerValue(1431655765), is_valid=True
        ),
        "ワークフロー.all_types_コンポーネント.strOut": acvi.VariableState(
            value=acvi.StringValue("•-•• --- •••- •"), is_valid=True
        ),
        "ワークフロー.all_types_コンポーネント.arrays.boolOut": acvi.VariableState(
            value=acvi.BooleanArrayValue(values=[True, False, False, True]), is_valid=True
        ),
        "ワークフロー.all_types_コンポーネント.arrays.realOut": acvi.VariableState(
            value=acvi.RealArrayValue(values=[1.1, 2.2, 3.3, 4.4]), is_valid=True
        ),
        "ワークフロー.all_types_コンポーネント.arrays.intOut": acvi.VariableState(
            value=acvi.IntegerArrayValue(values=[9, 8, 7, 6]), is_valid=True
        ),
        "ワークフロー.all_types_コンポーネント.arrays.strOut": acvi.VariableState(
            value=acvi.StringArrayValue(values=["風", "林", "火", "山"]), is_valid=True
        ),
    }
    assert expected_results == result
