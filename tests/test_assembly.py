from typing import Optional, Union

import clr
import pytest

import ansys.modelcenter.workflow.api as mcapi

clr.AddReference('phoenix-mocks/Phoenix.Mock.v45')
from Phoenix.Mock import MockAssemblies, MockAssembly

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


def test_assemblies() -> None:
    mock_assemblies = MockAssemblies()
    mock_assemblies.AddAssembly(MockAssembly("mock assembly 1"))
    mock_assemblies.AddAssembly(MockAssembly("mock assembly 2"))
    mock_assemblies.AddAssembly(MockAssembly("mock assembly 3"))

    wrapped_mock_comp.Assemblies = mock_assemblies

    result = sut_instance.assemblies

    assert all([isinstance(each_assembly, mcapi.Assembly) for each_assembly in result])
    assert [assembly.get_name() for assembly in result] == [
        "mock assembly 1", "mock assembly 2", "mock assembly 3"]


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


def test_rename() -> None:
    """Testing of the rename method."""
    new_name = "test_assembly_renamed"

    sut_instance.rename(new_name)

    assert sut_instance.get_name() == new_name


def test_delete_variable() -> None:
    """Testing of the delete_variable method."""
    delete_var_name = "variable_name"
    var_type = "real"
    assert wrapped_mock_comp.getCallCount("deleteVariable") == 0

    sut_instance.delete_variable(delete_var_name)

    assert wrapped_mock_comp.getCallCount("deleteVariable") == 1
    assert wrapped_mock_comp.getArgumentRecord("deleteVariable", 0) == [delete_var_name]


@pytest.mark.parametrize(
    'name,value,access,archive,value_is_xml,expected_type',
    [
        pytest.param("str_metadata", "some string data",
                     mcapi.ComponentMetadataAccess.PUBLIC,
                     True, False, mcapi.ComponentMetadataType.STRING),
        pytest.param("xml_metadata", "<metadata />",
                     mcapi.ComponentMetadataAccess.READONLY,
                     False, True, mcapi.ComponentMetadataType.XML),
        pytest.param("long_metadata", 47,
                     mcapi.ComponentMetadataAccess.READONLY,
                     False, False, mcapi.ComponentMetadataType.LONG),
        pytest.param("double_metadata", 9000.1,
                     mcapi.ComponentMetadataAccess.PRIVATE,
                     False, False, mcapi.ComponentMetadataType.DOUBLE),
        pytest.param("boolean_metadata", True,
                     mcapi.ComponentMetadataAccess.PRIVATE,
                     False, False, mcapi.ComponentMetadataType.BOOLEAN),
        pytest.param("boolean_metadata", False,
                     mcapi.ComponentMetadataAccess.PRIVATE,
                     False, False, mcapi.ComponentMetadataType.BOOLEAN),
    ]
)
def test_set_metadata(
        name: str, value: Union[str, int, float, bool],
        access: mcapi.ComponentMetadataAccess,
        archive: bool, value_is_xml: bool, expected_type: mcapi.ComponentMetadataType) -> None:
    """Testing of the set_metadata method."""
    assert wrapped_mock_comp.getCallCount("setMetadata") == 0

    sut_instance.set_metadata(name, value, access, archive, value_is_xml)

    assert wrapped_mock_comp.getCallCount("setMetadata") == 1
    assert wrapped_mock_comp.getArgumentRecord("setMetadata", 0) == [
        name, expected_type.value, value, access.value, archive]


@pytest.mark.parametrize(
    'name,value,access,archive,value_is_xml',
    [
        pytest.param("none_metadata", None,
                     mcapi.ComponentMetadataAccess.PUBLIC,
                     True, False),
        pytest.param("list_metadata", [0, 1, 2],
                     mcapi.ComponentMetadataAccess.PUBLIC,
                     True, False)
    ]
)
def test_set_metadata_invalid(
        name: str, value: Union[str, int, float, bool],
        access: mcapi.ComponentMetadataAccess,
        archive: bool, value_is_xml: bool) -> None:
    """Testing of the set_metadata method."""
    with pytest.raises(TypeError, match="Assembly or component metadata"):
        sut_instance.set_metadata(name, value, access, archive, value_is_xml)
    assert wrapped_mock_comp.getCallCount("setMetadata") == 0


def test_get_metadata() -> None:
    sut_instance.set_metadata("string_meta", "string metadata value",
                              mcapi.ComponentMetadataAccess.PUBLIC,
                              False, False)

    result = sut_instance.get_metadata("string_meta")

    assert result == "string metadata value"
