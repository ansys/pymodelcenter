from typing import Optional, Sequence

import clr
import pytest

import ansys.modelcenter.workflow.api as mcapi

clr.AddReference("phoenix-mocks/Phoenix.Mock.v45")
from Phoenix.Mock import (  # type: ignore
    MockAssemblies,
    MockAssembly,
    MockBooleanVariable,
    MockComponent,
    MockComponents,
    MockDoubleVariable,
    MockGroup,
    MockGroups,
    MockIntegerVariable,
)

wrapped_mock_comp: MockAssembly = None


sut_instance: mcapi.Assembly = None


def setup_function(test_func):
    """
    Called before each test in the module.
    """
    global wrapped_mock_comp, sut_instance
    wrapped_mock_comp = MockAssembly("mock_comp_name")
    sut_instance = mcapi.Assembly(wrapped_mock_comp)


def test_variables() -> None:
    """Testing of variables property."""
    """Testing of the variables property."""
    mock_vars = [
        MockDoubleVariable("mockvar", 0),
        MockIntegerVariable("mockVar2", 0),
        MockBooleanVariable("mockVar3", 0),
    ]
    for mock_var in mock_vars:
        wrapped_mock_comp.Variables.addItem(mock_var)

    result: Sequence[mcapi.IVariable] = sut_instance.get_variables()

    assert isinstance(result[0], mcapi.IDoubleVariable)
    assert isinstance(result[1], mcapi.IIntegerVariable)
    assert isinstance(result[2], mcapi.IBooleanVariable)
    assert [each_result_item._wrapped for each_result_item in result] == mock_vars


def test_groups() -> None:
    """Testing of groups property."""
    mock_groups = MockGroups()
    mock_groups.addItem(MockGroup())
    mock_groups.addItem(MockGroup())
    mock_groups.addItem(MockGroup())
    mock_groups.Item(0).setName("mock group 1")
    mock_groups.Item(1).setName("mock group 2")
    mock_groups.Item(2).setName("mock group 3")

    wrapped_mock_comp.Groups = mock_groups

    result = sut_instance.groups

    assert all([isinstance(each_group, mcapi.IGroup) for each_group in result])
    assert [each_group.get_name() for each_group in result] == [
        "mock group 1",
        "mock group 2",
        "mock group 3",
    ]


def test_assemblies() -> None:
    mock_assemblies = MockAssemblies()
    mock_assemblies.AddAssembly(MockAssembly("mock assembly 1"))
    mock_assemblies.AddAssembly(MockAssembly("mock assembly 2"))
    mock_assemblies.AddAssembly(MockAssembly("mock assembly 3"))

    wrapped_mock_comp.Assemblies = mock_assemblies

    result = sut_instance.assemblies

    assert all([isinstance(each_assembly, mcapi.Assembly) for each_assembly in result])
    assert [assembly.name for assembly in result] == [
        "mock assembly 1",
        "mock assembly 2",
        "mock assembly 3",
    ]


def test_components() -> None:
    """Testing of the `get_components` method."""

    # Setup
    mock_components = MockComponents()
    mock_components.AddComponent(MockComponent("mock component 1"))
    mock_components.AddComponent(MockComponent("mock component 2"))
    mock_components.AddComponent(MockComponent("mock component 3"))

    wrapped_mock_comp.Components = mock_components

    # Execute
    result = sut_instance.get_components()

    # Verify
    assert all([isinstance(each_component, mcapi.IComponent) for each_component in result])
    assert [component.name for component in result] == [
        "mock component 1",
        "mock component 2",
        "mock component 3",
    ]


def test_icon_id() -> None:
    # Setup
    wrapped_mock_comp.iconID = 8675309

    # Execute
    result = sut_instance.icon_id

    # Verify
    assert result == 8675309


def test_set_icon_id() -> None:
    # Setup
    wrapped_mock_comp.iconId = 0

    # Execute
    sut_instance.icon_id = 8675309

    # Verify
    assert wrapped_mock_comp.iconID == 8675309


def test_index_in_parent() -> None:
    """Testing of the index_in_parent property."""
    # Setup
    wrapped_mock_comp.IndexInParent = 9001

    # Execute
    result: int = sut_instance.index_in_parent

    # Verify
    assert result == 9001


def test_index_in_parent_readonly() -> None:
    """Testing of the index_in_parent property."""
    with pytest.raises(AttributeError, match="can't set"):
        sut_instance.index_in_parent = 9001


def test_parent_assembly() -> None:
    wrapped_mock_comp.ParentAssembly = MockAssembly("a parent")

    result: Optional[mcapi.Assembly] = sut_instance.parent_assembly

    assert isinstance(result, mcapi.Assembly)
    assert result.name == "a parent"


