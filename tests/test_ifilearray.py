import clr
import pytest

import ansys.modelcenter.workflow.api as mcapi

clr.AddReference('phoenix-mocks/Phoenix.Mock.v45')
from Phoenix.Mock import MockFileArray  # type: ignore


def test_value_setter():
    """
    Verify setting `value` property works for IFileArray implementation.
    """
    mock = MockFileArray('Workflow.Assembly.fileArray', 0)
    sut = mcapi.IFileArray(mock)

    dummy_file = None

    # Execute
    sut.set_value(dummy_file)

    assert sut._wrapped.getCallCount('fromString') == 1


def test_value_getter():
    """
    Verify getting `value` property works for IFileArray implementation.
    """
    mock = MockFileArray('Workflow.Assembly.fileArray', 0)
    sut = mcapi.IFileArray(mock)

    # Execute
    value = sut.get_value(None)

    assert value is None
    assert sut._wrapped.getCallCount('toString') == 1


@pytest.mark.parametrize('value', [
    pytest.param(True),
    pytest.param(False)
])
def test_save_with_model(value: bool) -> None:
    """
    Verify that `save_with_model` property works for IFileArray implementation.
    """
    mock = MockFileArray('Workflow.Assembly.fileArray', 0)
    sut = mcapi.IFileArray(mock)

    # Execute
    sut.save_with_model = value
    result = sut.save_with_model

    assert result is value
    assert sut._wrapped.getCallCount('set_saveWithModel') == 1
    assert sut._wrapped.getCallCount('get_saveWithModel') == 1
