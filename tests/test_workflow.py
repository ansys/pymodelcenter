"""Tests for Workflow."""
import ansys.modelcenter.workflow.api as mcapi
import pytest
from typing import Optional


def test_get_component():
    # Setup
    engine = mcapi.Engine()
    workflow = engine.new_workflow()
    engine._instance.createComponent("a", "word", "a", 0, 0)

    # SUT
    result: mcapi.IComponent = workflow.get_component("a.word")

    # Verification
    assert result.get_name() == "word"


def test_get_component_missing():
    # Setup
    engine = mcapi.Engine()
    workflow = engine.new_workflow()

    # SUT
    with pytest.raises(Exception) as except_info:
        workflow.get_component("a.word")

    # Verification
    assert except_info.value.args[0] == "Error: A component with the given name was not found."


def test_trade_study_start():
    # Setup
    engine = mcapi.Engine()
    workflow = engine.new_workflow()

    # SUT
    workflow.trade_study_start()

    # Verification
    assert engine._instance.getCallCount("tradeStudyStart") == 1


def test_trade_study_end():
    # Setup
    engine = mcapi.Engine()
    workflow = engine.new_workflow()

    # SUT
    workflow.trade_study_end()

    # Verification
    assert engine._instance.getCallCount("tradeStudyEnd") == 1


def test_workflow_close():
    # Setup
    sut_engine = mcapi.Engine()
    sut_workflow: mcapi.Workflow = sut_engine.new_workflow()

    # Check pre-reqs.
    try:
        sut_engine.new_workflow()
        assert False, "Should have failed by now."
    except Exception:
        pass

    # Execute
    sut_workflow.close_workflow()

    # Verify
    next_workflow = sut_engine.new_workflow()
    assert isinstance(next_workflow, mcapi.Workflow)
    assert sut_engine._instance.getCallCount("closeModel") == 1


def test_save_workflow():
    # Setup
    sut_engine = mcapi.Engine()
    sut_workflow: mcapi.Workflow = sut_engine.new_workflow()
    assert sut_workflow._instance.getCallCount("saveModel") == 0

    # Execute
    sut_workflow.save_workflow()

    # Verify
    assert sut_workflow._instance.getCallCount("saveModel") == 1


def test_save_workflow_as():
    # Setup
    sut_engine = mcapi.Engine()
    sut_workflow: mcapi.Workflow = sut_engine.new_workflow()
    assert sut_workflow._instance.getCallCount("saveModelAs") == 0

    # Execute
    sut_workflow.save_workflow_as(r"C:\Temp\workflow.pxcz")

    # Verify
    assert sut_workflow._instance.getCallCount("saveModelAs") == 1
    argument = sut_workflow._instance.getArgumentRecord("saveModelAs", 0)[0]
    assert argument == r"C:\Temp\workflow.pxcz"


@pytest.mark.parametrize(
    'server_path,parent,name,x_pos,y_pos,expected_passed_x_pos,expected_passed_y_pos',
    [
        pytest.param('saserv://tests/add42', 'Adder', 'Workflow.model.workflow.model', 47, 42,
                     47, 42, id="fully specified position"),
        # It's difficult to test these cases, because the mock expects Missing.Value,
        # and that really screws with the reflection-based method matching in pythonnet,
        # since it seems Missing.Value has special meaning in that case.
        # Passing None doesn't work and neither does leaving the method off.
        # This is probably something that the real GRPC api will have to solve.
        # pytest.param('saserv://tests/add42', 'Adder', 'Workflow.model.workflow.model', None, 42,
        #             Missing.Value, 42, id="missing x value"),
        # pytest.param('saserv://tests/add42', 'Adder', 'Workflow.model.workflow.model', 47, None,
        #             47, Missing.Value, id="missing y value")
    ]
)
def test_create_component(
        server_path: str,
        name: str,
        parent: str,
        x_pos: Optional[object],
        y_pos: Optional[object],
        expected_passed_x_pos,
        expected_passed_y_pos
) -> None:
    # Setup
    sut_engine = mcapi.Engine()
    sut_workflow: mcapi.Workflow = sut_engine.new_workflow()
    assert sut_workflow._instance.getCallCount("createComponent") == 0

    # Execute
    sut_workflow.create_component(server_path, name, parent, x_pos, y_pos)

    # Verify
    assert sut_workflow._instance.getCallCount("createComponent") == 1
    assert sut_workflow._instance.getArgumentRecord("createComponent", 0) == [
        server_path, name, parent, expected_passed_x_pos, expected_passed_y_pos]


def test_create_link() -> None:
    # Setup
    sut_engine = mcapi.Engine()
    sut_workflow: mcapi.Workflow = sut_engine.new_workflow()
    assert sut_workflow._instance.getCallCount("createLink") == 0
    test_var_name = "inputs.var1"
    test_eqn = "Workflow.comp.output4"

    # Execute
    sut_workflow.create_link(test_var_name, test_eqn)

    # Verify
    assert sut_workflow._instance.getCallCount("createLink") == 1
    assert sut_workflow._instance.getArgumentRecord("createLink", 0) == [
        test_var_name, test_eqn
    ]