import clr
clr.AddReference('phoenix-mocks/Phoenix.Mock.v45')

from System.Collections.Generic import List
from System import String

import ansys.modelcenter.workflow.api as mcapi
from typing import Any
import pytest


@pytest.mark.parametrize(
    "actual_value,expected_result",
    [
        pytest.param(0, False, id='zero is false'),
        pytest.param(1, True, id='one is true'),
        pytest.param(-1, True, id='negative one is true'),
    ]
)
def test_is_interactive(actual_value: int, expected_result: bool) -> None:
    """
    Test that the is_interactive implementation properly calls and interprets results
    from the mock.
    """
    sut: mcapi.Engine = mcapi.Engine()
    # Configure the mock to report a particular result when asked if it is interactive.
    sut._instance.IsInteractive = actual_value

    # Execute
    result: bool = sut.is_interactive

    # Verify
    assert result == expected_result


def test_process_id() -> None:
    # Setup
    # Construct an instance of the API adaptor.
    sut: mcapi.Engine = mcapi.Engine()
    # The mock contains a hardcoded implementation for the tested method.

    # Execute
    result: int = sut.process_id

    # Verify
    assert result == 4294967290


def __set_up_test_unit_categories(mock_mc: Any) -> None:
    mock_mc.SetSimulatedUnitCategoryUnits("001_empty_category", List[String]())
    length_measures: List[String] = List[String]()
    length_measures.Add("inches")
    length_measures.Add("feet")
    length_measures.Add("mm")
    length_measures.Add("cm")
    mock_mc.SetSimulatedUnitCategoryUnits("002_length", length_measures)
    seconds: List[String] = List[String]()
    seconds.Add("seconds")
    mock_mc.SetSimulatedUnitCategoryUnits("003_seconds", seconds)


def test_get_num_unit_categories_zero() -> None:
    # Setup
    # Construct an instance of the API adaptor.
    sut: mcapi.Engine = mcapi.Engine()

    # Execute
    result: int = sut.get_num_unit_categories()

    # Verify
    assert result == 0


def test_get_num_unit_categories() -> None:
    # Setup
    # Construct a mock MC.
    # Construct an instance of the API adaptor.
    sut: mcapi.Engine = mcapi.Engine()
    __set_up_test_unit_categories(sut._instance)

    # Execute
    result: int = sut.get_num_unit_categories()

    # Verify
    assert result == 3


def test_get_num_unit_categories() -> None:
    # Setup
    # Construct an instance of the API adaptor.
    sut: mcapi.Engine = mcapi.Engine()
    __set_up_test_unit_categories(sut._instance)

    # Execute
    result: int = sut.get_num_unit_categories()

    # Verify
    assert result == 3


@pytest.mark.parametrize(
    'category,expected_result',
    [
        pytest.param('001_empty_category', 0, id="empty category"),
        pytest.param('002_length', 4, id="four units"),
        pytest.param('003_seconds', 1, id="one unit"),
    ]
)
def test_get_num_units(category: str, expected_result: int) -> None:
    # Setup
    # Construct an instance of the API adaptor.
    sut: mcapi.Engine = mcapi.Engine()
    __set_up_test_unit_categories(sut._instance)

    # Execute
    result: int = sut.get_num_units(category)

    # Verify
    assert result == expected_result


@pytest.mark.parametrize(
    'category_index,expected_result',
    [
        pytest.param(0, '001_empty_category'),
        pytest.param(1, '002_length'),
        pytest.param(2, "003_seconds")
    ]
)
def test_get_unit_category_name(category_index: int, expected_result: str) -> None:
    # Setup
    # Construct an instance of the API adaptor.
    sut: mcapi.Engine = mcapi.Engine()
    __set_up_test_unit_categories(sut._instance)

    # Execute
    result: str = sut.get_unit_category_name(category_index)

    # Verify
    assert result == expected_result


@pytest.mark.parametrize(
    'category,unit_index,expected_result',
    [
        pytest.param('002_length', 0, 'inches', id="inches"),
        pytest.param('002_length', 1, 'feet', id="feet"),
        pytest.param('002_length', 2, 'mm', id="cm"),
        pytest.param('002_length', 3, 'cm', id="mm"),
    ]
)
def test_get_unit_name(category: str, unit_index: int, expected_result: str) -> None:
    # Setup
    # Construct an instance of the API adaptor.
    sut: mcapi.Engine = mcapi.Engine()
    __set_up_test_unit_categories(sut._instance)

    # Execute
    result: str = sut.get_unit_name(category, unit_index)

    # Verify
    assert result == expected_result


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
