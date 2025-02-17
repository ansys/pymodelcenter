# Copyright (C) 2022 - 2025 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from typing import Type, Union
import unittest

from ansys.api.modelcenter.v0.element_messages_pb2 import ElementId
from ansys.api.modelcenter.v0.variable_value_messages_pb2 import (
    ArrayDimensions,
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
import ansys.tools.variableinterop as atvi
import pytest

from ansys.modelcenter.workflow.grpc_modelcenter.abstract_workflow_element import (
    AbstractWorkflowElement,
)
from ansys.modelcenter.workflow.grpc_modelcenter.string_datapin import (
    StringArrayDatapin,
    StringDatapin,
)
from ansys.modelcenter.workflow.grpc_modelcenter.var_metadata_convert import (
    CustomMetadataValueNotSupportedError,
)

from .grpc_server_test_utils.client_creation_monkeypatch import monkeypatch_client_creation
from .test_datapin import (
    do_get_state_test,
    do_get_state_test_with_hid,
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
        ("", StringDatapin, atvi.StringMetadata),
        ("This is a mock datapin description.", StringDatapin, atvi.StringMetadata),
        ("", StringArrayDatapin, atvi.StringArrayMetadata),
        ("This is a mock datapin description.", StringArrayDatapin, atvi.StringArrayMetadata),
    ],
)
def test_retrieved_metadata_should_include_description(
    monkeypatch,
    engine,
    description_string: str,
    sut_type: Union[Type[StringDatapin], Type[StringArrayDatapin]],
    expected_metadata_type: Union[Type[atvi.StringMetadata], Type[atvi.StringArrayMetadata]],
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
        sut = sut_type(sut_element_id, engine=engine)

        # Execute
        result: atvi.StringMetadata = sut.get_metadata()

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
    [(StringDatapin, atvi.StringMetadata), (StringArrayDatapin, atvi.StringArrayMetadata)],
)
def test_retrieved_metadata_should_include_custom_metadata_empty(
    monkeypatch,
    engine,
    sut_type: Union[Type[StringDatapin], Type[StringArrayDatapin]],
    expected_metadata_type: Union[Type[atvi.StringMetadata], Type[atvi.StringArrayMetadata]],
) -> None:
    # Set up
    mock_client = MockWorkflowClientForStringVarTest()
    mock_response = StringVariableMetadata()
    sut_element_id = ElementId(id_string="VAR_UNDER_TEST_ID")
    with unittest.mock.patch.object(
        mock_client, "StringVariableGetMetadata", return_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = sut_type(sut_element_id, engine=engine)

        # Execute
        result: atvi.StringMetadata = sut.get_metadata()

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
    [(StringDatapin, atvi.StringMetadata), (StringArrayDatapin, atvi.StringArrayMetadata)],
)
def test_retrieved_metadata_should_include_custom_metadata_populated(
    monkeypatch,
    engine,
    sut_type: Union[Type[StringDatapin], Type[StringArrayDatapin]],
    expected_metadata_type: Union[atvi.StringMetadata, atvi.StringArrayMetadata],
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
        sut = sut_type(sut_element_id, engine=engine)

        # Execute
        result: atvi.StringMetadata = sut.get_metadata()

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
    [(StringDatapin, atvi.StringMetadata), (StringArrayDatapin, atvi.StringArrayMetadata)],
)
def test_retrieved_metadata_includes_unsupported_type(
    monkeypatch,
    engine,
    sut_type: Union[Type[StringDatapin], Type[StringArrayDatapin]],
    expected_metadata_type: Union[Type[atvi.StringMetadata], Type[atvi.StringArrayMetadata]],
) -> None:
    # Set up
    mock_client = MockWorkflowClientForStringVarTest()
    mock_response = StringVariableMetadata()
    mock_response.base_metadata.custom_metadata["test_unsupported"].MergeFrom(VariableValue())
    sut_element_id = ElementId(id_string="VAR_UNDER_TEST_ID")
    with unittest.mock.patch.object(
        mock_client, "StringVariableGetMetadata", return_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = sut_type(sut_element_id, engine=engine)

        # Execute / Verify
        with pytest.raises(CustomMetadataValueNotSupportedError, match="unsupported type"):
            sut.get_metadata()

        # Verify
        mock_grpc_method.assert_called_once_with(sut_element_id)


@pytest.mark.parametrize(
    "sut_type",
    [
        StringDatapin,
        StringArrayDatapin,
    ],
)
def test_set_metadata_invalid_custom_metadata(
    monkeypatch, engine, sut_type: Union[Type[StringDatapin], Type[StringArrayDatapin]]
):
    # Set up
    mock_client = MockWorkflowClientForStringVarTest()
    mock_response = SetMetadataResponse()
    sut_element_id = ElementId(id_string="VAR_UNDER_TEST_ID")
    with unittest.mock.patch.object(
        mock_client, "StringVariableSetMetadata", return_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = sut_type(sut_element_id, engine=engine)
        new_metadata = atvi.FileMetadata()

        # Execute
        with pytest.raises(TypeError):
            sut.set_metadata(new_metadata)

        # Verify
        mock_grpc_method.assert_not_called()


@pytest.mark.parametrize(
    "description,sut_type,metadata_type",
    [
        ("", StringDatapin, atvi.StringMetadata),
        ("This is a mock datapin description.", StringDatapin, atvi.StringMetadata),
        ("", StringArrayDatapin, atvi.StringArrayMetadata),
        ("This is a mock datapin description.", StringArrayDatapin, atvi.StringArrayMetadata),
    ],
)
def test_set_metadata_empty_custom_metadata(
    monkeypatch,
    engine,
    description: str,
    sut_type: Union[Type[StringDatapin], Type[StringArrayDatapin]],
    metadata_type: Union[Type[atvi.StringMetadata], Type[atvi.StringArrayMetadata]],
) -> None:
    # Set up
    mock_client = MockWorkflowClientForStringVarTest()
    mock_response = SetMetadataResponse()
    sut_element_id = ElementId(id_string="VAR_UNDER_TEST_ID")
    with unittest.mock.patch.object(
        mock_client, "StringVariableSetMetadata", return_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = sut_type(sut_element_id, engine=engine)
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
        ("", StringDatapin, atvi.StringMetadata),
        ("This is a mock datapin description.", StringDatapin, atvi.StringMetadata),
        ("", StringArrayDatapin, atvi.StringArrayMetadata),
        ("This is a mock datapin description.", StringArrayDatapin, atvi.StringArrayMetadata),
    ],
)
def test_set_metadata_populated_custom_metadata(
    monkeypatch,
    engine,
    description: str,
    sut_type: Union[Type[StringDatapin], Type[StringArrayDatapin]],
    metadata_type: Union[Type[atvi.StringMetadata], Type[atvi.StringArrayMetadata]],
) -> None:
    # Set up
    mock_client = MockWorkflowClientForStringVarTest()
    mock_response = SetMetadataResponse()
    sut_element_id = ElementId(id_string="VAR_UNDER_TEST_ID")
    with unittest.mock.patch.object(
        mock_client, "StringVariableSetMetadata", return_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = sut_type(sut_element_id, engine=engine)
        new_metadata = metadata_type()
        new_metadata.description = description
        new_metadata.custom_metadata["int_value"] = atvi.IntegerValue(47)
        new_metadata.custom_metadata["real_value"] = atvi.RealValue(-867.5309)

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
        (StringDatapin, atvi.StringMetadata),
        (StringArrayDatapin, atvi.StringArrayMetadata),
    ],
)
def test_set_metadata_populated_enums(
    monkeypatch,
    engine,
    sut_type: Union[Type[StringDatapin], Type[StringArrayDatapin]],
    metadata_type: Union[Type[atvi.StringMetadata], Type[atvi.StringArrayMetadata]],
):
    # Set up
    mock_client = MockWorkflowClientForStringVarTest()
    mock_response = SetMetadataResponse()
    sut_element_id = ElementId(id_string="VAR_UNDER_TEST_ID")
    with unittest.mock.patch.object(
        mock_client, "StringVariableSetMetadata", return_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = sut_type(sut_element_id, engine=engine)
        new_metadata = metadata_type()
        new_metadata.enumerated_values = [atvi.StringValue("1"), atvi.StringValue("2")]
        new_metadata.enumerated_aliases = ["a", "b"]

        # Execute
        sut.set_metadata(new_metadata)

        # Verify
        expected_request = SetStringVariableMetadataRequest(target=sut_element_id)
        expected_request.new_metadata.base_metadata.description = ""
        expected_request.new_metadata.enum_values.MergeFrom(
            [atvi.StringValue("1"), atvi.StringValue("2")]
        )
        expected_request.new_metadata.enum_aliases.MergeFrom(["a", "b"])
        mock_grpc_method.assert_called_once_with(expected_request)


@pytest.mark.parametrize(
    "set_value,expected_value_in_request",
    [
        (atvi.StringValue(""), ""),
        (atvi.StringValue("This is a test string value."), "This is a test string value."),
        (
            atvi.StringValue("   leading and trailing whitespace   "),
            "   leading and trailing whitespace   ",
        ),
        (atvi.RealValue(-867.5309), "-867.5309"),
        (atvi.IntegerValue(47), "47"),
        (atvi.BooleanValue(True), "True"),
    ],
)
def test_scalar_set_allowed(monkeypatch, engine, set_value, expected_value_in_request) -> None:
    # Set up
    mock_client = MockWorkflowClientForStringVarTest()
    mock_response = SetVariableValueResponse()
    sut_element_id = ElementId(id_string="VAR_UNDER_TEST_ID")
    with unittest.mock.patch.object(
        mock_client, "StringVariableSetValue", retun_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = StringDatapin(sut_element_id, engine=engine)
        new_state = atvi.VariableState(set_value, True)

        # Execute
        sut.set_state(new_state)

        # Verify
        expected_request = SetStringValueRequest(
            target=sut_element_id, new_value=expected_value_in_request
        )
        mock_grpc_method.assert_called_once_with(expected_request)


@pytest.mark.parametrize(
    "set_value",
    [
        atvi.IntegerArrayValue(),
        atvi.RealArrayValue(),
        atvi.BooleanArrayValue(),
        atvi.StringArrayValue(),
    ],
)
def test_scalar_set_disallowed(monkeypatch, engine, set_value) -> None:
    # Set up
    mock_client = MockWorkflowClientForStringVarTest()
    mock_response = SetVariableValueResponse()
    sut_element_id = ElementId(id_string="VAR_UNDER_TEST_ID")
    with unittest.mock.patch.object(
        mock_client, "StringVariableSetValue", return_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = StringDatapin(sut_element_id, engine=engine)
        new_state = atvi.VariableState(set_value, True)

        # Execute / verify:
        with pytest.raises(TypeError):
            sut.set_state(new_state)

        # Verify
        mock_grpc_method.assert_not_called()


@pytest.mark.parametrize(
    "set_value,expected_value_in_request",
    [
        (
            atvi.StringArrayValue(shape_=(2, 2), values=[["string", "array"], ["test", "value"]]),
            StringArrayValue(
                dims=ArrayDimensions(dims=[2, 2]), values=["string", "array", "test", "value"]
            ),
        ),
        (
            atvi.BooleanArrayValue(shape_=(2, 2), values=[[True, False], [False, True]]),
            StringArrayValue(
                dims=ArrayDimensions(dims=[2, 2]), values=["True", "False", "False", "True"]
            ),
        ),
        (
            atvi.IntegerArrayValue(shape_=(2, 2), values=[[47, 9001], [1337, -9999]]),
            StringArrayValue(
                dims=ArrayDimensions(dims=[2, 2]), values=["47", "9001", "1337", "-9999"]
            ),
        ),
        (
            atvi.RealArrayValue(shape_=(2, 2), values=[[4.7, 9000.1], [13.37, -1.0]]),
            StringArrayValue(
                dims=ArrayDimensions(dims=[2, 2]), values=["4.7", "9000.1", "13.37", "-1.0"]
            ),
        ),
    ],
)
def test_array_set_allowed(monkeypatch, engine, set_value, expected_value_in_request) -> None:
    # Set up
    mock_client = MockWorkflowClientForStringVarTest()
    mock_response = SetVariableValueResponse()
    sut_element_id = ElementId(id_string="VAR_UNDER_TEST_ID")
    with unittest.mock.patch.object(
        mock_client, "StringArraySetValue", retun_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = StringArrayDatapin(sut_element_id, engine=engine)
        new_state = atvi.VariableState(set_value, True)

        # Execute
        sut.set_state(new_state)

        # Verify
        expected_request = SetStringArrayValueRequest(
            target=sut_element_id, new_value=expected_value_in_request
        )
        mock_grpc_method.assert_called_once_with(expected_request)


@pytest.mark.parametrize(
    "set_value",
    [
        atvi.IntegerValue(0),
        atvi.RealValue(0.0),
        atvi.BooleanValue(True),
        atvi.StringValue("scalar"),
    ],
)
def test_array_set_disallowed(monkeypatch, engine, set_value) -> None:
    # Set up
    mock_client = MockWorkflowClientForStringVarTest()
    mock_response = SetVariableValueResponse()
    sut_element_id = ElementId(id_string="VAR_UNDER_TEST_ID")
    with unittest.mock.patch.object(
        mock_client, "StringArraySetValue", return_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = StringArrayDatapin(sut_element_id, engine=engine)
        new_state = atvi.VariableState(set_value, True)

        # Execute / verify:
        with pytest.raises(TypeError):
            sut.set_state(new_state)

        # Verify
        mock_grpc_method.assert_not_called()


def test_scalar_get_type(monkeypatch, engine) -> None:
    do_get_type_test(
        monkeypatch,
        engine,
        StringDatapin,
        VariableType.VARIABLE_TYPE_STRING,
        atvi.VariableType.STRING,
    )


def test_array_get_type(monkeypatch, engine) -> None:
    do_get_type_test(
        monkeypatch,
        engine,
        StringArrayDatapin,
        VariableType.VARIABLE_TYPE_STRING_ARRAY,
        atvi.VariableType.STRING_ARRAY,
    )


@pytest.mark.parametrize(
    "value_in_response,validity_in_response,expected_acvi_state",
    [
        ("", True, atvi.VariableState(atvi.StringValue(""), True)),
        ("test string", False, atvi.VariableState(atvi.StringValue("test string"), False)),
        ("(╯°□°）╯︵ ┻━┻", True, atvi.VariableState(atvi.StringValue("(╯°□°）╯︵ ┻━┻"), True)),
    ],
)
def test_scalar_get_state(
    monkeypatch, engine, value_in_response, validity_in_response, expected_acvi_state
) -> None:
    do_get_state_test(
        monkeypatch,
        engine,
        StringDatapin,
        VariableState(
            is_valid=validity_in_response, value=VariableValue(string_value=value_in_response)
        ),
        expected_acvi_state,
    )


def test_scalar_get_state_with_hid(monkeypatch, engine):
    do_get_state_test_with_hid(monkeypatch, engine, StringDatapin)


def test_array_get_state_with_hid(monkeypatch, engine):
    do_get_state_test_with_hid(monkeypatch, engine, StringArrayDatapin)


@pytest.mark.parametrize(
    "value_in_response,validity_in_response,expected_acvi_state",
    [
        (
            StringArrayValue(
                dims=ArrayDimensions(dims=[2, 2]),
                values=["primary", "secondary", "first", "second"],
            ),
            True,
            atvi.VariableState(
                atvi.StringArrayValue(
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
            atvi.VariableState(
                atvi.StringArrayValue(shape_=(2, 2), values=[["one", "two"], ["three", "four"]]),
                False,
            ),
        ),
    ],
)
def test_array_get_state(
    monkeypatch, engine, value_in_response, validity_in_response, expected_acvi_state
) -> None:
    do_get_state_test(
        monkeypatch,
        engine,
        StringArrayDatapin,
        VariableState(
            is_valid=validity_in_response, value=VariableValue(string_array_value=value_in_response)
        ),
        expected_acvi_state,
    )


@pytest.mark.parametrize(
    "sut_type, flag_in_response",
    [
        (StringDatapin, True),
        (StringDatapin, False),
        (StringArrayDatapin, True),
        (StringArrayDatapin, False),
    ],
)
def test_is_input_component(monkeypatch, engine, sut_type, flag_in_response) -> None:
    do_test_is_input_component(monkeypatch, engine, sut_type, flag_in_response)


@pytest.mark.parametrize(
    "sut_type, flag_in_response",
    [
        (StringDatapin, True),
        (StringDatapin, False),
        (StringArrayDatapin, True),
        (StringArrayDatapin, False),
    ],
)
def test_is_input_workflow(monkeypatch, engine, sut_type, flag_in_response) -> None:
    do_test_is_input_workflow(monkeypatch, engine, sut_type, flag_in_response)
