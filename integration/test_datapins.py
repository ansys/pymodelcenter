import typing
from typing import Any, Mapping

import ansys.common.variableinterop as acvi
import ansys.engineeringworkflow.api as ewapi
import pytest

import ansys.modelcenter.workflow.api as mcapi
import ansys.modelcenter.workflow.grpc_modelcenter as grpcmc


@pytest.mark.parametrize(
    "name,var_type,is_array",
    [
        ("boolIn", grpcmc.BooleanDatapin, False),
        ("realIn", grpcmc.RealDatapin, False),
        ("intIn", grpcmc.IntegerDatapin, False),
        ("strIn", grpcmc.StringDatapin, False),
        ("boolIn", grpcmc.BooleanArrayDatapin, True),
        ("realIn", grpcmc.RealArrayDatapin, True),
        ("intIn", grpcmc.IntegerArrayDatapin, True),
        ("strIn", grpcmc.StringArrayDatapin, True),
    ],
)
def test_can_get_basic_variable_information(workflow, name, var_type, is_array) -> None:
    # Arrange
    parent: typing.Union[grpcmc.Component, mcapi.IGroup] = workflow.get_component(
        "ワークフロー.all_types_コンポーネント"
    )
    if is_array:
        parent = next(iter(parent.groups.values()))
    full_name: str = parent.full_name + "." + name

    # Act
    variable: mcapi.IDatapin = workflow.get_variable(full_name)

    # Assert
    assert isinstance(variable, var_type)
    assert variable.name == name
    assert variable.full_name == full_name
    assert variable.element_id is not None
    assert variable.parent_element_id == parent.element_id
    assert variable.get_parent_element() == parent
    assert variable.is_input_to_workflow
    assert variable.is_input_to_component


def test_can_manipulate_variable_properties(workflow) -> None:
    # Arrange
    variable: mcapi.IDatapin = workflow.get_variable("ワークフロー.all_types_コンポーネント.realIn")
    prop_name: str = "lowerBound"
    prop_value: acvi.IVariableValue = acvi.RealValue(5.5)

    # Act
    variable.set_property(property_name=prop_name, property_value=prop_value)
    prop: ewapi.Property = variable.get_property(property_name=prop_name)
    props: Mapping[str, ewapi.Property] = variable.get_properties()

    # Assert
    assert prop.property_name == prop_name
    assert prop.property_value == prop_value
    assert prop.parent_element_id == variable.element_id
    assert props[prop_name] == prop


def do_bool_setup(variable: mcapi.IDatapin, is_array: bool) -> None:
    meta_type = acvi.BooleanArrayMetadata if is_array else acvi.BooleanMetadata
    cast = typing.cast(Any, variable)
    metadata = meta_type()
    metadata.description = "boolブール"
    metadata.custom_metadata["blargඞ"] = acvi.RealValue(0.00000007)
    cast.set_metadata(metadata)


def do_bool_assert(variable: mcapi.IDatapin) -> None:
    cast = typing.cast(Any, variable)
    metadata = cast.get_metadata()
    assert metadata.description == "boolブール"
    assert metadata.custom_metadata["blargඞ"] == acvi.RealValue(0.00000007)


def do_real_setup(variable: mcapi.IDatapin, is_array: bool) -> None:
    meta_type = acvi.RealArrayMetadata if is_array else acvi.RealMetadata
    cast = typing.cast(Any, variable)
    metadata = meta_type()
    metadata.description = "real浮動小数点数"
    metadata.custom_metadata["blargඞ"] = acvi.RealValue(0.00000007)
    metadata.units = "cd/m²"
    metadata.display_format = "$#,##"
    metadata.lower_bound = 1.0
    metadata.upper_bound = 3.0
    metadata.enumerated_values = [1.0, 2.0, 3.0]
    metadata.enumerated_aliases = ["1ඞ", "2ඞ", "3ඞ"]
    cast.set_metadata(metadata)


def do_real_assert(variable: mcapi.IDatapin) -> None:
    cast = typing.cast(Any, variable)
    metadata = cast.get_metadata()
    assert metadata.description == "real浮動小数点数"
    assert metadata.custom_metadata["blargඞ"] == acvi.RealValue(0.00000007)
    assert metadata.units == "cd/m²"
    assert metadata.display_format == "$#,##0"
    assert metadata.lower_bound == 1.0
    assert metadata.upper_bound == 3.0
    assert metadata.enumerated_values == [1.0, 2.0, 3.0]
    assert metadata.enumerated_aliases == ["1ඞ", "2ඞ", "3ඞ"]


def do_int_setup(variable: mcapi.IDatapin, is_array: bool) -> None:
    meta_type = acvi.IntegerArrayMetadata if is_array else acvi.IntegerMetadata
    cast = typing.cast(Any, variable)
    metadata = meta_type()
    metadata.description = "int整数"
    metadata.custom_metadata["blargඞ"] = acvi.RealValue(0.00000007)
    metadata.units = "cd/m²"
    metadata.display_format = "$#,##"
    metadata.lower_bound = 1
    metadata.upper_bound = 3
    metadata.enumerated_values = [1, 2, 3]
    metadata.enumerated_aliases = ["1ඞ", "2ඞ", "3ඞ"]
    cast.set_metadata(metadata)


