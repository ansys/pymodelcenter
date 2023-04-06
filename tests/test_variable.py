import unittest

import ansys.common.variableinterop as acvi

from ansys.modelcenter.workflow.grpc_modelcenter.abstract_workflow_element import (
    AbstractWorkflowElement,
)
from ansys.modelcenter.workflow.grpc_modelcenter.proto.element_messages_pb2 import (
    ElementId,
    VariableIsInputResponse,
)
from ansys.modelcenter.workflow.grpc_modelcenter.proto.variable_value_messages_pb2 import (
    VariableState,
    VariableTypeResponse,
)

from .grpc_server_test_utils.client_creation_monkeypatch import monkeypatch_client_creation


class MockWorkflowClientForVariableTest:
    def __init__(self):
        pass

    def VariableGetType(self, request: ElementId) -> VariableTypeResponse:
        return VariableTypeResponse()

    def VariableGetState(self, request: ElementId) -> VariableState:
        return VariableState()

    def VariableGetIsInput(self, request: ElementId) -> VariableIsInputResponse:
        return VariableIsInputResponse()


def do_get_type_test(monkeypatch, sut_type, type_in_response, expected_acvi_type) -> None:
    """Perform a test of interop_type on a particular base variable."""

    mock_client = MockWorkflowClientForVariableTest()
    sut_element_id = ElementId(id_string="VAR_UNDER_TEST_ID")
    mock_response = VariableTypeResponse(var_type=type_in_response)
    with unittest.mock.patch.object(
        mock_client, "VariableGetType", return_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = sut_type(element_id=sut_element_id, channel=None)

        # Execute
        result: acvi.VariableType = sut.interop_type

        # Verify
        mock_grpc_method.assert_called_once_with(sut_element_id)
        assert result == expected_acvi_type, "The type returned by interop_type should be correct."


def do_get_state_test(monkeypatch, sut_type, mock_response, expected_acvi_state) -> None:
    """Perform a test of get_state on a particular base variable."""

    mock_client = MockWorkflowClientForVariableTest()
    sut_element_id = ElementId(id_string="VAR_UNDER_TEST_ID")
    with unittest.mock.patch.object(
        mock_client, "VariableGetState", return_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = sut_type(element_id=sut_element_id, channel=None)

        result: acvi.VariableState = sut.get_value(None)

        mock_grpc_method.assert_called_once_with(sut_element_id)
        assert result.value == expected_acvi_state.value
        assert result.is_valid == expected_acvi_state.is_valid


def do_test_is_input_component(monkeypatch, sut_type, flag_in_response) -> None:
    mock_client = MockWorkflowClientForVariableTest()
    sut_element_id = ElementId(id_string="VAR_UNDER_TEST_ID")
    mock_response = VariableIsInputResponse(
        is_input_in_component=flag_in_response, is_input_in_workflow=False
    )
    with unittest.mock.patch.object(
        mock_client, "VariableGetIsInput", return_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = sut_type(element_id=sut_element_id, channel=None)

        result: bool = sut.is_input_to_component

        mock_grpc_method.assert_called_once_with(sut_element_id)
        assert result == flag_in_response


def do_test_is_input_workflow(monkeypatch, sut_type, flag_in_response) -> None:
    mock_client = MockWorkflowClientForVariableTest()
    sut_element_id = ElementId(id_string="VAR_UNDER_TEST_ID")
    mock_response = VariableIsInputResponse(
        is_input_in_component=False, is_input_in_workflow=flag_in_response
    )
    with unittest.mock.patch.object(
        mock_client, "VariableGetIsInput", return_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = sut_type(element_id=sut_element_id, channel=None)

        result: bool = sut.is_input_to_model

        mock_grpc_method.assert_called_once_with(sut_element_id)
        assert result == flag_in_response
