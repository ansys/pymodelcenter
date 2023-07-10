from os import PathLike
from typing import Optional
from unittest.mock import MagicMock

import ansys.tools.variableinterop as atvi
import pytest

import ansys.modelcenter.workflow.grpc_modelcenter as grpcmc
from ansys.modelcenter.workflow.grpc_modelcenter import ValueTypeNotSupportedError
import ansys.modelcenter.workflow.grpc_modelcenter.proto.element_messages_pb2 as elem_msgs
import ansys.modelcenter.workflow.grpc_modelcenter.proto.variable_value_messages_pb2 as var_msgs
from ansys.modelcenter.workflow.grpc_modelcenter.reference_property import ReferenceProperty

from .grpc_server_test_utils.client_creation_monkeypatch import monkeypatch_client_creation
from .grpc_server_test_utils.mock_file_value import MockFileValue


def test_get_is_input(monkeypatch, engine) -> None:
    # Arrange: gRPC client
    mock_client = MagicMock()
    mock_response = var_msgs.ReferencePropertyGetIsInputResponse(is_input=True)
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
    assert is_input is True


def test_set_is_input(monkeypatch, engine) -> None:
    # Arrange: gRPC client
    mock_client = MagicMock()
    mock_response = var_msgs.ReferencePropertyGetIsInputResponse(is_input=True)
    mock_client.ReferencePropertySetIsInput.return_value = mock_response
    monkeypatch_client_creation(monkeypatch, ReferenceProperty, mock_client)

    # Arrange: SUT
    sut_id = elem_msgs.ElementId(id_string="VAR_UNDER_TEST_ID")
    sut_name = "Bob"
    sut = grpcmc.ReferenceProperty(element_id=sut_id, name=sut_name, engine=engine)

    # Act
    sut.is_input = True

    # Assert
    expected_target = var_msgs.ReferencePropertyIdentifier(reference_var=sut_id, prop_name=sut_name)
    expected_request = var_msgs.ReferencePropertySetIsInputRequest(
        target=expected_target, new_value=True
    )
    mock_client.ReferencePropertySetIsInput.assert_called_once_with(expected_request)


# Test data for get_value tests
get_value_test_data = [
    pytest.param(
        var_msgs.VariableValue(double_value=-867.5309),
        True,
        atvi.VariableState(atvi.RealValue(-867.5309), True),
        id="double"
    ),
    pytest.param(
        var_msgs.VariableValue(
            double_array_value=var_msgs.DoubleArrayValue(
                dims=var_msgs.ArrayDimensions(dims=[2, 2]), values=[1.0, 1.1, 2.0, 2.1]
            )
        ),
        False,
        atvi.VariableState(
            atvi.RealArrayValue(shape_=(2, 2), values=[[1.0, 1.1], [2.0, 2.1]]), False
        ),
        id="double_array"
    ),
    pytest.param(
        var_msgs.VariableValue(bool_value=True),
        False,
        atvi.VariableState(atvi.BooleanValue(True), False),
        id="boolean"
    ),
    pytest.param(
        var_msgs.VariableValue(
            bool_array_value=var_msgs.BooleanArrayValue(
                dims=var_msgs.ArrayDimensions(dims=[2, 2]), values=[True, False, False, True]
            )
        ),
        True,
        atvi.VariableState(
            atvi.BooleanArrayValue(shape_=(2, 2), values=[[True, False], [False, True]]), True
        ),
        id="boolean_array"
    ),
    pytest.param(
        var_msgs.VariableValue(int_value=47),
        True,
        atvi.VariableState(atvi.IntegerValue(47), True),
        id="int"
    ),
    pytest.param(
        var_msgs.VariableValue(
            int_array_value=var_msgs.IntegerArrayValue(
                dims=var_msgs.ArrayDimensions(dims=[2, 2]), values=[-8675309, 47, -1, 0]
            )
        ),
        False,
        atvi.VariableState(
            atvi.IntegerArrayValue(shape_=(2, 2), values=[[-8675309, 47], [-1, 0]]), False
        ),
        id="int_array"
    ),
    pytest.param(
        var_msgs.VariableValue(string_value="(╯°□°）╯︵ ┻━┻"),
        True,
        atvi.VariableState(atvi.StringValue("(╯°□°）╯︵ ┻━┻"), True),
        id="string"
    ),
    pytest.param(
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
        id="string_array"
    ),
    pytest.param(
        var_msgs.VariableValue(file_value=var_msgs.FileValue()),
        True,
        atvi.VariableState(MockFileValue(""), True),
        id="file"
    ),
    pytest.param(
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
        id="file_array"
    ),
]


@pytest.mark.parametrize("variable_value,is_valid,expected_result", get_value_test_data)
def test_reference_property_get_state(
    monkeypatch, engine, variable_value, is_valid, expected_result
) -> None:
    # Arrange: Setup client/mocks
    mock_client = get_value_setup(monkeypatch, variable_value, is_valid)

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
def test_reference_array_property_get_state(
    monkeypatch, engine, variable_value, is_valid, expected_result
) -> None:
    # Arrange: Setup client/mocks
    mock_client = get_value_setup(monkeypatch, variable_value, is_valid)

    # Arrange: SUT
    sut_id = elem_msgs.ElementId(id_string="VAR_UNDER_TEST_ID")
    sut_name = "Bob"
    sut = grpcmc.ReferenceArrayProperty(element_id=sut_id, name=sut_name, engine=engine)

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
    # Arrange: Setup client/mocks
    mock_client = get_value_setup(monkeypatch, variable_value, is_valid)

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


