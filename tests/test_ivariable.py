from typing import Sequence

import clr
import pytest

import ansys.modelcenter.workflow.api as mcapi

clr.AddReference("phoenix-mocks/Phoenix.Mock.v45")
from Phoenix.Mock import (
    MockBooleanVariable,
    MockComponent,
    MockDoubleVariable,
    MockIntegerVariable,
    MockVariableLink,
)

clr.AddReference("System.Reflection")
from System.Reflection import Missing

__instance_only_tests = [
    pytest.param(
        mcapi.IDoubleVariable(MockDoubleVariable("Workflow.Assembly.doubleVar", 0)), id="double"
    )
]


@pytest.mark.parametrize(
    "sut,expected_result",
    [
        pytest.param(
            mcapi.IDoubleVariable(MockDoubleVariable("Workflow.Assembly.doubleVar", 0)),
            "doubleVar",
            id="double",
        )
    ],
)
def test_get_name(sut: mcapi.IVariable, expected_result: str) -> None:
    """
    Verify that get_name works for different IVariable implementations.
    """

    # Execute
    result = sut.name

    assert result == expected_result


@pytest.mark.parametrize(
    "sut,expected_result",
    [
        pytest.param(
            mcapi.IDoubleVariable(MockDoubleVariable("Workflow.Assembly.doubleVar", 0)),
            "Workflow.Assembly.doubleVar",
            id="double",
        )
    ],
)
def test_get_full_name(sut: mcapi.IVariable, expected_result: str) -> None:
    """
    Verify that get_full_name works for different IVariable implementations.
    """

    # Execute
    result = sut.get_full_name()

    assert result == expected_result


@pytest.mark.parametrize(
    "sut",
    [
        pytest.param(
            mcapi.IDoubleVariable(MockDoubleVariable("Workflow.Assembly.doubleVar", 0)), id="double"
        )
    ],
)
def test_has_changed(sut: mcapi.IVariable) -> None:
    """
    Verify that `has_changed` property works for different IVariable implementations.
    """
    assert sut.has_changed is False

    # Execute
    sut.has_changed = True  # eventually change to sut.value = ...

    # Verify
    assert sut.has_changed is True


@pytest.mark.parametrize(
    "sut",
    [
        pytest.param(
            mcapi.IDoubleVariable(MockDoubleVariable("Workflow.Assembly.doubleVar", 0)), id="double"
        )
    ],
)
def test_hide(sut: mcapi.IVariable) -> None:
    """
    Verify that `hide` property works for different IVariable implementations.
    """
    assert sut.hide is False

    # Execute
    sut.hide = True

    # Verify
    assert sut.hide is True


@pytest.mark.parametrize(
    "sut",
    [
        pytest.param(
            mcapi.IDoubleVariable(MockDoubleVariable("Workflow.Assembly.doubleVar", 0)), id="double"
        )
    ],
)
def test_owning_component(sut: mcapi.IVariable) -> None:
    """
    Verify that `owning_component` property works for different IVariable implementations.
    """
    assert sut.owning_component is None
    mock_component = MockComponent("Assembly23")

    # Execute
    sut._wrapped.OwningComponent = mock_component
    component: mcapi.IComponent = sut.owning_component

    # Verify
    assert component.name == mock_component.getName()


__is_input_tests = [
    pytest.param(
        mcapi.IDoubleVariable(MockDoubleVariable("Workflow.Assembly.doubleVar", 0)),
        True,
        id="double input",
    ),
    pytest.param(
        mcapi.IDoubleVariable(MockDoubleVariable("Workflow.Assembly.doubleVar", 0)),
        True,
        id="double output",
    ),
]


@pytest.mark.parametrize("sut,expected_value", __is_input_tests)
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


@pytest.mark.parametrize("sut,expected_value", __is_input_tests)
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


@pytest.mark.parametrize("sut", __instance_only_tests)
def test_validate(sut: mcapi.IVariable) -> None:
    """
    Verify that validate calls through to the mock.
    """
    # Setup / sanity check
    assert sut._wrapped.getCallCount("validate") == 0

    # Execute
    sut.validate()

    # Verify
    assert sut._wrapped.getCallCount("validate") == 1


@pytest.mark.parametrize("sut", __instance_only_tests)
def test_invalidate(sut: mcapi.IVariable) -> None:
    """
    Verify that invalidate calls through to the mock.
    """
    # Setup / sanity check
    assert sut._wrapped.getCallCount("invalidate") == 0

    # Execute
    sut.invalidate()

    # Verify
    assert sut._wrapped.getCallCount("invalidate") == 1


@pytest.mark.parametrize("sut", __instance_only_tests)
@pytest.mark.skip(reason="rewrite for grpc api")
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


@pytest.mark.parametrize("sut", __instance_only_tests)
@pytest.mark.skip(reason="rewrite for grpc api")
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


