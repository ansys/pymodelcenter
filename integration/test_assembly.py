import os
from typing import Generator

import ansys.common.variableinterop as acvi
import pytest

import ansys.modelcenter.workflow.api as mc_api
import ansys.modelcenter.workflow.grpc_modelcenter as grpcmc


@pytest.fixture(name="data_assembly_workflow")
def load_data_assembly_workflow(engine) -> Generator[mc_api.IWorkflow, None, None]:
    workflow_path: str = os.path.join(os.getcwd(), "test_files", "data_assembly_tests.pxcz")
    with engine.load_workflow(file_name=workflow_path) as workflow:
        yield workflow


@pytest.fixture(name="process_sequence_workflow")
def load_process_sequence_workflow(engine) -> Generator[mc_api.IWorkflow, None, None]:
    workflow_path: str = os.path.join(os.getcwd(), "test_files", "process_sequence_tests.pxcz")
    with engine.load_workflow(file_name=workflow_path) as workflow:
        yield workflow


def test_correctly_gets_child_elements_dd_empty(data_assembly_workflow: mc_api.IWorkflow):
    assembly: mc_api.IAssembly = data_assembly_workflow.get_assembly("Model.empty_assembly")
    child_elements = assembly.get_elements()
    assert len(child_elements) == 0


def test_correctly_gets_child_elements_dd_haschildren(data_assembly_workflow):
    # Setup
    assembly: mc_api.IAssembly = data_assembly_workflow.get_assembly("Model.has_children")

    # TODO: get_elements should be typed as returning a Sequence, not a Collection.
    # Execute
    child_elements = [element for element in assembly.get_elements()]

    # Verify
    assert len(child_elements) == 4
    assert isinstance(child_elements[0], mc_api.IAssembly)
    assert child_elements[0].full_name == "Model.has_children.child_assembly_one"
    assert isinstance(child_elements[1], mc_api.IAssembly)
    assert child_elements[1].full_name == "Model.has_children.child_assembly_two"
    assert isinstance(child_elements[2], mc_api.IComponent)
    assert child_elements[2].full_name == "Model.has_children.Quad"
    assert isinstance(child_elements[3], mc_api.IComponent)
    assert child_elements[3].full_name == "Model.has_children.Cube"


def test_correctly_gets_parent_element_dd(data_assembly_workflow):
    # Setup
    assembly: mc_api.IAssembly = data_assembly_workflow.get_assembly(
        "Model.has_children.child_assembly_one"
    )

    # Execute
    parent_assembly = assembly.get_parent_element()

    # Verify
    assert isinstance(parent_assembly, mc_api.IAssembly)
    assert parent_assembly.full_name == "Model.has_children"


def test_parent_of_root_is_None_dd(data_assembly_workflow):
    # Setup
    assembly: mc_api.IAssembly = data_assembly_workflow.get_assembly(None)

    parent_assembly = assembly.get_parent_element()

    assert parent_assembly is None


def test_correctly_gets_child_elements_proc_empty(process_sequence_workflow):
    # Setup
    assembly: mc_api.IAssembly = process_sequence_workflow.get_assembly(
        "Model.main_branch.empty_seq"
    )

    results = assembly.get_elements()

    assert len(results) == 0


def test_correctly_gets_child_elements_proc_haschildren(process_sequence_workflow):
    # Setup
    assembly: mc_api.IAssembly = process_sequence_workflow.get_assembly(
        "Model.main_branch.has_items"
    )

    # TODO: get_elements should be typed as returning a Sequence, not a Collection.
    child_elements = [element for element in assembly.get_elements()]

    # Verify: There should be four child elements.
    assert len(child_elements) == 4
    # The order in which the elements appear is important;
    # it should correspond with the actual order in the sequence.
    assert isinstance(child_elements[0], mc_api.IAssembly)
    assert child_elements[0].full_name == "Model.main_branch.has_items.quads"
    assert isinstance(child_elements[1], mc_api.IComponent)
    assert child_elements[1].full_name == "Model.main_branch.has_items.Sum"
    assert isinstance(child_elements[2], mc_api.IAssembly)
    assert child_elements[2].full_name == "Model.main_branch.has_items.cubes"
    assert isinstance(child_elements[3], mc_api.IComponent)
    assert child_elements[3].full_name == "Model.main_branch.has_items.Script"


def test_adding_data_assembly_to_empty_data_assembly(data_assembly_workflow):
    # Setup
    target_assembly: mc_api.IAssembly = data_assembly_workflow.get_assembly("Model.empty_assembly")

    new_child_assembly = target_assembly.add_assembly("new_assembly")

    assert isinstance(new_child_assembly, mc_api.IAssembly)
    assert new_child_assembly.full_name == "Model.empty_assembly.new_assembly"


