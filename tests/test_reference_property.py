from os import PathLike
from typing import Optional
from unittest.mock import MagicMock

import ansys.api.modelcenter.v0.element_messages_pb2 as elem_msgs
import ansys.api.modelcenter.v0.variable_value_messages_pb2 as var_msgs
import ansys.tools.variableinterop as atvi
import pytest

import ansys.modelcenter.workflow.grpc_modelcenter as grpcmc
from ansys.modelcenter.workflow.grpc_modelcenter import ValueTypeNotSupportedError
from ansys.modelcenter.workflow.grpc_modelcenter.reference_property import (
    ReferenceArrayProperty,
    ReferenceProperty,
    ReferencePropertyBase,
)

from .grpc_server_test_utils.client_creation_monkeypatch import monkeypatch_client_creation
from .grpc_server_test_utils.mock_file_value import MockFileValue


@pytest.mark.parametrize(
    "value",
    [True, False],
)
def test_get_is_input(monkeypatch, engine, value) -> None:
    # Arrange: gRPC client
    mock_client = MagicMock()
    mock_response = var_msgs.ReferencePropertyGetIsInputResponse(is_input=value)
    mock_client.ReferencePropertyGetIsInput.return_value = mock_response
    monkeypatch_client_creation(monkeypatch, ReferenceProperty, mock_client)

    # Arrange: SUT
    sut_id = elem_msgs.ElementId(id_string="VAR_UNDER_TEST_ID")
    sut_name = "Bob"
    sut = grpcmc.ReferenceProperty(element_id=sut_id, name=sut_name, engine=engine)

    # Act
    is_input: bool = sut.is_input

    # Assert
    expected_request = var_msgs.ReferencePropertyIdentifier(
        reference_var=sut_id, prop_name=sut_name
    )
    mock_client.ReferencePropertyGetIsInput.assert_called_once_with(expected_request)
    assert is_input == value


# Test data for get_value tests
get_value_test_data = [
    (
        var_msgs.VariableValue(double_value=-867.5309),
        True,
        atvi.VariableState(atvi.RealValue(-867.5309), True),
    ),
    (
        var_msgs.VariableValue(
            double_array_value=var_msgs.DoubleArrayValue(
                dims=var_msgs.ArrayDimensions(dims=[2, 2]), values=[1.0, 1.1, 2.0, 2.1]
            )
        ),
        False,
        atvi.VariableState(
            atvi.RealArrayValue(shape_=(2, 2), values=[[1.0, 1.1], [2.0, 2.1]]), False
        ),
    ),
    (
        var_msgs.VariableValue(bool_value=True),
        False,
        atvi.VariableState(atvi.BooleanValue(True), False),
    ),
    (
        var_msgs.VariableValue(
            bool_array_value=var_msgs.BooleanArrayValue(
                dims=var_msgs.ArrayDimensions(dims=[2, 2]), values=[True, False, False, True]
            )
        ),
        True,
        atvi.VariableState(
            atvi.BooleanArrayValue(shape_=(2, 2), values=[[True, False], [False, True]]), True
        ),
    ),
    (
        var_msgs.VariableValue(int_value=47),
        True,
        atvi.VariableState(atvi.IntegerValue(47), True),
    ),
    (
        var_msgs.VariableValue(
            int_array_value=var_msgs.IntegerArrayValue(
                dims=var_msgs.ArrayDimensions(dims=[2, 2]), values=[-8675309, 47, -1, 0]
            )
        ),
        False,
        atvi.VariableState(
            atvi.IntegerArrayValue(shape_=(2, 2), values=[[-8675309, 47], [-1, 0]]), False
        ),
    ),
    (
        var_msgs.VariableValue(string_value="(╯°□°）╯︵ ┻━┻"),
        True,
        atvi.VariableState(atvi.StringValue("(╯°□°）╯︵ ┻━┻"), True),
    ),
    (
        var_msgs.VariableValue(
            string_array_value=var_msgs.StringArrayValue(
                dims=var_msgs.ArrayDimensions(dims=[2, 2]),
                values=["primary", "secondary", "first", "second"],
            )
        ),
        False,
        atvi.VariableState(
            atvi.StringArrayValue(
                shape_=(2, 2), values=[["primary", "secondary"], ["first", "second"]]
            ),
            False,
        ),
    ),
    (
        var_msgs.VariableValue(file_value=var_msgs.FileValue()),
        True,
        atvi.VariableState(MockFileValue(""), True),
    ),
    (
        var_msgs.VariableValue(
            file_array_value=var_msgs.FileArrayValue(
                dims=var_msgs.ArrayDimensions(dims=[2, 2]),
                values=[
                    var_msgs.FileValue(),
                    var_msgs.FileValue(),
                    var_msgs.FileValue(),
                    var_msgs.FileValue(),
                ],
            )
        ),
        False,
        atvi.VariableState(
            atvi.FileArrayValue(
                shape_=(2, 2),
                values=[
                    [MockFileValue(""), MockFileValue("")],
                    [MockFileValue(""), MockFileValue("")],
                ],
            ),
            False,
        ),
    ),
]