__dependent_precedent_tests = [
    pytest.param(
        mcapi.IDoubleVariable(MockDoubleVariable("Workflow.Assembly.doubleVar", 0)),
        True,
        id="double follow suspended",
    ),
    pytest.param(
        mcapi.IDoubleVariable(MockDoubleVariable("Workflow.Assembly.doubleVar", 0)),
        True,
        id="double do not follow suspended",
    ),
]


@pytest.mark.parametrize("sut,follow_suspend", __dependent_precedent_tests)
def test_direct_dependents(sut: mcapi.IVariable, follow_suspend: bool) -> None:
    mock_vars = [
        MockDoubleVariable("mockvar", 0),
        MockIntegerVariable("mockVar2", 0),
        MockBooleanVariable("mockVar3", 0),
    ]
    for mock_var in mock_vars:
        sut._wrapped.DirectDependentsStorage.addItem(mock_var)
    assert sut._wrapped.getCallCount("directDependents") == 0

    result: Sequence[mcapi.IVariable] = sut.direct_dependents(follow_suspend)

    assert isinstance(result[0], mcapi.IDoubleVariable)
    assert isinstance(result[1], mcapi.IIntegerVariable)
    assert isinstance(result[2], mcapi.IBooleanVariable)
    assert [each_result_item._wrapped for each_result_item in result] == mock_vars
    assert sut._wrapped.getCallCount("directDependents") == 1
    assert sut._wrapped.getArgumentRecord("directDependents", 0) == [follow_suspend, Missing.Value]


@pytest.mark.parametrize("sut,follow_suspend", __dependent_precedent_tests)
def test_direct_precedents(sut: mcapi.IVariable, follow_suspend: bool) -> None:
    mock_vars = [
        MockDoubleVariable("mockvar", 1),
        MockIntegerVariable("mockVar2", 1),
        MockBooleanVariable("mockVar3", 1),
    ]
    for mock_var in mock_vars:
        sut._wrapped.DirectPrecedentsStorage.addItem(mock_var)
    assert sut._wrapped.getCallCount("directPrecedents") == 0

    result: Sequence[mcapi.IVariable] = sut.direct_precedents(follow_suspend)

    assert isinstance(result[0], mcapi.IDoubleVariable)
    assert isinstance(result[1], mcapi.IIntegerVariable)
    assert isinstance(result[2], mcapi.IBooleanVariable)
    assert [each_result_item._wrapped for each_result_item in result] == mock_vars
    assert sut._wrapped.getCallCount("directPrecedents") == 1
    assert sut._wrapped.getArgumentRecord("directPrecedents", 0) == [follow_suspend, Missing.Value]


@pytest.mark.parametrize("sut,follow_suspend", __dependent_precedent_tests)
def test_dependents(sut: mcapi.IVariable, follow_suspend: bool) -> None:
    mock_vars = [
        MockDoubleVariable("mockvar", 0),
        MockIntegerVariable("mockVar2", 0),
        MockBooleanVariable("mockVar3", 0),
    ]
    for mock_var in mock_vars:
        sut._wrapped.DependentsStorage.addItem(mock_var)
    assert sut._wrapped.getCallCount("dependents") == 0

    result: Sequence[mcapi.IVariable] = sut.dependents(follow_suspend)

    assert isinstance(result[0], mcapi.IDoubleVariable)
    assert isinstance(result[1], mcapi.IIntegerVariable)
    assert isinstance(result[2], mcapi.IBooleanVariable)
    assert [each_result_item._wrapped for each_result_item in result] == mock_vars
    assert sut._wrapped.getCallCount("dependents") == 1
    assert sut._wrapped.getArgumentRecord("dependents", 0) == [follow_suspend, Missing.Value]


@pytest.mark.parametrize("sut,follow_suspend", __dependent_precedent_tests)
def test_precedents(sut: mcapi.IVariable, follow_suspend: bool) -> None:
    mock_vars = [
        MockDoubleVariable("mockvar", 1),
        MockIntegerVariable("mockVar2", 1),
        MockBooleanVariable("mockVar3", 1),
    ]
    for mock_var in mock_vars:
        sut._wrapped.PrecedentsStorage.addItem(mock_var)
    assert sut._wrapped.getCallCount("precedents") == 0

    result: Sequence[mcapi.IVariable] = sut.precedents(follow_suspend)

    assert isinstance(result[0], mcapi.IDoubleVariable)
    assert isinstance(result[1], mcapi.IIntegerVariable)
    assert isinstance(result[2], mcapi.IBooleanVariable)
    assert [each_result_item._wrapped for each_result_item in result] == mock_vars
    assert sut._wrapped.getCallCount("precedents") == 1
    assert sut._wrapped.getArgumentRecord("precedents", 0) == [follow_suspend, Missing.Value]
