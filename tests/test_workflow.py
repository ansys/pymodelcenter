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


def test_create_data_explorer():
    """
    Verify that create_data_explorer works as expected.
    """
    # Setup
    engine = mcapi.Engine()
    workflow = engine.new_workflow()

    # SUT
    de: mcapi.DataExplorer = workflow.create_data_explorer("MockTradeStudyType", "Mock Setup")

    # Verification
    assert engine._instance.getCallCount("createDataExplorer") == 1
    assert de is not None


def test_run_macro() -> None:
    """
    Verify that run_macro works as expected.
    """

    # Setup
    engine = mcapi.Engine()
    workflow = engine.new_workflow()

    # SUT
    result: object = workflow.run_macro("macro", False)

    # Verification
    assert engine._instance.getCallCount("runMacro") == 1
    assert result is None  # arbitrary value from MockModelCenter


def test_add_new_macro() -> None:
    """
    Verify that add_new_macro works as expected.
    """

    # Setup
    engine = mcapi.Engine()
    workflow = engine.new_workflow()

    # SUT
    workflow.add_new_macro("macro", False)

    # Verification
    assert engine._instance.getCallCount("addNewMacro") == 1


def test_set_macro_script() -> None:
    """
    Verify that set_macro_script works as expected.
    """

    # Setup
    engine = mcapi.Engine()
    workflow = engine.new_workflow()

    # SUT
    workflow.set_macro_script("macro", "a script to run")

    # Verification
    assert engine._instance.getCallCount("setMacroScript") == 1


def test_get_macro_script() -> None:
    """
    Verify that get_macro_script works as expected.
    """

    # Setup
    engine = mcapi.Engine()
    workflow = engine.new_workflow()

    # SUT
    script: str = workflow.get_macro_script("macro")

    # Verification
    assert engine._instance.getCallCount("getMacroScript") == 1
    assert script == "ここには何もない！目を逸らしてください！"  # arbitrary value from MockModelCenter


def test_set_macro_script_language() -> None:
    """
    Verify that set_macro_script_language works as expected.
    """

    # Setup
    engine = mcapi.Engine()
    workflow = engine.new_workflow()

    # SUT
    workflow.set_macro_script_language("macro", "JavaScript")

    # Verification
    assert engine._instance.getCallCount("setMacroScriptLanguage") == 1


def test_get_macro_script_language() -> None:
    """
    Verify that get_macro_script_language works as expected.
    """

    # Setup
    engine = mcapi.Engine()
    workflow = engine.new_workflow()

    # SUT
    script: str = workflow.get_macro_script_language("macro")

    # Verification
    assert engine._instance.getCallCount("getMacroScriptLanguage") == 1
    assert script == "いろいろなブランドの美味しさが楽しめます"  # arbitrary value from MockModelCenter


def test_set_macro_timeout() -> None:
    """
    Verify that set_macro_timeout works as expected.
    """

    # Setup
    engine = mcapi.Engine()
    workflow = engine.new_workflow()

    # SUT
    workflow.set_macro_timeout("macro", 3.5)

    # Verification
    assert engine._instance.getCallCount("setMacroTimeout") == 1


def test_get_macro_timeout() -> None:
    """
    Verify that get_macro_timeout works as expected.
    """

    # Setup
    engine = mcapi.Engine()
    workflow = engine.new_workflow()

    # SUT
    timeout: float = workflow.get_macro_timeout("macro")

    # Verification
    assert engine._instance.getCallCount("getMacroTimeout") == 1
    assert timeout == 25.0  # arbitrary value from MockModelCenter
