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

raw_scalars = [True, 6.7, 8, "$"]
mock_scalars = [
    MockBooleanVariable("var1", 0), MockDoubleVariable("var1", 0), MockIntegerVariable("var1", 0),
    MockStringVariable("var1", 0),
]
scalar_types = [
    mcapi.IBooleanVariable, mcapi.IDoubleVariable, mcapi.IIntegerVariable, mcapi.IStringVariable
]
acvi_scalars = [
    acvi.BooleanValue(True), acvi.RealValue(6.7), acvi.IntegerValue(8), acvi.StringValue("$")
]
scalar_names = ["Bool", "Real", "Integer", "String"]
value_test_cases = []
for i in range(4):
    value_test_cases.append(
        pytest.param(raw_scalars[i], mock_scalars[i], scalar_types[i], acvi_scalars[i],
                     id=scalar_names[i])
    )

raw_arrays = [[True, False, True], [1.1, 2.2, 3.3], [1, 2, 3], ["a", "b", "c"]]
mock_arrays = [
    MockBooleanArray("var1", 0), MockDoubleArray("var1", 0), MockIntegerArray("var1", 0),
    MockStringArray("var1", 0),
]
array_types = [
    mcapi.IBooleanArray, mcapi.IDoubleArray, mcapi.IIntegerArray, mcapi.IStringArray
]
acvi_arrays = [
    acvi.BooleanArrayValue(3, [True, False, True]), acvi.RealArrayValue(3, [1.1, 2.2, 3.3]),
    acvi.IntegerArrayValue(3, [1, 2, 3]), acvi.StringArrayValue(3, ["a", "b", "c"]),
]
array_names = ["Bool Array", "Real Array", "Integer Array", "String Array"]

value_array_cases = []
for i in range(4):
    value_test_cases.append(
        pytest.param(raw_arrays[i], mock_arrays[i], array_types[i], acvi_arrays[i],
                     id=array_names[i])
    )

scalar_metadata = [
    acvi.BooleanMetadata(), acvi.RealMetadata(), acvi.IntegerMetadata(), acvi.StringMetadata()
]
array_metadata = [
    acvi.BooleanArrayMetadata(), acvi.RealArrayMetadata(), acvi.IntegerArrayMetadata(),
    acvi.StringArrayMetadata()
]
metadata_test_cases = []
for i in range(4):
    metadata_test_cases.append(
        pytest.param(mock_scalars[i], scalar_types[i], scalar_metadata[i])
    )
    metadata_test_cases.append(
        pytest.param(mock_arrays[i], array_types[i], array_metadata[i])
    )


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


set_value_cases = []
for i in range(4):
    set_value_cases.append(
        pytest.param(mock_scalars[i], scalar_types[i], acvi_scalars[i],
                     id=scalar_names[i])
    )
set_value_array_cases = []
for i in range(4):
    set_value_array_cases.append(
        pytest.param(mock_arrays[i], array_types[i], acvi_arrays[i],
                     id=array_names[i])
    )


@pytest.mark.parametrize("mock,sut_type,expected", set_value_cases + set_value_array_cases)
def test_set_value(mock: MockVariable, sut_type: Type,
                   expected: acvi.IVariableValue) -> None:
    """
    Verifies setting the value for all IVariable descendants.

    Parameters
    ----------
    mock The native variable.
    sut_type The type of mcapi.IVariable to create.
    expected The expected result.
    """
    sut: mcapi.IVariable = sut_type(mock)

    sut.value = expected

    result: acvi.IVariableValue = sut.value
    assert result == expected


@pytest.mark.parametrize("mock,sut_type,expected", set_value_cases)
def test_set_initial_value(mock: MockVariable, sut_type: Type,
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


is_valid_cases = []
for i in range(4):
    is_valid_cases.append(
        pytest.param(mock_scalars[i], scalar_types[i], True, id=scalar_names[i] + " True")
    )
    is_valid_cases.append(
        pytest.param(mock_scalars[i], scalar_types[i], False, id=scalar_names[i] + " False")
    )
    is_valid_cases.append(
        pytest.param(mock_arrays[i], array_types[i], True, id=array_names[i] + " True")
    )
    is_valid_cases.append(
        pytest.param(mock_arrays[i], array_types[i], False, id=array_names[i] + " False")
    )


@pytest.mark.parametrize("mock,sut_type,valid", is_valid_cases)
def test_is_valid(mock: MockVariable, sut_type: Type, valid: bool) -> None:
    """
    Verifies is_valid for all variables.

    Parameters
    ----------
    mock The native variable.
    sut_type The type of mcapi.IVariable to create.
    valid The value is_valid should return.
    """
    mock.Valid = valid
    sut: mcapi.IVariable = sut_type(mock)

    result: bool = sut.is_valid()

    assert result == valid


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
