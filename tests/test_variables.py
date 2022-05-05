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
]
"""
Test cases that can be shared across all value tests.
Note that each test might not use all arguments, but still defines them.
"""

value_array_cases = [
    pytest.param([True, False, True], MockBooleanArray("var1", 0), mcapi.IBooleanArray,
                 acvi.BooleanArrayValue(3, [True, False, True]), id="BoolArray"),
    pytest.param([1, 2, 3], MockIntegerArray("var1", 0), mcapi.IIntegerArray,
                 acvi.IntegerArrayValue(3, [1, 2, 3]), id="IntegerArray"),
    pytest.param([1.1, 2.2, 3.3], MockDoubleArray("var1", 0), mcapi.IDoubleArray,
                 acvi.RealArrayValue(3, [1.1, 2.2, 3.3]), id="RealArray"),
    pytest.param(["a", "b", "c"], MockStringArray("var1", 0), mcapi.IStringArray,
                 acvi.StringArrayValue(3, ["a", "b", "c"]), id="StringArray"),
]

metadata_test_cases = [
    pytest.param(MockBooleanVariable("var1", 0), mcapi.IBooleanVariable, acvi.BooleanMetadata()),
    pytest.param(MockDoubleVariable("var1", 0), mcapi.IDoubleVariable, acvi.RealMetadata()),
    pytest.param(MockIntegerVariable("var1", 0), mcapi.IIntegerVariable, acvi.IntegerMetadata()),
    pytest.param(MockStringVariable("var1", 0), mcapi.IStringVariable, acvi.StringMetadata()),
    pytest.param(MockBooleanArray("var1", 0), mcapi.IBooleanArray, acvi.BooleanArrayMetadata()),
    pytest.param(MockDoubleArray("var1", 0), mcapi.IDoubleArray, acvi.RealArrayMetadata()),
    pytest.param(MockIntegerArray("var1", 0), mcapi.IIntegerArray, acvi.IntegerArrayMetadata()),
    pytest.param(MockStringArray("var1", 0), mcapi.IStringArray, acvi.StringArrayMetadata()),
]


@pytest.mark.parametrize("value,mock,sut_type,expected", value_test_cases + value_array_cases)
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


@pytest.mark.parametrize("value,mock,sut_type,expected", value_test_cases + value_array_cases)
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


@pytest.mark.parametrize("value,mock,sut_type,expected", value_test_cases + value_array_cases)
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


@pytest.mark.parametrize("value,mock,sut_type,expected", value_test_cases)
def test_set_initial_value(value: object, mock: MockVariable, sut_type: Type,
                           expected: acvi.IVariableValue) -> None:
    """
    Verifies setting the initial value for all ScalarVariable descendants.

    Parameters
    ----------
    value Not used.
    mock The native variable.
    sut_type The type of mcapi.IVariable to create.
    expected The expected result.
    """
    sut: mcapi.IVariable = sut_type(mock)

    sut.set_initial_value(expected)

    assert mock.getArgumentRecord("setInitialValue", 0)[0] == expected


@pytest.mark.parametrize("mock,sut_type,expected", metadata_test_cases)
def test_get_metadata(mock: MockVariable, sut_type: Type, expected: acvi.CommonVariableMetadata) \
        -> None:
    sut: mcapi.IVariable = sut_type(mock)

    result: acvi.CommonVariableMetadata = sut.standard_metadata

    assert result == expected


@pytest.mark.parametrize("mock,sut_type,value", metadata_test_cases)
def test_set_metadata(mock: MockVariable, sut_type: Type, value: acvi.CommonVariableMetadata) \
        -> None:
    sut: mcapi.IVariable = sut_type(mock)
    assert sut.standard_metadata is not value

    sut.standard_metadata = value

    result: acvi.CommonVariableMetadata = sut.standard_metadata
    assert result is value
