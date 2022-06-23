"""ansys.engineeringworkflow.api functionality tests"""

import pytest
import clr
import ansys.common.variableinterop as acvi

from ansys.modelcenter.workflow.api import Assembly
from ansys.engineeringworkflow.api import Property

clr.AddReference('phoenix-mocks/Phoenix.Mock.v45')
from Phoenix.Mock import MockAssembly, MockComponent, MockVariable  # type: ignore


@pytest.mark.parametrize('value', [
    pytest.param(acvi.BooleanValue(True), id="BooleanValue"),
    pytest.param(acvi.RealValue(3.14159), id="RealValue"),
    pytest.param(acvi.IntegerValue(42), id="IntegerValue"),
    pytest.param(acvi.StringValue("A string value."), id="StringValue"),
])
def test_get_set_property(value: acvi.IVariableValue) -> None:
    # Setup
    assembly = Assembly(MockAssembly("assemblyName"))

    # SUT
    assembly.set_property("prop1", value)
    prop = assembly.get_property("prop1")

    # Verification
    assert isinstance(prop, Property)
    assert prop.property_name == "prop1"
    assert prop.property_value == value
    assert prop.parent_element_id is None


@pytest.mark.parametrize('value', [
    pytest.param(acvi.BooleanArrayValue(values=[True, False]), id="BooleanArrayValue"),
    pytest.param(acvi.IntegerArrayValue(values=[1, 2, 3]), id="IntegerArrayValue"),
    pytest.param(acvi.RealArrayValue(values=[1.1, 2.2, 3.3]), id="RealArrayValue"),
    pytest.param(acvi.StringArrayValue(values=["one", "two"]), id="StringArrayValue"),
])
def test_get_set_property_invalid_type(value: acvi.IVariableValue) -> None:
    # Setup
    assembly = Assembly(MockAssembly("assemblyName"))

    # SUT
    with pytest.raises(Exception) as except_info:
        assembly.set_property("prop1", value)

    # Verification
    assert except_info.value.args[0] == "Assembly or component metadata must be str," \
                                        " float, int, or bool."

