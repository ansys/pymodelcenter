from typing import Sequence

import clr
import pytest

import ansys.modelcenter.workflow.api as mcapi

clr.AddReference('phoenix-mocks/Phoenix.Mock.v45')
from Phoenix.Mock import MockDoubleVariable, MockVariableLink

__instance_only_tests = [
    pytest.param(mcapi.IDoubleVariable(MockDoubleVariable('Workflow.Assembly.doubleVar', 0)),
                 id = "double")
]


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


@pytest.mark.parametrize('sut', __instance_only_tests)
def test_validate(sut: mcapi.IVariable) -> None:
    """
    Verify that validate calls through to the mock.
    """
    # Setup / sanity check
    assert sut._wrapped.getCallCount('validate') == 0

    # Execute
    sut.validate()

    # Verify
    assert sut._wrapped.getCallCount('validate') == 1


@pytest.mark.parametrize('sut', __instance_only_tests)
def test_invalidate(sut: mcapi.IVariable) -> None:
    """
    Verify that invalidate calls through to the mock.
    """
    # Setup / sanity check
    assert sut._wrapped.getCallCount('invalidate') == 0

    # Execute
    sut.invalidate()

    # Verify
    assert sut._wrapped.getCallCount('invalidate') == 1


@pytest.mark.parametrize('sut', __instance_only_tests)
def test_dependent_links(sut: mcapi.IVariable) -> None:
    """
    Verify that dependent_links works correctly.
    """
    mock_links = [MockVariableLink(), MockVariableLink(), MockVariableLink()]
    mock_links[0].LHS = "link_lhs_0"
    mock_links[0].RHS = "link_rhs_0"
    mock_links[1].LHS = "link_lhs_1"
    mock_links[1].RHS = "link_rhs_1"
    mock_links[1].LHS = "link_lhs_2"
    mock_links[1].RHS = "link_rhs_2"
    for mock_link in mock_links:
        sut._wrapped.DependentLinksStorage.AddItem(mock_link)

    result: Sequence[mcapi.VariableLink] = sut.dependent_links()

    assert all([isinstance(each_result_item, mcapi.VariableLink) for each_result_item in result])
    assert [each_result_item._link for each_result_item in result] == mock_links


@pytest.mark.parametrize('sut', __instance_only_tests)
def test_precedent_links(sut: mcapi.IVariable) -> None:
    """
    Verify that precedent_links works correctly.
    """
    mock_links = [MockVariableLink(), MockVariableLink(), MockVariableLink()]
    mock_links[0].LHS = "link_lhs_0"
    mock_links[0].RHS = "link_rhs_0"
    mock_links[1].LHS = "link_lhs_1"
    mock_links[1].RHS = "link_rhs_1"
    mock_links[1].LHS = "link_lhs_2"
    mock_links[1].RHS = "link_rhs_2"
    for mock_link in mock_links:
        sut._wrapped.PrecedentLinksStorage.AddItem(mock_link)

    result: Sequence[mcapi.VariableLink] = sut.precedent_links()

    assert all([isinstance(each_result_item, mcapi.VariableLink) for each_result_item in result])
    assert [each_result_item._link for each_result_item in result] == mock_links
