import clr
clr.AddReference('phoenix-mocks/Phoenix.Mock.v45')

from Phoenix.Mock import MockModelCenter
from System.Collections.Generic import List
from System import String

from ansys.modelcenter.workflow.api import Engine
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
    # Setup
    # Construct a mock MC.
    mock_mc: Any = MockModelCenter()
    # Construct an instance of the API adaptor.
    sut: Engine = Engine(mock_mc)
    # Configure the mock to report a particular result when asked if it is interactive.
    mock_mc.IsInteractive = actual_value

    # Execute
    result: bool = sut.is_interactive

    # Verify
    assert result == expected_result


def test_process_id() -> None:
    # Setup
    # Construct a mock MC.
    mock_mc: Any = MockModelCenter()
    # Construct an instance of the API adaptor.
    sut: Engine = Engine(mock_mc)
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
    # Construct a mock MC.
    mock_mc: Any = MockModelCenter()
    # Construct an instance of the API adaptor.
    sut: Engine = Engine(mock_mc)

    # Execute
    result: int = sut.get_num_unit_categories()

    # Verify
    assert result == 0


def test_get_num_unit_categories() -> None:
    # Setup
    # Construct a mock MC.
    mock_mc: Any = MockModelCenter()
    __set_up_test_unit_categories(mock_mc)
    # Construct an instance of the API adaptor.
    sut: Engine = Engine(mock_mc)

    # Execute
    result: int = sut.get_num_unit_categories()

    # Verify
    assert result == 3


def test_get_num_unit_categories() -> None:
    # Setup
    # Construct a mock MC.
    mock_mc: Any = MockModelCenter()
    __set_up_test_unit_categories(mock_mc)
    # Construct an instance of the API adaptor.
    sut: Engine = Engine(mock_mc)

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
    # Construct a mock MC.
    mock_mc: Any = MockModelCenter()
    __set_up_test_unit_categories(mock_mc)
    # Construct an instance of the API adaptor.
    sut: Engine = Engine(mock_mc)

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
    # Construct a mock MC.
    mock_mc: Any = MockModelCenter()
    __set_up_test_unit_categories(mock_mc)
    # Construct an instance of the API adaptor.
    sut: Engine = Engine(mock_mc)

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
    # Construct a mock MC.
    mock_mc: Any = MockModelCenter()
    __set_up_test_unit_categories(mock_mc)
    # Construct an instance of the API adaptor.
    sut: Engine = Engine(mock_mc)

    # Execute
    result: str = sut.get_unit_name(category, unit_index)

    # Verify
    assert result == expected_result