@pytest.mark.parametrize("variable_value,is_valid,expected_result", get_value_test_data)
def test_reference_property_get_state(
    monkeypatch, engine, variable_value, is_valid, expected_result
) -> None:
    # Arrange: Mock file setup
    def mock_read(self, to_read: PathLike, mime_type: Optional[str], encoding: Optional[str]):
        return MockFileValue(str(to_read))

    monkeypatch.setattr(atvi.NonManagingFileScope, "read_from_file", mock_read)

    # Arrange: gRPC client
    mock_client = MagicMock()
    mock_response = var_msgs.VariableState(value=variable_value, is_valid=is_valid)
    monkeypatch_client_creation(monkeypatch, ReferenceProperty, mock_client)
    mock_client.ReferencePropertyGetValue.return_value = mock_response

    # Arrange: SUT
    sut_id = elem_msgs.ElementId(id_string="VAR_UNDER_TEST_ID")
    sut_name = "Bob"
    sut = grpcmc.ReferenceProperty(element_id=sut_id, name=sut_name, engine=engine)

    # Act
    result: atvi.VariableState = sut.get_state()

    # Assert
    expected_target = var_msgs.ReferencePropertyIdentifier(reference_var=sut_id, prop_name=sut_name)
    expected_request = var_msgs.IndexedReferencePropertyIdentifier(target_prop=expected_target)
    mock_client.ReferencePropertyGetValue.assert_called_once_with(expected_request)

    assert result.value == expected_result.value
    assert result.is_valid == expected_result.is_valid


@pytest.mark.parametrize("variable_value,is_valid,expected_result", get_value_test_data)
def test_reference_array_property_get_state_at(
    monkeypatch, engine, variable_value, is_valid, expected_result
):
    # Arrange: Mock file setup
    def mock_read(self, to_read: PathLike, mime_type: Optional[str], encoding: Optional[str]):
        return MockFileValue(str(to_read))

    monkeypatch.setattr(atvi.NonManagingFileScope, "read_from_file", mock_read)

    # Arrange: gRPC client
    mock_client = MagicMock()
    mock_response = var_msgs.VariableState(value=variable_value, is_valid=is_valid)
    monkeypatch_client_creation(monkeypatch, ReferenceArrayProperty, mock_client)
    mock_client.ReferencePropertyGetValue.return_value = mock_response

    # Arrange: SUT
    sut_id = elem_msgs.ElementId(id_string="VAR_UNDER_TEST_ID")
    sut_name = "Bob"
    sut = grpcmc.ReferenceArrayProperty(element_id=sut_id, name=sut_name, engine=engine)

    test_index = 5

    # Act
    result: atvi.VariableState = sut.get_state_at(test_index)

    # Assert
    expected_target = var_msgs.ReferencePropertyIdentifier(reference_var=sut_id, prop_name=sut_name)
    expected_request = var_msgs.IndexedReferencePropertyIdentifier(
        target_prop=expected_target, index=test_index
    )
    mock_client.ReferencePropertyGetValue.assert_called_once_with(expected_request)

    assert result.value == expected_result.value
    assert result.is_valid == expected_result.is_valid


