from typing import Literal
import unittest

import ansys.common.variableinterop as acvi
import pytest

from ansys.modelcenter.workflow.grpc_modelcenter.abstract_workflow_element import (
    AbstractWorkflowElement,
)
from ansys.modelcenter.workflow.grpc_modelcenter.boolean_variable import (
    BooleanArray,
    BooleanVariable,
)
from ansys.modelcenter.workflow.grpc_modelcenter.proto.element_messages_pb2 import ElementId
from ansys.modelcenter.workflow.grpc_modelcenter.proto.variable_value_messages_pb2 import (
    ArrayDimensions,
    BooleanArrayValue,
    BooleanVariableMetadata,
    FileValue,
    SetBooleanArrayValueRequest,
    SetBooleanValueRequest,
    SetBooleanVariableMetadataRequest,
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
from .test_variable import (
    do_get_state_test,
    do_get_type_test,
    do_test_is_input_component,
    do_test_is_input_workflow,
)


class MockWorkflowClientForBooleanVarTest:
    def __init__(self):
        pass

    def BooleanVariableSetMetadata(
        self, request: SetBooleanVariableMetadataRequest
    ) -> SetMetadataResponse:
        return SetMetadataResponse()

    def BooleanVariableGetMetadata(self, request: ElementId) -> BooleanVariableMetadata:
        return BooleanVariableMetadata()

    def BooleanVariableSetValue(self, request: SetBooleanValueRequest) -> SetVariableValueResponse:
        return SetVariableValueResponse()

    def BooleanArraySetValue(self, request: SetBooleanValueRequest) -> SetVariableValueResponse:
        return SetVariableValueResponse()


@pytest.mark.parametrize(
    "description_string,sut_type,expected_metadata_type",
    [
        ("", BooleanVariable, acvi.BooleanMetadata),
        ("This is a mock variable description.", BooleanVariable, acvi.BooleanMetadata),
        ("", BooleanArray, acvi.BooleanArrayMetadata),
        ("This is a mock variable description.", BooleanArray, acvi.BooleanArrayMetadata),
    ],
)
def test_retrieved_metadata_should_include_description(
    monkeypatch,
    description_string: str,
    sut_type: Literal[BooleanVariable, BooleanArray],
    expected_metadata_type: Literal[acvi.BooleanMetadata, acvi.BooleanArrayMetadata],
):
    # Set up
    mock_client = MockWorkflowClientForBooleanVarTest()
    mock_response = BooleanVariableMetadata()
    sut_element_id = ElementId(id_string="VAR_UNDER_TEST_ID")
    mock_response.base_metadata.description = description_string
    with unittest.mock.patch.object(
        mock_client, "BooleanVariableGetMetadata", return_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = sut_type(sut_element_id, None)

        # Execute
        result: acvi.BooleanMetadata = sut.get_metadata()

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
    [(BooleanVariable, acvi.BooleanMetadata), (BooleanArray, acvi.BooleanArrayMetadata)],
)
def test_retrieved_metadata_should_include_custom_metadata_empty(
    monkeypatch,
    sut_type: Literal[BooleanVariable, BooleanArray],
    expected_metadata_type: Literal[acvi.BooleanMetadata, acvi.BooleanArrayMetadata],
):
    # Set up
    mock_client = MockWorkflowClientForBooleanVarTest()
    mock_response = BooleanVariableMetadata()
    sut_element_id = ElementId(id_string="VAR_UNDER_TEST_ID")
    with unittest.mock.patch.object(
        mock_client, "BooleanVariableGetMetadata", return_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = sut_type(sut_element_id, None)

        # Execute
        result: acvi.BooleanMetadata = sut.get_metadata()

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
    [(BooleanVariable, acvi.BooleanMetadata), (BooleanArray, acvi.BooleanArrayMetadata)],
)
def test_retrieved_metadata_should_include_custom_metadata_populated(
    monkeypatch,
    sut_type: Literal[BooleanVariable, BooleanArray],
    expected_metadata_type: Literal[acvi.BooleanMetadata, acvi.BooleanArrayMetadata],
):
    # Set up
    mock_client = MockWorkflowClientForBooleanVarTest()
    mock_response = BooleanVariableMetadata()
    mock_response.base_metadata.custom_metadata["test_integer_value"].MergeFrom(
        VariableValue(int_value=47)
    )
    mock_response.base_metadata.custom_metadata["test_double_value"].MergeFrom(
        VariableValue(double_value=-867.5309)
    )
    sut_element_id = ElementId(id_string="VAR_UNDER_TEST_ID")
    with unittest.mock.patch.object(
        mock_client, "BooleanVariableGetMetadata", return_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = sut_type(sut_element_id, None)

        # Execute
        result: acvi.BooleanMetadata = sut.get_metadata()

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
    [(BooleanVariable, acvi.BooleanMetadata), (BooleanArray, acvi.BooleanArrayMetadata)],
)
def test_retrieved_metadata_includes_unsupported_type(
    monkeypatch,
    sut_type: Literal[BooleanVariable, BooleanArray],
    expected_metadata_type: Literal[acvi.BooleanMetadata, acvi.BooleanArrayMetadata],
):
    # Set up
    mock_client = MockWorkflowClientForBooleanVarTest()
    mock_response = BooleanVariableMetadata()
    mock_response.base_metadata.custom_metadata["test_unsupported"].MergeFrom(
        VariableValue(file_value=FileValue())
    )
    sut_element_id = ElementId(id_string="VAR_UNDER_TEST_ID")
    with unittest.mock.patch.object(
        mock_client, "BooleanVariableGetMetadata", return_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = sut_type(sut_element_id, None)

        # Execute / Verify
        with pytest.raises(CustomMetadataValueNotSupportedError, match="unsupported type"):
            sut.get_metadata()

        # Verify
        mock_grpc_method.assert_called_once_with(sut_element_id)


@pytest.mark.parametrize(
    "description,sut_type,metadata_type",
    [
        ("", BooleanVariable, acvi.BooleanMetadata),
        ("This is a mock variable description.", BooleanVariable, acvi.BooleanMetadata),
        ("", BooleanArray, acvi.BooleanArrayMetadata),
        ("This is a mock variable description.", BooleanArray, acvi.BooleanArrayMetadata),
    ],
)
def test_set_metadata_empty_custom_metadata(
    monkeypatch,
    description: str,
    sut_type: Literal[BooleanVariable, BooleanArray],
    metadata_type: Literal[acvi.BooleanMetadata, acvi.BooleanArrayMetadata],
):
    # Set up
    mock_client = MockWorkflowClientForBooleanVarTest()
    mock_response = SetMetadataResponse()
    sut_element_id = ElementId(id_string="VAR_UNDER_TEST_ID")
    with unittest.mock.patch.object(
        mock_client, "BooleanVariableSetMetadata", return_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = sut_type(sut_element_id, None)
        new_metadata = metadata_type()
        new_metadata.description = description

        # Execute
        sut.set_metadata(new_metadata)

        # Verify
        expected_request = SetBooleanVariableMetadataRequest(target=sut_element_id)
        expected_request.new_metadata.base_metadata.description = description
        mock_grpc_method.assert_called_once_with(expected_request)


@pytest.mark.parametrize(
    "description,sut_type,metadata_type",
    [
        ("", BooleanVariable, acvi.BooleanMetadata),
        ("This is a mock variable description.", BooleanVariable, acvi.BooleanMetadata),
        ("", BooleanArray, acvi.BooleanArrayMetadata),
        ("This is a mock variable description.", BooleanArray, acvi.BooleanArrayMetadata),
    ],
)
def test_set_metadata_populated_custom_metadata(
    monkeypatch,
    description: str,
    sut_type: Literal[BooleanVariable, BooleanArray],
    metadata_type: Literal[acvi.BooleanMetadata, acvi.BooleanArrayMetadata],
):
    # Set up
    mock_client = MockWorkflowClientForBooleanVarTest()
    mock_response = SetMetadataResponse()
    sut_element_id = ElementId(id_string="VAR_UNDER_TEST_ID")
    with unittest.mock.patch.object(
        mock_client, "BooleanVariableSetMetadata", return_value=mock_response
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
        expected_request = SetBooleanVariableMetadataRequest(target=sut_element_id)
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
    [(acvi.BooleanValue(True), True), (acvi.BooleanValue(False), False)],
)
def test_scalar_set_allowed(monkeypatch, set_value, expected_value_in_request):
    # Set up
    mock_client = MockWorkflowClientForBooleanVarTest()
    mock_response = SetVariableValueResponse()
    sut_element_id = ElementId(id_string="VAR_UNDER_TEST_ID")
    with unittest.mock.patch.object(
        mock_client, "BooleanVariableSetValue", retun_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = BooleanVariable(sut_element_id, None)
        new_value = acvi.VariableState(set_value, True)

        # Execute
        sut.set_value(new_value)

        # Verify
        expected_request = SetBooleanValueRequest(
            target=sut_element_id, new_value=expected_value_in_request
        )
        mock_grpc_method.assert_called_once_with(expected_request)


@pytest.mark.parametrize(
    "set_value",
    [
        acvi.IntegerValue(0),
        acvi.RealValue(0.0),
        acvi.StringValue("False"),
        acvi.IntegerArrayValue(),
        acvi.RealArrayValue(),
        acvi.BooleanArrayValue(),
        acvi.StringArrayValue(),
    ],
)
def test_scalar_set_disallowed(monkeypatch, set_value):
    # Set up
    mock_client = MockWorkflowClientForBooleanVarTest()
    mock_response = SetVariableValueResponse()
    sut_element_id = ElementId(id_string="VAR_UNDER_TEST_ID")
    with unittest.mock.patch.object(
        mock_client, "BooleanVariableSetValue", return_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = BooleanVariable(sut_element_id, None)
        new_value = acvi.VariableState(set_value, True)

        # Execute / verify:
        with pytest.raises(acvi.IncompatibleTypesException):
            sut.set_value(new_value)

        # Verify
        mock_grpc_method.assert_not_called()


@pytest.mark.parametrize(
    "set_value,expected_value_in_request",
    [
        (
            acvi.BooleanArrayValue(shape_=(0,)),
            BooleanArrayValue(dims=ArrayDimensions(dims=[0]), values=[]),
        ),
        (
            acvi.BooleanArrayValue(shape_=(2, 2), values=[[True, False], [False, True]]),
            BooleanArrayValue(dims=ArrayDimensions(dims=[2, 2]), values=[True, False, False, True]),
        ),
    ],
)
def test_array_set_allowed(monkeypatch, set_value, expected_value_in_request):
    # Set up
    mock_client = MockWorkflowClientForBooleanVarTest()
    mock_response = SetVariableValueResponse()
    sut_element_id = ElementId(id_string="VAR_UNDER_TEST_ID")
    with unittest.mock.patch.object(
        mock_client, "BooleanArraySetValue", retun_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = BooleanArray(sut_element_id, None)
        new_value = acvi.VariableState(set_value, True)

        # Execute
        sut.set_value(new_value)

        # Verify
        expected_request = SetBooleanArrayValueRequest(
            target=sut_element_id, new_value=expected_value_in_request
        )
        mock_grpc_method.assert_called_once_with(expected_request)


@pytest.mark.parametrize(
    "set_value",
    [
        acvi.IntegerValue(0),
        acvi.RealValue(0.0),
        acvi.BooleanValue(False),
        acvi.StringValue("False"),
        acvi.IntegerArrayValue(),
        acvi.RealArrayValue(),
        acvi.StringArrayValue(),
    ],
)
def test_array_set_disallowed(monkeypatch, set_value):
    # Set up
    mock_client = MockWorkflowClientForBooleanVarTest()
    mock_response = SetVariableValueResponse()
    sut_element_id = ElementId(id_string="VAR_UNDER_TEST_ID")
    with unittest.mock.patch.object(
        mock_client, "BooleanArraySetValue", return_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = BooleanArray(sut_element_id, None)
        new_value = acvi.VariableState(set_value, True)

        # Execute / verify:
        with pytest.raises(acvi.IncompatibleTypesException):
            sut.set_value(new_value)

        # Verify
        mock_grpc_method.assert_not_called()


def test_scalar_get_type(monkeypatch):
    do_get_type_test(
        monkeypatch, BooleanVariable, VariableType.VARTYPE_BOOLEAN, acvi.VariableType.BOOLEAN
    )


def test_array_get_type(monkeypatch):
    do_get_type_test(
        monkeypatch,
        BooleanArray,
        VariableType.VARTYPE_BOOLEAN_ARRAY,
        acvi.VariableType.BOOLEAN_ARRAY,
    )


@pytest.mark.parametrize(
    "value_in_response,validity_in_response,expected_acvi_state",
    [
        (True, True, acvi.VariableState(acvi.BooleanValue(True), True)),
        (True, False, acvi.VariableState(acvi.BooleanValue(True), False)),
        (False, True, acvi.VariableState(acvi.BooleanValue(False), True)),
        (False, False, acvi.VariableState(acvi.BooleanValue(False), False)),
    ],
)
def test_scalar_get_state(
    monkeypatch, value_in_response, validity_in_response, expected_acvi_state
):
    do_get_state_test(
        monkeypatch,
        BooleanVariable,
        VariableState(
            is_valid=validity_in_response, value=VariableValue(bool_value=value_in_response)
        ),
        expected_acvi_state,
    )


@pytest.mark.parametrize(
    "value_in_response,validity_in_response,expected_acvi_state",
    [
        (
            BooleanArrayValue(dims=ArrayDimensions(dims=[2, 2]), values=[True, False, False, True]),
            True,
            acvi.VariableState(
                acvi.BooleanArrayValue(shape_=(2, 2), values=[[True, False], [False, True]]), True
            ),
        ),
        (
            BooleanArrayValue(dims=ArrayDimensions(dims=[2, 2]), values=[False, True, True, False]),
            False,
            acvi.VariableState(
                acvi.BooleanArrayValue(shape_=(2, 2), values=[[False, True], [True, False]]), False
            ),
        ),
    ],
)
def test_array_get_state(monkeypatch, value_in_response, validity_in_response, expected_acvi_state):
    do_get_state_test(
        monkeypatch,
        BooleanArray,
        VariableState(
            is_valid=validity_in_response, value=VariableValue(bool_array_value=value_in_response)
        ),
        expected_acvi_state,
    )


@pytest.mark.parametrize(
    "sut_type, flag_in_response",
    [
        (BooleanVariable, True),
        (BooleanVariable, False),
        (BooleanArray, True),
        (BooleanArray, False),
    ],
)
def test_is_input_component(monkeypatch, sut_type, flag_in_response):
    do_test_is_input_component(monkeypatch, sut_type, flag_in_response)


@pytest.mark.parametrize(
    "sut_type, flag_in_response",
    [
        (BooleanVariable, True),
        (BooleanVariable, False),
        (BooleanArray, True),
        (BooleanArray, False),
    ],
)
def test_is_input_workflow(monkeypatch, sut_type, flag_in_response):
    do_test_is_input_workflow(monkeypatch, sut_type, flag_in_response)
