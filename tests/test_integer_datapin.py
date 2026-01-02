# Copyright (C) 2022 - 2026 ANSYS, Inc. and/or its affiliates.
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

from typing import Optional, Type, Union
import unittest

from ansys.api.modelcenter.v0.element_messages_pb2 import ElementId
from ansys.api.modelcenter.v0.variable_value_messages_pb2 import (
    ArrayDimensions,
    IntegerArrayValue,
    IntegerVariableMetadata,
    NumericVariableMetadata,
    SetIntegerArrayValueRequest,
    SetIntegerValueRequest,
    SetIntegerVariableMetadataRequest,
    SetMetadataResponse,
    SetVariableValueResponse,
    VariableState,
    VariableType,
    VariableValue,
)
import ansys.tools.variableinterop as atvi
import pytest

from ansys.modelcenter.workflow.grpc_modelcenter.abstract_workflow_element import (
    AbstractWorkflowElement,
)
from ansys.modelcenter.workflow.grpc_modelcenter.integer_datapin import (
    IntegerArrayDatapin,
    IntegerDatapin,
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


class MockWorkflowClientForIntegerVarTest:
    def __init__(self):
        pass

    def IntegerVariableSetMetadata(
        self, request: SetIntegerVariableMetadataRequest
    ) -> SetMetadataResponse:
        return SetMetadataResponse()

    def IntegerVariableGetMetadata(self, request: ElementId) -> IntegerVariableMetadata:
        return IntegerVariableMetadata()

    def IntegerVariableSetValue(self, request: SetIntegerValueRequest) -> SetVariableValueResponse:
        return SetVariableValueResponse()

    def IntegerArraySetValue(
        self, request: SetIntegerArrayValueRequest
    ) -> SetVariableValueResponse:
        return SetVariableValueResponse()


@pytest.mark.parametrize(
    "description_string,sut_type,expected_metadata_type",
    [
        ("", IntegerDatapin, atvi.IntegerMetadata),
        ("This is a mock datapin description.", IntegerDatapin, atvi.IntegerMetadata),
        ("", IntegerArrayDatapin, atvi.IntegerArrayMetadata),
        ("This is a mock datapin description.", IntegerArrayDatapin, atvi.IntegerArrayMetadata),
    ],
)
def test_retrieved_metadata_should_include_description(
    monkeypatch,
    engine,
    description_string: str,
    sut_type: Union[Type[IntegerDatapin], Type[IntegerArrayDatapin]],
    expected_metadata_type: Union[Type[atvi.IntegerMetadata], Type[atvi.IntegerArrayMetadata]],
):
    # Set up
    mock_client = MockWorkflowClientForIntegerVarTest()
    mock_response = IntegerVariableMetadata()
    sut_element_id = ElementId(id_string="VAR_UNDER_TEST_ID")
    mock_response.base_metadata.description = description_string
    with unittest.mock.patch.object(
        mock_client, "IntegerVariableGetMetadata", return_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = sut_type(sut_element_id, engine=engine)

        # Execute
        result: atvi.IntegerMetadata = sut.get_metadata()

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
    [(IntegerDatapin, atvi.IntegerMetadata), (IntegerArrayDatapin, atvi.IntegerArrayMetadata)],
)
def test_retrieved_metadata_should_include_custom_metadata_empty(
    monkeypatch,
    engine,
    sut_type: Union[Type[IntegerDatapin], Type[IntegerArrayDatapin]],
    expected_metadata_type: Union[Type[atvi.IntegerMetadata], Type[atvi.IntegerArrayMetadata]],
):
    # Set up
    mock_client = MockWorkflowClientForIntegerVarTest()
    mock_response = IntegerVariableMetadata()
    sut_element_id = ElementId(id_string="VAR_UNDER_TEST_ID")
    with unittest.mock.patch.object(
        mock_client, "IntegerVariableGetMetadata", return_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = sut_type(sut_element_id, engine=engine)

        # Execute
        result: atvi.IntegerMetadata = sut.get_metadata()

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
    [(IntegerDatapin, atvi.IntegerMetadata), (IntegerArrayDatapin, atvi.IntegerArrayMetadata)],
)
def test_retrieved_metadata_should_include_custom_metadata_populated(
    monkeypatch,
    engine,
    sut_type: Union[Type[IntegerDatapin], Type[IntegerArrayDatapin]],
    expected_metadata_type: Union[Type[atvi.IntegerMetadata], Type[atvi.IntegerArrayMetadata]],
):
    # Set up
    mock_client = MockWorkflowClientForIntegerVarTest()
    mock_response = IntegerVariableMetadata()
    mock_response.base_metadata.custom_metadata["test_integer_value"].MergeFrom(
        VariableValue(int_value=47)
    )
    mock_response.base_metadata.custom_metadata["test_double_value"].MergeFrom(
        VariableValue(double_value=-867.5309)
    )
    sut_element_id = ElementId(id_string="VAR_UNDER_TEST_ID")
    with unittest.mock.patch.object(
        mock_client, "IntegerVariableGetMetadata", return_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = sut_type(sut_element_id, engine=engine)

        # Execute
        result: atvi.IntegerMetadata = sut.get_metadata()

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
    [(IntegerDatapin, atvi.IntegerMetadata), (IntegerArrayDatapin, atvi.IntegerArrayMetadata)],
)
def test_retrieved_metadata_includes_unsupported_type(
    monkeypatch,
    engine,
    sut_type: Union[Type[IntegerDatapin], Type[IntegerArrayDatapin]],
    expected_metadata_type: Union[Type[atvi.IntegerMetadata], Type[atvi.IntegerArrayMetadata]],
):
    # Set up
    mock_client = MockWorkflowClientForIntegerVarTest()
    mock_response = IntegerVariableMetadata()
    mock_response.base_metadata.custom_metadata["test_unsupported"].MergeFrom(VariableValue())
    sut_element_id = ElementId(id_string="VAR_UNDER_TEST_ID")
    with unittest.mock.patch.object(
        mock_client, "IntegerVariableGetMetadata", return_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = sut_type(sut_element_id, engine=engine)

        # Execute / Verify
        with pytest.raises(CustomMetadataValueNotSupportedError, match="unsupported type"):
            sut.get_metadata()

        # Verify
        mock_grpc_method.assert_called_once_with(sut_element_id)


@pytest.mark.parametrize(
    "sut_type,expected_metadata_type,upper_bound,set_upper_bound,expected_upper_bound,"
    "lower_bound,set_lower_bound,expected_lower_bound",
    [
        (IntegerDatapin, atvi.IntegerMetadata, 0, False, None, 0, False, None),
        (IntegerDatapin, atvi.IntegerMetadata, -47, True, -47, 9000, True, 9000),
        (IntegerDatapin, atvi.IntegerMetadata, 0, False, None, 9000, True, 9000),
        (IntegerDatapin, atvi.IntegerMetadata, -47, True, -47, 0, False, None),
        (IntegerArrayDatapin, atvi.IntegerArrayMetadata, 0, False, None, 0, False, None),
        (IntegerArrayDatapin, atvi.IntegerArrayMetadata, -47, True, -47, 9000, True, 9000),
        (IntegerArrayDatapin, atvi.IntegerArrayMetadata, 0, False, None, 9000, True, 9000),
        (IntegerArrayDatapin, atvi.IntegerArrayMetadata, -47, True, -47, 0, False, None),
    ],
)
def test_retrieved_metadata_should_convert_bounds(
    monkeypatch,
    engine,
    sut_type: Union[Type[IntegerDatapin], Type[IntegerArrayDatapin]],
    expected_metadata_type: Union[Type[atvi.IntegerMetadata], Type[atvi.IntegerArrayMetadata]],
    upper_bound: int,
    set_upper_bound: bool,
    expected_upper_bound: Optional[int],
    lower_bound: int,
    set_lower_bound: bool,
    expected_lower_bound: Optional[int],
):
    # Set up
    mock_client = MockWorkflowClientForIntegerVarTest()
    mock_response = IntegerVariableMetadata()
    if set_upper_bound:
        mock_response.upper_bound = upper_bound
    if set_lower_bound:
        mock_response.lower_bound = lower_bound
    sut_element_id = ElementId(id_string="VAR_UNDER_TEST_ID")
    with unittest.mock.patch.object(
        mock_client, "IntegerVariableGetMetadata", return_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = sut_type(sut_element_id, engine=engine)

        # Execute
        result: atvi.IntegerMetadata = sut.get_metadata()

        # Verify
        mock_grpc_method.assert_called_once_with(sut_element_id)
        assert isinstance(
            result, expected_metadata_type
        ), "The metadata should have the correct type."
        assert (
            result.lower_bound == expected_lower_bound
        ), "The lower bound should be correctly set."
        assert (
            result.upper_bound == expected_upper_bound
        ), "The upper bound should be correctly set."


@pytest.mark.parametrize(
    "sut_type",
    [
        IntegerDatapin,
        IntegerArrayDatapin,
    ],
)
def test_set_metadata_invalid_custom_metadata(
    monkeypatch, engine, sut_type: Union[Type[IntegerDatapin], Type[IntegerArrayDatapin]]
):
    # Set up
    mock_client = MockWorkflowClientForIntegerVarTest()
    mock_response = SetMetadataResponse()
    sut_element_id = ElementId(id_string="VAR_UNDER_TEST_ID")
    with unittest.mock.patch.object(
        mock_client, "IntegerVariableSetMetadata", return_value=mock_response
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
        ("", IntegerDatapin, atvi.IntegerMetadata),
        ("This is a mock datapin description.", IntegerDatapin, atvi.IntegerMetadata),
        ("", IntegerArrayDatapin, atvi.IntegerArrayMetadata),
        ("This is a mock datapin description.", IntegerArrayDatapin, atvi.IntegerArrayMetadata),
    ],
)
def test_set_metadata_empty_custom_metadata(
    monkeypatch,
    engine,
    description: str,
    sut_type: Union[Type[IntegerDatapin], Type[IntegerArrayDatapin]],
    metadata_type: Union[Type[atvi.IntegerMetadata], Type[atvi.IntegerArrayMetadata]],
):
    # Set up
    mock_client = MockWorkflowClientForIntegerVarTest()
    mock_response = SetMetadataResponse()
    sut_element_id = ElementId(id_string="VAR_UNDER_TEST_ID")
    with unittest.mock.patch.object(
        mock_client, "IntegerVariableSetMetadata", return_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = sut_type(sut_element_id, engine=engine)
        new_metadata = metadata_type()
        new_metadata.description = description

        # Execute
        sut.set_metadata(new_metadata)

        # Verify
        expected_request = SetIntegerVariableMetadataRequest(target=sut_element_id)
        expected_request.new_metadata.base_metadata.description = description
        expected_request.new_metadata.numeric_metadata.MergeFrom(
            NumericVariableMetadata(units="", display_format="")
        )
        mock_grpc_method.assert_called_once_with(expected_request)


@pytest.mark.parametrize(
    "description,sut_type,metadata_type",
    [
        ("", IntegerDatapin, atvi.IntegerMetadata),
        ("This is a mock datapin description.", IntegerDatapin, atvi.IntegerMetadata),
        ("", IntegerArrayDatapin, atvi.IntegerArrayMetadata),
        ("This is a mock datapin description.", IntegerArrayDatapin, atvi.IntegerArrayMetadata),
    ],
)
def test_set_metadata_populated_custom_metadata(
    monkeypatch,
    engine,
    description: str,
    sut_type: Union[Type[IntegerDatapin], Type[IntegerArrayDatapin]],
    metadata_type: Union[Type[atvi.IntegerMetadata], Type[atvi.IntegerArrayMetadata]],
):
    # Set up
    mock_client = MockWorkflowClientForIntegerVarTest()
    mock_response = SetMetadataResponse()
    sut_element_id = ElementId(id_string="VAR_UNDER_TEST_ID")
    with unittest.mock.patch.object(
        mock_client, "IntegerVariableSetMetadata", return_value=mock_response
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
        expected_request = SetIntegerVariableMetadataRequest(target=sut_element_id)
        expected_request.new_metadata.base_metadata.description = description
        expected_request.new_metadata.numeric_metadata.MergeFrom(
            NumericVariableMetadata(units="", display_format="")
        )
        expected_request.new_metadata.base_metadata.custom_metadata["int_value"].MergeFrom(
            VariableValue(int_value=47)
        )
        expected_request.new_metadata.base_metadata.custom_metadata["real_value"].MergeFrom(
            VariableValue(double_value=-867.5309)
        )
        mock_grpc_method.assert_called_once_with(expected_request)


@pytest.mark.parametrize(
    "sut_type,metadata_type,original_lower_bound,expected_lower_bound,expected_lower_bound_set,"
    "original_upper_bound,expected_upper_bound,expected_upper_bound_set",
    [
        (IntegerDatapin, atvi.IntegerMetadata, None, 0, False, None, 0, False),
        (IntegerDatapin, atvi.IntegerMetadata, -47, -47, True, 9001, 9001, True),
        (IntegerDatapin, atvi.IntegerMetadata, None, 0, False, 9001, 9001, True),
        (IntegerDatapin, atvi.IntegerMetadata, -47, -47, True, None, 0, False),
        (IntegerArrayDatapin, atvi.IntegerArrayMetadata, None, 0, False, None, 0, False),
        (IntegerArrayDatapin, atvi.IntegerArrayMetadata, -47, -47, True, 9001, 9001, True),
        (IntegerArrayDatapin, atvi.IntegerArrayMetadata, None, 0, False, 9001, 9001, True),
        (IntegerArrayDatapin, atvi.IntegerArrayMetadata, -47, -47, True, None, 0, False),
    ],
)
def test_set_metadata_should_convert_bounds(
    monkeypatch,
    engine,
    sut_type: Union[Type[IntegerDatapin], Type[IntegerArrayDatapin]],
    metadata_type: Union[Type[atvi.IntegerMetadata], Type[atvi.IntegerArrayMetadata]],
    original_lower_bound: Optional[int],
    expected_lower_bound: int,
    expected_lower_bound_set: bool,
    original_upper_bound: Optional[int],
    expected_upper_bound: int,
    expected_upper_bound_set: bool,
):
    # Set up
    mock_client = MockWorkflowClientForIntegerVarTest()
    mock_response = SetMetadataResponse()
    sut_element_id = ElementId(id_string="VAR_UNDER_TEST_ID")
    with unittest.mock.patch.object(
        mock_client, "IntegerVariableSetMetadata", return_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = sut_type(sut_element_id, engine=engine)
        new_metadata = metadata_type()
        new_metadata.lower_bound = original_lower_bound
        new_metadata.upper_bound = original_upper_bound

        # Execute
        sut.set_metadata(new_metadata)

        # Verify
        expected_request = SetIntegerVariableMetadataRequest(target=sut_element_id)
        expected_request.new_metadata.base_metadata.description = ""
        if expected_upper_bound_set:
            expected_request.new_metadata.upper_bound = expected_upper_bound
        if expected_lower_bound_set:
            expected_request.new_metadata.lower_bound = expected_lower_bound
        expected_request.new_metadata.numeric_metadata.MergeFrom(
            NumericVariableMetadata(units="", display_format="")
        )
        mock_grpc_method.assert_called_once_with(expected_request)


@pytest.mark.parametrize(
    "sut_type,metadata_type",
    [
        (IntegerDatapin, atvi.IntegerMetadata),
        (IntegerArrayDatapin, atvi.IntegerArrayMetadata),
    ],
)
def test_set_metadata_populated_enums(
    monkeypatch,
    engine,
    sut_type: Union[Type[IntegerDatapin], Type[IntegerArrayDatapin]],
    metadata_type: Union[Type[atvi.IntegerMetadata], Type[atvi.IntegerArrayMetadata]],
):
    # Set up
    mock_client = MockWorkflowClientForIntegerVarTest()
    mock_response = SetMetadataResponse()
    sut_element_id = ElementId(id_string="VAR_UNDER_TEST_ID")
    with unittest.mock.patch.object(
        mock_client, "IntegerVariableSetMetadata", return_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = sut_type(sut_element_id, engine=engine)
        new_metadata = metadata_type()
        new_metadata.enumerated_values = [atvi.IntegerValue(1), atvi.IntegerValue(2)]
        new_metadata.enumerated_aliases = ["a", "b"]

        # Execute
        sut.set_metadata(new_metadata)

        # Verify
        expected_request = SetIntegerVariableMetadataRequest(target=sut_element_id)
        expected_request.new_metadata.base_metadata.description = ""
        expected_request.new_metadata.enum_values.MergeFrom(
            [atvi.IntegerValue(1), atvi.IntegerValue(2)]
        )
        expected_request.new_metadata.enum_aliases.MergeFrom(["a", "b"])
        expected_request.new_metadata.numeric_metadata.MergeFrom(
            NumericVariableMetadata(units="", display_format="")
        )
        mock_grpc_method.assert_called_once_with(expected_request)


@pytest.mark.parametrize(
    "set_value,expected_value_in_request",
    [
        (atvi.IntegerValue(-47), -47),
        (atvi.IntegerValue(47), 47),
        (atvi.BooleanValue(True), 1),
        (atvi.BooleanValue(False), 0),
    ],
)
def test_scalar_set_allowed(monkeypatch, engine, set_value, expected_value_in_request):
    # Set up
    mock_client = MockWorkflowClientForIntegerVarTest()
    mock_response = SetVariableValueResponse()
    sut_element_id = ElementId(id_string="VAR_UNDER_TEST_ID")
    with unittest.mock.patch.object(
        mock_client, "IntegerVariableSetValue", retun_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = IntegerDatapin(sut_element_id, engine=engine)
        new_state = atvi.VariableState(set_value, True)

        # Execute
        sut.set_state(new_state)

        # Verify
        expected_request = SetIntegerValueRequest(
            target=sut_element_id, new_value=expected_value_in_request
        )
        mock_grpc_method.assert_called_once_with(expected_request)


@pytest.mark.parametrize(
    "set_value",
    [
        atvi.RealValue(4.0),
        atvi.StringValue("47"),
        atvi.IntegerArrayValue(),
        atvi.RealArrayValue(),
        atvi.BooleanArrayValue(),
        atvi.StringArrayValue(),
    ],
)
def test_scalar_set_disallowed(monkeypatch, engine, set_value):
    # Set up
    mock_client = MockWorkflowClientForIntegerVarTest()
    mock_response = SetVariableValueResponse()
    sut_element_id = ElementId(id_string="VAR_UNDER_TEST_ID")
    with unittest.mock.patch.object(
        mock_client, "IntegerVariableSetValue", return_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = IntegerDatapin(sut_element_id, engine=engine)
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
            atvi.IntegerArrayValue(shape_=(2, 2), values=[[101, 102], [201, 202]]),
            IntegerArrayValue(dims=ArrayDimensions(dims=[2, 2]), values=[101, 102, 201, 202]),
        ),
        (
            atvi.BooleanArrayValue(shape_=(2, 2), values=[[True, False], [False, True]]),
            IntegerArrayValue(dims=ArrayDimensions(dims=[2, 2]), values=[1, 0, 0, 1]),
        ),
    ],
)
def test_array_set_allowed(monkeypatch, engine, set_value, expected_value_in_request):
    # Set up
    mock_client = MockWorkflowClientForIntegerVarTest()
    mock_response = SetVariableValueResponse()
    sut_element_id = ElementId(id_string="VAR_UNDER_TEST_ID")
    with unittest.mock.patch.object(
        mock_client, "IntegerArraySetValue", retun_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = IntegerArrayDatapin(sut_element_id, engine=engine)
        new_state = atvi.VariableState(set_value, True)

        # Execute
        sut.set_state(new_state)

        # Verify
        expected_request = SetIntegerArrayValueRequest(
            target=sut_element_id, new_value=expected_value_in_request
        )
        mock_grpc_method.assert_called_once_with(expected_request)


@pytest.mark.parametrize(
    "set_value",
    [
        atvi.IntegerValue(0),
        atvi.RealValue(0.0),
        atvi.BooleanValue(True),
        atvi.StringValue("0"),
        atvi.RealArrayValue(),
        atvi.StringArrayValue(),
    ],
)
def test_array_set_disallowed(monkeypatch, engine, set_value):
    # Set up
    mock_client = MockWorkflowClientForIntegerVarTest()
    mock_response = SetVariableValueResponse()
    sut_element_id = ElementId(id_string="VAR_UNDER_TEST_ID")
    with unittest.mock.patch.object(
        mock_client, "IntegerArraySetValue", return_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = IntegerArrayDatapin(sut_element_id, engine=engine)
        new_state = atvi.VariableState(set_value, True)

        # Execute / verify:
        with pytest.raises(TypeError):
            sut.set_state(new_state)

        # Verify
        mock_grpc_method.assert_not_called()


def test_scalar_get_type(monkeypatch, engine):
    do_get_type_test(
        monkeypatch,
        engine,
        IntegerDatapin,
        VariableType.VARIABLE_TYPE_INTEGER,
        atvi.VariableType.INTEGER,
    )


def test_array_get_type(monkeypatch, engine):
    do_get_type_test(
        monkeypatch,
        engine,
        IntegerArrayDatapin,
        VariableType.VARIABLE_TYPE_INTEGER_ARRAY,
        atvi.VariableType.INTEGER_ARRAY,
    )


@pytest.mark.parametrize(
    "value_in_response,validity_in_response,expected_acvi_state",
    [
        (47, True, atvi.VariableState(atvi.IntegerValue(47), True)),
        (-8675309, False, atvi.VariableState(atvi.IntegerValue(-8675309), False)),
        (0, True, atvi.VariableState(atvi.IntegerValue(0), True)),
        (1, False, atvi.VariableState(atvi.IntegerValue(1), False)),
    ],
)
def test_scalar_get_state(
    monkeypatch, engine, value_in_response, validity_in_response, expected_acvi_state
):
    do_get_state_test(
        monkeypatch,
        engine,
        IntegerDatapin,
        VariableState(
            is_valid=validity_in_response, value=VariableValue(int_value=value_in_response)
        ),
        expected_acvi_state,
    )


def test_scalar_get_state_with_hid(monkeypatch, engine):
    do_get_state_test_with_hid(monkeypatch, engine, IntegerDatapin)


def test_array_get_state_with_hid(monkeypatch, engine):
    do_get_state_test_with_hid(monkeypatch, engine, IntegerArrayDatapin)


@pytest.mark.parametrize(
    "value_in_response,validity_in_response,expected_acvi_state",
    [
        (
            IntegerArrayValue(dims=ArrayDimensions(dims=[2, 2]), values=[-8675309, 47, -1, 0]),
            True,
            atvi.VariableState(
                atvi.IntegerArrayValue(shape_=(2, 2), values=[[-8675309, 47], [-1, 0]]), True
            ),
        ),
        (
            IntegerArrayValue(dims=ArrayDimensions(dims=[2, 2]), values=[101, 102, 201, 202]),
            False,
            atvi.VariableState(
                atvi.IntegerArrayValue(shape_=(2, 2), values=[[101, 102], [201, 202]]), False
            ),
        ),
    ],
)
def test_array_get_state(
    monkeypatch, engine, value_in_response, validity_in_response, expected_acvi_state
):
    do_get_state_test(
        monkeypatch,
        engine,
        IntegerArrayDatapin,
        VariableState(
            is_valid=validity_in_response, value=VariableValue(int_array_value=value_in_response)
        ),
        expected_acvi_state,
    )


@pytest.mark.parametrize(
    "sut_type, flag_in_response",
    [
        (IntegerDatapin, True),
        (IntegerDatapin, False),
        (IntegerArrayDatapin, True),
        (IntegerArrayDatapin, False),
    ],
)
def test_is_input_component(monkeypatch, engine, sut_type, flag_in_response):
    do_test_is_input_component(monkeypatch, engine, sut_type, flag_in_response)


@pytest.mark.parametrize(
    "sut_type, flag_in_response",
    [
        (IntegerDatapin, True),
        (IntegerDatapin, False),
        (IntegerArrayDatapin, True),
        (IntegerArrayDatapin, False),
    ],
)
def test_is_input_workflow(monkeypatch, engine, sut_type, flag_in_response):
    do_test_is_input_workflow(monkeypatch, engine, sut_type, flag_in_response)
