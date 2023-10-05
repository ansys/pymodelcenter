import contextlib
import tempfile
import typing
from typing import Any, Mapping
import unittest

import ansys.engineeringworkflow.api as ewapi
import ansys.tools.variableinterop as atvi
import numpy
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
        parent = next(iter(parent.get_groups().values()))
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


@pytest.mark.parametrize(
    "name,var_type",
    [
        ("fileASCIIIn", grpcmc.FileDatapin),
        ("fileArrayASCIIIn", grpcmc.FileArrayDatapin),
        ("fileBinaryIn", grpcmc.FileDatapin),
        ("fileArrayBinaryIn", grpcmc.FileArrayDatapin),
    ],
)
@pytest.mark.workflow_name("file_tests.pxcz")
def test_can_get_file_type_information(workflow, name, var_type) -> None:
    # Arrange
    parent: grpcmc.Assembly = workflow.get_root()
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


@pytest.mark.parametrize(
    "name,var_type",
    [
        ("doubleInRef", grpcmc.ReferenceDatapin),
        ("intInRef", grpcmc.ReferenceDatapin),
        ("doubleArrayInRef", grpcmc.ReferenceArrayDatapin),
    ],
)
@pytest.mark.workflow_name("reference_tests.pxcz")
def test_can_get_reference_type_information(workflow, name, var_type) -> None:
    # Arrange
    parent: grpcmc.Assembly = workflow.get_assembly("Model.ReferenceScript")
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
    assert variable.is_input_to_workflow is False
    assert variable.is_input_to_component is False


def test_can_manipulate_variable_properties(workflow) -> None:
    # Arrange
    variable: mcapi.IDatapin = workflow.get_variable("ワークフロー.all_types_コンポーネント.realIn")
    prop_name: str = "lowerBound"
    prop_value: atvi.IVariableValue = atvi.RealValue(5.5)

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
    meta_type = atvi.BooleanArrayMetadata if is_array else atvi.BooleanMetadata
    cast = typing.cast(Any, variable)
    metadata = meta_type()
    metadata.description = "boolブール"
    metadata.custom_metadata["blargඞ"] = atvi.RealValue(0.00000007)
    cast.set_metadata(metadata)


def do_bool_assert(variable: mcapi.IDatapin) -> None:
    cast = typing.cast(Any, variable)
    metadata = cast.get_metadata()
    assert metadata.description == "boolブール"
    assert metadata.custom_metadata["blargඞ"] == atvi.RealValue(0.00000007)


def do_real_setup(variable: mcapi.IDatapin, is_array: bool) -> None:
    meta_type = atvi.RealArrayMetadata if is_array else atvi.RealMetadata
    cast = typing.cast(Any, variable)
    metadata = meta_type()
    metadata.description = "real浮動小数点数"
    metadata.custom_metadata["blargඞ"] = atvi.RealValue(0.00000007)
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
    assert metadata.custom_metadata["blargඞ"] == atvi.RealValue(0.00000007)
    assert metadata.units == "cd/m²"
    assert metadata.display_format == "$#,##0"
    assert metadata.lower_bound == 1.0
    assert metadata.upper_bound == 3.0
    assert metadata.enumerated_values == [1.0, 2.0, 3.0]
    assert metadata.enumerated_aliases == ["1ඞ", "2ඞ", "3ඞ"]


def do_int_setup(variable: mcapi.IDatapin, is_array: bool) -> None:
    meta_type = atvi.IntegerArrayMetadata if is_array else atvi.IntegerMetadata
    cast = typing.cast(Any, variable)
    metadata = meta_type()
    metadata.description = "int整数"
    metadata.custom_metadata["blargඞ"] = atvi.RealValue(0.00000007)
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
    assert metadata.custom_metadata["blargඞ"] == atvi.RealValue(0.00000007)
    assert metadata.units == "cd/m²"
    assert metadata.display_format == "$#,##0"
    assert metadata.lower_bound == 1
    assert metadata.upper_bound == 3
    assert metadata.enumerated_values == [1, 2, 3]
    assert metadata.enumerated_aliases == ["1ඞ", "2ඞ", "3ඞ"]


def do_string_setup(variable: mcapi.IDatapin, is_array: bool) -> None:
    meta_type = atvi.StringArrayMetadata if is_array else atvi.StringMetadata
    cast = typing.cast(Any, variable)
    metadata = meta_type()
    metadata.description = "string文字"
    metadata.custom_metadata["blargඞ"] = atvi.RealValue(0.00000007)
    metadata.enumerated_values = ["a", "b", "c"]
    metadata.enumerated_aliases = ["aඞ", "bඞ", "cඞ"]
    cast.set_metadata(metadata)


