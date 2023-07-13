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


@pytest.mark.parametrize(
    "target,name,expected_type,expected_description",
    [
        pytest.param(
            "Model.RefPropsScript.scalarInput",
            "stringParam",
            atvi.StringMetadata,
            "文字列型",
            id="scalar string",
        ),
        pytest.param(
            "Model.RefPropsScript.scalarInput",
            "realParam",
            atvi.RealMetadata,
            "浮動小数点数値型",
            id="scalar real",
        ),
        pytest.param(
            "Model.RefPropsScript.scalarInput",
            "intParam",
            atvi.IntegerMetadata,
            "整数数値型",
            id="scalar int",
        ),
        pytest.param(
            "Model.RefPropsScript.scalarInput",
            "boolParam",
            atvi.BooleanMetadata,
            "ブール値",
            id="scalar bool",
        ),
        pytest.param(
            "Model.RefPropsScript.arrayInput",
            "stringParam",
            atvi.StringMetadata,
            "文字列型",
            id="array string",
        ),
        pytest.param(
            "Model.RefPropsScript.arrayInput",
            "realParam",
            atvi.RealMetadata,
            "浮動小数点数値型",
            id="array real",
        ),
        pytest.param(
            "Model.RefPropsScript.arrayInput",
            "intParam",
            atvi.IntegerMetadata,
            "整数数値型",
            id="array int",
        ),
        pytest.param(
            "Model.RefPropsScript.arrayInput",
            "boolParam",
            atvi.BooleanMetadata,
            "ブール値",
            id="array bool",
        ),
    ],
)
@pytest.mark.workflow_name("reference_properties_tests.pxcz")
def test_can_get_reference_property_metadata(
    workflow, target: str, name: str, expected_type, expected_description: str
) -> None:
    # Arrange
    variable: mcapi.IReferenceDatapin = workflow.get_variable(target)
    # prop: mcapi.IReferenceArrayProperty = variable.get_reference_properties()[name]
    prop = grpcmc.ReferenceArrayProperty(
        ElementId(id_string=variable.element_id), name, variable._engine
    )

    # Act
    result: atvi.CommonVariableMetadata = prop.get_metadata()

    # Assert
    assert isinstance(result, expected_type)
    assert result.description == expected_description


@pytest.mark.parametrize(
    "target,name,expected_type",
    [
        pytest.param(
            "Model.RefPropsScript.scalarInput",
            "stringParam",
            atvi.VariableType.STRING,
            id="scalar string",
        ),
        pytest.param(
            "Model.RefPropsScript.scalarInput",
            "realParam",
            atvi.VariableType.REAL,
            id="scalar real",
        ),
        pytest.param(
            "Model.RefPropsScript.scalarInput",
            "intParam",
            atvi.VariableType.INTEGER,
            id="scalar int",
        ),
        pytest.param(
            "Model.RefPropsScript.scalarInput",
            "boolParam",
            atvi.VariableType.BOOLEAN,
            id="scalar bool",
        ),
        pytest.param(
            "Model.RefPropsScript.arrayInput",
            "stringParam",
            atvi.VariableType.STRING,
            id="array string",
        ),
        pytest.param(
            "Model.RefPropsScript.arrayInput",
            "realParam",
            atvi.VariableType.REAL,
            id="array real",
        ),
        pytest.param(
            "Model.RefPropsScript.arrayInput",
            "intParam",
            atvi.VariableType.INTEGER,
            id="array int",
        ),
        pytest.param(
            "Model.RefPropsScript.arrayInput",
            "boolParam",
            atvi.VariableType.BOOLEAN,
            id="array bool",
        ),
    ],
)
@pytest.mark.workflow_name("reference_properties_tests.pxcz")
def test_can_get_reference_property_value_type(
    workflow, target: str, name: str, expected_type: atvi.VariableType
) -> None:
    # Arrange
    variable: mcapi.IReferenceDatapin = workflow.get_variable(target)
    # prop: mcapi.IReferenceArrayProperty = variable.get_reference_properties()[name]
    prop = grpcmc.ReferenceArrayProperty(
        ElementId(id_string=variable.element_id), name, variable._engine
    )

    # Act
    result: atvi.VariableType = prop.get_value_type()

    # Assert
    assert result == expected_type


@pytest.mark.parametrize(
    "target,is_input",
    pytest.param("Model.RefPropsScript.scalarInput", True, id="input"),
    pytest.param("Model.RefPropsScript.scalarOutput", False, id="output"),
)
@pytest.mark.workflow_name("reference_properties_tests.pxcz")
def test_can_get_if_a_reference_property_is_an_input(workflow, target: str, is_input: bool) -> None:
    # Arrange
    variable: mcapi.IReferenceDatapin = workflow.get_variable(target)
    # prop: mcapi.IReferenceArrayProperty = variable.get_reference_properties()["realParam"]
    prop = grpcmc.ReferenceArrayProperty(
        ElementId(id_string=variable.element_id), "realParam", variable._engine
    )

    # Act
    result: bool = prop.is_input

    # Assert
    assert result == is_input
