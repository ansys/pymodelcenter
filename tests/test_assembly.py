from typing import Optional

import clr
import pytest

import ansys.modelcenter.workflow.api as mcapi

clr.AddReference('phoenix-mocks/Phoenix.Mock.v45')
from Phoenix.Mock import MockAssembly

wrapped_mock_comp: MockAssembly = None


sut_instance: mcapi.Assembly(wrapped_mock_comp) = None


def setup_function(test_func):
    """
    Called before each test in the module.
    """
    global wrapped_mock_comp, sut_instance
    wrapped_mock_comp = MockAssembly("mock_comp_name")
    sut_instance = mcapi.Assembly(wrapped_mock_comp)


@pytest.mark.skip(reason="Not implemented.")
def test_variables() -> None:
    """Testing of variables property."""
    raise NotImplementedError


@pytest.mark.skip(reason="Not implemented.")
def test_groups() -> None:
    """Testing of groups property."""
    raise NotImplementedError


@pytest.mark.skip(reason="Not implemented.")
def test_assemblies() -> None:
    """Testing of assemblies property"""
    raise NotImplementedError


@pytest.mark.skip(reason="Not implemented.")
def test_components() -> None:
    """Testing of the components property."""
    raise NotImplementedError


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
    assert result.get_name() == "a parent"


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

    result: str = sut_instance.assembly_type

    assert result == "Sequence"


def test_assembly_type_readonly() -> None:
    """Testing of the assembly_type property."""
    with pytest.raises(AttributeError, match="can't set"):
        sut_instance.assembly_type = "Sequence"


@pytest.mark.skip(reason="Not implemented.")
def test_user_data() -> None:
    """Testing of the user_data method."""
    raise NotImplementedError


def test_get_name() -> None:
    assert sut_instance.get_name() == "mock_comp_name"


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
        subassembly_name, x_pos, y_pos, sub_assembly_type)

    assert wrapped_mock_comp.getCallCount("addAssembly2") == 1
    assert wrapped_mock_comp.getCallCount("addAssembly") == 0
    assert wrapped_mock_comp.getArgumentRecord("addAssembly2", 0) == [
        subassembly_name, x_pos, y_pos, sub_assembly_type]
    assert isinstance(result, mcapi.Assembly)
    assert result.get_name() == subassembly_name


@pytest.mark.parametrize(
    'x_pos,y_pos',
    [
        pytest.param(47, None, id="no y"),
        pytest.param(None, 47, id="no x"),
        pytest.param(None, None, id="no position"),
    ]
)
def test_add_assembly_no_position(x_pos: Optional[int], y_pos: Optional[int]) -> None:
    """Testing of the add_assembly method when some position info is missing"""
    subassembly_name = "subassembly"
    sub_assembly_type = "Sequence"
    assert wrapped_mock_comp.getCallCount("addAssembly2") == 0
    assert wrapped_mock_comp.getCallCount("addAssembly") == 0

    result: mcapi.Assembly = sut_instance.add_assembly(
        subassembly_name, x_pos, y_pos, sub_assembly_type)

    assert wrapped_mock_comp.getCallCount("addAssembly2") == 0
    assert wrapped_mock_comp.getCallCount("addAssembly") == 1
    assert wrapped_mock_comp.getArgumentRecord("addAssembly", 0) == [
        subassembly_name, sub_assembly_type]
    assert isinstance(result, mcapi.Assembly)
    assert result.get_name() == subassembly_name


def test_add_variable() -> None:
    var_name = "variable_name"
    var_type = "real"
    assert wrapped_mock_comp.getCallCount("addVariable") == 0

    sut_instance.add_variable(var_name, var_type)

    assert wrapped_mock_comp.getCallCount("addVariable") == 1
    assert wrapped_mock_comp.getArgumentRecord("addVariable", 0) == [
        var_name, var_type]


@pytest.mark.skip(reason="Not implemented.")
def test_rename() -> None:
    """Testing of the rename method."""
    raise NotImplementedError


@pytest.mark.skip(reason="Not implemented.")
def test_delete_variable() -> None:
    """Testing of the delete_variable method."""
    raise NotImplementedError


@pytest.mark.skip(reason="Not implemented.")
def test_set_metadata() -> None:
    """Testing of the set_metadata method."""
    raise NotImplementedError


@pytest.mark.skip(reason="Not implemented.")
def test_get_metadata() -> None:
    """Testing of the get_metadata method."""
    raise NotImplementedError