def do_string_assert(variable: mcapi.IDatapin) -> None:
    cast = typing.cast(Any, variable)
    metadata = cast.get_metadata()
    assert metadata.description == "string文字"
    assert metadata.custom_metadata["blargඞ"] == atvi.RealValue(0.00000007)
    assert metadata.enumerated_values == ["a", "b", "c"]
    assert metadata.enumerated_aliases == ["aඞ", "bඞ", "cඞ"]


@pytest.mark.parametrize(
    "var_name,val_type,value,var_setup,var_assert,is_array",
    [
        (
            "ワークフロー.all_types_コンポーネント.boolIn",
            atvi.VariableType.BOOLEAN,
            ewapi.VariableState(value=atvi.BooleanValue(True), is_valid=True),
            do_bool_setup,
            do_bool_assert,
            False,
        ),
        (
            "ワークフロー.all_types_コンポーネント.realIn",
            atvi.VariableType.REAL,
            ewapi.VariableState(value=atvi.RealValue(1.0), is_valid=True),
            do_real_setup,
            do_real_assert,
            False,
        ),
        (
            "ワークフロー.all_types_コンポーネント.intIn",
            atvi.VariableType.INTEGER,
            ewapi.VariableState(value=atvi.IntegerValue(1), is_valid=True),
            do_int_setup,
            do_int_assert,
            False,
        ),
        (
            "ワークフロー.all_types_コンポーネント.strIn",
            atvi.VariableType.STRING,
            ewapi.VariableState(value=atvi.StringValue("a"), is_valid=True),
            do_string_setup,
            do_string_assert,
            False,
        ),
        (
            "ワークフロー.all_types_コンポーネント.arrays.boolIn",
            atvi.VariableType.BOOLEAN_ARRAY,
            ewapi.VariableState(
                value=atvi.BooleanArrayValue(values=[True, False, True]), is_valid=True
            ),
            do_bool_setup,
            do_bool_assert,
            True,
        ),
        (
            "ワークフロー.all_types_コンポーネント.arrays.realIn",
            atvi.VariableType.REAL_ARRAY,
            ewapi.VariableState(value=atvi.RealArrayValue(values=[1.0, 2.0, 3.0]), is_valid=True),
            do_real_setup,
            do_real_assert,
            True,
        ),
        (
            "ワークフロー.all_types_コンポーネント.arrays.intIn",
            atvi.VariableType.INTEGER_ARRAY,
            ewapi.VariableState(value=atvi.IntegerArrayValue(values=[1, 2, 3]), is_valid=True),
            do_int_setup,
            do_int_assert,
            True,
        ),
        (
            "ワークフロー.all_types_コンポーネント.arrays.strIn",
            atvi.VariableType.STRING_ARRAY,
            ewapi.VariableState(value=atvi.StringArrayValue(values=["a", "b", "c"]), is_valid=True),
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
    value_result: ewapi.VariableState = variable.get_value()

    # Assert
    assert value_result == value
    assert variable.value_type == val_type
    var_assert(variable)


@pytest.mark.workflow_name("multiple_linked_identity.pxcz")
def test_dependents_with_direct_dependents_and_follow_suspended_links(workflow) -> None:
    # Setup
    case = unittest.TestCase()

    # Setup: The variable we'll get_dependents on
    a1: mcapi.IDatapin = workflow.get_variable("Model.Identity1.a")

    # Setup: Variables we expect to be linked to
    # The link between Model.Identity1.a and Model.Identity2.a should be suspended
    expected = [
        workflow.get_variable("Model.Identity2.a"),
        workflow.get_variable("Model.Identity1.b"),
    ]

    # Execute
    result = a1.get_dependents(only_fetch_direct_dependents=True, follow_suspended_links=True)

    # Verify
    case.assertCountEqual(first=result, second=expected)


@pytest.mark.workflow_name("multiple_linked_identity.pxcz")
def test_dependents_with_direct_dependents_and_do_not_follow_suspended_links(workflow) -> None:
    # Setup
    case = unittest.TestCase()

    # Setup: The variable we'll get_dependents on
    a1: mcapi.IDatapin = workflow.get_variable("Model.Identity1.a")

    # Setup: Variables we expect to be linked to.
    # The only variable we expect is Identity1.b since the link between
    #   Identity1.a -> Identity2.a is suspended.
    expected = [workflow.get_variable("Model.Identity1.b")]

    # Execute
    result = a1.get_dependents(only_fetch_direct_dependents=True, follow_suspended_links=False)

    # Verify
    case.assertCountEqual(first=result, second=expected)


@pytest.mark.workflow_name("multiple_linked_identity.pxcz")
def test_dependents_with_recursive_dependents_and_follow_suspended_links(workflow) -> None:
    # Setup
    case = unittest.TestCase()

    # Setup: The variable we'll get_dependents on
    a: mcapi.IDatapin = workflow.get_variable("Model.Identity.a")

    # Setup: Variables we expect to be linked to
    # The link between Model.Identity1.a and Model.Identity2.a should be suspended
    expected = [
        workflow.get_variable("Model.Identity1.a"),
        workflow.get_variable("Model.Identity2.a"),
        workflow.get_variable("Model.Identity3.a"),
        workflow.get_variable("Model.Identity.b"),
        workflow.get_variable("Model.Identity1.b"),
        workflow.get_variable("Model.Identity2.b"),
        workflow.get_variable("Model.Identity3.b"),
    ]

    # Execute
    result = a.get_dependents(only_fetch_direct_dependents=False, follow_suspended_links=True)

    # Verify
    case.assertCountEqual(first=result, second=expected)


@pytest.mark.workflow_name("multiple_linked_identity.pxcz")
def test_dependents_with_recursive_dependents_and_do_not_follow_suspended_links(workflow) -> None:
    # Setup
    case = unittest.TestCase()

    # Setup: The variable we'll get_dependents on
    a: mcapi.IDatapin = workflow.get_variable("Model.Identity.a")

    # Setup: Variables we expect to be linked to.
    # We only expect the 3 variables since the link between
    #   Identity1.a -> Identity2.a is suspended.
    expected = [
        workflow.get_variable("Model.Identity1.a"),
        workflow.get_variable("Model.Identity.b"),
        workflow.get_variable("Model.Identity1.b"),
    ]

    # Execute
    result = a.get_dependents(only_fetch_direct_dependents=False, follow_suspended_links=False)

    # Verify
    case.assertCountEqual(first=result, second=expected)


@pytest.mark.workflow_name("multiple_linked_identity.pxcz")
def test_precedents_with_direct_precedents_and_follow_suspended_links(workflow) -> None:
    # Setup
    case = unittest.TestCase()

    # Setup: The variable we'll get_precedents on
    a2: mcapi.IDatapin = workflow.get_variable("Model.Identity2.a")

    # Setup: Variables we expect to be linked to
    # The link between Model.Identity1.a and Model.Identity2.a should be suspended
    expected = [workflow.get_variable("Model.Identity1.a")]

    # Execute
    result = a2.get_precedents(only_fetch_direct_precedents=True, follow_suspended_links=True)

    # Verify
    case.assertCountEqual(first=result, second=expected)


@pytest.mark.workflow_name("multiple_linked_identity.pxcz")
def test_precedents_with_direct_precedents_and_do_not_follow_suspended_links(workflow) -> None:
    # Setup: The variable we'll get_precedents on
    a2: mcapi.IDatapin = workflow.get_variable("Model.Identity2.a")

    # Execute
    result = a2.get_precedents(only_fetch_direct_precedents=True, follow_suspended_links=False)

    # Verify: We expect no precedents to Model.Identity2.a since the link
    # from Model.Identity1.a and Model.Identity2.a should be suspended
    assert len(result) == 0


@pytest.mark.workflow_name("multiple_linked_identity.pxcz")
def test_precedents_with_recursive_precedents_and_follow_suspended_links(workflow) -> None:
    # Setup
    case = unittest.TestCase()

    # Setup: The variable we'll get_precedents on
    b3: mcapi.IDatapin = workflow.get_variable("Model.Identity3.b")

    # Setup: Variables we expect to be linked to
    # The link between Model.Identity1.a and Model.Identity2.a should be suspended
    expected = [
        workflow.get_variable("Model.Identity3.a"),
        workflow.get_variable("Model.Identity2.a"),
        workflow.get_variable("Model.Identity1.a"),
        workflow.get_variable("Model.Identity.a"),
    ]

    # Execute
    result = b3.get_precedents(only_fetch_direct_precedents=False, follow_suspended_links=True)

    # Verify
    case.assertCountEqual(first=result, second=expected)


@pytest.mark.workflow_name("multiple_linked_identity.pxcz")
def test_precedents_with_recursive_precedents_and_do_not_follow_suspended_links(workflow) -> None:
    # Setup
    case = unittest.TestCase()

    # Setup: The variable we'll get_precedents on
    b3: mcapi.IDatapin = workflow.get_variable("Model.Identity3.b")

    # Setup: Variables we expect to be linked to.
    # We only expect the 2 precedents since the link between
    #   Identity1.a -> Identity2.a is suspended.
    expected = [
        workflow.get_variable("Model.Identity3.a"),
        workflow.get_variable("Model.Identity2.a"),
    ]

    # Execute
    result = b3.get_precedents(only_fetch_direct_precedents=False, follow_suspended_links=False)

    # Verify
    case.assertCountEqual(first=result, second=expected)


def do_file_setup(variable: mcapi.IDatapin, is_array: bool) -> None:
    meta_type = atvi.FileArrayMetadata if is_array else atvi.FileMetadata
    cast = typing.cast(Any, variable)
    metadata = meta_type()
    metadata.description = "fileファイル"
    metadata.custom_metadata["blargඞ"] = atvi.RealValue(0.00000007)
    cast.set_metadata(metadata)


def do_file_assert(variable: mcapi.IDatapin) -> None:
    cast = typing.cast(Any, variable)
    metadata = cast.get_metadata()
    assert metadata.description == "fileファイル"
    assert metadata.custom_metadata["blargඞ"] == atvi.RealValue(0.00000007)


@pytest.mark.parametrize(
    "var_name,val_type,value,var_setup,var_assert,is_array",
    [
        (
            "Model.fileASCIIIn",
            atvi.VariableType.FILE,
            ewapi.VariableState(value=atvi.EMPTY_FILE, is_valid=True),
            do_file_setup,
            do_file_assert,
            False,
        ),
        (
            "Model.fileBinaryIn",
            atvi.VariableType.FILE,
            ewapi.VariableState(value=atvi.EMPTY_FILE, is_valid=True),
            do_file_setup,
            do_file_assert,
            False,
        ),
        (
            "Model.fileArrayASCIIIn",
            atvi.VariableType.FILE_ARRAY,
            ewapi.VariableState(
                value=atvi.FileArrayValue(values=[atvi.EMPTY_FILE, atvi.EMPTY_FILE]), is_valid=True
            ),
            do_file_setup,
            do_file_assert,
            True,
        ),
        (
            "Model.fileArrayBinaryIn",
            atvi.VariableType.FILE_ARRAY,
            ewapi.VariableState(
                value=atvi.FileArrayValue(values=[atvi.EMPTY_FILE, atvi.EMPTY_FILE]), is_valid=True
            ),
            do_file_setup,
            do_file_assert,
            True,
        ),
    ],
)
@pytest.mark.workflow_name("file_tests.pxcz")
def test_can_manipulate_type_specific_file_information(
    workflow, var_name, val_type, value, var_setup, var_assert, is_array
) -> None:
    # Arrange
    variable: mcapi.IDatapin = workflow.get_variable(var_name)
    var_setup(variable, is_array)

    # Act
    # variable.set_value(value)  # TODO: File set not yet implemented
    value_result: ewapi.VariableState = variable.get_value()

    # Assert
    # assert value_result == value
    assert variable.value_type == val_type
    var_assert(variable)


@pytest.mark.workflow_name("file_tests.pxcz")
def test_can_set_scalar_file_value_content(workflow) -> None:
    input_variable: mcapi.IDatapin = workflow.get_variable("Model.fileReader.scalarFileIn")
    with tempfile.TemporaryFile() as temp_file:
        temp_file.write(
            b"This is some temporary file content.\r\n" b"This is some more temporary file content."
        )
        temp_file.flush()
        with atvi.NonManagingFileScope() as file_scope:
            new_value = file_scope.read_from_file(temp_file.name, mime_type=None, encoding=None)
            input_variable.set_value(atvi.VariableState(new_value, True))

            workflow.run()

            string_value = workflow.get_value("Model.fileReader.scalarFileContents").safe_value
            assert (
                string_value == "This is some temporary file content.\r\n"
                "This is some more temporary file content."
            )


@pytest.mark.workflow_name("file_tests.pxcz")
def test_can_set_array_file_value_content(workflow) -> None:
    input_variable: mcapi.IDatapin = workflow.get_variable("Model.fileReader.fileArrayIn")
    with contextlib.ExitStack() as exit_stack:
        temp_files: list = [
            [exit_stack.enter_context(tempfile.TemporaryFile()), None],
            [
                exit_stack.enter_context(tempfile.TemporaryFile()),
                exit_stack.enter_context(tempfile.TemporaryFile()),
            ],
        ]
        temp_files[0][0].write(b"greatest file content in the world in next index")
        temp_files[0][0].flush()
        temp_files[1][0].write(b"this is not the greatest file content in the world")
        temp_files[1][0].flush()
        temp_files[1][1].write(b"this is just a tribute")
        temp_files[1][1].flush()
        with atvi.NonManagingFileScope() as file_scope:
            new_value = atvi.FileArrayValue(
                [2, 2],
                values=[
                    [file_scope.read_from_file(temp_files[0][0].name, None, None), atvi.EMPTY_FILE],
                    [
                        file_scope.read_from_file(temp_files[1][0].name, None, None),
                        file_scope.read_from_file(temp_files[1][1].name, None, None),
                    ],
                ],
            )
            input_variable.set_value(atvi.VariableState(new_value, True))

            workflow.run()

            string_array_value = workflow.get_value("Model.fileReader.fileArrayContents").safe_value
            assert string_array_value == atvi.StringArrayValue(
                [2, 2],
                [
                    ["greatest file content in the world in next index", ""],
                    [
                        "this is not the greatest file content in the world",
                        "this is just a tribute",
                    ],
                ],
            )


def do_ref_setup(variable: mcapi.IDatapin) -> None:
    meta_type = grpcmc.ReferenceDatapinMetadata
    cast = typing.cast(Any, variable)
    metadata = meta_type()
    # reference variables do not support a description
    metadata.custom_metadata["blargඞ"] = atvi.RealValue(0.00000007)
    cast.set_metadata(metadata)


def do_ref_assert(variable: mcapi.IDatapin) -> None:
    cast = typing.cast(Any, variable)
    metadata = cast.get_metadata()
    assert metadata.custom_metadata["blargඞ"] == atvi.RealValue(0.00000007)


@pytest.mark.parametrize(
    "var_name", ["Model.ReferenceScript.doubleInRef", "Model.ReferenceScript.doubleOutRef"]
)
@pytest.mark.workflow_name("reference_tests.pxcz")
def test_can_set_reference_value_and_metadata(workflow, var_name) -> None:
    # Arrange
    variable: mcapi.IDatapin = workflow.get_variable(var_name)
    do_ref_setup(variable)
    new_value = atvi.VariableState(value=atvi.RealValue(2.0), is_valid=True)

    # Act
    variable.set_value(new_value)
    value_result: ewapi.VariableState = variable.get_value()

    # Assert
    assert value_result == new_value
    assert variable.value_type == atvi.VariableType.UNKNOWN
    do_ref_assert(variable)


@pytest.mark.parametrize(
    "var_name",
    ["Model.ReferenceScript.doubleArrayInRef", "Model.ReferenceScript.doubleArrayOutRef"],
)
@pytest.mark.workflow_name("reference_tests.pxcz")
def test_can_set_reference_array_element_value_and_metadata(workflow, var_name) -> None:
    # Arrange
    variable: mcapi.IReferenceArrayDatapin = workflow.get_variable(var_name)
    do_ref_setup(variable)
    new_value = atvi.VariableState(value=atvi.RealValue(2.0), is_valid=True)

    # Act
    variable[0].set_value(new_value)
    value_result: ewapi.VariableState = variable.get_value()

    # Assert
    assert value_result.value[0] == new_value.value
    assert variable.value_type == atvi.VariableType.UNKNOWN
    do_ref_assert(variable)


@pytest.mark.parametrize(
    "index",
    [99, -1],
)
@pytest.mark.workflow_name("reference_tests.pxcz")
def test_setting_reference_array_element_value_at_out_of_bounds_index_gives_good_error(
    workflow, index
) -> None:
    # Arrange
    variable: mcapi.IReferenceArrayDatapin = workflow.get_variable(
        "Model.ReferenceScript.doubleArrayInRef"
    )
    do_ref_setup(variable)
    new_value = atvi.VariableState(value=atvi.RealValue(2.0), is_valid=True)

    # Act and assert
    with pytest.raises(
        ewapi.ValueOutOfRangeError, match="The requested index is outside the bounds of the array."
    ):
        variable[index].set_value(new_value)


@pytest.mark.parametrize(
    "index",
    [99, -1],
)
@pytest.mark.workflow_name("reference_tests.pxcz")
def test_getting_reference_array_element_value_at_out_of_bounds_index_gives_good_error(
    workflow, index
) -> None:
    # Arrange
    variable: mcapi.IReferenceArrayDatapin = workflow.get_variable(
        "Model.ReferenceScript.doubleArrayInRef"
    )
    do_ref_setup(variable)
    new_value = atvi.VariableState(value=atvi.RealValue(2.0), is_valid=True)

    # Act
    variable[0].set_value(new_value)

    # Assert
    with pytest.raises(
        ewapi.ValueOutOfRangeError, match="The requested index is outside the bounds of the array."
    ):
        variable[index].get_value()


@pytest.mark.parametrize(
    "var_name",
    ["Model.ReferenceScript.doubleArrayInRef", "Model.ReferenceScript.doubleArrayOutRef"],
)
@pytest.mark.workflow_name("reference_tests.pxcz")
def test_can_set_reference_array_value_and_metadata(workflow, var_name) -> None:
    # Arrange
    variable: mcapi.IDatapin = workflow.get_variable(var_name)
    do_ref_setup(variable)
    new_value = atvi.VariableState(
        value=atvi.RealArrayValue(values=[2.0, 3.0, 4.0, 5.0]), is_valid=False
    )

    # Act
    variable.set_value(new_value)
    value_result: ewapi.VariableState = variable.get_value()
    length = len(variable)

    # Assert
    assert value_result == new_value
    assert variable.value_type == atvi.VariableType.UNKNOWN
    assert length == 4
    do_ref_assert(variable)


@pytest.mark.workflow_name("reference_tests.pxcz")
def test_getting_non_double_reference_array_values_gets_nan(workflow) -> None:
    # Arrange
    variable: mcapi.IDatapin = workflow.get_variable("Model.ReferenceScript.intArrayInRef")

    # Act
    value_result: ewapi.VariableState = variable.get_value()

    # Assert
    assert numpy.array_equal(
        value_result.value,
        atvi.RealArrayValue(values=[numpy.NAN, numpy.NAN, numpy.NAN, numpy.NAN]),
        equal_nan=True,
    )


@pytest.mark.parametrize(
    "index",
    [99, -1],
)
@pytest.mark.workflow_name("reference_tests.pxcz")
def test_getting_the_reference_directness_with_an_out_of_bounds_index_returns_a_good_error(
    workflow, index
) -> None:
    # Arrange
    variable: mcapi.IReferenceArrayDatapin = workflow.get_variable(
        "Model.ReferenceScript.doubleArrayInRef"
    )
    do_ref_setup(variable)
    new_value = atvi.VariableState(value=atvi.RealValue(2.0), is_valid=True)

    # Act and assert
    with pytest.raises(
        ewapi.ValueOutOfRangeError, match="The requested index is outside the bounds of the array."
    ):
        result = variable[index].is_direct


@pytest.mark.parametrize(
    "index",
    [99, -1],
)
@pytest.mark.workflow_name("reference_tests.pxcz")
def test_getting_the_reference_equation_with_an_out_of_bounds_index_returns_a_good_error(
    workflow, index
) -> None:
    # Arrange
    variable: mcapi.IReferenceArrayDatapin = workflow.get_variable(
        "Model.ReferenceScript.doubleArrayInRef"
    )
    do_ref_setup(variable)
    new_value = atvi.VariableState(value=atvi.RealValue(2.0), is_valid=True)

    # Act and assert
    with pytest.raises(
        ewapi.ValueOutOfRangeError, match="The requested index is outside the bounds of the array."
    ):
        result = variable[index].equation


@pytest.mark.parametrize(
    "index",
    [99, -1],
)
@pytest.mark.workflow_name("reference_tests.pxcz")
def test_setting_the_reference_equation_with_an_out_of_bounds_index_returns_a_good_error(
    workflow, index
) -> None:
    # Arrange
    variable: mcapi.IReferenceArrayDatapin = workflow.get_variable(
        "Model.ReferenceScript.doubleArrayInRef"
    )
    do_ref_setup(variable)
    new_value = atvi.VariableState(value=atvi.RealValue(2.0), is_valid=True)

    # Act and assert
    with pytest.raises(
        ewapi.ValueOutOfRangeError, match="The requested index is outside the bounds of the array."
    ):
        variable[index].equation = "ඞ"
