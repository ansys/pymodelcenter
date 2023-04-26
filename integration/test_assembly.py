import ansys.common.variableinterop as acvi
import pytest

import ansys.modelcenter.workflow.api as mc_api
import ansys.modelcenter.workflow.grpc_modelcenter as grpcmc


@pytest.mark.workflow_name("data_assembly_tests.pxcz")
def test_correctly_gets_child_elements_data_model_empty(workflow):
    assembly: mc_api.IAssembly = workflow.get_assembly("Model.empty_assembly")
    child_elements = assembly.get_elements()
    assert len(child_elements) == 0


@pytest.mark.workflow_name("data_assembly_tests.pxcz")
def test_correctly_gets_child_elements_data_model_haschildren(workflow):
    # Setup
    assembly: mc_api.IAssembly = workflow.get_assembly("Model.has_children")

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


@pytest.mark.workflow_name("data_assembly_tests.pxcz")
def test_correctly_gets_parent_element_data_model(workflow):
    # Setup
    assembly: mc_api.IAssembly = workflow.get_assembly("Model.has_children.child_assembly_one")

    # Execute
    parent_assembly = assembly.get_parent_element()

    # Verify
    assert isinstance(parent_assembly, mc_api.IAssembly)
    assert parent_assembly.full_name == "Model.has_children"


@pytest.mark.workflow_name("data_assembly_tests.pxcz")
def test_parent_of_root_is_None_data_model(workflow):
    # Setup
    assembly: mc_api.IAssembly = workflow.get_assembly(None)

    parent_assembly = assembly.get_parent_element()

    assert parent_assembly is None


@pytest.mark.workflow_name("process_sequence_tests.pxcz")
def test_correctly_gets_child_elements_proc_empty(workflow):
    # Setup
    assembly: mc_api.IAssembly = workflow.get_assembly("Model.main_branch.empty_seq")

    results = assembly.get_elements()

    assert len(results) == 0


@pytest.mark.workflow_name("process_sequence_tests.pxcz")
def test_correctly_gets_child_elements_proc_haschildren(workflow):
    # Setup
    assembly: mc_api.IAssembly = workflow.get_assembly("Model.main_branch.has_items")

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


@pytest.mark.workflow_name("data_assembly_tests.pxcz")
def test_adding_data_assembly_to_empty_data_assembly(workflow):
    # Setup
    target_assembly: mc_api.IAssembly = workflow.get_assembly("Model.empty_assembly")

    new_child_assembly = target_assembly.add_assembly("new_assembly")

    assert isinstance(new_child_assembly, mc_api.IAssembly)
    assert new_child_assembly.full_name == "Model.empty_assembly.new_assembly"


@pytest.mark.workflow_name("data_assembly_tests.pxcz")
def test_adding_data_assembly_to_empty_data_assembly_with_position(workflow):
    # Setup
    target_assembly: mc_api.IAssembly = workflow.get_assembly("Model.empty_assembly")

    new_child_assembly = target_assembly.add_assembly("new_assembly", (47, 500))

    assert isinstance(new_child_assembly, mc_api.IAssembly)
    assert new_child_assembly.full_name == "Model.empty_assembly.new_assembly"
    assert new_child_assembly.get_analysis_view_position() == (47, 500)


@pytest.mark.workflow_name("data_assembly_tests.pxcz")
def test_adding_data_assembly_to_empty_data_assembly_invalid_name(workflow):
    # Setup
    target_assembly: mc_api.IAssembly = workflow.get_assembly("Model.empty_assembly")

    with pytest.raises(ValueError, match="invalid"):
        target_assembly.add_assembly("&&&")

    assert len(target_assembly.get_elements()) == 0, "The assembly should still be empty."


@pytest.mark.workflow_name("data_assembly_tests.pxcz")
def test_adding_data_assembly_to_populated_data_assembly_name_collision(workflow):
    # Setup
    target_assembly: mc_api.IAssembly = workflow.get_assembly("Model.has_children")
    assert (
        len(target_assembly.get_elements()) == 4
    ), "The number of assemblies should be 4 before taking any action."

    with pytest.raises(grpcmc.NameCollisionError):
        target_assembly.add_assembly("Quad")

    assert len(target_assembly.get_elements()) == 4, "No new subassemblies should be added."


@pytest.mark.workflow_name("process_sequence_tests.pxcz")
def test_adding_datapin_to_data_assembly_valid(workflow):
    # Setup
    target_assembly: mc_api.IAssembly = workflow.get_assembly("Model.main_branch")
    datapin = target_assembly.add_datapin("データ", acvi.VariableType.INTEGER)

    assert isinstance(datapin, mc_api.IIntegerDatapin)
    assert datapin.full_name == "Model.main_branch.データ"


@pytest.mark.workflow_name("process_sequence_tests.pxcz")
def test_adding_datapin_to_data_assembly_invalid_name(workflow):
    # Setup
    target_assembly: mc_api.IAssembly = workflow.get_assembly("Model.main_branch")

    with pytest.raises(ValueError, match="invalid"):
        target_assembly.add_datapin("&&&", acvi.VariableType.INTEGER)

    assert len(target_assembly.get_datapins()) == 0


@pytest.mark.workflow_name("process_sequence_tests.pxcz")
def test_adding_datapin_to_data_assembly_name_collision(workflow):
    # Setup
    target_assembly: mc_api.IAssembly = workflow.get_assembly("Model.main_branch")
    datapin = target_assembly.add_datapin("データ", acvi.VariableType.INTEGER)
    assert isinstance(datapin, mc_api.IIntegerDatapin)
    assert datapin.full_name == "Model.main_branch.データ"

    with pytest.raises(grpcmc.NameCollisionError):
        target_assembly.add_datapin("データ", acvi.VariableType.BOOLEAN)

    previous_datapin = target_assembly.get_datapins()["データ"]
    assert isinstance(previous_datapin, mc_api.IIntegerDatapin)
    assert previous_datapin.full_name == "Model.main_branch.データ"
    assert previous_datapin.element_id == datapin.element_id


@pytest.mark.workflow_name("process_sequence_tests.pxcz")
def test_rename_affects_child_elements(workflow):
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
def test_rename_name_collision(workflow):
    # Setup
    has_items: mc_api.IAssembly = workflow.get_assembly("Model.main_branch.has_items")
    no_children: mc_api.IAssembly = workflow.get_assembly("Model.main_branch.empty_seq")

    with pytest.raises(grpcmc.NameCollisionError):
        no_children.rename("has_items")

    assert no_children.full_name == "Model.main_branch.empty_seq"
    assert has_items.full_name == "Model.main_branch.has_items"