# Test data for set_value tests.
set_value_test_data = [
    (atvi.BooleanValue(True), var_msgs.VariableValue(bool_value=True)),
    (atvi.RealValue(4.7), var_msgs.VariableValue(double_value=4.7)),
    (atvi.IntegerValue(47), var_msgs.VariableValue(int_value=47)),
    (
        atvi.StringValue("This is a test string value."),
        var_msgs.VariableValue(string_value="This is a test string value."),
    ),
    (atvi.StringValue("(╯°□°）╯︵ ┻━┻"), var_msgs.VariableValue(string_value="(╯°□°）╯︵ ┻━┻")),
    (
        atvi.BooleanArrayValue(shape_=(2, 2), values=[[True, False], [False, True]]),
        var_msgs.VariableValue(
            bool_array_value=var_msgs.BooleanArrayValue(
                dims=var_msgs.ArrayDimensions(dims=[2, 2]), values=[True, False, False, True]
            )
        ),
    ),
    (
        atvi.RealArrayValue(shape_=(2, 2), values=[[1.0, 1.1], [2.0, 2.1]]),
        var_msgs.VariableValue(
            double_array_value=var_msgs.DoubleArrayValue(
                dims=var_msgs.ArrayDimensions(dims=[2, 2]), values=[1.0, 1.1, 2.0, 2.1]
            )
        ),
    ),
    (
        atvi.IntegerArrayValue(shape_=(2, 2), values=[[-8675309, 47], [-1, 0]]),
        var_msgs.VariableValue(
            int_array_value=var_msgs.IntegerArrayValue(
                dims=var_msgs.ArrayDimensions(dims=[2, 2]), values=[-8675309, 47, -1, 0]
            )
        ),
    ),
    (
        atvi.StringArrayValue(
            shape_=(2, 2), values=[["primary", "secondary"], ["first", "second"]]
        ),
        var_msgs.VariableValue(
            string_array_value=var_msgs.StringArrayValue(
                dims=var_msgs.ArrayDimensions(dims=[2, 2]),
                values=["primary", "secondary", "first", "second"],
            )
        ),
    ),
]


@pytest.mark.parametrize("set_value,expected_value_in_request", set_value_test_data)
def test_reference_property_set_value(monkeypatch, engine, set_value, expected_value_in_request):
    # Arrange: gRPC client
    mock_client = MagicMock()
    monkeypatch_client_creation(monkeypatch, ReferenceProperty, mock_client)

    # Arrange: SUT
    sut_id = elem_msgs.ElementId(id_string="VAR_UNDER_TEST_ID")
    sut_name = "Bob"
    sut = grpcmc.ReferenceProperty(element_id=sut_id, name=sut_name, engine=engine)

    new_value = atvi.VariableState(set_value, True)

    # Act
    sut.set_value(new_value=new_value)

    # Assert
    expected_target = var_msgs.IndexedReferencePropertyIdentifier(
        target_prop=var_msgs.ReferencePropertyIdentifier(reference_var=sut_id, prop_name=sut_name)
    )
    expected_request = var_msgs.ReferencePropertySetValueRequest(
        target_prop=expected_target, new_value=expected_value_in_request
    )
    mock_client.ReferencePropertySetValue.assert_called_once_with(expected_request)


