from typing import Sequence

import ansys.common.variableinterop as acvi
import clr
import pytest

import ansys.modelcenter.workflow.api as mcapi

clr.AddReference("phoenix-mocks/Phoenix.Mock.v45")
import Phoenix.Mock as mocks
from System.Runtime.InteropServices import COMException

# Globals
sut: mcapi.IReferenceVariable


def generate_referenced_variables(start: float, num: int) -> Sequence[mcapi.IDoubleVariable]:
    """
    Generate a list of ``IDoubleVariables`` suitable to be used as \
    ``IReferenceVariable.referenced_variables``.

    Parameters
    ----------
    start : float
        Value of first result will start here. Subsequent result values
        are increased by 1.
    num : int
        How many MockDoubleVariables to make.

    Returns
    -------
    Sequence[IDoubleVariable]
        The generated list of IDoubleVariables.
    """
    refs = []
    value = start
    for i in range(num):
        mock = mocks.MockDoubleVariable(f"name{i}", mcapi.VarType.INPUT)
        mock.value = value
        value += 1
        refs.append(mcapi.IDoubleVariable(mock))
    return refs


def setup_function():
    """Setup called before each test in this module."""
    global sut
    sut = mcapi.IReferenceVariable(mocks.MockReferenceVariable("test name", mcapi.VarType.INPUT))
    sut.value = acvi.RealValue(1.1)
    sut.standard_metadata.description = "initial description"
    sut.reference = "initial reference"
    sut.referenced_variables = generate_referenced_variables(start=1.5, num=3)
    sut.referenced_variable = mcapi.IDoubleVariable(
        mocks.MockDoubleVariable("ref var", mcapi.VarType.INPUT)
    )
    sut.create_real_ref_prop("refprop1", "double")
    sut.set_real_ref_prop_value("refprop1", "1.2")


####################################################################################################


def test_value():
    """Tests the 'value' property."""
    # Setup/initial check
    assert sut.value == 1.1
    sut.value = 2.0

    # Verify setter
    assert sut.value == 2.0


def test_value_absolute():
    """Tests the 'value_absolute' property."""
    # Setup/initial check
    assert sut.value_absolute == 1.1
    sut.value = 2.0

    # Verify setter
    assert sut.value_absolute == 2.0


def test_standard_metadata():
    """Tests the 'standard_metadata' property."""
    # Setup/SUT
    original = sut.standard_metadata
    sut.standard_metadata = acvi.RealMetadata()

    # Verify
    assert original.description == "initial description"
    assert sut.standard_metadata is not original


def test_reference():
    """Tests the 'reference' property."""
    # Setup/SUT
    original = sut.reference
    sut.reference = "new reference"

    # Verify
    assert original == "initial reference"
    assert sut.reference == "new reference"


def test_referenced_variables():
    """Tests the 'referenced_variables' property."""
    # Setup/SUT
    original = sut.referenced_variables
    sut.referenced_variables = generate_referenced_variables(start=2.5, num=4)

    # Verify
    assert [var.get_value(None).value for var in original] == [1.5, 2.5, 3.5]
    assert [var.get_value(None).value for var in sut.referenced_variables] == [2.5, 3.5, 4.5, 5.5]


def test_referenced_variable():
    """Tests the 'referenced_variable' property."""
    # Setup/SUT
    original = sut.referenced_variable
    sut.referenced_variable = mcapi.IDoubleVariable(
        mocks.MockDoubleVariable("new name", mcapi.VarType.INPUT)
    )

    # Verify
    assert original is not sut.referenced_variable


def test_create_real_ref_prop():
    """Tests the 'create_real_ref_prop' method."""
    # Setup/SUT
    result: mcapi.IRefProp = sut.create_real_ref_prop("test refprop", "double")

    # Verify IRefProp creation
    assert sut._wrapped.getCallCount("createRefProp") == 2  # +1 from setup function
    assert result.get_name() == "test refprop"
    assert result.get_type() == "double"

    # Verify exception is raised when name already exists
    with pytest.raises(COMException):
        sut.create_real_ref_prop("test refprop", "double")


def test_get_set_real_ref_prop_value():
    """
    Tests the 'get_real_ref_prop_value' method.

    Also a valid test for 'set_real_ref_prop_value' since that method
    was called in the setup function.
    """
    # Setup/SUT
    result: acvi.RealValue = sut.get_real_ref_prop_value("refprop1")

    # Verify
    assert sut._wrapped.getCallCount("setRefPropValue") == 1
    assert result == 1.2


def test_get_real_ref_prop_value_absolute():
    """Tests the 'get_real_ref_prop_value_absolute' method."""
    # Setup/SUT
    result: acvi.RealValue = sut.get_real_ref_prop_value_absolute("refprop1")

    # Verify
    assert result == 1.2