def get_value_setup(monkeypatch, variable_value, is_valid):
    """Set up the client and mocks for get_value tests."""
    # Arrange: Mock file setup
    def mock_read(self, to_read: PathLike, mime_type: Optional[str], encoding: Optional[str]):
        return MockFileValue(str(to_read))

    monkeypatch.setattr(atvi.NonManagingFileScope, "read_from_file", mock_read)

    # Arrange: gRPC client
    mock_client = MagicMock()
    mock_response = var_msgs.VariableState(value=variable_value, is_valid=is_valid)
    mock_client.ReferencePropertyGetValue.return_value = mock_response
    monkeypatch_client_creation(monkeypatch, ReferenceProperty, mock_client)
    return mock_client


# Test data for set_value tests.
set_value_test_data = [
    pytest.param(
        atvi.BooleanValue(True), var_msgs.VariableValue(bool_value=True), id="boolean"
    ),
    pytest.param(
        atvi.RealValue(4.7), var_msgs.VariableValue(double_value=4.7), id="double"
    ),
    pytest.param(
        atvi.IntegerValue(47), var_msgs.VariableValue(int_value=47), id="int"
    ),
    pytest.param(
        atvi.StringValue("This is a test string value."),
        var_msgs.VariableValue(string_value="This is a test string value."),
        id="string"
    ),
    pytest.param(
        atvi.StringValue("(╯°□°）╯︵ ┻━┻"),
        var_msgs.VariableValue(string_value="(╯°□°）╯︵ ┻━┻"),
        id="string_unicode"
    )
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
def test_reference_array_property_set_value(
    monkeypatch, engine, set_value, expected_value_in_request
):
    # Arrange: gRPC client
    mock_client = MagicMock()
    monkeypatch_client_creation(monkeypatch, ReferenceProperty, mock_client)

    # Arrange: SUT
    sut_id = elem_msgs.ElementId(id_string="VAR_UNDER_TEST_ID")
    sut_name = "Bob"
    sut = grpcmc.ReferenceArrayProperty(element_id=sut_id, name=sut_name, engine=engine)

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
    monkeypatch_client_creation(monkeypatch, ReferenceProperty, mock_client)

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
    pytest.param(
        atvi.BooleanArrayValue(shape_=(2, 2), values=[[True, False], [False, True]]), id="boolean_array"
    ),
    pytest.param(
        atvi.RealArrayValue(shape_=(2, 2), values=[[1.0, 1.1], [2.0, 2.1]]), id="real_array"
    ),
    pytest.param(
        atvi.IntegerArrayValue(shape_=(2, 2), values=[[-8675309, 47], [-1, 0]]), id="int_array",
    ),
    pytest.param(
        atvi.StringArrayValue(
            shape_=(2, 2), values=[["primary", "secondary"], ["first", "second"]]
        ),
        id="string_array"
    ),
    pytest.param(
        atvi.FileArrayValue(
            shape_=(2, 2),
            values=[
                [MockFileValue(""), MockFileValue("")],
                [MockFileValue(""), MockFileValue("")],
            ],
        ),
        id="file_array"
    ),
    pytest.param(
        MockFileValue(""), id="file"
    )
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
    with pytest.raises(TypeError, match="Cannot set the value of reference property to a type of"):
        sut.set_value(new_value=new_value)

    mock_client.ReferencePropertySetValue.assert_not_called()


@pytest.mark.parametrize("set_value", set_value_not_supported_test_data)
def test_reference_array_property_set_value_not_supported(monkeypatch, engine, set_value):
    # Arrange: gRPC client
    mock_client = MagicMock()
    monkeypatch_client_creation(monkeypatch, ReferenceProperty, mock_client)

    # Arrange: SUT
    sut_id = elem_msgs.ElementId(id_string="VAR_UNDER_TEST_ID")
    sut_name = "Bob"
    sut = grpcmc.ReferenceArrayProperty(element_id=sut_id, name=sut_name, engine=engine)

    new_value = atvi.VariableState(set_value, True)

    # Act/Assert
    with pytest.raises(TypeError, match="Cannot set the value of reference property to a type of"):
        sut.set_value(new_value=new_value)

    mock_client.ReferencePropertySetValue.assert_not_called()


@pytest.mark.parametrize("set_value", set_value_not_supported_test_data)
def test_set_value_at_not_supported(monkeypatch, engine, set_value):
    # Arrange: gRPC client
    mock_client = MagicMock()
    monkeypatch_client_creation(monkeypatch, ReferenceProperty, mock_client)

    # Arrange: SUT
    sut_id = elem_msgs.ElementId(id_string="VAR_UNDER_TEST_ID")
    sut_name = "Bob"
    sut = grpcmc.ReferenceArrayProperty(element_id=sut_id, name=sut_name, engine=engine)

    new_value = atvi.VariableState(set_value, True)
    test_index = 5

    # Act/Assert
    with pytest.raises(TypeError, match="Cannot set the value of reference property to a type of"):
        sut.set_value_at(new_value=new_value, index=test_index)

    mock_client.ReferencePropertySetValue.assert_not_called()