@pytest.mark.parametrize("set_value,expected_value_in_request", set_value_test_data)
def test_set_value_at(monkeypatch, engine, set_value, expected_value_in_request):
    # Arrange: gRPC client
    mock_client = MagicMock()
    monkeypatch_client_creation(monkeypatch, ReferenceArrayProperty, mock_client)

    # Arrange: SUT
    sut_id = elem_msgs.ElementId(id_string="VAR_UNDER_TEST_ID")
    sut_name = "Bob"
    sut = grpcmc.ReferenceArrayProperty(element_id=sut_id, name=sut_name, engine=engine)

    new_value = atvi.VariableState(set_value, True)
    test_index = 5

    # Act
    sut.set_value_at(test_index, new_value=new_value)

    # Assert
    expected_target = var_msgs.IndexedReferencePropertyIdentifier(
        target_prop=var_msgs.ReferencePropertyIdentifier(reference_var=sut_id, prop_name=sut_name),
        index=test_index,
    )
    expected_request = var_msgs.ReferencePropertySetValueRequest(
        target_prop=expected_target, new_value=expected_value_in_request
    )
    mock_client.ReferencePropertySetValue.assert_called_once_with(expected_request)


# Test data for set_value not supported tests.
set_value_not_supported_test_data = [
    atvi.FileArrayValue(
        shape_=(2, 2),
        values=[
            [MockFileValue(""), MockFileValue("")],
            [MockFileValue(""), MockFileValue("")],
        ],
    ),
    MockFileValue(""),
]


@pytest.mark.parametrize("set_value", set_value_not_supported_test_data)
def test_reference_property_set_value_not_supported(monkeypatch, engine, set_value):
    # Arrange: gRPC client
    mock_client = MagicMock()
    monkeypatch_client_creation(monkeypatch, ReferenceProperty, mock_client)

    # Arrange: SUT
    sut_id = elem_msgs.ElementId(id_string="VAR_UNDER_TEST_ID")
    sut_name = "Bob"
    sut = grpcmc.ReferenceProperty(element_id=sut_id, name=sut_name, engine=engine)

    new_value = atvi.VariableState(set_value, True)

    # Act/Assert
    with pytest.raises(ValueTypeNotSupportedError):
        sut.set_value(new_value=new_value)

    mock_client.ReferencePropertySetValue.assert_not_called()


@pytest.mark.parametrize("set_value", set_value_not_supported_test_data)
def test_set_value_at_not_supported(monkeypatch, engine, set_value):
    # Arrange: gRPC client
    mock_client = MagicMock()
    monkeypatch_client_creation(monkeypatch, ReferenceArrayProperty, mock_client)

    # Arrange: SUT
    sut_id = elem_msgs.ElementId(id_string="VAR_UNDER_TEST_ID")
    sut_name = "Bob"
    sut = grpcmc.ReferenceArrayProperty(element_id=sut_id, name=sut_name, engine=engine)

    new_value = atvi.VariableState(set_value, True)
    test_index = 5

    # Act/Assert
    with pytest.raises(ValueTypeNotSupportedError):
        sut.set_value_at(new_value=new_value, index=test_index)

    mock_client.ReferencePropertySetValue.assert_not_called()


def test_cannot_instantiate_reference_property_base(engine):
    # Act/Assert
    with pytest.raises(TypeError, match="Can't instantiate abstract class ReferencePropertyBase"):
        ReferencePropertyBase(
            element_id=elem_msgs.ElementId(id_string="VAR_UNDER_TEST_ID"), name="Bob", engine=engine
        )