def do_int_assert(variable: mcapi.IDatapin) -> None:
    cast = typing.cast(Any, variable)
    metadata = cast.get_metadata()
    assert metadata.description == "int整数"
    assert metadata.custom_metadata["blargඞ"] == acvi.RealValue(0.00000007)
    assert metadata.units == "cd/m²"
    assert metadata.display_format == "$#,##0"
    assert metadata.lower_bound == 1
    assert metadata.upper_bound == 3
    assert metadata.enumerated_values == [1, 2, 3]
    assert metadata.enumerated_aliases == ["1ඞ", "2ඞ", "3ඞ"]


def do_string_setup(variable: mcapi.IDatapin, is_array: bool) -> None:
    meta_type = acvi.StringArrayMetadata if is_array else acvi.StringMetadata
    cast = typing.cast(Any, variable)
    metadata = meta_type()
    metadata.description = "string文字"
    metadata.custom_metadata["blargඞ"] = acvi.RealValue(0.00000007)
    metadata.enumerated_values = ["a", "b", "c"]
    metadata.enumerated_aliases = ["aඞ", "bඞ", "cඞ"]
    cast.set_metadata(metadata)


def do_string_assert(variable: mcapi.IDatapin) -> None:
    cast = typing.cast(Any, variable)
    metadata = cast.get_metadata()
    assert metadata.description == "string文字"
    assert metadata.custom_metadata["blargඞ"] == acvi.RealValue(0.00000007)
    assert metadata.enumerated_values == ["a", "b", "c"]
    assert metadata.enumerated_aliases == ["aඞ", "bඞ", "cඞ"]


@pytest.mark.parametrize(
    "var_name,val_type,value,var_setup,var_assert,is_array",
    [
        (
            "ワークフロー.all_types_コンポーネント.boolIn",
            acvi.VariableType.BOOLEAN,
            ewapi.VariableState(value=acvi.BooleanValue(True), is_valid=True),
            do_bool_setup,
            do_bool_assert,
            False,
        ),
        (
            "ワークフロー.all_types_コンポーネント.realIn",
            acvi.VariableType.REAL,
            ewapi.VariableState(value=acvi.RealValue(1.0), is_valid=True),
            do_real_setup,
            do_real_assert,
            False,
        ),
        (
            "ワークフロー.all_types_コンポーネント.intIn",
            acvi.VariableType.INTEGER,
            ewapi.VariableState(value=acvi.IntegerValue(1), is_valid=True),
            do_int_setup,
            do_int_assert,
            False,
        ),
        (
            "ワークフロー.all_types_コンポーネント.strIn",
            acvi.VariableType.STRING,
            ewapi.VariableState(value=acvi.StringValue("a"), is_valid=True),
            do_string_setup,
            do_string_assert,
            False,
        ),
        (
            "ワークフロー.all_types_コンポーネント.arrays.boolIn",
            acvi.VariableType.BOOLEAN_ARRAY,
            ewapi.VariableState(
                value=acvi.BooleanArrayValue(values=[True, False, True]), is_valid=True
            ),
            do_bool_setup,
            do_bool_assert,
            True,
        ),
        (
            "ワークフロー.all_types_コンポーネント.arrays.realIn",
            acvi.VariableType.REAL_ARRAY,
            ewapi.VariableState(value=acvi.RealArrayValue(values=[1.0, 2.0, 3.0]), is_valid=True),
            do_real_setup,
            do_real_assert,
            True,
        ),
        (
            "ワークフロー.all_types_コンポーネント.arrays.intIn",
            acvi.VariableType.INTEGER_ARRAY,
            ewapi.VariableState(value=acvi.IntegerArrayValue(values=[1, 2, 3]), is_valid=True),
            do_int_setup,
            do_int_assert,
            True,
        ),
        (
            "ワークフロー.all_types_コンポーネント.arrays.strIn",
            acvi.VariableType.STRING_ARRAY,
            ewapi.VariableState(value=acvi.StringArrayValue(values=["a", "b", "c"]), is_valid=True),
            do_string_setup,
            do_string_assert,
            True,
        ),
    ],
)
def test_can_manipulate_type_specific_variable_information(
    workflow, var_name, val_type, value, var_setup, var_assert, is_array
) -> None:
    # Arrange
    variable: mcapi.IDatapin = workflow.get_variable(var_name)
    var_setup(variable, is_array)

    # Act
    variable.set_value(value)
    value_result: ewapi.VariableState = variable.get_value(hid=None)

    # Assert
    assert value_result == value
    assert variable.value_type == val_type
    var_assert(variable)