def test_parent_assembly_none() -> None:
    wrapped_mock_comp.ParentAssembly = None

    result: Optional[mcapi.Assembly] = sut_instance.parent_assembly

    assert result is None


def test_parent_assembly_readonly() -> None:
    with pytest.raises(AttributeError, match="can't set"):
        sut_instance.parent_assembly = mcapi.Assembly(MockAssembly("trying to set parent"))


def test_assembly_type() -> None:
    """Testing of the assembly_type property."""
    wrapped_mock_comp.AssemblyType = "Sequence"

    result: str = sut_instance.control_type

    assert result == "Sequence"


def test_assembly_type_readonly() -> None:
    """Testing of the assembly_type property."""
    with pytest.raises(AttributeError, match="can't set"):
        sut_instance.control_type = "Sequence"


def test_user_data() -> None:
    """Testing of the user_data method."""
    wrapped_mock_comp.userData = "some user data"

    result = sut_instance.user_data

    assert result == "some user data"


def test_user_data_set() -> None:
    """Testing of the user_data setter method."""
    wrapped_mock_comp.userData = "unchanged"

    sut_instance.user_data = "pass test"

    assert wrapped_mock_comp.userData == "pass test"


def test_get_name() -> None:
    assert sut_instance.name == "mock_comp_name"


def test_get_full_name() -> None:
    """Testing of the get_full_name method."""
    assert sut_instance.get_full_name() == "mock_comp_name"


def test_add_assembly() -> None:
    """Testing of the add_assembly method when position info is specified."""
    subassembly_name = "subassembly"
    x_pos = 47
    y_pos = 9001
    sub_assembly_type = "Sequence"
    assert wrapped_mock_comp.getCallCount("addAssembly2") == 0
    assert wrapped_mock_comp.getCallCount("addAssembly") == 0

    result: mcapi.Assembly = sut_instance.add_assembly(
        subassembly_name, x_pos, y_pos, sub_assembly_type
    )

    assert wrapped_mock_comp.getCallCount("addAssembly2") == 1
    assert wrapped_mock_comp.getCallCount("addAssembly") == 0
    assert wrapped_mock_comp.getArgumentRecord("addAssembly2", 0) == [
        subassembly_name,
        x_pos,
        y_pos,
        sub_assembly_type,
    ]
    assert isinstance(result, mcapi.Assembly)
    assert result.name == subassembly_name


@pytest.mark.parametrize(
    "x_pos,y_pos",
    [
        pytest.param(47, None, id="no y"),
        pytest.param(None, 47, id="no x"),
        pytest.param(None, None, id="no position"),
    ],
)
def test_add_assembly_no_position(x_pos: Optional[int], y_pos: Optional[int]) -> None:
    """Testing of the add_assembly method when some position info is missing"""
    subassembly_name = "subassembly"
    sub_assembly_type = "Sequence"
    assert wrapped_mock_comp.getCallCount("addAssembly2") == 0
    assert wrapped_mock_comp.getCallCount("addAssembly") == 0

    result: mcapi.Assembly = sut_instance.add_assembly(
        subassembly_name, x_pos, y_pos, sub_assembly_type
    )

    assert wrapped_mock_comp.getCallCount("addAssembly2") == 0
    assert wrapped_mock_comp.getCallCount("addAssembly") == 1
    assert wrapped_mock_comp.getArgumentRecord("addAssembly", 0) == [
        subassembly_name,
        sub_assembly_type,
    ]
    assert isinstance(result, mcapi.Assembly)
    assert result.name == subassembly_name


def test_add_variable() -> None:
    var_name = "variable_name"
    var_type = "real"
    assert wrapped_mock_comp.getCallCount("addVariable") == 0

    sut_instance.add_variable(var_name, var_type)

    assert wrapped_mock_comp.getCallCount("addVariable") == 1
    assert wrapped_mock_comp.getArgumentRecord("addVariable", 0) == [var_name, var_type]


def test_rename() -> None:
    """Testing of the rename method."""
    new_name = "test_assembly_renamed"

    sut_instance.rename(new_name)

    assert sut_instance.name == new_name


def test_delete_variable() -> None:
    """Testing of the delete_variable method."""
    delete_var_name = "variable_name"
    var_type = "real"
    assert wrapped_mock_comp.getCallCount("deleteVariable") == 0

    sut_instance.delete_variable(delete_var_name)

    assert wrapped_mock_comp.getCallCount("deleteVariable") == 1
    assert wrapped_mock_comp.getArgumentRecord("deleteVariable", 0) == [delete_var_name]