# Test data for get_metadata tests
get_metadata_test_data = [
    pytest.param(
        var_msgs.VariableMetadata(
            int_metadata=var_msgs.IntegerVariableMetadata(
                base_metadata=var_msgs.BaseVariableMetadata(description="int_var_metadata")
            )
        ),
        atvi.IntegerMetadata,
        "int_var_metadata",
        id="int",
    ),
    pytest.param(
        var_msgs.VariableMetadata(
            double_metadata=var_msgs.DoubleVariableMetadata(
                base_metadata=var_msgs.BaseVariableMetadata(description="double_var_metadata")
            )
        ),
        atvi.RealMetadata,
        "double_var_metadata",
        id="double",
    ),
    pytest.param(
        var_msgs.VariableMetadata(
            bool_metadata=var_msgs.BooleanVariableMetadata(
                base_metadata=var_msgs.BaseVariableMetadata(description="bool_var_metadata")
            )
        ),
        atvi.BooleanMetadata,
        "bool_var_metadata",
        id="bool",
    ),
    pytest.param(
        var_msgs.VariableMetadata(
            string_metadata=var_msgs.StringVariableMetadata(
                base_metadata=var_msgs.BaseVariableMetadata(description="string_var_metadata")
            )
        ),
        atvi.StringMetadata,
        "string_var_metadata",
        id="string",
    ),
    pytest.param(
        var_msgs.VariableMetadata(
            file_metadata=var_msgs.FileVariableMetadata(
                base_metadata=var_msgs.BaseVariableMetadata(description="file_var_metadata")
            )
        ),
        atvi.FileMetadata,
        "file_var_metadata",
        id="file",
    ),
]


@pytest.mark.parametrize("mock_response,expected_result_type,description", get_metadata_test_data)
def test_reference_property_get_metadata(
    monkeypatch, engine, mock_response, expected_result_type, description
):
    # Arrange: gRPC client
    mock_client = MagicMock()
    mock_client.ReferencePropertyGetMetadata.return_value = mock_response
    monkeypatch_client_creation(monkeypatch, ReferenceProperty, mock_client)

    # Arrange: SUT
    sut_id = elem_msgs.ElementId(id_string="VAR_UNDER_TEST_ID")
    sut_name = "Bob"
    sut = grpcmc.ReferenceProperty(element_id=sut_id, name=sut_name, engine=engine)

    # Act
    result: atvi.CommonVariableMetadata = sut.get_metadata()

    # Assert: Correct grpc call
    expected_request = var_msgs.ReferencePropertyIdentifier(
        reference_var=sut_id, prop_name=sut_name
    )
    mock_client.ReferencePropertyGetMetadata.assert_called_once_with(expected_request)

    # Assert: Result is properly converted
    assert type(result) == expected_result_type
    assert result.description == description


@pytest.mark.parametrize("mock_response,expected_result_type,description", get_metadata_test_data)
def test_reference_array_property_get_metadata(
    monkeypatch, engine, mock_response, expected_result_type, description
):
    # Arrange: gRPC client
    mock_client = MagicMock()
    mock_client.ReferencePropertyGetMetadata.return_value = mock_response
    monkeypatch_client_creation(monkeypatch, ReferenceArrayProperty, mock_client)

    # Arrange: SUT
    sut_id = elem_msgs.ElementId(id_string="VAR_UNDER_TEST_ID")
    sut_name = "Bob"
    sut = grpcmc.ReferenceArrayProperty(element_id=sut_id, name=sut_name, engine=engine)

    # Act
    result: atvi.CommonVariableMetadata = sut.get_metadata()

    # Assert: Correct grpc call
    expected_request = var_msgs.ReferencePropertyIdentifier(
        reference_var=sut_id, prop_name=sut_name
    )
    mock_client.ReferencePropertyGetMetadata.assert_called_once_with(expected_request)

    # Assert: Result is properly converted
    assert type(result) == expected_result_type
    assert result.description == description


