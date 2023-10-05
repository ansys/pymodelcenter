"""Integration tests around Workflow functionality."""
import os
import tempfile
import time
from typing import Collection, List, Mapping, Set, cast
import unittest

import ansys.engineeringworkflow.api as eng_api
import ansys.engineeringworkflow.api as ewapi
import ansys.tools.variableinterop as atvi
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
        name="assembly_シークエンス", parent=root, assembly_type=mcapi.AssemblyType.SEQUENCE
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
    new_value: atvi.IVariableValue = atvi.RealValue(87.32498)

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
    metadata: atvi.CommonVariableMetadata = workflow.get_variable_meta_data(
        name="ワークフロー.all_types_コンポーネント.realIn"
    )

    # Assert
    assert variable.full_name == "ワークフロー.all_types_コンポーネント.realIn"
    assert metadata.variable_type == atvi.VariableType.REAL


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
    inputs: Mapping[str, atvi.VariableState] = {
        "ワークフロー.all_types_コンポーネント.boolIn": atvi.VariableState(
            value=atvi.BooleanValue(True), is_valid=True
        ),
        "ワークフロー.all_types_コンポーネント.realIn": atvi.VariableState(
            value=atvi.RealValue(984.65646754), is_valid=True
        ),
        "ワークフロー.all_types_コンポーネント.intIn": atvi.VariableState(
            value=atvi.IntegerValue(1431655765), is_valid=True
        ),
        "ワークフロー.all_types_コンポーネント.strIn": atvi.VariableState(
            value=atvi.StringValue("•-•• --- •••- •"), is_valid=True
        ),
        "ワークフロー.all_types_コンポーネント.arrays.boolIn": atvi.VariableState(
            value=atvi.BooleanArrayValue(values=[True, False, False, True]), is_valid=True
        ),
        "ワークフロー.all_types_コンポーネント.arrays.realIn": atvi.VariableState(
            value=atvi.RealArrayValue(values=[1.1, 2.2, 3.3, 4.4]), is_valid=True
        ),
        "ワークフロー.all_types_コンポーネント.arrays.intIn": atvi.VariableState(
            value=atvi.IntegerArrayValue(values=[9, 8, 7, 6]), is_valid=True
        ),
        "ワークフロー.all_types_コンポーネント.arrays.strIn": atvi.VariableState(
            value=atvi.StringArrayValue(values=["風", "林", "火", "山"]), is_valid=True
        ),
    }

    # Act
    result: Mapping[str, atvi.VariableState] = workflow.run(
        inputs=inputs, reset=True, validation_names=validation_names, collect_names=collection_names
    )

    # Assert
    expected_results: Mapping[str, atvi.VariableState] = {
        "ワークフロー.all_types_コンポーネント.boolOut": atvi.VariableState(
            value=atvi.BooleanValue(True), is_valid=True
        ),
        "ワークフロー.all_types_コンポーネント.realOut": atvi.VariableState(
            value=atvi.RealValue(984.65646754), is_valid=True
        ),
        "ワークフロー.all_types_コンポーネント.intOut": atvi.VariableState(
            value=atvi.IntegerValue(1431655765), is_valid=True
        ),
        "ワークフロー.all_types_コンポーネント.strOut": atvi.VariableState(
            value=atvi.StringValue("•-•• --- •••- •"), is_valid=True
        ),
        "ワークフロー.all_types_コンポーネント.arrays.boolOut": atvi.VariableState(
            value=atvi.BooleanArrayValue(values=[True, False, False, True]), is_valid=True
        ),
        "ワークフロー.all_types_コンポーネント.arrays.realOut": atvi.VariableState(
            value=atvi.RealArrayValue(values=[1.1, 2.2, 3.3, 4.4]), is_valid=True
        ),
        "ワークフロー.all_types_コンポーネント.arrays.intOut": atvi.VariableState(
            value=atvi.IntegerArrayValue(values=[9, 8, 7, 6]), is_valid=True
        ),
        "ワークフロー.all_types_コンポーネント.arrays.strOut": atvi.VariableState(
            value=atvi.StringArrayValue(values=["風", "林", "火", "山"]), is_valid=True
        ),
    }
    assert expected_results == result


