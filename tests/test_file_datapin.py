from os import PathLike
from typing import Optional, Type, Union
import unittest

import ansys.tools.variableinterop as atvi
import pytest

from ansys.modelcenter.workflow.grpc_modelcenter.abstract_workflow_element import (
    AbstractWorkflowElement,
)
from ansys.modelcenter.workflow.grpc_modelcenter.file_datapin import FileArrayDatapin, FileDatapin
from ansys.modelcenter.workflow.grpc_modelcenter.proto.element_messages_pb2 import ElementId
from ansys.modelcenter.workflow.grpc_modelcenter.proto.variable_value_messages_pb2 import (
    ArrayDimensions,
    FileArrayValue,
    FileValue,
    FileVariableMetadata,
    SetFileArrayValueRequest,
    SetFileValueRequest,
    SetFileVariableMetadataRequest,
    SetMetadataResponse,
    SetVariableValueResponse,
    VariableState,
    VariableType,
    VariableValue,
)
from ansys.modelcenter.workflow.grpc_modelcenter.var_metadata_convert import (
    CustomMetadataValueNotSupportedError,
)

from .grpc_server_test_utils.client_creation_monkeypatch import monkeypatch_client_creation
from .grpc_server_test_utils.mock_file_value import MockFileValue
from .test_datapin import (
    do_get_state_test,
    do_get_state_test_with_hid,
    do_get_type_test,
    do_test_is_input_component,
    do_test_is_input_workflow,
)


class MockWorkflowClientForFileVarTest:
    def __init__(self):
        pass

    def FileVariableSetMetadata(
        self, request: SetFileVariableMetadataRequest
    ) -> SetMetadataResponse:
        return SetMetadataResponse()

    def FileVariableGetMetadata(self, request: ElementId) -> FileVariableMetadata:
        return FileVariableMetadata()

    def FileVariableSetValue(self, request: SetFileValueRequest) -> SetVariableValueResponse:
        return SetVariableValueResponse()

    def FileArraySetValue(self, request: SetFileValueRequest) -> SetVariableValueResponse:
        return SetVariableValueResponse()


