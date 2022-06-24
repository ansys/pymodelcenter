"""Tests for GlobalParameters."""
import clr
import pytest

import ansys.modelcenter.workflow.api as mcapi

clr.AddReference(r"phoenix-mocks\Phoenix.Mock.v45")
from Phoenix.Mock import MockGlobalParameters

mock: MockGlobalParameters
sut: mcapi.IGlobalParameters


def setup_function(_):
    """
    Setup called before each test function in this module.

    Parameters
    ----------
    _ :
        The function about to test.
    """
    global mock, sut

    mock = MockGlobalParameters()
    sut = mcapi.IGlobalParameters(mock)


def test_count() -> None:
    """Testing of the count property."""
    # SUT
    result: int = sut.count
    with pytest.raises(Exception) as except_info:
        sut.count = 1

    # Verification
    assert result == 0
    assert except_info.value.args[0] == "can't set attribute"


@pytest.mark.parametrize(
    "index, value",
    [
        pytest.param(1, 2),
        pytest.param(1, 2.2),
        pytest.param("a", True),
        pytest.param("a", "b"),
        # LTTODO: check all types that can be passed over GRPC
    ],
)
def test_get_item(index: object, value: object) -> None:
    """Testing of the get_item method."""
    # Setup
    mock[index] = value

    # SUT
    result: object = sut.get_item(index)

    # Verification
    assert result == value


@pytest.mark.parametrize(
    "index, value",
    [
        pytest.param(1, 2),
        pytest.param(1, 2.2),
        pytest.param("a", True),
        pytest.param("a", "b"),
        # LTTODO: check all types that can be passed over GRPC
    ],
)
def test_set_item(index: object, value: object) -> None:
    """Testing of the set_item method."""
    # SUT
    sut.set_item(index, value)
    result: object = sut.get_item(index)

    # Verification
    assert result == value


def test_set_export_to_remote_components() -> None:
    """Testing of the set_export_to_remote_components method."""
    # Setup
    sut.set_item(1, 2)

    # SUT
    sut.set_export_to_remote_components(1, True)

    # Verification
    mock.getCallCount("setExportToRemoteComponents") == 1
    assert mock.getArgumentRecord("setExportToRemoteComponents", 0) == [1, True]


def test_set_export_on_missing_item() -> None:
    """Testing of set_export_to_remote_components when the index does \
    not exist."""
    # SUT
    with pytest.raises(Exception) as except_info:
        sut.set_export_to_remote_components("1", True)

    # Verification
    assert except_info.value.args[0] == "The given key was not present in the dictionary."


def test_remove() -> None:
    """Testing of the remove method."""
    # Setup
    sut.set_item(1, 2)

    # SUT
    sut.remove(1)

    # Verification
    assert sut.count == 0


def test_remove_missing_item() -> None:
    """Testing of remove when the index does not exist."""
    # SUT
    sut.remove("1")

    # Verification
    mock.getCallCount("Remove") == 1
    assert mock.getArgumentRecord("Remove", 0) == ["1"]