def test_running_asynchronously_and_getting_results(workflow) -> None:
    # Arrange
    validation_names: Set[str] = set()
    inputs: Mapping[str, atvi.VariableState] = {
        "ワークフロー.all_types_コンポーネント.boolIn": atvi.VariableState(
            value=atvi.BooleanValue(True), is_valid=True
        ),
        "ワークフロー.all_types_コンポーネント.realIn": atvi.VariableState(
            value=atvi.RealValue(984.65646754), is_valid=True
        ),
        "ワークフロー.all_types_コンポーネント.intIn": atvi.VariableState(
            value=atvi.IntegerValue(1431655765), is_valid=True
        ),
        "ワークフロー.all_types_コンポーネント.strIn": atvi.VariableState(
            value=atvi.StringValue("•-•• --- •••- •"), is_valid=True
        ),
        "ワークフロー.all_types_コンポーネント.arrays.boolIn": atvi.VariableState(
            value=atvi.BooleanArrayValue(values=[True, False, False, True]), is_valid=True
        ),
        "ワークフロー.all_types_コンポーネント.arrays.realIn": atvi.VariableState(
            value=atvi.RealArrayValue(values=[1.1, 2.2, 3.3, 4.4]), is_valid=True
        ),
        "ワークフロー.all_types_コンポーネント.arrays.intIn": atvi.VariableState(
            value=atvi.IntegerArrayValue(values=[9, 8, 7, 6]), is_valid=True
        ),
        "ワークフロー.all_types_コンポーネント.arrays.strIn": atvi.VariableState(
            value=atvi.StringArrayValue(values=["風", "林", "火", "山"]), is_valid=True
        ),
    }

    # Act
    workflow.start_run(inputs=inputs, reset=True, validation_names=validation_names)
    after_run_state = workflow.get_state()
    time.sleep(1)
    end_state = workflow.get_state()

    # Assert
    assert after_run_state == eng_api.WorkflowInstanceState.RUNNING
    assert end_state == eng_api.WorkflowInstanceState.SUCCESS


@pytest.mark.workflow_name("file_tests.pxcz")
def test_run_setting_file_vars(workflow) -> None:
    with tempfile.TemporaryFile() as temp_file:
        temp_file.write(
            b"This is some temporary file content.\r\n" b"This is some more temporary file content."
        )
        temp_file.flush()
        with atvi.NonManagingFileScope() as file_scope:
            new_value = file_scope.read_from_file(temp_file.name, mime_type=None, encoding=None)

            results = workflow.run(
                inputs={"Model.fileReader.scalarFileIn": atvi.VariableState(new_value, True)},
                collect_names=set(["Model.fileReader.scalarFileContents"]),
            )
            assert (
                results["Model.fileReader.scalarFileContents"].safe_value
                == "This is some temporary file content.\r\n"
                "This is some more temporary file content."
            )


@pytest.mark.parametrize(
    "workflow_type",
    [mcapi.WorkflowType.DATA, mcapi.WorkflowType.PROCESS],
)
def test_create_and_run_optimizer_very_basic(engine, workflow_type) -> None:
    """
    Set up a very basic optimization problem from scratch.
    """
    workflow_name = "optimizer_create_test.pxcz"
    workflow_path: str = os.path.join(os.getcwd(), workflow_name)
    if os.path.isfile(workflow_path):
        os.remove(workflow_path)  # delete the file if it already exists

    # Create a new workflow
    with engine.new_workflow(workflow_path, workflow_type=workflow_type) as workflow:
        # Add an optimizer and a quadratic
        root: mcapi.IAssembly = workflow.get_root()
        optimizer: mcapi.IComponent = workflow.create_component(
            "component plug-in:SOFTWARE\\Phoenix Integration\\"
            "Component Plug-Ins\\Optimization Tool",
            "Optimizer",
            root,
        )
        parent = root if workflow_type == mcapi.WorkflowType.DATA else optimizer
        target: mcapi.IComponent = workflow.create_component(
            "common:\\Functions\\Quadratic",
            "Target",
            parent,
        )
        optimizer.get_datapins()["algorithm"].set_value(
            atvi.VariableState("4F3D67F6-5838-460F-8696-821D34C527AF", True)
        )

        # Configure the optimization objective
        objectives: mcapi.IDatapin = optimizer.get_datapins()["objectives"]
        assert isinstance(objectives, mcapi.IReferenceArrayDatapin)
        objectives_cast: mcapi.IReferenceArrayDatapin = cast(
            mcapi.IReferenceArrayDatapin, objectives
        )
        objectives_cast.set_length(1)
        objectives_cast[0].equation = target.full_name + ".y"
        objective_ref_props = objectives_cast.get_reference_properties()
        assert "goal" in objective_ref_props
        objective_ref_props["goal"].set_value_at(0, atvi.VariableState("solveFor", True))

        # Configure the design variable
        dvs: mcapi.IDatapin = optimizer.get_datapins()["continuousDesignVariables"]
        assert isinstance(dvs, mcapi.IReferenceArrayDatapin)
        dvs_cast: mcapi.IReferenceArrayDatapin = cast(mcapi.IReferenceArrayDatapin, dvs)
        dvs_cast.set_length(1)
        dvs_cast[0].equation = target.full_name + ".x"
        dvs_ref_props = dvs.get_reference_properties()
        assert "startValue" in dvs_ref_props
        dvs_ref_props["startValue"].set_value_at(
            0, atvi.VariableState(atvi.StringValue("5.0"), True)
        )
        assert "lowerBound" in dvs_ref_props
        dvs_ref_props["lowerBound"].set_value_at(0, atvi.VariableState(atvi.RealValue(-10.0), True))
        assert "upperBound" in dvs_ref_props
        dvs_ref_props["upperBound"].set_value_at(0, atvi.VariableState(atvi.RealValue(10.0), True))

        workflow.save_workflow()
        # Run the workflow
        workflow.run(validation_names={"Model.Optimizer.optimizationToolReturnStatus"})

        # Verify that optimization occurred
        assert workflow.get_variable(target.full_name + ".y").get_value().is_valid
        assert workflow.get_variable(target.full_name + ".y").get_value().value == 0.0
