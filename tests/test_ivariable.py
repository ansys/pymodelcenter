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


__is_input_tests = [
    pytest.param(mcapi.IDoubleVariable(MockDoubleVariable('Workflow.Assembly.doubleVar', 0)),
                 True, id="double input"),
    pytest.param(mcapi.IDoubleVariable(MockDoubleVariable('Workflow.Assembly.doubleVar', 0)),
                 True, id="double output")
]


@pytest.mark.parametrize('sut,expected_value', __is_input_tests)
def test_is_input_to_model(sut: mcapi.IVariable, expected_value: bool) -> None:
    """
    Verify that is_input_to_model works for different IVariable implementations.
    """
    # Setup
    sut._wrapped.InputToModel = expected_value

    # Execute
    result = sut.is_input_to_model()

    # Verify
    assert result == expected_value


@pytest.mark.parametrize('sut,expected_value', __is_input_tests)
def test_is_input_to_component(sut: mcapi.IVariable, expected_value: bool) -> None:
    """
    Verify that is_input_to_component works for different IVariable implementations.
    """
    # Setup
    sut._wrapped.InputToComponent = expected_value

    # Execute
    result = sut.is_input_to_component()

    # Verify
    assert result == expected_value