@pytest.mark.parametrize(
    "description_string,sut_type,expected_metadata_type",
    [
        ("", FileDatapin, atvi.FileMetadata),
        ("This is a mock datapin description.", FileDatapin, atvi.FileMetadata),
        ("", FileArrayDatapin, atvi.FileArrayMetadata),
        ("This is a mock datapin description.", FileArrayDatapin, atvi.FileArrayMetadata),
    ],
)
def test_retrieved_metadata_should_include_description(
    monkeypatch,
    engine,
    description_string: str,
    sut_type: Union[Type[FileDatapin], Type[FileArrayDatapin]],
    expected_metadata_type: Union[Type[atvi.FileMetadata], Type[atvi.FileArrayMetadata]],
) -> None:
    # Set up
    mock_client = MockWorkflowClientForFileVarTest()
    mock_response = FileVariableMetadata()
    sut_element_id = ElementId(id_string="VAR_UNDER_TEST_ID")
    mock_response.base_metadata.description = description_string
    with unittest.mock.patch.object(
        mock_client, "FileVariableGetMetadata", return_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = sut_type(sut_element_id, engine=engine)

        # Execute
        result: atvi.FileMetadata = sut.get_metadata()

        # Verify
        mock_grpc_method.assert_called_once_with(sut_element_id)
        assert isinstance(
            result, expected_metadata_type
        ), "The metadata should have the correct type."
        assert (
            result.description == description_string
        ), "The description string should match what was supplied by the gRPC client."


@pytest.mark.parametrize(
    "sut_type,expected_metadata_type",
    [(FileDatapin, atvi.FileMetadata), (FileArrayDatapin, atvi.FileArrayMetadata)],
)
def test_retrieved_metadata_should_include_custom_metadata_empty(
    monkeypatch,
    engine,
    sut_type: Union[Type[FileDatapin], Type[FileArrayDatapin]],
    expected_metadata_type: Union[Type[atvi.FileMetadata], Type[atvi.FileArrayMetadata]],
) -> None:
    # Set up
    mock_client = MockWorkflowClientForFileVarTest()
    mock_response = FileVariableMetadata()
    sut_element_id = ElementId(id_string="VAR_UNDER_TEST_ID")
    with unittest.mock.patch.object(
        mock_client, "FileVariableGetMetadata", return_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = sut_type(sut_element_id, engine)

        # Execute
        result: atvi.FileMetadata = sut.get_metadata()

        # Verify
        mock_grpc_method.assert_called_once_with(sut_element_id)
        assert isinstance(
            result, expected_metadata_type
        ), "The metadata should have the correct type."
        assert (
            len(result.custom_metadata) == 0
        ), "There should be no entries in the custom metadata map."


@pytest.mark.parametrize(
    "sut_type,expected_metadata_type",
    [(FileDatapin, atvi.FileMetadata), (FileArrayDatapin, atvi.FileArrayMetadata)],
)
def test_retrieved_metadata_should_include_custom_metadata_populated(
    monkeypatch,
    engine,
    sut_type: Union[Type[FileDatapin], Type[FileArrayDatapin]],
    expected_metadata_type: Union[Type[atvi.FileMetadata], Type[atvi.FileArrayMetadata]],
) -> None:
    # Set up
    mock_client = MockWorkflowClientForFileVarTest()
    mock_response = FileVariableMetadata()
    mock_response.base_metadata.custom_metadata["test_integer_value"].MergeFrom(
        VariableValue(int_value=47)
    )
    mock_response.base_metadata.custom_metadata["test_double_value"].MergeFrom(
        VariableValue(double_value=-867.5309)
    )
    sut_element_id = ElementId(id_string="VAR_UNDER_TEST_ID")
    with unittest.mock.patch.object(
        mock_client, "FileVariableGetMetadata", return_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = sut_type(sut_element_id, engine)

        # Execute
        result: atvi.FileMetadata = sut.get_metadata()

        # Verify
        mock_grpc_method.assert_called_once_with(sut_element_id)
        assert isinstance(
            result, expected_metadata_type
        ), "The metadata should have the correct type."
        expected_custom_metadata = {
            "test_integer_value": atvi.IntegerValue(47),
            "test_double_value": atvi.RealValue(-867.5309),
        }
        assert (
            result.custom_metadata == expected_custom_metadata
        ), "The custom metadata should have been transferred correctly."


@pytest.mark.parametrize(
    "sut_type,expected_metadata_type",
    [(FileDatapin, atvi.FileMetadata), (FileArrayDatapin, atvi.FileArrayMetadata)],
)
def test_retrieved_metadata_includes_unsupported_type(
    monkeypatch,
    engine,
    sut_type: Union[Type[FileDatapin], Type[FileArrayDatapin]],
    expected_metadata_type: Union[Type[atvi.FileMetadata], Type[atvi.FileArrayMetadata]],
) -> None:
    # Set up
    mock_client = MockWorkflowClientForFileVarTest()
    mock_response = FileVariableMetadata()
    mock_response.base_metadata.custom_metadata["test_unsupported"].MergeFrom(VariableValue())
    sut_element_id = ElementId(id_string="VAR_UNDER_TEST_ID")
    with unittest.mock.patch.object(
        mock_client, "FileVariableGetMetadata", return_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = sut_type(sut_element_id, engine)

        # Execute / Verify
        with pytest.raises(CustomMetadataValueNotSupportedError, match="unsupported type"):
            sut.get_metadata()

        # Verify
        mock_grpc_method.assert_called_once_with(sut_element_id)


@pytest.mark.parametrize(
    "sut_type",
    [
        FileDatapin,
        FileArrayDatapin,
    ],
)
def test_set_metadata_invalid_custom_metadata(
    monkeypatch, engine, sut_type: Union[Type[FileDatapin], Type[FileArrayDatapin]]
) -> None:
    # Set up
    mock_client = MockWorkflowClientForFileVarTest()
    mock_response = SetMetadataResponse()
    sut_element_id = ElementId(id_string="VAR_UNDER_TEST_ID")
    with unittest.mock.patch.object(
        mock_client, "FileVariableSetMetadata", return_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = sut_type(sut_element_id, engine)
        new_metadata = atvi.BooleanMetadata()

        # Execute
        with pytest.raises(TypeError):
            sut.set_metadata(new_metadata)

        # Verify
        mock_grpc_method.assert_not_called()


@pytest.mark.parametrize(
    "description,sut_type,metadata_type",
    [
        ("", FileDatapin, atvi.FileMetadata),
        ("This is a mock datapin description.", FileDatapin, atvi.FileMetadata),
        ("", FileArrayDatapin, atvi.FileArrayMetadata),
        ("This is a mock datapin description.", FileArrayDatapin, atvi.FileArrayMetadata),
    ],
)
def test_set_metadata_empty_custom_metadata(
    monkeypatch,
    engine,
    description: str,
    sut_type: Union[Type[FileDatapin], Type[FileArrayDatapin]],
    metadata_type: Union[Type[atvi.FileMetadata], Type[atvi.FileArrayMetadata]],
) -> None:
    # Set up
    mock_client = MockWorkflowClientForFileVarTest()
    mock_response = SetMetadataResponse()
    sut_element_id = ElementId(id_string="VAR_UNDER_TEST_ID")
    with unittest.mock.patch.object(
        mock_client, "FileVariableSetMetadata", return_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = sut_type(sut_element_id, engine)
        new_metadata = metadata_type()
        new_metadata.description = description

        # Execute
        sut.set_metadata(new_metadata)

        # Verify
        expected_request = SetFileVariableMetadataRequest(target=sut_element_id)
        expected_request.new_metadata.base_metadata.description = description
        mock_grpc_method.assert_called_once_with(expected_request)


@pytest.mark.parametrize(
    "description,sut_type,metadata_type",
    [
        ("", FileDatapin, atvi.FileMetadata),
        ("This is a mock datapin description.", FileDatapin, atvi.FileMetadata),
        ("", FileArrayDatapin, atvi.FileArrayMetadata),
        ("This is a mock datapin description.", FileArrayDatapin, atvi.FileArrayMetadata),
    ],
)
def test_set_metadata_populated_custom_metadata(
    monkeypatch,
    engine,
    description: str,
    sut_type: Union[Type[FileDatapin], Type[FileArrayDatapin]],
    metadata_type: Union[Type[atvi.FileMetadata], Type[atvi.FileArrayMetadata]],
) -> None:
    # Set up
    mock_client = MockWorkflowClientForFileVarTest()
    mock_response = SetMetadataResponse()
    sut_element_id = ElementId(id_string="VAR_UNDER_TEST_ID")
    with unittest.mock.patch.object(
        mock_client, "FileVariableSetMetadata", return_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = sut_type(sut_element_id, engine)
        new_metadata = metadata_type()
        new_metadata.description = description
        new_metadata.custom_metadata["int_value"] = atvi.IntegerValue(47)
        new_metadata.custom_metadata["real_value"] = atvi.RealValue(-867.5309)

        # Execute
        sut.set_metadata(new_metadata)

        # Verify
        expected_request = SetFileVariableMetadataRequest(target=sut_element_id)
        expected_request.new_metadata.base_metadata.description = description
        expected_request.new_metadata.base_metadata.custom_metadata["int_value"].MergeFrom(
            VariableValue(int_value=47)
        )
        expected_request.new_metadata.base_metadata.custom_metadata["real_value"].MergeFrom(
            VariableValue(double_value=-867.5309)
        )
        mock_grpc_method.assert_called_once_with(expected_request)


@pytest.mark.parametrize(
    "set_value,expected_value_in_request",
    [(atvi.EMPTY_FILE, FileValue()), (MockFileValue("a.path"), FileValue(content_path="a.path"))],
)
def test_scalar_set_allowed(monkeypatch, engine, set_value, expected_value_in_request) -> None:
    # Set up
    mock_client = MockWorkflowClientForFileVarTest()
    mock_response = SetVariableValueResponse()
    sut_element_id = ElementId(id_string="VAR_UNDER_TEST_ID")
    with unittest.mock.patch.object(
        mock_client, "FileVariableSetValue", retun_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = FileDatapin(sut_element_id, engine)
        new_value = atvi.VariableState(set_value, True)

        # Execute
        sut.set_value(new_value)

        # Verify
        expected_request = SetFileValueRequest(
            target=sut_element_id, new_value=expected_value_in_request
        )
        mock_grpc_method.assert_called_once_with(expected_request)


@pytest.mark.parametrize(
    "set_value,expected_value_in_request",
    [
        (
            atvi.FileArrayValue(shape_=(0,)),
            FileArrayValue(dims=ArrayDimensions(dims=[0]), values=[]),
        ),
        (
            atvi.FileArrayValue(
                shape_=(2, 2),
                values=[[FileValue(), FileValue()], [FileValue(), FileValue()]],
            ),
            FileArrayValue(
                dims=ArrayDimensions(dims=[2, 2]),
                values=[FileValue(), FileValue(), FileValue(), FileValue()],
            ),
        ),
    ],
)
@pytest.mark.skip("Set not yet implemented")
def test_array_set_allowed(monkeypatch, engine, set_value, expected_value_in_request) -> None:
    # Set up
    mock_client = MockWorkflowClientForFileVarTest()
    mock_response = SetVariableValueResponse()
    sut_element_id = ElementId(id_string="VAR_UNDER_TEST_ID")
    with unittest.mock.patch.object(
        mock_client, "FileArraySetValue", retun_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = FileArrayDatapin(sut_element_id, engine)
        new_value = atvi.VariableState(set_value, True)

        # Execute
        sut.set_value(new_value)

        # Verify
        expected_request = SetFileArrayValueRequest(
            target=sut_element_id, new_value=expected_value_in_request
        )
        mock_grpc_method.assert_called_once_with(expected_request)


@pytest.mark.parametrize(
    "set_value",
    [
        atvi.BooleanValue(True),
        atvi.IntegerValue(0),
        atvi.RealValue(0.0),
        MockFileValue(),
        atvi.StringValue("False"),
        atvi.IntegerArrayValue(),
        atvi.RealArrayValue(),
        atvi.StringArrayValue(),
    ],
)
def test_array_set_disallowed(monkeypatch, engine, set_value) -> None:
    # Set up
    mock_client = MockWorkflowClientForFileVarTest()
    mock_response = SetVariableValueResponse()
    sut_element_id = ElementId(id_string="VAR_UNDER_TEST_ID")
    with unittest.mock.patch.object(
        mock_client, "FileArraySetValue", return_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = FileArrayDatapin(sut_element_id, engine)
        new_value = atvi.VariableState(set_value, True)

        # Execute / verify:
        with pytest.raises(atvi.IncompatibleTypesException):
            sut.set_value(new_value)

        # Verify
        mock_grpc_method.assert_not_called()


def test_scalar_get_type(monkeypatch, engine) -> None:
    do_get_type_test(
        monkeypatch, engine, FileDatapin, VariableType.VARTYPE_FILE, atvi.VariableType.FILE
    )


def test_array_get_type(monkeypatch, engine) -> None:
    do_get_type_test(
        monkeypatch,
        engine,
        FileArrayDatapin,
        VariableType.VARTYPE_FILE_ARRAY,
        atvi.VariableType.FILE_ARRAY,
    )


@pytest.mark.parametrize(
    "value_in_response,validity_in_response,expected_atvi_state",
    [
        (FileValue(), True, atvi.VariableState(MockFileValue(""), True)),
        (FileValue(), False, atvi.VariableState(MockFileValue(""), False)),
        (FileValue(), True, atvi.VariableState(MockFileValue(""), True)),
        (FileValue(), False, atvi.VariableState(MockFileValue(""), False)),
    ],
)
def test_scalar_get_state(
    monkeypatch, engine, value_in_response, validity_in_response, expected_atvi_state
) -> None:
    def mock_read(self, to_read: PathLike, mime_type: Optional[str], encoding: Optional[str]):
        return MockFileValue(str(to_read))

    monkeypatch.setattr(atvi.NonManagingFileScope, "read_from_file", mock_read)

    do_get_state_test(
        monkeypatch,
        engine,
        FileDatapin,
        VariableState(
            is_valid=validity_in_response, value=VariableValue(file_value=value_in_response)
        ),
        expected_atvi_state,
    )


def test_scalar_get_state_with_hid(monkeypatch, engine) -> None:
    do_get_state_test_with_hid(monkeypatch, engine, FileDatapin)


@pytest.mark.parametrize(
    "value_in_response,validity_in_response,expected_atvi_state",
    [
        (
            FileArrayValue(
                dims=ArrayDimensions(dims=[2, 2]),
                values=[FileValue(), FileValue(), FileValue(), FileValue()],
            ),
            True,
            atvi.VariableState(
                atvi.FileArrayValue(
                    shape_=(2, 2),
                    values=[
                        [MockFileValue(""), MockFileValue("")],
                        [MockFileValue(""), MockFileValue("")],
                    ],
                ),
                True,
            ),
        ),
        (
            FileArrayValue(
                dims=ArrayDimensions(dims=[2, 2]),
                values=[FileValue(), FileValue(), FileValue(), FileValue()],
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
    ],
)
def test_array_get_state(
    monkeypatch, engine, value_in_response, validity_in_response, expected_atvi_state
) -> None:
    def mock_read(self, to_read: PathLike, mime_type: Optional[str], encoding: Optional[str]):
        return MockFileValue(str(to_read))

    monkeypatch.setattr(atvi.NonManagingFileScope, "read_from_file", mock_read)

    do_get_state_test(
        monkeypatch,
        engine,
        FileArrayDatapin,
        VariableState(
            is_valid=validity_in_response, value=VariableValue(file_array_value=value_in_response)
        ),
        expected_atvi_state,
    )


def test_array_get_state_with_hid(monkeypatch, engine) -> None:
    do_get_state_test_with_hid(monkeypatch, engine, FileArrayDatapin)


@pytest.mark.parametrize(
    "sut_type, flag_in_response",
    [
        (FileDatapin, True),
        (FileDatapin, False),
        (FileArrayDatapin, True),
        (FileArrayDatapin, False),
    ],
)
def test_is_input_component(monkeypatch, engine, sut_type, flag_in_response) -> None:
    do_test_is_input_component(monkeypatch, engine, sut_type, flag_in_response)


@pytest.mark.parametrize(
    "sut_type, flag_in_response",
    [
        (FileDatapin, True),
        (FileDatapin, False),
        (FileArrayDatapin, True),
        (FileArrayDatapin, False),
    ],
)
def test_is_input_workflow(monkeypatch, engine, sut_type, flag_in_response) -> None:
    do_test_is_input_workflow(monkeypatch, engine, sut_type, flag_in_response)
