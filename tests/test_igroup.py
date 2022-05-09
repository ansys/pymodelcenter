from typing import Sequence

import clr

import ansys.modelcenter.workflow.api as mcapi

clr.AddReference(r"phoenix-mocks\Phoenix.Mock.v45")
from Phoenix.Mock import MockBooleanVariable, MockDoubleVariable, MockGroup, MockIntegerVariable

mock: MockGroup
sut: mcapi.IGroup


def setup_function(_):
    """
    Setup called before each test function in this module.

    Parameters
    ----------
    _ :
        The function about to test.
    """
    global mock, sut
    mock = MockGroup()

    # TODO: Setup variables

    subgroup1 = MockGroup()
    subgroup1.setName("Model.MockGroup.Subgroup1")
    mock.Groups.addItem(subgroup1)

    subgroup2 = MockGroup()
    subgroup2.setName("Model.MockGroup.Subgroup2")
    mock.Groups.addItem(subgroup2)

    sut = mcapi.IGroup(mock)


def test_variables() -> None:
    """Testing of the variables property."""
    mock_vars = [MockDoubleVariable("mockvar", 0),
                 MockIntegerVariable("mockVar2", 0),
                 MockBooleanVariable("mockVar3", 0)]
    for mock_var in mock_vars:
        mock.Variables.addItem(mock_var)

    result: Sequence[mcapi.IVariable] = sut.variables

    assert isinstance(result[0], mcapi.IDoubleVariable)
    assert isinstance(result[1], mcapi.IIntegerVariable)
    assert isinstance(result[2], mcapi.IBooleanVariable)
    assert [each_result_item._wrapped for each_result_item in result] == mock_vars


def test_groups() -> None:
    """Testing of the groups property."""
    # SUT
    result: Sequence[mcapi.IGroup] = sut.groups

    # Verification
    assert result[0].get_name() == "Subgroup1"
    assert result[1].get_name() == "Subgroup2"


def test_icon_id() -> None:
    """Testing of the icon_id property."""
    # SUT
    sut.icon_id = 12
    result: int = sut.icon_id

    # Verification
    assert result == 12


def test_get_name() -> None:
    """Testing of the get_name method."""
    # SUT
    result: str = sut.get_name()

    # Verification
    assert result == "MockGroup"


def test_get_full_name() -> None:
    """Testing of the get_full_name method."""

    # SUT
    result: str = sut.get_full_name()

    # Verification
    assert result == "Model.MockGroup"
