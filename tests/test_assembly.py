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


@pytest.mark.skip(reason="Not implemented.")
def test_icon_id() -> None:
    """Testing of the icon_id property"""
    raise NotImplementedError


@pytest.mark.skip(reason="Not implemented.")
def test_index_in_parent() -> None:
    """Testing of the index_in_parent property."""
    raise NotImplementedError


@pytest.mark.skip(reason="Not implemented.")
def test_parent_assembly() -> None:
    """Testing of the parent_assembly property."""
    raise NotImplementedError


@pytest.mark.skip(reason="Not implemented.")
def test_assembly_type() -> None:
    """Testing of the assembly_type property."""
    raise NotImplementedError


@pytest.mark.skip(reason="Not implemented.")
def test_user_data() -> None:
    """Testing of the user_data method."""
    raise NotImplementedError


def test_get_name() -> None:
    assert sut_instance.get_name() == "mock_comp_name"


def test_get_full_name() -> None:
    """Testing of the get_full_name method."""
    assert sut_instance.get_full_name() == "mock_comp_name"


@pytest.mark.skip(reason="Not implemented.")
def test_add_assembly() -> None:
    """Testing of the add_assembly method."""
    raise NotImplementedError


@pytest.mark.skip(reason="Not implemented.")
def test_add_variable() -> None:
    """Testing of the add_variable method."""
    raise NotImplementedError


@pytest.mark.skip(reason="Not implemented.")
def test_rename() -> None:
    """Testing of the rename method."""
    raise NotImplementedError


@pytest.mark.skip(reason="Not implemented.")
def test_delete_variable() -> None:
    """Testing of the delete_variable method."""
    raise NotImplementedError


@pytest.mark.skip(reason="Not implemented.")
def test_add_assembly2() -> None:
    """Testing of the add_assembly2 method."""
    raise NotImplementedError


@pytest.mark.skip(reason="Not implemented.")
def test_set_metadata() -> None:
    """Testing of the set_metadata method."""
    raise NotImplementedError


@pytest.mark.skip(reason="Not implemented.")
def test_get_metadata() -> None:
    """Testing of the get_metadata method."""
    raise NotImplementedError
