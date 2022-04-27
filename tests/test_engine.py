import pytest

import ansys.modelcenter.workflow.api as mcapi


@pytest.mark.parametrize(
    "workflow_type",
    [
        mcapi.WorkflowType.DATA,
        mcapi.WorkflowType.PROCESS
    ]
)
def test_new_workflow(workflow_type: mcapi.WorkflowType) -> None:
    """
    Verify that new_workflow works as expected.

    Parameters
    ----------
    workflow_type The type of workflow to create.
    """

    # Setup
    engine = mcapi.Engine()

    # SUT
    result: mcapi.Workflow = engine.new_workflow(workflow_type)

    # Verification
    assert isinstance(result, mcapi.Workflow)
    assert engine._instance.getCallCount("newModel") == 1


def test_new_workflow_with_existing() -> None:
    """
    Verify that new_workflow throws an appropriate exception when an \
    existing Workflow is not closed beforehand.
    """

    # Setup
    engine = mcapi.Engine()
    result: mcapi.Workflow = engine.new_workflow()

    # SUT
    with pytest.raises(Exception) as except_info:
        engine.new_workflow()

    # Verification
    assert except_info.value.args[0] == "Error: Only one Workflow can be open at a time. "\
                                        "Close the current Workflow before loading or creating a "\
                                        "new one."


@pytest.mark.parametrize(
    "path, error",
    [
        ("", mcapi.OnConnectionErrorMode.ERROR),
        # TODO: More cases when we have a real backend
    ]
)
def test_load_workflow(path: str, error: mcapi.OnConnectionErrorMode) -> None:
    """
    Verify that load_workflow works as expected.

    Parameters
    ----------
    path The path to the file to load.
    error The error handling mode to use.
    """

    # Setup
    engine = mcapi.Engine()

    # SUT
    result: mcapi.Workflow = engine.load_workflow(path, error)

    # Verification
    assert isinstance(result, mcapi.Workflow)
    assert engine._instance.getCallCount("loadModel") == 1


def test_load_workflow_existing() -> None:
    """
    Verify that load_workflow throws an appropriate exception when an \
    existing Workflow is not closed beforehand.
    """

    # Setup
    engine = mcapi.Engine()
    result: mcapi.Workflow = engine.new_workflow()

    # SUT
    with pytest.raises(Exception) as except_info:
        engine.load_workflow("", mcapi.OnConnectionErrorMode.ERROR)

    # Verification
    assert except_info.value.args[0] == "Error: Only one Workflow can be open at a time. " \
                                        "Close the current Workflow before loading or creating a " \
                                        "new one."


@pytest.mark.parametrize(
    "fmt",
    [
        "",
        "0.00",
        "$#,##0.00",
        "0.00%",
        "# ?/?",
        "0.00E+00",
        "EpSec"
    ]
)
def test_get_formatter(fmt: str) -> None:
    """
    Verify that get_formatter works as expected.

    Parameters
    ----------
    fmt The format style to use in the formatter.
    """
    # Setup
    engine = mcapi.Engine()

    # SUT
    result: mcapi.IFormat = engine.get_formatter(fmt)

    # Verification
    assert result.get_format() == fmt


def test_set_user_name() -> None:
    """
    Verify set_user_name works as expected.
    """
    # Setup
    engine = mcapi.Engine()

    # SUT
    engine.set_user_name("Bob")

    # Verification
    assert engine._instance.getCallCount("setUserName") == 1


def test_set_password() -> None:
    """
    Verify set_user_name works as expected.
    """
    # Setup
    engine = mcapi.Engine()

    # SUT
    engine.set_password("12345")

    # Verification
    assert engine._instance.getCallCount("setPassword") == 1


@pytest.mark.parametrize(
    "key, value",
    [
        ("a", True),
        ("b", 1),
        ("c", "2.3"),
        ("d", "e")
    ]
)
def test_get_preference(key: str, value: object) -> None:
    """

    Parameters
    ----------
    key The preference key.
    value The preference value.
    """

    # Setup
    engine = mcapi.Engine()
    engine._instance.setPreference(key, str(value))

    # SUT
    result: object = engine.get_preference(key)

    # Verification
    assert result == value or result == str(value)
    # boolean's return raw value, everything else is a string
