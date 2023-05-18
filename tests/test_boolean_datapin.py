from typing import Type, Union
import unittest

import ansys.tools.variableinterop as atvi
import pytest

from ansys.modelcenter.workflow.grpc_modelcenter.abstract_workflow_element import (
    AbstractWorkflowElement,
)
from ansys.modelcenter.workflow.grpc_modelcenter.boolean_datapin import (
    BooleanArrayDatapin,
    BooleanDatapin,
)
from ansys.modelcenter.workflow.grpc_modelcenter.proto.element_messages_pb2 import ElementId
from ansys.modelcenter.workflow.grpc_modelcenter.proto.variable_value_messages_pb2 import (
    ArrayDimensions,
    BooleanArrayValue,
    BooleanVariableMetadata,
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
from .test_datapin import (
    do_get_state_test,
    do_get_state_test_with_hid,
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
        ("", BooleanDatapin, atvi.BooleanMetadata),
        ("This is a mock datapin description.", BooleanDatapin, atvi.BooleanMetadata),
        ("", BooleanArrayDatapin, atvi.BooleanArrayMetadata),
        ("This is a mock datapin description.", BooleanArrayDatapin, atvi.BooleanArrayMetadata),
    ],
)
def test_retrieved_metadata_should_include_description(
    monkeypatch,
    engine,
    description_string: str,
    sut_type: Union[Type[BooleanDatapin], Type[BooleanArrayDatapin]],
    expected_metadata_type: Union[Type[atvi.BooleanMetadata], Type[atvi.BooleanArrayMetadata]],
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
        sut = sut_type(sut_element_id, engine=engine)

        # Execute
        result: atvi.BooleanMetadata = sut.get_metadata()

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
    [(BooleanDatapin, atvi.BooleanMetadata), (BooleanArrayDatapin, atvi.BooleanArrayMetadata)],
)
def test_retrieved_metadata_should_include_custom_metadata_empty(
    monkeypatch,
    engine,
    sut_type: Union[Type[BooleanDatapin], Type[BooleanArrayDatapin]],
    expected_metadata_type: Union[Type[atvi.BooleanMetadata], Type[atvi.BooleanArrayMetadata]],
):
    # Set up
    mock_client = MockWorkflowClientForBooleanVarTest()
    mock_response = BooleanVariableMetadata()
    sut_element_id = ElementId(id_string="VAR_UNDER_TEST_ID")
    with unittest.mock.patch.object(
        mock_client, "BooleanVariableGetMetadata", return_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = sut_type(sut_element_id, engine)

        # Execute
        result: atvi.BooleanMetadata = sut.get_metadata()

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
    [(BooleanDatapin, atvi.BooleanMetadata), (BooleanArrayDatapin, atvi.BooleanArrayMetadata)],
)
def test_retrieved_metadata_should_include_custom_metadata_populated(
    monkeypatch,
    engine,
    sut_type: Union[Type[BooleanDatapin], Type[BooleanArrayDatapin]],
    expected_metadata_type: Union[Type[atvi.BooleanMetadata], Type[atvi.BooleanArrayMetadata]],
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
        sut = sut_type(sut_element_id, engine)

        # Execute
        result: atvi.BooleanMetadata = sut.get_metadata()

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
    [(BooleanDatapin, atvi.BooleanMetadata), (BooleanArrayDatapin, atvi.BooleanArrayMetadata)],
)
def test_retrieved_metadata_includes_unsupported_type(
    monkeypatch,
    engine,
    sut_type: Union[Type[BooleanDatapin], Type[BooleanArrayDatapin]],
    expected_metadata_type: Union[Type[atvi.BooleanMetadata], Type[atvi.BooleanArrayMetadata]],
):
    # Set up
    mock_client = MockWorkflowClientForBooleanVarTest()
    mock_response = BooleanVariableMetadata()
    mock_response.base_metadata.custom_metadata["test_unsupported"].MergeFrom(VariableValue())
    sut_element_id = ElementId(id_string="VAR_UNDER_TEST_ID")
    with unittest.mock.patch.object(
        mock_client, "BooleanVariableGetMetadata", return_value=mock_response
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
        BooleanDatapin,
        BooleanArrayDatapin,
    ],
)
def test_set_metadata_invalid_custom_metadata(
    monkeypatch, engine, sut_type: Union[Type[BooleanDatapin], Type[BooleanArrayDatapin]]
):
    # Set up
    mock_client = MockWorkflowClientForBooleanVarTest()
    mock_response = SetMetadataResponse()
    sut_element_id = ElementId(id_string="VAR_UNDER_TEST_ID")
    with unittest.mock.patch.object(
        mock_client, "BooleanVariableSetMetadata", return_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = sut_type(sut_element_id, engine)
        new_metadata = atvi.FileMetadata()

        # Execute
        with pytest.raises(TypeError):
            sut.set_metadata(new_metadata)

        # Verify
        mock_grpc_method.assert_not_called()


@pytest.mark.parametrize(
    "description,sut_type,metadata_type",
    [
        ("", BooleanDatapin, atvi.BooleanMetadata),
        ("This is a mock datapin description.", BooleanDatapin, atvi.BooleanMetadata),
        ("", BooleanArrayDatapin, atvi.BooleanArrayMetadata),
        ("This is a mock datapin description.", BooleanArrayDatapin, atvi.BooleanArrayMetadata),
    ],
)
def test_set_metadata_empty_custom_metadata(
    monkeypatch,
    engine,
    description: str,
    sut_type: Union[Type[BooleanDatapin], Type[BooleanArrayDatapin]],
    metadata_type: Union[Type[atvi.BooleanMetadata], Type[atvi.BooleanArrayMetadata]],
):
    # Set up
    mock_client = MockWorkflowClientForBooleanVarTest()
    mock_response = SetMetadataResponse()
    sut_element_id = ElementId(id_string="VAR_UNDER_TEST_ID")
    with unittest.mock.patch.object(
        mock_client, "BooleanVariableSetMetadata", return_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = sut_type(sut_element_id, engine)
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
        ("", BooleanDatapin, atvi.BooleanMetadata),
        ("This is a mock datapin description.", BooleanDatapin, atvi.BooleanMetadata),
        ("", BooleanArrayDatapin, atvi.BooleanArrayMetadata),
        ("This is a mock datapin description.", BooleanArrayDatapin, atvi.BooleanArrayMetadata),
    ],
)
def test_set_metadata_populated_custom_metadata(
    monkeypatch,
    engine,
    description: str,
    sut_type: Union[Type[BooleanDatapin], Type[BooleanArrayDatapin]],
    metadata_type: Union[Type[atvi.BooleanMetadata], Type[atvi.BooleanArrayMetadata]],
):
    # Set up
    mock_client = MockWorkflowClientForBooleanVarTest()
    mock_response = SetMetadataResponse()
    sut_element_id = ElementId(id_string="VAR_UNDER_TEST_ID")
    with unittest.mock.patch.object(
        mock_client, "BooleanVariableSetMetadata", return_value=mock_response
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
    [(atvi.BooleanValue(True), True), (atvi.BooleanValue(False), False)],
)
def test_scalar_set_allowed(monkeypatch, engine, set_value, expected_value_in_request):
    # Set up
    mock_client = MockWorkflowClientForBooleanVarTest()
    mock_response = SetVariableValueResponse()
    sut_element_id = ElementId(id_string="VAR_UNDER_TEST_ID")
    with unittest.mock.patch.object(
        mock_client, "BooleanVariableSetValue", retun_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = BooleanDatapin(sut_element_id, engine)
        new_value = atvi.VariableState(set_value, True)

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
        atvi.IntegerValue(0),
        atvi.RealValue(0.0),
        atvi.StringValue("False"),
        atvi.IntegerArrayValue(),
        atvi.RealArrayValue(),
        atvi.BooleanArrayValue(),
        atvi.StringArrayValue(),
    ],
)
def test_scalar_set_disallowed(monkeypatch, engine, set_value):
    # Set up
    mock_client = MockWorkflowClientForBooleanVarTest()
    mock_response = SetVariableValueResponse()
    sut_element_id = ElementId(id_string="VAR_UNDER_TEST_ID")
    with unittest.mock.patch.object(
        mock_client, "BooleanVariableSetValue", return_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = BooleanDatapin(sut_element_id, engine)
        new_value = atvi.VariableState(set_value, True)

        # Execute / verify:
        with pytest.raises(atvi.IncompatibleTypesException):
            sut.set_value(new_value)

        # Verify
        mock_grpc_method.assert_not_called()


@pytest.mark.parametrize(
    "set_value,expected_value_in_request",
    [
        (
            atvi.BooleanArrayValue(shape_=(0,)),
            BooleanArrayValue(dims=ArrayDimensions(dims=[0]), values=[]),
        ),
        (
            atvi.BooleanArrayValue(shape_=(2, 2), values=[[True, False], [False, True]]),
            BooleanArrayValue(dims=ArrayDimensions(dims=[2, 2]), values=[True, False, False, True]),
        ),
    ],
)
def test_array_set_allowed(monkeypatch, engine, set_value, expected_value_in_request):
    # Set up
    mock_client = MockWorkflowClientForBooleanVarTest()
    mock_response = SetVariableValueResponse()
    sut_element_id = ElementId(id_string="VAR_UNDER_TEST_ID")
    with unittest.mock.patch.object(
        mock_client, "BooleanArraySetValue", retun_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = BooleanArrayDatapin(sut_element_id, engine)
        new_value = atvi.VariableState(set_value, True)

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
        atvi.IntegerValue(0),
        atvi.RealValue(0.0),
        atvi.BooleanValue(False),
        atvi.StringValue("False"),
        atvi.IntegerArrayValue(),
        atvi.RealArrayValue(),
        atvi.StringArrayValue(),
    ],
)
def test_array_set_disallowed(monkeypatch, engine, set_value):
    # Set up
    mock_client = MockWorkflowClientForBooleanVarTest()
    mock_response = SetVariableValueResponse()
    sut_element_id = ElementId(id_string="VAR_UNDER_TEST_ID")
    with unittest.mock.patch.object(
        mock_client, "BooleanArraySetValue", return_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = BooleanArrayDatapin(sut_element_id, engine)
        new_value = atvi.VariableState(set_value, True)

        # Execute / verify:
        with pytest.raises(atvi.IncompatibleTypesException):
            sut.set_value(new_value)

        # Verify
        mock_grpc_method.assert_not_called()


def test_scalar_get_type(monkeypatch, engine):
    do_get_type_test(
        monkeypatch, engine, BooleanDatapin, VariableType.VARTYPE_BOOLEAN, atvi.VariableType.BOOLEAN
    )


def test_array_get_type(monkeypatch, engine):
    do_get_type_test(
        monkeypatch,
        engine,
        BooleanArrayDatapin,
        VariableType.VARTYPE_BOOLEAN_ARRAY,
        atvi.VariableType.BOOLEAN_ARRAY,
    )


@pytest.mark.parametrize(
    "value_in_response,validity_in_response,expected_atvi_state",
    [
        (True, True, atvi.VariableState(atvi.BooleanValue(True), True)),
        (True, False, atvi.VariableState(atvi.BooleanValue(True), False)),
        (False, True, atvi.VariableState(atvi.BooleanValue(False), True)),
        (False, False, atvi.VariableState(atvi.BooleanValue(False), False)),
    ],
)
def test_scalar_get_state(
    monkeypatch, engine, value_in_response, validity_in_response, expected_atvi_state
):
    do_get_state_test(
        monkeypatch,
        engine,
        BooleanDatapin,
        VariableState(
            is_valid=validity_in_response, value=VariableValue(bool_value=value_in_response)
        ),
        expected_atvi_state,
    )


def test_scalar_get_state_with_hid(monkeypatch, engine):
    do_get_state_test_with_hid(monkeypatch, engine, BooleanDatapin)


@pytest.mark.parametrize(
    "value_in_response,validity_in_response,expected_atvi_state",
    [
        (
            BooleanArrayValue(dims=ArrayDimensions(dims=[2, 2]), values=[True, False, False, True]),
            True,
            atvi.VariableState(
                atvi.BooleanArrayValue(shape_=(2, 2), values=[[True, False], [False, True]]), True
            ),
        ),
        (
            BooleanArrayValue(dims=ArrayDimensions(dims=[2, 2]), values=[False, True, True, False]),
            False,
            atvi.VariableState(
                atvi.BooleanArrayValue(shape_=(2, 2), values=[[False, True], [True, False]]), False
            ),
        ),
    ],
)
def test_array_get_state(
    monkeypatch, engine, value_in_response, validity_in_response, expected_atvi_state
):
    do_get_state_test(
        monkeypatch,
        engine,
        BooleanArrayDatapin,
        VariableState(
            is_valid=validity_in_response, value=VariableValue(bool_array_value=value_in_response)
        ),
        expected_atvi_state,
    )


def test_array_get_state_with_hid(monkeypatch, engine):
    do_get_state_test_with_hid(monkeypatch, engine, BooleanArrayDatapin)


@pytest.mark.parametrize(
    "sut_type, flag_in_response",
    [
        (BooleanDatapin, True),
        (BooleanDatapin, False),
        (BooleanArrayDatapin, True),
        (BooleanArrayDatapin, False),
    ],
)
def test_is_input_component(monkeypatch, engine, sut_type, flag_in_response):
    do_test_is_input_component(monkeypatch, engine, sut_type, flag_in_response)


@pytest.mark.parametrize(
    "sut_type, flag_in_response",
    [
        (BooleanDatapin, True),
        (BooleanDatapin, False),
        (BooleanArrayDatapin, True),
        (BooleanArrayDatapin, False),
    ],
)
def test_is_input_workflow(monkeypatch, engine, sut_type, flag_in_response):
    do_test_is_input_workflow(monkeypatch, engine, sut_type, flag_in_response)
