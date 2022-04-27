"""Tests for Workflow."""

import pytest

import ansys.modelcenter.workflow.api as mcapi


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
