from typing import Union
import unittest

import ansys.common.variableinterop as acvi
import pytest

from ansys.modelcenter.workflow.grpc_modelcenter.abstract_workflow_element import (
    AbstractWorkflowElement,
)
from ansys.modelcenter.workflow.grpc_modelcenter.proto.element_messages_pb2 import ElementId
from ansys.modelcenter.workflow.grpc_modelcenter.proto.variable_value_messages_pb2 import (
    ArrayDimensions,
    FileValue,
    SetMetadataResponse,
    SetStringArrayValueRequest,
    SetStringValueRequest,
    SetStringVariableMetadataRequest,
    SetVariableValueResponse,
    StringArrayValue,
    StringVariableMetadata,
    VariableState,
    VariableType,
    VariableValue,
)
from ansys.modelcenter.workflow.grpc_modelcenter.string_variable import (
    StringArrayVariable,
    StringVariable,
)
from ansys.modelcenter.workflow.grpc_modelcenter.var_metadata_convert import (
    CustomMetadataValueNotSupportedError,
)

from .grpc_server_test_utils.client_creation_monkeypatch import monkeypatch_client_creation
from .test_variable import (
    do_get_state_test,
    do_get_type_test,
    do_test_is_input_component,
    do_test_is_input_workflow,
)


class MockWorkflowClientForStringVarTest:
    def __init__(self):
        pass

    def StringVariableSetMetadata(
        self, request: SetStringVariableMetadataRequest
    ) -> SetMetadataResponse:
        return SetMetadataResponse()

    def StringVariableGetMetadata(self, request: ElementId) -> StringVariableMetadata:
        return StringVariableMetadata()

    def StringVariableSetValue(self, request: SetStringValueRequest) -> SetVariableValueResponse:
        return SetVariableValueResponse()

    def StringArraySetValue(self, request: SetStringArrayValueRequest) -> SetVariableValueResponse:
        return SetVariableValueResponse()


