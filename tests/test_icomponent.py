"""Testing of IComponent."""
from typing import Any, Type

import clr
import pytest

import ansys.modelcenter.workflow.api as mcapi
from ansys.modelcenter.workflow.api import Assembly

clr.AddReference("phoenix-mocks/Phoenix.Mock.v45")
from Phoenix.Mock import (
    MockAssembly,
    MockComponent,
    MockDoubleVariable,
    MockGroup,
    MockGroups,
    MockIntegerVariable,
    MockVariables,
)

mock_component: MockComponent
"""
Mock ModelCenter object.

Used to simulate ModelCenter's response to different API calls."""

component: mcapi.IComponent
"""
Component object under test.
"""


def setup_function(_):
    """
    Setup called before each test function in this module.

    Parameters
    ----------
    _ :
        The function about to test.
    """
    global mock_component, component
    mock_component = MockComponent("some.path.ComponentName")
    component = mcapi.IComponent(mock_component)


def test_variables() -> None:
    """Testing of the variables-property."""
    global mock_component, component
    mock_variables = MockVariables()
    mock_variable = MockIntegerVariable("One", 0)
    mock_variables.addItem(mock_variable)
    mock_variable = MockDoubleVariable("Two", 0)
    mock_variables.addItem(mock_variable)
    mock_component.Variables = mock_variables

    # SUT
    result = component.get_variables()

    # Verify
    assert isinstance(result, mcapi.Arrayish)
    assert len(result) == 2
    assert result[0].name == "One"
    assert isinstance(result[0], mcapi.IIntegerVariable)
    assert result[1].name == "Two"
    assert isinstance(result[1], mcapi.IDoubleVariable)


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
    assert isinstance(result, mcapi.Arrayish)
    assert result._converter is mcapi.IGroup
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
    pytest.param(["one", "two"], id="[str]"),
    pytest.param([42, 86], id="[int]"),
    pytest.param([1.414, 0.717], id="[float]"),
    pytest.param([True, False], id="[bool]"),

    # Did not expect these to work
    pytest.param(["str", 42, 1.414, True], id="[mixed]"),
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
def test_user_data(value: Any) -> None:
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
def test_associated_files(value: Any) -> None:
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
    assert type(result) == Assembly
    assert result.name == "Assembly Name"


def test_get_name() -> None:
    """Testing of the get_name method."""
    # SUT
    result = component.name

    # Verify
    assert result == "ComponentName"
    assert isinstance(result, str)


def test_get_full_name() -> None:
    """Testing of the get_full_name method."""
    # SUT
    result = component.get_full_name()

    # Verify
    assert result == "some.path.ComponentName"
    assert isinstance(result, str)


def test_get_source() -> None:
    """Testing of the get_source method."""
    # SUT
    result = component.get_source()

    # Verify
    assert result == "有りのままの姿見せるのよ"     # Value comes from MockComponent.getSource()
    assert isinstance(result, str)


@pytest.mark.parametrize(
    "name,type_,value",
    [
        pytest.param("i", mcapi.IIntegerVariable, 42, id="int"),
        pytest.param("d", mcapi.IDoubleVariable, 1.414, id="double"),
    ]
)
def test_get_variable(name: str, type_: Type, value) -> None:
    """Testing of the get_variable method."""
    mock_variables = MockVariables()
    mock_variable = MockIntegerVariable("a.i", 0)
    mock_variable.value = 42
    mock_variables.addItem(mock_variable)
    mock_variable = MockDoubleVariable("a.d", 0)
    mock_variable.value = 1.414
    mock_variables.addItem(mock_variable)
    mock_component.Variables = mock_variables

    # SUT
    result = component.get_variable(name)

    # Verify
    assert isinstance(result, mcapi.IVariable)
    assert isinstance(result, type_)
    if isinstance(result, mcapi.IIntegerVariable) or isinstance(result, mcapi.IDoubleVariable):
        assert result.get_value(None).value == value
    else:
        TypeError("Unsupported type in test")


def test_get_type() -> None:
    # SUT
    result = component.get_type()

    # Verify
    assert result == "それは早いぞ"       # Value came from MockComponents.MockComponent(string)


def test_run() -> None:
    """Testing of the run method."""
    # SUT
    component.run()

    # Verify
    assert mock_component.getCallCount("run") == 1


def test_invoke_method() -> None:
    """Testing of the invoke_method method."""
    # SUT
    component.invoke_method("method_name")

    # Verify
    assert mock_component.getCallCount("invokeMethod") == 1
    args = mock_component.getArgumentRecord("invokeMethod", 0)
    assert args[0] == "method_name"


def test_invalidate() -> None:
    """Testing of the invalidate method."""
    # SUT
    component.invalidate()

    # Verify
    assert mock_component.getCallCount("invalidate")


def test_reconnect() -> None:
    """Testing of the reconnect method."""
    # SUT
    component.reconnect()

    # Verify
    assert mock_component.getCallCount("reconnect")


def test_download_values() -> None:
    """Testing of the download_values method."""
    # SUT
    component.download_values()

    # Verify
    assert mock_component.getCallCount("downloadValues")


def test_rename() -> None:
    """Testing of the rename method."""
    # SUT
    component.rename("the.new.name")

    # Verify
    assert mock_component.getCallCount("rename")
    assert component.get_full_name() == "the.new.name"
    assert component.name == "name"


def test_get_position_x() -> None:
    """Testing of the get_position_x method."""
    # SUT
    result = component.get_position_x()

    # Verify
    assert result == 24     # value from MockComponent(string name)


def test_get_position_y() -> None:
    """Testing of the get_position_y method."""
    # SUT
    result = component.get_position_y()

    # Verify
    assert result == 31     # value from MockComponent(string name)


def test_show() -> None:
    """Testing of the show method."""
    # SUT
    component.show()

    # Verify
    assert mock_component.getCallCount("show") == 1
