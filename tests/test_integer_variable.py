from typing import Literal, Optional
import unittest

import ansys.common.variableinterop as acvi
import pytest

from ansys.modelcenter.workflow.grpc_modelcenter.abstract_workflow_element import (
    AbstractWorkflowElement,
)
from ansys.modelcenter.workflow.grpc_modelcenter.integer_variable import (
    IntegerArray,
    IntegerVariable,
)
from ansys.modelcenter.workflow.grpc_modelcenter.proto.element_messages_pb2 import ElementId
from ansys.modelcenter.workflow.grpc_modelcenter.proto.variable_value_messages_pb2 import (
    ArrayDimensions,
    FileValue,
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
from ansys.modelcenter.workflow.grpc_modelcenter.var_metadata_convert import (
    CustomMetadataValueNotSupportedError,
)

from .grpc_server_test_utils.client_creation_monkeypatch import monkeypatch_client_creation
from .test_variable import do_get_state_test, do_get_type_test


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
        ("", IntegerVariable, acvi.IntegerMetadata),
        ("This is a mock variable description.", IntegerVariable, acvi.IntegerMetadata),
        ("", IntegerArray, acvi.IntegerArrayMetadata),
        ("This is a mock variable description.", IntegerArray, acvi.IntegerArrayMetadata),
    ],
)
def test_retrieved_metadata_should_include_description(
    monkeypatch,
    description_string: str,
    sut_type: Literal[IntegerVariable, IntegerArray],
    expected_metadata_type: Literal[acvi.IntegerMetadata, acvi.IntegerArrayMetadata],
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
        sut = sut_type(sut_element_id, None)

        # Execute
        result: acvi.IntegerMetadata = sut.get_metadata()

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
    [(IntegerVariable, acvi.IntegerMetadata), (IntegerArray, acvi.IntegerArrayMetadata)],
)
def test_retrieved_metadata_should_include_custom_metadata_empty(
    monkeypatch,
    sut_type: Literal[IntegerVariable, IntegerArray],
    expected_metadata_type: Literal[acvi.IntegerMetadata, acvi.IntegerArrayMetadata],
):
    # Set up
    mock_client = MockWorkflowClientForIntegerVarTest()
    mock_response = IntegerVariableMetadata()
    sut_element_id = ElementId(id_string="VAR_UNDER_TEST_ID")
    with unittest.mock.patch.object(
        mock_client, "IntegerVariableGetMetadata", return_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = sut_type(sut_element_id, None)

        # Execute
        result: acvi.IntegerMetadata = sut.get_metadata()

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
    [(IntegerVariable, acvi.IntegerMetadata), (IntegerArray, acvi.IntegerArrayMetadata)],
)
def test_retrieved_metadata_should_include_custom_metadata_populated(
    monkeypatch,
    sut_type: Literal[IntegerVariable, IntegerArray],
    expected_metadata_type: Literal[acvi.IntegerMetadata, acvi.IntegerArrayMetadata],
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
        sut = sut_type(sut_element_id, None)

        # Execute
        result: acvi.IntegerMetadata = sut.get_metadata()

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
    [(IntegerVariable, acvi.IntegerMetadata), (IntegerArray, acvi.IntegerArrayMetadata)],
)
def test_retrieved_metadata_includes_unsupported_type(
    monkeypatch,
    sut_type: Literal[IntegerVariable, IntegerArray],
    expected_metadata_type: Literal[acvi.IntegerMetadata, acvi.IntegerArrayMetadata],
):
    # Set up
    mock_client = MockWorkflowClientForIntegerVarTest()
    mock_response = IntegerVariableMetadata()
    mock_response.base_metadata.custom_metadata["test_unsupported"].MergeFrom(
        VariableValue(file_value=FileValue())
    )
    sut_element_id = ElementId(id_string="VAR_UNDER_TEST_ID")
    with unittest.mock.patch.object(
        mock_client, "IntegerVariableGetMetadata", return_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = sut_type(sut_element_id, None)

        # Execute / Verify
        with pytest.raises(CustomMetadataValueNotSupportedError, match="unsupported type"):
            sut.get_metadata()

        # Verify
        mock_grpc_method.assert_called_once_with(sut_element_id)


@pytest.mark.parametrize(
    "sut_type,expected_metadata_type,upper_bound,set_upper_bound,expected_upper_bound,"
    "lower_bound,set_lower_bound,expected_lower_bound",
    [
        (IntegerVariable, acvi.IntegerMetadata, 0, False, None, 0, False, None),
        (IntegerVariable, acvi.IntegerMetadata, -47, True, -47, 9000, True, 9000),
        (IntegerVariable, acvi.IntegerMetadata, 0, False, None, 9000, True, 9000),
        (IntegerVariable, acvi.IntegerMetadata, -47, True, -47, 0, False, None),
        (IntegerArray, acvi.IntegerArrayMetadata, 0, False, None, 0, False, None),
        (IntegerArray, acvi.IntegerArrayMetadata, -47, True, -47, 9000, True, 9000),
        (IntegerArray, acvi.IntegerArrayMetadata, 0, False, None, 9000, True, 9000),
        (IntegerArray, acvi.IntegerArrayMetadata, -47, True, -47, 0, False, None),
    ],
)
def test_retrieved_metadata_should_convert_bounds(
    monkeypatch,
    sut_type: Literal[IntegerVariable, IntegerArray],
    expected_metadata_type: Literal[acvi.IntegerMetadata, acvi.IntegerArrayMetadata],
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
        sut = sut_type(sut_element_id, None)

        # Execute
        result: acvi.IntegerMetadata = sut.get_metadata()

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
    "description,sut_type,metadata_type",
    [
        ("", IntegerVariable, acvi.IntegerMetadata),
        ("This is a mock variable description.", IntegerVariable, acvi.IntegerMetadata),
        ("", IntegerArray, acvi.IntegerArrayMetadata),
        ("This is a mock variable description.", IntegerArray, acvi.IntegerArrayMetadata),
    ],
)
def test_set_metadata_empty_custom_metadata(
    monkeypatch,
    description: str,
    sut_type: Literal[IntegerVariable, IntegerArray],
    metadata_type: Literal[acvi.IntegerMetadata, acvi.IntegerArrayMetadata],
):
    # Set up
    mock_client = MockWorkflowClientForIntegerVarTest()
    mock_response = SetMetadataResponse()
    sut_element_id = ElementId(id_string="VAR_UNDER_TEST_ID")
    with unittest.mock.patch.object(
        mock_client, "IntegerVariableSetMetadata", return_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = sut_type(sut_element_id, None)
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
        ("", IntegerVariable, acvi.IntegerMetadata),
        ("This is a mock variable description.", IntegerVariable, acvi.IntegerMetadata),
        ("", IntegerArray, acvi.IntegerArrayMetadata),
        ("This is a mock variable description.", IntegerArray, acvi.IntegerArrayMetadata),
    ],
)
def test_set_metadata_populated_custom_metadata(
    monkeypatch,
    description: str,
    sut_type: Literal[IntegerVariable, IntegerArray],
    metadata_type: Literal[acvi.IntegerMetadata, acvi.IntegerArrayMetadata],
):
    # Set up
    mock_client = MockWorkflowClientForIntegerVarTest()
    mock_response = SetMetadataResponse()
    sut_element_id = ElementId(id_string="VAR_UNDER_TEST_ID")
    with unittest.mock.patch.object(
        mock_client, "IntegerVariableSetMetadata", return_value=mock_response
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
        (IntegerVariable, acvi.IntegerMetadata, None, 0, False, None, 0, False),
        (IntegerVariable, acvi.IntegerMetadata, -47, -47, True, 9001, 9001, True),
        (IntegerVariable, acvi.IntegerMetadata, None, 0, False, 9001, 9001, True),
        (IntegerVariable, acvi.IntegerMetadata, -47, -47, True, None, 0, False),
        (IntegerArray, acvi.IntegerArrayMetadata, None, 0, False, None, 0, False),
        (IntegerArray, acvi.IntegerArrayMetadata, -47, -47, True, 9001, 9001, True),
        (IntegerArray, acvi.IntegerArrayMetadata, None, 0, False, 9001, 9001, True),
        (IntegerArray, acvi.IntegerArrayMetadata, -47, -47, True, None, 0, False),
    ],
)
def test_set_metadata_should_convert_bounds(
    monkeypatch,
    sut_type: Literal[IntegerVariable, IntegerArray],
    metadata_type: Literal[acvi.IntegerMetadata, acvi.IntegerArrayMetadata],
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
        sut = sut_type(sut_element_id, None)
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
    "set_value,expected_value_in_request",
    [
        (acvi.IntegerValue(-47), -47),
        (acvi.IntegerValue(47), 47),
        (acvi.BooleanValue(True), 1),
        (acvi.BooleanValue(False), 0),
    ],
)
def test_scalar_set_allowed(monkeypatch, set_value, expected_value_in_request):
    # Set up
    mock_client = MockWorkflowClientForIntegerVarTest()
    mock_response = SetVariableValueResponse()
    sut_element_id = ElementId(id_string="VAR_UNDER_TEST_ID")
    with unittest.mock.patch.object(
        mock_client, "IntegerVariableSetValue", retun_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = IntegerVariable(sut_element_id, None)
        new_value = acvi.VariableState(set_value, True)

        # Execute
        sut.set_value(new_value)

        # Verify
        expected_request = SetIntegerValueRequest(
            target=sut_element_id, new_value=expected_value_in_request
        )
        mock_grpc_method.assert_called_once_with(expected_request)


@pytest.mark.parametrize(
    "set_value",
    [
        acvi.RealArrayValue(),
        acvi.BooleanArrayValue(),
        acvi.IntegerArrayValue(),
        acvi.RealValue(4.0),
        acvi.StringValue("47"),
    ],
)
def test_scalar_set_disallowed(monkeypatch, set_value):
    # Set up
    mock_client = MockWorkflowClientForIntegerVarTest()
    mock_response = SetVariableValueResponse()
    sut_element_id = ElementId(id_string="VAR_UNDER_TEST_ID")
    with unittest.mock.patch.object(
        mock_client, "IntegerVariableSetValue", return_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = IntegerVariable(sut_element_id, None)
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
            acvi.IntegerArrayValue(shape_=(2, 2), values=[[101, 102], [201, 202]]),
            IntegerArrayValue(dims=ArrayDimensions(dims=[2, 2]), values=[101, 102, 201, 202]),
        ),
        (
            acvi.BooleanArrayValue(shape_=(2, 2), values=[[True, False], [False, True]]),
            IntegerArrayValue(dims=ArrayDimensions(dims=[2, 2]), values=[1, 0, 0, 1]),
        ),
    ],
)
def test_array_set_allowed(monkeypatch, set_value, expected_value_in_request):
    # Set up
    mock_client = MockWorkflowClientForIntegerVarTest()
    mock_response = SetVariableValueResponse()
    sut_element_id = ElementId(id_string="VAR_UNDER_TEST_ID")
    with unittest.mock.patch.object(
        mock_client, "IntegerArraySetValue", retun_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = IntegerArray(sut_element_id, None)
        new_value = acvi.VariableState(set_value, True)

        # Execute
        sut.set_value(new_value)

        # Verify
        expected_request = SetIntegerArrayValueRequest(
            target=sut_element_id, new_value=expected_value_in_request
        )
        mock_grpc_method.assert_called_once_with(expected_request)


@pytest.mark.parametrize(
    "set_value", [acvi.IntegerValue(0), acvi.RealArrayValue(), acvi.StringArrayValue()]
)
def test_array_set_disallowed(monkeypatch, set_value):
    # Set up
    mock_client = MockWorkflowClientForIntegerVarTest()
    mock_response = SetVariableValueResponse()
    sut_element_id = ElementId(id_string="VAR_UNDER_TEST_ID")
    with unittest.mock.patch.object(
        mock_client, "IntegerArraySetValue", return_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = IntegerArray(sut_element_id, None)
        new_value = acvi.VariableState(set_value, True)

        # Execute / verify:
        with pytest.raises(TypeError):
            sut.set_value(new_value)

        # Verify
        mock_grpc_method.assert_not_called()


def test_scalar_get_type(monkeypatch):
    do_get_type_test(
        monkeypatch, IntegerVariable, VariableType.VARTYPE_INTEGER, acvi.VariableType.INTEGER
    )


def test_array_get_type(monkeypatch):
    do_get_type_test(
        monkeypatch,
        IntegerArray,
        VariableType.VARTYPE_INTEGER_ARRAY,
        acvi.VariableType.INTEGER_ARRAY,
    )


@pytest.mark.parametrize(
    "value_in_response,validity_in_response,expected_acvi_state",
    [
        (47, True, acvi.VariableState(acvi.IntegerValue(47), True)),
        (-8675309, False, acvi.VariableState(acvi.IntegerValue(-8675309), False)),
        (0, True, acvi.VariableState(acvi.IntegerValue(0), True)),
        (1, False, acvi.VariableState(acvi.IntegerValue(1), False)),
    ],
)
def test_scalar_get_state(
    monkeypatch, value_in_response, validity_in_response, expected_acvi_state
):
    do_get_state_test(
        monkeypatch,
        IntegerVariable,
        VariableState(
            is_valid=validity_in_response, value=VariableValue(int_value=value_in_response)
        ),
        expected_acvi_state,
    )


@pytest.mark.parametrize(
    "value_in_response,validity_in_response,expected_acvi_state",
    [
        (
            IntegerArrayValue(dims=ArrayDimensions(dims=[2, 2]), values=[-8675309, 47, -1, 0]),
            True,
            acvi.VariableState(
                acvi.IntegerArrayValue(shape_=(2, 2), values=[[-8675309, 47], [-1, 0]]), True
            ),
        ),
        (
            IntegerArrayValue(dims=ArrayDimensions(dims=[2, 2]), values=[101, 102, 201, 202]),
            False,
            acvi.VariableState(
                acvi.IntegerArrayValue(shape_=(2, 2), values=[[101, 102], [201, 202]]), False
            ),
        ),
    ],
)
def test_array_get_state(monkeypatch, value_in_response, validity_in_response, expected_acvi_state):
    do_get_state_test(
        monkeypatch,
        IntegerArray,
        VariableState(
            is_valid=validity_in_response, value=VariableValue(int_array_value=value_in_response)
        ),
        expected_acvi_state,
    )
