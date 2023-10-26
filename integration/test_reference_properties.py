from typing import cast

from ansys.engineeringworkflow.api import ValueOutOfRangeError
import ansys.tools.variableinterop as atvi
import pytest

import ansys.modelcenter.workflow.api as mcapi
from ansys.modelcenter.workflow.api import IReferenceArrayProperty, IReferenceProperty
from ansys.modelcenter.workflow.grpc_modelcenter import ReferenceArrayProperty, ReferenceProperty


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
    datapin: mcapi.IReferenceDatapin = workflow.get_datapin("Model.RefPropsScript.scalarInput")
    prop: IReferenceProperty = cast(IReferenceProperty, datapin.get_reference_properties()[name])

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
    datapin: mcapi.IReferenceArrayDatapin = workflow.get_datapin("Model.RefPropsScript.arrayInput")
    prop: IReferenceArrayProperty = cast(
        IReferenceArrayProperty, datapin.get_reference_properties()[name]
    )

    # Act
    result: atvi.VariableState = prop.get_state_at(0)

    # Assert
    assert result.is_valid is True
    assert result.value == expected_value


@pytest.mark.parametrize(
    "index",
    [99, -1],
)
@pytest.mark.workflow_name("reference_properties_tests.pxcz")
def test_getting_reference_array_property_values_at_out_of_bounds_index_returns_good_error(
    workflow, index
) -> None:
    # Arrange
    datapin: mcapi.IReferenceArrayDatapin = workflow.get_datapin("Model.RefPropsScript.arrayInput")
    prop: IReferenceArrayProperty = cast(
        IReferenceArrayProperty, datapin.get_reference_properties()["stringParam"]
    )

    # Act and assert
    with pytest.raises(ValueOutOfRangeError, match="The specified index is out of range."):
        prop.get_state_at(index)


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
    datapin: mcapi.IReferenceDatapin = workflow.get_datapin("Model.RefPropsScript.scalarInput")
    prop: IReferenceProperty = cast(IReferenceProperty, datapin.get_reference_properties()[name])

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
    datapin: mcapi.IReferenceArrayDatapin = workflow.get_datapin("Model.RefPropsScript.arrayInput")
    prop: IReferenceArrayProperty = cast(
        IReferenceArrayProperty, datapin.get_reference_properties()[name]
    )

    # Act
    prop.set_value_at(0, atvi.VariableState(value=value, is_valid=True))

    # Assert
    result: atvi.VariableState = prop.get_state_at(0)
    assert result.is_valid is True
    assert result.value == value


@pytest.mark.parametrize(
    "index",
    [99, -1],
)
@pytest.mark.workflow_name("reference_properties_tests.pxcz")
def test_setting_reference_array_property_values_at_out_bounds_index_returns_good_error(
    workflow, index
) -> None:
    # Arrange
    datapin: mcapi.IReferenceArrayDatapin = workflow.get_datapin("Model.RefPropsScript.arrayInput")
    prop: IReferenceArrayProperty = cast(
        IReferenceArrayProperty, datapin.get_reference_properties()["stringParam"]
    )

    # Act and assert
    with pytest.raises(ValueOutOfRangeError, match="The specified index is out of range."):
        prop.set_value_at(index, atvi.VariableState(value=atvi.StringValue("Sun日"), is_valid=True))


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
    datapin: mcapi.IReferenceDatapin = workflow.get_datapin(target)
    prop: IReferenceProperty = datapin.get_reference_properties()[name]

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
    datapin: mcapi.IReferenceDatapin = workflow.get_datapin(target)
    prop: IReferenceProperty = datapin.get_reference_properties()[name]

    # Act
    result: atvi.VariableType = prop.get_value_type()

    # Assert
    assert result == expected_type


@pytest.mark.parametrize(
    "target,is_input",
    [
        pytest.param("Model.RefPropsScript.scalarInput", True, id="scalar_input"),
        pytest.param("Model.RefPropsScript.arrayInput", True, id="array_input"),
        pytest.param("Model.RefPropsScript.scalarOutput", False, id="scalar_output"),
        pytest.param("Model.RefPropsScript.arrayOutput", False, id="array_output"),
    ],
)
@pytest.mark.workflow_name("reference_properties_tests.pxcz")
def test_can_get_if_a_reference_property_is_an_input(workflow, target: str, is_input: bool) -> None:
    # Arrange
    datapin: mcapi.IReferenceDatapin = workflow.get_datapin(target)
    prop: IReferenceProperty = datapin.get_reference_properties()["realParam"]

    # Act
    result: bool = prop.is_input

    # Assert
    assert result == is_input


@pytest.mark.parametrize(
    "target, ref_prop_type",
    [
        pytest.param("Model.RefPropsScript.scalarInput", ReferenceProperty, id="scalar"),
        pytest.param("Model.RefPropsScript.arrayInput", ReferenceArrayProperty, id="array"),
    ],
)
@pytest.mark.workflow_name("reference_properties_tests.pxcz")
def test_get_reference_properties(workflow, target: str, ref_prop_type: type):
    # Arrange
    datapin: mcapi.IReferenceDatapin = workflow.get_datapin(target)
    expected_names = ["stringParam", "realParam", "intParam", "boolParam"]

    # Act
    result = datapin.get_reference_properties()

    # Assert
    assert len(result) == len(expected_names)

    for name in expected_names:
        if name in result.keys():
            ref_prop: ReferenceProperty = cast(ReferenceProperty, result[name])

            assert ref_prop.name == name
            assert ref_prop._element_id == datapin._element_id
            assert ref_prop._engine == datapin._engine
        else:
            assert False, f"{name} not found in reference property map."
