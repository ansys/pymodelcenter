"""Tests for IVariable and its descendants."""
from typing import Type

import ansys.common.variableinterop as acvi
import clr
import pytest

import ansys.modelcenter.workflow.api as mcapi

clr.AddReference('phoenix-mocks/Phoenix.Mock.v45')
from Phoenix.Mock import (
    MockBooleanArray,
    MockBooleanVariable,
    MockDoubleArray,
    MockDoubleVariable,
    MockIntegerArray,
    MockIntegerVariable,
    MockStringArray,
    MockStringVariable,
    MockVariable,
)

value_test_cases = [
    pytest.param(True, MockBooleanVariable("var1", 0), mcapi.IBooleanVariable,
                 acvi.BooleanValue(True), id="Bool"),
    pytest.param(6.7, MockDoubleVariable("var1", 0), mcapi.IDoubleVariable,
                 acvi.RealValue(6.7), id="Real"),
    pytest.param(8, MockIntegerVariable("var1", 0), mcapi.IIntegerVariable,
                 acvi.IntegerValue(8), id="Integer"),
    pytest.param("$", MockStringVariable("var1", 0), mcapi.IStringVariable,
                 acvi.StringValue("$"), id="String"),
    pytest.param([True, False, True], MockBooleanArray("var1", 0), mcapi.IBooleanArray,
                 acvi.BooleanArrayValue(3, [True, False, True]), id="BoolArray"),
    pytest.param([1, 2, 3], MockIntegerArray("var1", 0), mcapi.IIntegerArray,
                 acvi.IntegerArrayValue(3, [1, 2, 3]), id="IntegerArray"),
    pytest.param([1.1, 2.2, 3.3], MockDoubleArray("var1", 0), mcapi.IDoubleArray,
                 acvi.RealArrayValue(3, [1.1, 2.2, 3.3]), id="RealArray"),
    pytest.param(["a", "b", "c"], MockStringArray("var1", 0), mcapi.IStringArray,
                 acvi.StringArrayValue(3, ["a", "b", "c"]), id="StringArray"),
]
"""
Test cases that can be shared across all value tests.
Note that each test might not use all arguments, but still defines them.
"""


@pytest.mark.parametrize("value,mock,sut_type,expected", value_test_cases)
def test_get_value(value: object, mock: MockVariable, sut_type: Type,
                   expected: acvi.IVariableValue) -> None:
    """
    Verifies getting the value for all IVariable descendants.

    Parameters
    ----------
    value The value to set on the native variable.
    mock The native variable.
    sut_type The type of mcapi.IVariable to create.
    expected The expected result.
    """
    mock.value = value
    mock.MockSetStringValue(str(value).replace('[', '').replace(']', '').replace('\'', ''))
    # TODO: looks like I need to change to setting value via MockSetStringValue to support arrays
    sut: mcapi.IVariable = sut_type(mock)

    result: acvi.IVariableValue = sut.value

    assert result == expected


@pytest.mark.parametrize("value,mock,sut_type,expected", value_test_cases)
def test_get_value_absolute(value: object, mock: MockVariable, sut_type: Type,
                            expected: acvi.IVariableValue) -> None:
    """
    Verifies getting the 'absolute' value for all IVariable descendants.

    Parameters
    ----------
    value The value to set on the native variable.
    mock The native variable.
    sut_type The type of mcapi.IVariable to create.
    expected The expected result.
    """
    mock.valueAbsolute = value
    mock.MockSetStringValue(str(value).replace('[', '').replace(']', '').replace('\'', ''))
    sut: mcapi.IVariable = sut_type(mock)

    result: acvi.IVariableValue = sut.value_absolute

    assert result == expected


@pytest.mark.parametrize("value,mock,sut_type,expected", value_test_cases)
def test_set_value(value: object, mock: MockVariable, sut_type: Type,
                   expected: acvi.IVariableValue) -> None:
    """
    Verifies setting the value for all IVariable descendants.

    Parameters
    ----------
    value Not used.
    mock The native variable.
    sut_type The type of mcapi.IVariable to create.
    expected The expected result.
    """
    sut: mcapi.IVariable = sut_type(mock)

    sut.value = expected

    result: acvi.IVariableValue = sut.value
    assert result == expected
