import ansys.engineeringworkflow.api as aew_api
import ansys.tools.variableinterop as atvi
import pytest

import ansys.modelcenter.workflow.api as mc_api


@pytest.mark.workflow_name("data_assembly_tests.pxcz")
def test_correctly_gets_child_elements_data_model_empty(workflow) -> None:
    assembly: mc_api.IAssembly = workflow.get_assembly("Model.empty_assembly")
    child_elements = assembly.get_elements()
    assert len(child_elements) == 0


@pytest.mark.workflow_name("data_assembly_tests.pxcz")
def test_correctly_gets_child_elements_data_model_haschildren(workflow) -> None:
    # Setup
    assembly: mc_api.IAssembly = workflow.get_assembly("Model.has_children")

    # Execute
    child_elements = assembly.get_elements()

    # Verify
    assert len(child_elements) == 4
    assert isinstance(child_elements["child_assembly_one"], mc_api.IAssembly)
    assert child_elements["child_assembly_one"].full_name == "Model.has_children.child_assembly_one"
    assert isinstance(child_elements["child_assembly_two"], mc_api.IAssembly)
    assert child_elements["child_assembly_two"].full_name == "Model.has_children.child_assembly_two"
    assert isinstance(child_elements["Quad"], mc_api.IComponent)
    assert child_elements["Quad"].full_name == "Model.has_children.Quad"
    assert isinstance(child_elements["Cube"], mc_api.IComponent)
    assert child_elements["Cube"].full_name == "Model.has_children.Cube"


@pytest.mark.workflow_name("data_assembly_tests.pxcz")
def test_correctly_gets_parent_element_data_model(workflow) -> None:
    # Setup
    assembly: mc_api.IAssembly = workflow.get_assembly("Model.has_children.child_assembly_one")

    # Execute
    parent_assembly = assembly.get_parent_element()

    # Verify
    assert isinstance(parent_assembly, mc_api.IAssembly)
    assert parent_assembly.full_name == "Model.has_children"


@pytest.mark.workflow_name("data_assembly_tests.pxcz")
def test_parent_of_root_is_None_data_model(workflow) -> None:
    # Setup
    assembly: mc_api.IAssembly = workflow.get_assembly(None)

    # Execute
    parent_assembly = assembly.get_parent_element()

    # Verify
    assert parent_assembly is None


@pytest.mark.workflow_name("process_sequence_tests.pxcz")
def test_correctly_gets_child_elements_proc_empty(workflow) -> None:
    # Setup
    assembly: mc_api.IAssembly = workflow.get_assembly("Model.main_branch.empty_seq")

    # Execute
    results = assembly.get_elements()

    # Verify
    assert len(results) == 0


@pytest.mark.workflow_name("process_sequence_tests.pxcz")
def test_correctly_gets_child_elements_proc_haschildren(workflow) -> None:
    # Setup
    assembly: mc_api.IAssembly = workflow.get_assembly("Model.main_branch.has_items")

    # Execute
    child_elements = assembly.get_elements()

    # Verify
    assert len(child_elements) == 4
    assert isinstance(child_elements["quads"], mc_api.IAssembly)
    assert child_elements["quads"].full_name == "Model.main_branch.has_items.quads"
    assert isinstance(child_elements["Sum"], mc_api.IComponent)
    assert child_elements["Sum"].full_name == "Model.main_branch.has_items.Sum"
    assert isinstance(child_elements["cubes"], mc_api.IAssembly)
    assert child_elements["cubes"].full_name == "Model.main_branch.has_items.cubes"
    assert isinstance(child_elements["Script"], mc_api.IComponent)
    assert child_elements["Script"].full_name == "Model.main_branch.has_items.Script"

    # The order in which the elements appear is important;
    # it should correspond with the actual order in the sequence.
    child_element_order = [name for name in child_elements]
    assert child_element_order == ["quads", "Sum", "cubes", "Script"]


@pytest.mark.workflow_name("process_sequence_tests.pxcz")
def test_correctly_gets_child_elements_proc_after_move(workflow) -> None:
    # Setup
    assembly: mc_api.IAssembly = workflow.get_assembly("Model.main_branch.has_items")

    comp_to_move: mc_api.IComponent = workflow.get_component("Model.main_branch.has_items.Script")
    workflow.move_component(comp_to_move, assembly, 1)

    # Execute
    child_elements = assembly.get_elements()

    # Verify: There should be four child elements.
    assert len(child_elements) == 4
    assert isinstance(child_elements["quads"], mc_api.IAssembly)
    assert child_elements["quads"].full_name == "Model.main_branch.has_items.quads"
    assert isinstance(child_elements["Sum"], mc_api.IComponent)
    assert child_elements["Sum"].full_name == "Model.main_branch.has_items.Sum"
    assert isinstance(child_elements["cubes"], mc_api.IAssembly)
    assert child_elements["cubes"].full_name == "Model.main_branch.has_items.cubes"
    assert isinstance(child_elements["Script"], mc_api.IComponent)
    assert child_elements["Script"].full_name == "Model.main_branch.has_items.Script"
    # The order in which the elements appear is important;
    # it should correspond with the actual order in the sequence.
    child_element_order = [name for name in child_elements]
    assert child_element_order == ["quads", "Script", "Sum", "cubes"]


