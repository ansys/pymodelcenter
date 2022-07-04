import clr
import pytest

import ansys.modelcenter.workflow.api as mcapi

clr.AddReference("phoenix-mocks/Phoenix.Mock.v45")
from Phoenix.Mock import MockFileVariable


def test_value_setter():
    """
    Verify setting `value` property works for IFileVariable implementation.
    """
    mock = MockFileVariable("Workflow.Assembly.fileVar", 0)
    sut = mcapi.IFileVariable(mock)

    dummy_file = None

    # Execute
    sut.set_value(dummy_file)

    assert sut._wrapped.getCallCount("set_value") == 1
    assert sut._wrapped.value is None


def test_value_getter():
    """
    Verify getting `value` property works for IFileVariable implementation.
    """
    mock = MockFileVariable("Workflow.Assembly.fileVar", 0)
    sut = mcapi.IFileVariable(mock)

    # Execute
    value = sut.value

    assert value is None
    assert sut._wrapped.getCallCount("get_value") == 1


@pytest.mark.parametrize("value", [pytest.param(True), pytest.param(False)])
def test_save_with_model(value: bool) -> None:
    """
    Verify that `save_with_model` property works for IFileVariable implementation.
    """
    mock = MockFileVariable("Workflow.Assembly.fileVar", 0)
    sut = mcapi.IFileVariable(mock)

    # Execute
    sut.save_with_model = value
    result = sut.save_with_model

    assert result is value
    assert sut._wrapped.getCallCount("set_saveWithModel") == 1
    assert sut._wrapped.getCallCount("get_saveWithModel") == 1


@pytest.mark.parametrize("value", [pytest.param(True), pytest.param(False)])
def test_direct_transfer(value: bool) -> None:
    """
    Verify that `direct_transfer` property works for IFileVariable implementation.
    """
    mock = MockFileVariable("Workflow.Assembly.fileVar", 0)
    sut = mcapi.IFileVariable(mock)

    # Execute
    sut.direct_transfer = value
    result = sut.direct_transfer

    assert result is value
    assert sut._wrapped.getCallCount("set_directTransfer") == 1
    assert sut._wrapped.getCallCount("get_directTransfer") == 1