def test_adding_data_assembly_to_empty_data_assembly_with_position(data_assembly_workflow):
    # Setup
    target_assembly: mc_api.IAssembly = data_assembly_workflow.get_assembly("Model.empty_assembly")

    new_child_assembly = target_assembly.add_assembly("new_assembly", (47, 500))

    assert isinstance(new_child_assembly, mc_api.IAssembly)
    assert new_child_assembly.full_name == "Model.empty_assembly.new_assembly"
    assert new_child_assembly.get_analysis_view_position() == (47, 500)


def test_adding_data_assembly_to_empty_data_assembly_invalid_name(data_assembly_workflow):
    # Setup
    target_assembly: mc_api.IAssembly = data_assembly_workflow.get_assembly("Model.empty_assembly")

    with pytest.raises(ValueError, match="invalid"):
        target_assembly.add_assembly("&&&")

    assert len(target_assembly.get_elements()) == 0, "The assembly should still be empty."


def test_adding_data_assembly_to_populated_data_assembly_name_collision(data_assembly_workflow):
    # Setup
    target_assembly: mc_api.IAssembly = data_assembly_workflow.get_assembly("Model.has_children")
    assert (
        len(target_assembly.get_elements()) == 4
    ), "The number of assemblies should be 4 before taking any action."

    with pytest.raises(grpcmc.NameCollisionError):
        target_assembly.add_assembly("Quad")

    assert len(target_assembly.get_elements()) == 4, "No new subassemblies should be added."


def test_adding_datapin_to_data_assembly_valid(process_sequence_workflow):
    # Setup
    target_assembly: mc_api.IAssembly = process_sequence_workflow.get_assembly("Model.main_branch")
    datapin = target_assembly.add_datapin("データ", acvi.VariableType.INTEGER)

    assert isinstance(datapin, mc_api.IIntegerDatapin)
    assert datapin.full_name == "Model.main_branch.データ"


def test_adding_datapin_to_data_assembly_invalid_name(process_sequence_workflow):
    # Setup
    target_assembly: mc_api.IAssembly = process_sequence_workflow.get_assembly("Model.main_branch")

    with pytest.raises(ValueError, match="invalid"):
        target_assembly.add_datapin("&&&", acvi.VariableType.INTEGER)

    assert len(target_assembly.get_datapins()) == 0


def test_adding_datapin_to_data_assembly_name_collision(process_sequence_workflow):
    # Setup
    target_assembly: mc_api.IAssembly = process_sequence_workflow.get_assembly("Model.main_branch")
    datapin = target_assembly.add_datapin("データ", acvi.VariableType.INTEGER)
    assert isinstance(datapin, mc_api.IIntegerDatapin)
    assert datapin.full_name == "Model.main_branch.データ"

    with pytest.raises(grpcmc.NameCollisionError):
        target_assembly.add_datapin("データ", acvi.VariableType.BOOLEAN)

    previous_datapin = target_assembly.get_datapins()["データ"]
    assert isinstance(previous_datapin, mc_api.IIntegerDatapin)
    assert previous_datapin.full_name == "Model.main_branch.データ"
    assert previous_datapin.element_id == datapin.element_id


def test_rename_affects_child_elements(process_sequence_workflow):
    # Setup
    model: mc_api.IAssembly = process_sequence_workflow.get_assembly()
    main_branch: mc_api.IAssembly = process_sequence_workflow.get_assembly("Model.main_branch")
    has_items: mc_api.IAssembly = process_sequence_workflow.get_assembly(
        "Model.main_branch.has_items"
    )

    # Execute
    main_branch.rename("the_big_parallel")

    # Verify
    assert model.full_name == "Model"
    assert main_branch.full_name == "Model.the_big_parallel"
    assert has_items.full_name == "Model.the_big_parallel.has_items"
    assert has_items.get_parent_element() == main_branch
    assert main_branch.get_parent_element() == model


def test_rename_name_collision(process_sequence_workflow):
    # Setup
    has_items: mc_api.IAssembly = process_sequence_workflow.get_assembly(
        "Model.main_branch.has_items"
    )
    no_children: mc_api.IAssembly = process_sequence_workflow.get_assembly(
        "Model.main_branch.empty_seq"
    )

    with pytest.raises(grpcmc.NameCollisionError):
        no_children.rename("has_items")

    assert no_children.full_name == "Model.main_branch.empty_seq"
    assert has_items.full_name == "Model.main_branch.has_items"