@pytest.mark.workflow_name("data_assembly_tests.pxcz")
def test_adding_data_assembly_to_empty_data_assembly(workflow) -> None:
    # Setup
    target_assembly: mc_api.IAssembly = workflow.get_assembly("Model.empty_assembly")

    # Execute
    new_child_assembly = target_assembly.add_assembly("new_assembly")

    # Verify
    assert isinstance(new_child_assembly, mc_api.IAssembly)
    assert new_child_assembly.full_name == "Model.empty_assembly.new_assembly"


@pytest.mark.workflow_name("data_assembly_tests.pxcz")
def test_adding_data_assembly_to_empty_data_assembly_with_position(workflow) -> None:
    # Setup
    target_assembly: mc_api.IAssembly = workflow.get_assembly("Model.empty_assembly")

    # Execute
    new_child_assembly = target_assembly.add_assembly("new_assembly", (47, 500))

    # Verify
    assert isinstance(new_child_assembly, mc_api.IAssembly)
    assert new_child_assembly.full_name == "Model.empty_assembly.new_assembly"
    assert new_child_assembly.get_analysis_view_position() == (47, 500)


@pytest.mark.workflow_name("data_assembly_tests.pxcz")
def test_adding_data_assembly_to_empty_data_assembly_invalid_name(workflow) -> None:
    # Setup
    target_assembly: mc_api.IAssembly = workflow.get_assembly("Model.empty_assembly")

    # Execute
    with pytest.raises(ValueError, match="invalid"):
        target_assembly.add_assembly("&&&")

    # Verify
    assert len(target_assembly.get_elements()) == 0, "The assembly should still be empty."


@pytest.mark.workflow_name("data_assembly_tests.pxcz")
def test_adding_data_assembly_to_populated_data_assembly_name_collision(workflow) -> None:
    # Setup
    target_assembly: mc_api.IAssembly = workflow.get_assembly("Model.has_children")
    assert (
        len(target_assembly.get_elements()) == 4
    ), "The number of assemblies should be 4 before taking any action."

    # Execute
    with pytest.raises(aew_api.NameCollisionError):
        target_assembly.add_assembly("Quad")

    # Verify
    assert len(target_assembly.get_elements()) == 4, "No new subassemblies should be added."


@pytest.mark.workflow_name("process_sequence_tests.pxcz")
def test_adding_datapin_to_data_assembly_valid(workflow) -> None:
    # Setup
    target_assembly: mc_api.IAssembly = workflow.get_assembly("Model.main_branch")

    # Execute
    datapin = target_assembly.add_datapin("データ", atvi.VariableType.INTEGER)

    # Verify
    assert isinstance(datapin, mc_api.IIntegerDatapin)
    assert datapin.full_name == "Model.main_branch.データ"


@pytest.mark.workflow_name("process_sequence_tests.pxcz")
def test_adding_datapin_to_data_assembly_invalid_name(workflow) -> None:
    # Setup
    target_assembly: mc_api.IAssembly = workflow.get_assembly("Model.main_branch")

    # Execute
    with pytest.raises(ValueError, match="invalid"):
        target_assembly.add_datapin("&&&", atvi.VariableType.INTEGER)

    # Verify
    assert len(target_assembly.get_datapins()) == 0


@pytest.mark.workflow_name("process_sequence_tests.pxcz")
def test_adding_datapin_to_data_assembly_name_collision(workflow) -> None:
    # Setup
    target_assembly: mc_api.IAssembly = workflow.get_assembly("Model.main_branch")
    datapin = target_assembly.add_datapin("データ", atvi.VariableType.INTEGER)
    assert isinstance(datapin, mc_api.IIntegerDatapin)
    assert datapin.full_name == "Model.main_branch.データ"

    # Execute
    with pytest.raises(aew_api.NameCollisionError):
        target_assembly.add_datapin("データ", atvi.VariableType.BOOLEAN)

    # Verify
    previous_datapin = target_assembly.get_datapins()["データ"]
    assert isinstance(previous_datapin, mc_api.IIntegerDatapin)
    assert previous_datapin.full_name == "Model.main_branch.データ"
    assert previous_datapin.element_id == datapin.element_id


@pytest.mark.workflow_name("process_sequence_tests.pxcz")
def test_rename_affects_child_elements(workflow) -> None:
    # Setup
    model: mc_api.IAssembly = workflow.get_assembly()
    main_branch: mc_api.IAssembly = workflow.get_assembly("Model.main_branch")
    has_items: mc_api.IAssembly = workflow.get_assembly("Model.main_branch.has_items")

    # Execute
    main_branch.rename("the_big_parallel")

    # Verify
    assert model.full_name == "Model"
    assert main_branch.full_name == "Model.the_big_parallel"
    assert has_items.full_name == "Model.the_big_parallel.has_items"
    assert has_items.get_parent_element() == main_branch
    assert main_branch.get_parent_element() == model


@pytest.mark.workflow_name("process_sequence_tests.pxcz")
def test_rename_name_collision(workflow) -> None:
    # Setup
    has_items: mc_api.IAssembly = workflow.get_assembly("Model.main_branch.has_items")
    no_children: mc_api.IAssembly = workflow.get_assembly("Model.main_branch.empty_seq")

    # Execute
    with pytest.raises(aew_api.NameCollisionError):
        no_children.rename("has_items")

    # Verify
    assert no_children.full_name == "Model.main_branch.empty_seq"
    assert has_items.full_name == "Model.main_branch.has_items"
