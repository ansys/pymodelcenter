"""ansys.engineeringworkflow.api functionality tests"""

import ansys.common.variableinterop as acvi
from ansys.engineeringworkflow.api import IElement, Property
import clr
import pytest

from ansys.modelcenter.workflow.api import Assembly, IComponent, IDoubleVariable, IIntegerArray

clr.AddReference("phoenix-mocks/Phoenix.Mock.v45")
from Phoenix.Mock import (  # type: ignore
    MockAssembly,
    MockComponent,
    MockDoubleVariable,
    MockIntegerArray,
)


@pytest.mark.parametrize(
    "value",
    [
        pytest.param(acvi.BooleanValue(True), id="BooleanValue"),
        pytest.param(acvi.RealValue(3.14159), id="RealValue"),
        pytest.param(acvi.IntegerValue(42), id="IntegerValue"),
        pytest.param(acvi.StringValue("A string value."), id="StringValue"),
    ],
)
def test_get_set_property_value(value: acvi.IVariableValue) -> None:
    """
    Verify `set_property` and `get_property` methods work for different value types.
    """
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


@pytest.mark.parametrize(
    "value",
    [
        pytest.param(acvi.BooleanArrayValue(values=[True, False]), id="BooleanArrayValue"),
        pytest.param(acvi.IntegerArrayValue(values=[1, 2, 3]), id="IntegerArrayValue"),
        pytest.param(acvi.RealArrayValue(values=[1.1, 2.2, 3.3]), id="RealArrayValue"),
        pytest.param(acvi.StringArrayValue(values=["one", "two"]), id="StringArrayValue"),
    ],
)
def test_get_set_property_invalid_type(value: acvi.IVariableValue) -> None:
    """
    Verify `set_property` raises proper exception for unsupported value types.
    """
    # Setup
    assembly = Assembly(MockAssembly("assemblyName"))

    # SUT
    with pytest.raises(Exception) as except_info:
        assembly.set_property("prop1", value)

    # Verification
    assert (
        except_info.value.args[0] == "Assembly or component metadata must be str,"
        " float, int, or bool."
    )


@pytest.mark.parametrize(
    "value",
    [
        pytest.param(acvi.IntegerValue(42), id="IntegerValue"),
    ],
)
def test_get_properties(value: acvi.IVariableValue) -> None:
    """
    Verify `get_properties` raises an exception.
    """
    # Setup
    assembly = Assembly(MockAssembly("assemblyName"))
    assembly.set_property("prop1", value)

    # SUT
    with pytest.raises(Exception) as except_info:
        _ = assembly.get_properties()

    # Verification
    assert isinstance(except_info.value, NotImplementedError)


@pytest.mark.parametrize(
    "element",
    [
        pytest.param(
            IDoubleVariable(MockDoubleVariable("Workflow.Assembly.doubleVar", 0)), id="double"
        ),
        pytest.param(
            IIntegerArray(MockIntegerArray("Workflow.Assembly.intArray", 0)), id="integer array"
        ),
        pytest.param(Assembly(MockAssembly("first_assembly")), id="assembly"),
        pytest.param(IComponent(MockComponent("component")), id="component"),
    ],
)
def test_get_set_property_for_element(element: IElement) -> None:
    """
    Verify `set_property` and `get_property` methods work for different `IElement` implementations.
    """
    value = acvi.BooleanValue(True)

    # SUT
    element.set_property("prop1", value)
    prop = element.get_property("prop1")

    # Verification
    assert isinstance(prop, Property)
    assert prop.property_name == "prop1"
    assert prop.property_value == value
    assert prop.parent_element_id is None


@pytest.mark.parametrize(
    "sut,expected_name",
    [
        pytest.param(
            IDoubleVariable(MockDoubleVariable("Workflow.Assembly.doubleVar", 0)),
            "doubleVar",
            id="double",
        ),
        pytest.param(
            IIntegerArray(MockIntegerArray("Workflow.Assembly.intArray", 0)),
            "intArray",
            id="integer array",
        ),
        pytest.param(Assembly(MockAssembly("Workflow.TopAssembly")), "TopAssembly", id="assembly"),
        pytest.param(
            IComponent(MockComponent("Workflow.TopAssembly.Optimizer")), "Optimizer", id="component"
        ),
    ],
)
def test_name_for_element(sut: IElement, expected_name: str) -> None:
    """
    Verify `set_property` and `get_property` methods work for different `IElement` implementations.
    """
    value = acvi.BooleanValue(True)

    # SUT
    sut.set_property("prop1", value)
    name = sut.name

    # Verification
    assert name == expected_name
