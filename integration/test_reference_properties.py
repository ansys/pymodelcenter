import ansys.tools.variableinterop as atvi
import pytest

import ansys.modelcenter.workflow.api as mcapi
import ansys.modelcenter.workflow.grpc_modelcenter as grpcmc
from ansys.modelcenter.workflow.grpc_modelcenter.proto.element_messages_pb2 import ElementId


@pytest.mark.parametrize(
    "name,expected_value",
    [
        ("stringParam", atvi.StringValue("Mon月")),
        ("realParam", atvi.RealValue(6.0)),
        ("intParam", atvi.IntegerValue(7)),
        ("boolParam", atvi.BooleanValue(True)),
    ],
)
@pytest.mark.workflow_name("reference_properties_tests.pxcz")
def test_can_get_reference_property_values(workflow, name, expected_value) -> None:
    # Arrange
    variable: mcapi.IReferenceDatapin = workflow.get_variable("Model.RefPropsScript.scalarInput")
    # prop: mcapi.IReferenceProperty = variable.get_reference_properties()[name]
    prop = grpcmc.ReferenceProperty(
        ElementId(id_string=variable.element_id), name, variable._engine
    )

    # Act
    result: atvi.VariableState = prop.get_state()

    # Assert
    assert result.is_valid is True
    assert result.value == expected_value


@pytest.mark.parametrize(
    "name,expected_value",
    [
        ("stringParam", atvi.StringValue("Tues火")),
        ("realParam", atvi.RealValue(8.0)),
        ("intParam", atvi.IntegerValue(9)),
        ("boolParam", atvi.BooleanValue(False)),
    ],
)
@pytest.mark.workflow_name("reference_properties_tests.pxcz")
def test_can_get_reference_array_property_values(workflow, name, expected_value) -> None:
    # Arrange
    variable: mcapi.IReferenceDatapin = workflow.get_variable("Model.RefPropsScript.arrayInput")
    # prop: mcapi.IReferenceArrayProperty = variable.get_reference_properties()[name]
    prop = grpcmc.ReferenceArrayProperty(
        ElementId(id_string=variable.element_id), name, variable._engine
    )

    # Act
    result: atvi.VariableState = prop.get_state_at(0)

    # Assert
    assert result.is_valid is True
    assert result.value == expected_value


@pytest.mark.parametrize(
    "name,value",
    [
        ("stringParam", atvi.StringValue("Sun日")),
        ("realParam", atvi.RealValue(1.0)),
        ("intParam", atvi.IntegerValue(2)),
        ("boolParam", atvi.BooleanValue(False)),
    ],
)
@pytest.mark.workflow_name("reference_properties_tests.pxcz")
def test_can_set_reference_property_values(workflow, name, value) -> None:
    # Arrange
    variable: mcapi.IReferenceDatapin = workflow.get_variable("Model.RefPropsScript.scalarInput")
    # prop: mcapi.IReferenceProperty = variable.get_reference_properties()[name]
    prop = grpcmc.ReferenceProperty(
        ElementId(id_string=variable.element_id), name, variable._engine
    )

    # Act
    prop.set_value(atvi.VariableState(value=value, is_valid=True))

    # Assert
    result: atvi.VariableState = prop.get_state()
    assert result.is_valid is True
    assert result.value == value


@pytest.mark.parametrize(
    "name,value",
    [
        ("stringParam", atvi.StringValue("Sun日")),
        ("realParam", atvi.RealValue(8.0)),
        ("intParam", atvi.IntegerValue(9)),
        ("boolParam", atvi.BooleanValue(False)),
    ],
)
@pytest.mark.workflow_name("reference_properties_tests.pxcz")
def test_can_set_reference_array_property_values(workflow, name, value) -> None:
    # Arrange
    variable: mcapi.IReferenceDatapin = workflow.get_variable("Model.RefPropsScript.arrayInput")
    # prop: mcapi.IReferenceArrayProperty = variable.get_reference_properties()[name]
    prop = grpcmc.ReferenceArrayProperty(
        ElementId(id_string=variable.element_id), name, variable._engine
    )

    # Act
    prop.set_value_at(0, atvi.VariableState(value=value, is_valid=True))

    # Assert
    result: atvi.VariableState = prop.get_state_at(0)
    assert result.is_valid is True
    assert result.value == value
