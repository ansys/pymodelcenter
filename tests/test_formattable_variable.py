"""Tests for the FormattableVariable class."""

import clr
import pytest

import ansys.modelcenter.workflow.api as mcapi

clr.AddReference('phoenix-mocks/Phoenix.Mock.v45')
from Phoenix.Mock import MockDoubleArray, MockDoubleVariable, MockIntegerArray, MockIntegerVariable

__format_cases = [
    pytest.param(mcapi.IDoubleVariable(MockDoubleVariable("mockdbl", 0)), id="double"),
    pytest.param(mcapi.IDoubleArray(MockDoubleArray("mockdblarray", 0)), id="double array"),
    pytest.param(mcapi.IIntegerVariable(MockIntegerVariable("mockint", 0)), id="integer"),
    pytest.param(mcapi.IIntegerArray(MockIntegerArray("mockintarray", 0)), id="integer array"),
]


@pytest.mark.parametrize('sut', __format_cases)
def test_get_format(sut: mcapi.FormattableVariable):
    """Verify that the format can be retrieved."""
    # Setup
    sut._wrapped.format = "TEST PASS"

    # Execute
    result: str = sut.format

    # Verify
    assert result == "TEST PASS"


@pytest.mark.parametrize('sut', __format_cases)
def test_set_format(sut: mcapi.FormattableVariable):
    """Verify that the format can be set."""
    # Setup
    sut._wrapped.format = "UNCHANGED"

    # Execute
    sut.format = "TEST PASS"

    # Verify
    assert sut._wrapped.format == "TEST PASS"