@pytest.mark.parametrize(
    "description_string,sut_type,expected_metadata_type",
    [
        ("", StringVariable, acvi.StringMetadata),
        ("This is a mock variable description.", StringVariable, acvi.StringMetadata),
        ("", StringArrayVariable, acvi.StringArrayMetadata),
        ("This is a mock variable description.", StringArrayVariable, acvi.StringArrayMetadata),
    ],
)
def test_retrieved_metadata_should_include_description(
    monkeypatch,
    description_string: str,
    sut_type: Union[StringVariable, StringArrayVariable],
    expected_metadata_type: Union[acvi.StringMetadata, acvi.StringArrayMetadata],
) -> None:
    # Set up
    mock_client = MockWorkflowClientForStringVarTest()
    mock_response = StringVariableMetadata()
    sut_element_id = ElementId(id_string="VAR_UNDER_TEST_ID")
    mock_response.base_metadata.description = description_string
    with unittest.mock.patch.object(
        mock_client, "StringVariableGetMetadata", return_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = sut_type(sut_element_id, None)

        # Execute
        result: acvi.StringMetadata = sut.get_metadata()

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
    [(StringVariable, acvi.StringMetadata), (StringArrayVariable, acvi.StringArrayMetadata)],
)
def test_retrieved_metadata_should_include_custom_metadata_empty(
    monkeypatch,
    sut_type: Union[StringVariable, StringArrayVariable],
    expected_metadata_type: Union[acvi.StringMetadata, acvi.StringArrayMetadata],
) -> None:
    # Set up
    mock_client = MockWorkflowClientForStringVarTest()
    mock_response = StringVariableMetadata()
    sut_element_id = ElementId(id_string="VAR_UNDER_TEST_ID")
    with unittest.mock.patch.object(
        mock_client, "StringVariableGetMetadata", return_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = sut_type(sut_element_id, None)

        # Execute
        result: acvi.StringMetadata = sut.get_metadata()

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
    [(StringVariable, acvi.StringMetadata), (StringArrayVariable, acvi.StringArrayMetadata)],
)
def test_retrieved_metadata_should_include_custom_metadata_populated(
    monkeypatch,
    sut_type: Union[StringVariable, StringArrayVariable],
    expected_metadata_type: Union[acvi.StringMetadata, acvi.StringArrayMetadata],
) -> None:
    # Set up
    mock_client = MockWorkflowClientForStringVarTest()
    mock_response = StringVariableMetadata()
    mock_response.base_metadata.custom_metadata["test_integer_value"].MergeFrom(
        VariableValue(int_value=47)
    )
    mock_response.base_metadata.custom_metadata["test_double_value"].MergeFrom(
        VariableValue(double_value=-867.5309)
    )
    sut_element_id = ElementId(id_string="VAR_UNDER_TEST_ID")
    with unittest.mock.patch.object(
        mock_client, "StringVariableGetMetadata", return_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = sut_type(sut_element_id, None)

        # Execute
        result: acvi.StringMetadata = sut.get_metadata()

        # Verify
        mock_grpc_method.assert_called_once_with(sut_element_id)
        assert isinstance(
            result, expected_metadata_type
        ), "The metadata should have the correct type."
        expected_custom_metadata = {
            "test_integer_value": acvi.IntegerValue(47),
            "test_double_value": acvi.RealValue(-867.5309),
        }
        assert (
            result.custom_metadata == expected_custom_metadata
        ), "The custom metadata should have been transferred correctly."


@pytest.mark.parametrize(
    "sut_type,expected_metadata_type",
    [(StringVariable, acvi.StringMetadata), (StringArrayVariable, acvi.StringArrayMetadata)],
)
def test_retrieved_metadata_includes_unsupported_type(
    monkeypatch,
    sut_type: Union[StringVariable, StringArrayVariable],
    expected_metadata_type: Union[acvi.StringMetadata, acvi.StringArrayMetadata],
) -> None:
    # Set up
    mock_client = MockWorkflowClientForStringVarTest()
    mock_response = StringVariableMetadata()
    mock_response.base_metadata.custom_metadata["test_unsupported"].MergeFrom(
        VariableValue(file_value=FileValue())
    )
    sut_element_id = ElementId(id_string="VAR_UNDER_TEST_ID")
    with unittest.mock.patch.object(
        mock_client, "StringVariableGetMetadata", return_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = sut_type(sut_element_id, None)

        # Execute / Verify
        with pytest.raises(CustomMetadataValueNotSupportedError, match="unsupported type"):
            sut.get_metadata()

        # Verify
        mock_grpc_method.assert_called_once_with(sut_element_id)


@pytest.mark.parametrize(
    "sut_type",
    [
        StringVariable,
        StringArrayVariable,
    ],
)
def test_set_metadata_invalid_custom_metadata(
    monkeypatch, sut_type: Union[StringVariable, StringArrayVariable]
):
    # Set up
    mock_client = MockWorkflowClientForStringVarTest()
    mock_response = SetMetadataResponse()
    sut_element_id = ElementId(id_string="VAR_UNDER_TEST_ID")
    with unittest.mock.patch.object(
        mock_client, "StringVariableSetMetadata", return_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = sut_type(sut_element_id, None)
        new_metadata = acvi.FileMetadata()

        # Execute
        with pytest.raises(TypeError):
            sut.set_metadata(new_metadata)

        # Verify
        mock_grpc_method.assert_not_called()


@pytest.mark.parametrize(
    "description,sut_type,metadata_type",
    [
        ("", StringVariable, acvi.StringMetadata),
        ("This is a mock variable description.", StringVariable, acvi.StringMetadata),
        ("", StringArrayVariable, acvi.StringArrayMetadata),
        ("This is a mock variable description.", StringArrayVariable, acvi.StringArrayMetadata),
    ],
)
def test_set_metadata_empty_custom_metadata(
    monkeypatch,
    description: str,
    sut_type: Union[StringVariable, StringArrayVariable],
    metadata_type: Union[acvi.StringMetadata, acvi.StringArrayMetadata],
) -> None:
    # Set up
    mock_client = MockWorkflowClientForStringVarTest()
    mock_response = SetMetadataResponse()
    sut_element_id = ElementId(id_string="VAR_UNDER_TEST_ID")
    with unittest.mock.patch.object(
        mock_client, "StringVariableSetMetadata", return_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = sut_type(sut_element_id, None)
        new_metadata = metadata_type()
        new_metadata.description = description

        # Execute
        sut.set_metadata(new_metadata)

        # Verify
        expected_request = SetStringVariableMetadataRequest(target=sut_element_id)
        expected_request.new_metadata.base_metadata.description = description
        mock_grpc_method.assert_called_once_with(expected_request)


@pytest.mark.parametrize(
    "description,sut_type,metadata_type",
    [
        ("", StringVariable, acvi.StringMetadata),
        ("This is a mock variable description.", StringVariable, acvi.StringMetadata),
        ("", StringArrayVariable, acvi.StringArrayMetadata),
        ("This is a mock variable description.", StringArrayVariable, acvi.StringArrayMetadata),
    ],
)
def test_set_metadata_populated_custom_metadata(
    monkeypatch,
    description: str,
    sut_type: Union[StringVariable, StringArrayVariable],
    metadata_type: Union[acvi.StringMetadata, acvi.StringArrayMetadata],
) -> None:
    # Set up
    mock_client = MockWorkflowClientForStringVarTest()
    mock_response = SetMetadataResponse()
    sut_element_id = ElementId(id_string="VAR_UNDER_TEST_ID")
    with unittest.mock.patch.object(
        mock_client, "StringVariableSetMetadata", return_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = sut_type(sut_element_id, None)
        new_metadata = metadata_type()
        new_metadata.description = description
        new_metadata.custom_metadata["int_value"] = acvi.IntegerValue(47)
        new_metadata.custom_metadata["real_value"] = acvi.RealValue(-867.5309)

        # Execute
        sut.set_metadata(new_metadata)

        # Verify
        expected_request = SetStringVariableMetadataRequest(target=sut_element_id)
        expected_request.new_metadata.base_metadata.description = description
        expected_request.new_metadata.base_metadata.custom_metadata["int_value"].MergeFrom(
            VariableValue(int_value=47)
        )
        expected_request.new_metadata.base_metadata.custom_metadata["real_value"].MergeFrom(
            VariableValue(double_value=-867.5309)
        )
        mock_grpc_method.assert_called_once_with(expected_request)


@pytest.mark.parametrize(
    "sut_type,metadata_type",
    [
        (StringVariable, acvi.StringMetadata),
        (StringArrayVariable, acvi.StringArrayMetadata),
    ],
)
def test_set_metadata_populated_enums(
    monkeypatch,
    sut_type: Union[StringVariable, StringArrayVariable],
    metadata_type: Union[acvi.StringMetadata, acvi.StringArrayMetadata],
):
    # Set up
    mock_client = MockWorkflowClientForStringVarTest()
    mock_response = SetMetadataResponse()
    sut_element_id = ElementId(id_string="VAR_UNDER_TEST_ID")
    with unittest.mock.patch.object(
        mock_client, "StringVariableSetMetadata", return_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = sut_type(sut_element_id, None)
        new_metadata = metadata_type()
        new_metadata.enumerated_values = [acvi.StringValue("1"), acvi.StringValue("2")]
        new_metadata.enumerated_aliases = ["a", "b"]

        # Execute
        sut.set_metadata(new_metadata)

        # Verify
        expected_request = SetStringVariableMetadataRequest(target=sut_element_id)
        expected_request.new_metadata.base_metadata.description = ""
        expected_request.new_metadata.enum_values.MergeFrom(
            [acvi.StringValue("1"), acvi.StringValue("2")]
        )
        expected_request.new_metadata.enum_aliases.MergeFrom(["a", "b"])
        mock_grpc_method.assert_called_once_with(expected_request)


@pytest.mark.parametrize(
    "set_value,expected_value_in_request",
    [
        (acvi.StringValue(""), ""),
        (acvi.StringValue("This is a test string value."), "This is a test string value."),
        (
            acvi.StringValue("   leading and trailing whitespace   "),
            "   leading and trailing whitespace   ",
        ),
        (acvi.RealValue(-867.5309), "-867.5309"),
        (acvi.IntegerValue(47), "47"),
        (acvi.BooleanValue(True), "True"),
    ],
)
def test_scalar_set_allowed(monkeypatch, set_value, expected_value_in_request) -> None:
    # Set up
    mock_client = MockWorkflowClientForStringVarTest()
    mock_response = SetVariableValueResponse()
    sut_element_id = ElementId(id_string="VAR_UNDER_TEST_ID")
    with unittest.mock.patch.object(
        mock_client, "StringVariableSetValue", retun_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = StringVariable(sut_element_id, None)
        new_value = acvi.VariableState(set_value, True)

        # Execute
        sut.set_value(new_value)

        # Verify
        expected_request = SetStringValueRequest(
            target=sut_element_id, new_value=expected_value_in_request
        )
        mock_grpc_method.assert_called_once_with(expected_request)


@pytest.mark.parametrize(
    "set_value",
    [
        acvi.IntegerArrayValue(),
        acvi.RealArrayValue(),
        acvi.BooleanArrayValue(),
        acvi.StringArrayValue(),
    ],
)
def test_scalar_set_disallowed(monkeypatch, set_value) -> None:
    # Set up
    mock_client = MockWorkflowClientForStringVarTest()
    mock_response = SetVariableValueResponse()
    sut_element_id = ElementId(id_string="VAR_UNDER_TEST_ID")
    with unittest.mock.patch.object(
        mock_client, "StringVariableSetValue", return_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = StringVariable(sut_element_id, None)
        new_value = acvi.VariableState(set_value, True)

        # Execute / verify:
        with pytest.raises(TypeError):
            sut.set_value(new_value)

        # Verify
        mock_grpc_method.assert_not_called()


@pytest.mark.parametrize(
    "set_value,expected_value_in_request",
    [
        (
            acvi.StringArrayValue(shape_=(2, 2), values=[["string", "array"], ["test", "value"]]),
            StringArrayValue(
                dims=ArrayDimensions(dims=[2, 2]), values=["string", "array", "test", "value"]
            ),
        ),
        (
            acvi.BooleanArrayValue(shape_=(2, 2), values=[[True, False], [False, True]]),
            StringArrayValue(
                dims=ArrayDimensions(dims=[2, 2]), values=["True", "False", "False", "True"]
            ),
        ),
        (
            acvi.IntegerArrayValue(shape_=(2, 2), values=[[47, 9001], [1337, -9999]]),
            StringArrayValue(
                dims=ArrayDimensions(dims=[2, 2]), values=["47", "9001", "1337", "-9999"]
            ),
        ),
        (
            acvi.RealArrayValue(shape_=(2, 2), values=[[4.7, 9000.1], [13.37, -1.0]]),
            StringArrayValue(
                dims=ArrayDimensions(dims=[2, 2]), values=["4.7", "9000.1", "13.37", "-1.0"]
            ),
        ),
    ],
)
def test_array_set_allowed(monkeypatch, set_value, expected_value_in_request) -> None:
    # Set up
    mock_client = MockWorkflowClientForStringVarTest()
    mock_response = SetVariableValueResponse()
    sut_element_id = ElementId(id_string="VAR_UNDER_TEST_ID")
    with unittest.mock.patch.object(
        mock_client, "StringArraySetValue", retun_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = StringArrayVariable(sut_element_id, None)
        new_value = acvi.VariableState(set_value, True)

        # Execute
        sut.set_value(new_value)

        # Verify
        expected_request = SetStringArrayValueRequest(
            target=sut_element_id, new_value=expected_value_in_request
        )
        mock_grpc_method.assert_called_once_with(expected_request)


@pytest.mark.parametrize(
    "set_value",
    [
        acvi.IntegerValue(0),
        acvi.RealValue(0.0),
        acvi.BooleanValue(True),
        acvi.StringValue("scalar"),
    ],
)
def test_array_set_disallowed(monkeypatch, set_value) -> None:
    # Set up
    mock_client = MockWorkflowClientForStringVarTest()
    mock_response = SetVariableValueResponse()
    sut_element_id = ElementId(id_string="VAR_UNDER_TEST_ID")
    with unittest.mock.patch.object(
        mock_client, "StringArraySetValue", return_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = StringArrayVariable(sut_element_id, None)
        new_value = acvi.VariableState(set_value, True)

        # Execute / verify:
        with pytest.raises(TypeError):
            sut.set_value(new_value)

        # Verify
        mock_grpc_method.assert_not_called()


def test_scalar_get_type(monkeypatch) -> None:
    do_get_type_test(
        monkeypatch, StringVariable, VariableType.VARTYPE_STRING, acvi.VariableType.STRING
    )


def test_array_get_type(monkeypatch) -> None:
    do_get_type_test(
        monkeypatch,
        StringArrayVariable,
        VariableType.VARTYPE_STRING_ARRAY,
        acvi.VariableType.STRING_ARRAY,
    )


@pytest.mark.parametrize(
    "value_in_response,validity_in_response,expected_acvi_state",
    [
        ("", True, acvi.VariableState(acvi.StringValue(""), True)),
        ("test string", False, acvi.VariableState(acvi.StringValue("test string"), False)),
        ("(╯°□°）╯︵ ┻━┻", True, acvi.VariableState(acvi.StringValue("(╯°□°）╯︵ ┻━┻"), True)),
    ],
)
def test_scalar_get_state(
    monkeypatch, value_in_response, validity_in_response, expected_acvi_state
) -> None:
    do_get_state_test(
        monkeypatch,
        StringVariable,
        VariableState(
            is_valid=validity_in_response, value=VariableValue(string_value=value_in_response)
        ),
        expected_acvi_state,
    )


@pytest.mark.parametrize(
    "value_in_response,validity_in_response,expected_acvi_state",
    [
        (
            StringArrayValue(
                dims=ArrayDimensions(dims=[2, 2]),
                values=["primary", "secondary", "first", "second"],
            ),
            True,
            acvi.VariableState(
                acvi.StringArrayValue(
                    shape_=(2, 2), values=[["primary", "secondary"], ["first", "second"]]
                ),
                True,
            ),
        ),
        (
            StringArrayValue(
                dims=ArrayDimensions(dims=[2, 2]), values=["one", "two", "three", "four"]
            ),
            False,
            acvi.VariableState(
                acvi.StringArrayValue(shape_=(2, 2), values=[["one", "two"], ["three", "four"]]),
                False,
            ),
        ),
    ],
)
def test_array_get_state(
    monkeypatch, value_in_response, validity_in_response, expected_acvi_state
) -> None:
    do_get_state_test(
        monkeypatch,
        StringArrayVariable,
        VariableState(
            is_valid=validity_in_response, value=VariableValue(string_array_value=value_in_response)
        ),
        expected_acvi_state,
    )


@pytest.mark.parametrize(
    "sut_type, flag_in_response",
    [
        (StringVariable, True),
        (StringVariable, False),
        (StringArrayVariable, True),
        (StringArrayVariable, False),
    ],
)
def test_is_input_component(monkeypatch, sut_type, flag_in_response) -> None:
    do_test_is_input_component(monkeypatch, sut_type, flag_in_response)


@pytest.mark.parametrize(
    "sut_type, flag_in_response",
    [
        (StringVariable, True),
        (StringVariable, False),
        (StringArrayVariable, True),
        (StringArrayVariable, False),
    ],
)
def test_is_input_workflow(monkeypatch, sut_type, flag_in_response) -> None:
    do_test_is_input_workflow(monkeypatch, sut_type, flag_in_response)
