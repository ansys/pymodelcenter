import pytest

import ansys.modelcenter.workflow.api as mcapi

sut: mcapi.IReferenceArray


def setup_function():
    """Setup called before each test in this module."""
    global sut
    sut = mcapi.IReferenceArray("test name", mcapi.VarType.INPUT)
    sut.auto_grow = True
    sut.set_value(1.1, 0)
    sut.set_value(2.2, 1)
    sut.set_value(3.3, 2)


@pytest.mark.skip(reason="Not implemented.")
def test_auto_grow() -> None:
    """Testing of the auto_grow property."""
    # SUT
    original_auto_grow = sut.auto_grow
    sut.auto_grow = False

    # Verify
    assert original_auto_grow
    assert not sut.auto_grow


@pytest.mark.skip(reason="Not implemented.")
def test_value() -> None:
    """Testing of the value property."""
    pass


@pytest.mark.skip(reason="Not implemented.")
def test_reference() -> None:
    """Testing of the reference property."""
    raise NotImplementedError


@pytest.mark.skip(reason="Not implemented.")
def test_get_value() -> None:
    """Testing of the get_value method."""
    raise NotImplementedError


@pytest.mark.skip(reason="Not implemented.")
def test_set_value() -> None:
    """Testing of the set_value method."""
    raise NotImplementedError


@pytest.mark.skip(reason="Not implemented.")
def test_create_ref_prop() -> None:
    """Testing of the create_ref_prop method."""
    raise NotImplementedError


@pytest.mark.skip(reason="Not implemented.")
def test_get_ref_prop_value() -> None:
    """Testing of the get_ref_prop_value method."""
    raise NotImplementedError


@pytest.mark.skip(reason="Not implemented.")
def test_set_ref_prop_value() -> None:
    """Testing of the set_ref_prop_value method."""
    raise NotImplementedError


@pytest.mark.skip(reason="Not implemented.")
def test_get_ref_prop_value_absolute() -> None:
    """Testing of the get_ref_prop_value_absolute method."""
    raise NotImplementedError


@pytest.mark.skip(reason="Not implemented.")
def test_referenced_variables() -> None:
    """Testing of the referenced_variables method."""
    raise NotImplementedError


@pytest.mark.skip(reason="Not implemented.")
def test_referenced_variable() -> None:
    """Testing of the referenced_variable method."""
    raise NotImplementedError


@pytest.mark.skip(reason="Not implemented.")
def test_get_value_absolute() -> None:
    """Testing of the get_value_absolute method."""
    raise NotImplementedError
