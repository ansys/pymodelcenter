"""Testing of IComponent."""
from typing import Optional

import clr
import pytest

import ansys.modelcenter.workflow.api as mcapi
from ansys.modelcenter.workflow.api import IAssembly

clr.AddReference("phoenix-mocks/Phoenix.Mock.v45")
from Phoenix.Mock import (
    MockAssembly,
    MockComponent,
    MockGroup,
    MockGroups,
    MockVariable,
    MockVariables,
)

mock_component: Optional[MockComponent] = None
"""
Mock ModelCenter object.

Used to simulate ModelCenter's response to different API calls."""

component: Optional[mcapi.IComponent] = None
"""
Component object under test.
"""


def setup_function(_):
    """
    Setup called befor each test funciton in this module.

    Parameters
    ----------
    _ :
        The function about to test.
    """
    global mock_component, component
    mock_component = MockComponent("ComponentName")
    component = mcapi.IComponent(mock_component)


def test_variables() -> None:
    """Testing of the variables-property."""
    global mock_component, component
    mock_variables = MockVariables()
    mock_variable = MockVariable("One", 0, 1)
    mock_variables.addItem(mock_variable)
    mock_variable = MockVariable("Two", 0, 1)
    mock_variables.addItem(mock_variable)
    mock_component.Variables = mock_variables

    # SUT
    result = component.variables

    # Verify
    assert isinstance(result, mcapi.IVariables)
    assert len(result) == 2
    assert result[0].get_name() == "One"
    assert result[1].get_name() == "Two"


def test_groups() -> None:
    """Testing of the groups-property."""
    global mock_component, component
    mock_groups = MockGroups()
    mock_group = MockGroup()
    mock_group.setName("One")
    mock_groups.addItem(mock_group)
    mock_group = MockGroup()
    mock_group.setName("Two")
    mock_groups.addItem(mock_group)
    mock_component.Groups = mock_groups

    # SUT
    result = component.groups

    # Verify
    assert isinstance(result, mcapi.IGroups)
    assert len(result) == 2
    assert result[0].get_name() == "One"
    assert result[1].get_name() == "Two"


user_data_tests = [
    pytest.param("user data", id="str"),
    pytest.param(42, id="int"),
    pytest.param(3.14, id="float"),
    pytest.param(True, id="bool"),
    pytest.param(None, id="None"),
    pytest.param(2 + 1j, id="complex"),

    # Expected these to work
    pytest.param(["one", "two"], id="[str]", marks=pytest.mark.xfail),
    pytest.param([42, 86], id="[int]", marks=pytest.mark.xfail),
    pytest.param([1.414, 0.717], id="[float]", marks=pytest.mark.xfail),
    pytest.param([True, False], id="[bool]", marks=pytest.mark.xfail),

    # Did not expect these to work
    pytest.param({"one", "two"}, id="{str}"),
    pytest.param({42, 86}, id="{int}"),
    pytest.param({1.414, 0.717}, id="{float}"),
    pytest.param({True, False}, id="{bool}"),
    pytest.param({"one", 2, 3.14, True}, id="{mixed}"),
    pytest.param({"one": 1, "two": 2}, id="dict"),
    pytest.param({"one": "un", "two": 2, "three": 3.14, "four": False}, id="dict-mixed"),
    pytest.param({2: "two", 3.14: "pi", False: "nine"}, id="dict-key-mixed"),

    # Other types to be complete
    pytest.param(("one", "two"), id="(str)", marks=pytest.mark.xfail),
    pytest.param((42, 86), id="(int)", marks=pytest.mark.xfail),
    pytest.param((1.414, 0.717), id="(float)", marks=pytest.mark.xfail),
    pytest.param((True, False), id="(bool)", marks=pytest.mark.xfail),
]


@pytest.mark.parametrize(
    "value", user_data_tests
)
def test_user_data(value: any) -> None:
    """Testing of the user_data property."""
    global component

    component.user_data = value
    result = component.user_data

    # Verify
    assert result == value
    assert type(result) == type(value)


@pytest.mark.parametrize(
    "value",
    [
        pytest.param("a string", id="str"),
        pytest.param(["one string", "two string"], id="[str]"),
    ]
)
def test_associated_files(value: any) -> None:
    """Testing of the associated_files property."""
    global component

    component.associated_files = value
    result = component.associated_files

    # Verify
    assert result == value
    assert type(result) == type(value)


def test_index_in_parent() -> None:
    """Testing of the index_in_parent property."""
    mock_component.IndexInParent = 42

    # SUT
    result = component.index_in_parent

    # Verify
    assert result == 42
    assert type(result) == int


def test_parent_assembly() -> None:
    """Testing of the parent_assembly property."""
    mock_parent = MockAssembly("Assembly Name")
    mock_component.ParentAssembly = mock_parent

    # SUT
    result = component.parent_assembly

    # Verify
    assert type(result) == IAssembly
    assert result.get_name() == "Assembly Name"


@pytest.mark.skip(reason="Not implemented.")
def test_get_name() -> None:
    """Testing of the get_name method."""
    raise NotImplementedError


@pytest.mark.skip(reason="Not implemented.")
def test_get_full_name() -> None:
    """Testing of the get_full_name method."""
    raise NotImplementedError


@pytest.mark.skip(reason="Not implemented.")
def test_get_source() -> None:
    """Testing of the get_source method."""
    raise NotImplementedError


@pytest.mark.skip(reason="Not implemented.")
def test_get_variable() -> None:
    """Testing of the get_variable method."""
    raise NotImplementedError


@pytest.mark.skip(reason="Not implemented.")
def test_get_type() -> None:
    """Testing of the get_type method."""
    raise NotImplementedError


@pytest.mark.skip(reason="Not implemented.")
def test_get_metadata() -> None:
    """Testing of the get_metadata method."""
    raise NotImplementedError


@pytest.mark.skip(reason="Not implemented.")
def test_set_metadata() -> None:
    """Testing of the set_metadata method."""
    raise NotImplementedError


@pytest.mark.skip(reason="Not implemented.")
def test_run() -> None:
    """Testing of the run method."""
    raise NotImplementedError


@pytest.mark.skip(reason="Not implemented.")
def test_invoke_method() -> None:
    """Testing of the invoke_method method."""
    raise NotImplementedError


@pytest.mark.skip(reason="Not implemented.")
def test_invalidate() -> None:
    """Testing of the invalidate method."""
    raise NotImplementedError


@pytest.mark.skip(reason="Not implemented.")
def test_reconnect() -> None:
    """Testing of the reconnect method."""
    raise NotImplementedError


@pytest.mark.skip(reason="Not implemented.")
def test_download_values() -> None:
    """Testing of the download_values method."""
    raise NotImplementedError


@pytest.mark.skip(reason="Not implemented.")
def test_rename() -> None:
    """Testing of the rename method."""
    raise NotImplementedError


@pytest.mark.skip(reason="Not implemented.")
def test_get_position_x() -> None:
    """Testing of the get_position_x method."""
    raise NotImplementedError


@pytest.mark.skip(reason="Not implemented.")
def test_get_position_y() -> None:
    """Testing of the get_position_y method."""
    raise NotImplementedError


@pytest.mark.skip(reason="Not implemented.")
def test_show() -> None:
    """Testing of the show method."""
    raise NotImplementedError
