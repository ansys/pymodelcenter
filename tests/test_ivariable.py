import clr
import pytest

import ansys.modelcenter.workflow.api as mcapi

clr.AddReference('phoenix-mocks/Phoenix.Mock.v45')
from Phoenix.Mock import MockDoubleVariable


@pytest.mark.parametrize('sut,expected_result', [
    pytest.param(mcapi.IDoubleVariable(MockDoubleVariable('Workflow.Assembly.doubleVar', 0)),
                 'doubleVar', id="double")
])
def test_get_name(sut: mcapi.IVariable, expected_result: str) -> None:
    """
    Verify that get_name works for different IVariable implementations.
    """

    # Execute
    result = sut.get_name()

    assert result == expected_result


@pytest.mark.parametrize('sut,expected_result', [
    pytest.param(mcapi.IDoubleVariable(MockDoubleVariable('Workflow.Assembly.doubleVar', 0)),
                 'Workflow.Assembly.doubleVar', id="double")
])
def test_get_full_name(sut: mcapi.IVariable, expected_result: str) -> None:
    """
    Verify that get_full_name works for different IVariable implementations.
    """

    # Execute
    result = sut.get_full_name()

    assert result == expected_result