# Test data for get_type
get_type_test_data = [
    pytest.param(var_msgs.VARIABLE_TYPE_UNSPECIFIED, atvi.VariableType.UNKNOWN, id="unknown"),
    pytest.param(var_msgs.VARIABLE_TYPE_REAL, atvi.VariableType.REAL, id="real"),
    pytest.param(var_msgs.VARIABLE_TYPE_REAL_ARRAY, atvi.VariableType.REAL_ARRAY, id="real_arr"),
    pytest.param(var_msgs.VARIABLE_TYPE_INTEGER, atvi.VariableType.INTEGER, id="int"),
    pytest.param(
        var_msgs.VARIABLE_TYPE_INTEGER_ARRAY, atvi.VariableType.INTEGER_ARRAY, id="int_arr"
    ),
    pytest.param(var_msgs.VARIABLE_TYPE_BOOLEAN, atvi.VariableType.BOOLEAN, id="bool"),
    pytest.param(
        var_msgs.VARIABLE_TYPE_BOOLEAN_ARRAY, atvi.VariableType.BOOLEAN_ARRAY, id="bool_arr"
    ),
    pytest.param(var_msgs.VARIABLE_TYPE_STRING, atvi.VariableType.STRING, id="string"),
    pytest.param(
        var_msgs.VARIABLE_TYPE_STRING_ARRAY, atvi.VariableType.STRING_ARRAY, id="string_arr"
    ),
    pytest.param(var_msgs.VARIABLE_TYPE_FILE, atvi.VariableType.FILE, id="file"),
    pytest.param(var_msgs.VARIABLE_TYPE_FILE_ARRAY, atvi.VariableType.FILE_ARRAY, id="file_arr"),
    pytest.param(var_msgs.VARIABLE_TYPE_REFERENCE, atvi.VariableType.UNKNOWN, id="reference"),
    pytest.param(
        var_msgs.VARIABLE_TYPE_REFERENCE_ARRAY, atvi.VariableType.UNKNOWN, id="reference_arr"
    ),
]


@pytest.mark.parametrize("mock_response,expected_result", get_type_test_data)
def test_reference_property_get_type(monkeypatch, engine, mock_response, expected_result):
    # Arrange: gRPC client
    mock_client = MagicMock()
    mock_client.ReferencePropertyGetType.return_value = var_msgs.ReferencePropertyGetTypeResponse(
        type=mock_response
    )
    monkeypatch_client_creation(monkeypatch, ReferenceProperty, mock_client)

    # Arrange: SUT
    sut_id = elem_msgs.ElementId(id_string="VAR_UNDER_TEST_ID")
    sut_name = "Bob"
    sut = grpcmc.ReferenceProperty(element_id=sut_id, name=sut_name, engine=engine)

    # Act
    result: atvi.VariableType = sut.get_value_type()

    # Assert: Correct grpc call
    expected_request = var_msgs.ReferencePropertyIdentifier(
        reference_var=sut_id, prop_name=sut_name
    )
    mock_client.ReferencePropertyGetType.assert_called_once_with(expected_request)

    # Assert: Result is properly converted
    assert result == expected_result


@pytest.mark.parametrize("mock_response,expected_result", get_type_test_data)
def test_reference_array_property_get_type(monkeypatch, engine, mock_response, expected_result):
    # Arrange: gRPC client
    mock_client = MagicMock()
    mock_client.ReferencePropertyGetType.return_value = var_msgs.ReferencePropertyGetTypeResponse(
        type=mock_response
    )
    monkeypatch_client_creation(monkeypatch, ReferenceArrayProperty, mock_client)

    # Arrange: SUT
    sut_id = elem_msgs.ElementId(id_string="VAR_UNDER_TEST_ID")
    sut_name = "Bob"
    sut = grpcmc.ReferenceArrayProperty(element_id=sut_id, name=sut_name, engine=engine)

    # Act
    result: atvi.VariableType = sut.get_value_type()

    # Assert: Correct grpc call
    expected_request = var_msgs.ReferencePropertyIdentifier(
        reference_var=sut_id, prop_name=sut_name
    )
    mock_client.ReferencePropertyGetType.assert_called_once_with(expected_request)

    # Assert: Result is properly converted
    assert result == expected_result
