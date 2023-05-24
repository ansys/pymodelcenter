import unittest.mock

import ansys.tools.variableinterop as atvi
from grpc_server_test_utils.client_creation_monkeypatch import monkeypatch_client_creation
import pytest

import ansys.modelcenter.workflow.grpc_modelcenter as grpcmc
from ansys.modelcenter.workflow.grpc_modelcenter.abstract_workflow_element import (
    AbstractWorkflowElement,
)
import ansys.modelcenter.workflow.grpc_modelcenter.proto.element_messages_pb2 as elem_msgs
import ansys.modelcenter.workflow.grpc_modelcenter.proto.variable_value_messages_pb2 as var_msgs


class MockWorkflowClientForRefVarTest:
    def __init__(self):
        pass

    def ReferenceVariableGetReferenceEquation(self, request):
        pass

    def ReferenceVariableSetReferenceEquation(self, request):
        pass

    def ReferenceVariableGetIsDirect(self, request):
        pass

    def ReferenceVariableSetValue(self, request):
        pass


def test_get_reference_equation(monkeypatch, engine) -> None:
    # Arrange
    mock_client = MockWorkflowClientForRefVarTest()
    mock_response = var_msgs.GetReferenceEquationResponse()
    with unittest.mock.patch.object(
        mock_client, "ReferenceVariableGetReferenceEquation", retun_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut_element_id = elem_msgs.ElementId(id_string="VAR_UNDER_TEST_ID")
        sut = grpcmc.ReferenceDatapin(sut_element_id, engine)

        # Act
        equation: str = sut.equation

        # Assert
        expected_request = var_msgs.GetReferenceEquationRequest(target=sut_element_id)
        mock_grpc_method.assert_called_once_with(expected_request)


def test_set_reference_equation(monkeypatch, engine) -> None:
    # Arrange
    mock_client = MockWorkflowClientForRefVarTest()
    mock_response = var_msgs.SetReferenceEquationResponse()
    with unittest.mock.patch.object(
        mock_client, "ReferenceVariableSetReferenceEquation", retun_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut_element_id = elem_msgs.ElementId(id_string="VAR_UNDER_TEST_ID")
        sut = grpcmc.ReferenceDatapin(sut_element_id, engine)

        # Act
        sut.equation = "ඞ"

        # Assert
        expected_request = var_msgs.SetReferenceEquationRequest(target=sut_element_id, equation="ඞ")
        mock_grpc_method.assert_called_once_with(expected_request)


def test_get_is_direct(monkeypatch, engine) -> None:
    # Arrange
    mock_client = MockWorkflowClientForRefVarTest()
    mock_response = var_msgs.GetReferenceIsDirectResponse()
    with unittest.mock.patch.object(
        mock_client, "ReferenceVariableGetIsDirect", retun_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut_element_id = elem_msgs.ElementId(id_string="VAR_UNDER_TEST_ID")
        sut = grpcmc.ReferenceDatapin(sut_element_id, engine)

        # Act
        is_direct: bool = sut.is_direct

        # Assert
        expected_request = var_msgs.GetReferenceIsDirectRequest(target=sut_element_id)
        mock_grpc_method.assert_called_once_with(expected_request)


@pytest.mark.parametrize(
    "set_value,expected_value_in_request",
    [
        (atvi.BooleanValue(True), var_msgs.VariableValue(bool_value=True)),
        (atvi.RealValue(4.7), var_msgs.VariableValue(double_value=4.7)),
        (atvi.IntegerValue(47), var_msgs.VariableValue(int_value=47)),
        (
            atvi.StringValue("This is a test string value."),
            var_msgs.VariableValue(string_value="This is a test string value."),
        ),
    ],
)
def test_scalar_set_allowed(monkeypatch, engine, set_value, expected_value_in_request):
    # Arrange
    mock_client = MockWorkflowClientForRefVarTest()
    mock_response = var_msgs.SetVariableValueResponse()
    with unittest.mock.patch.object(
        mock_client, "ReferenceVariableSetValue", retun_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut_element_id = elem_msgs.ElementId(id_string="VAR_UNDER_TEST_ID")
        sut = grpcmc.ReferenceDatapin(sut_element_id, engine)
        new_value = atvi.VariableState(set_value, True)

        # Act
        sut.set_value(new_value)

        # Assert
        expected_request = var_msgs.SetReferenceValueRequest(
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
def test_scalar_set_disallowed(monkeypatch, engine, set_value):
    # Arrange
    mock_client = MockWorkflowClientForRefVarTest()
    mock_response = var_msgs.SetVariableValueResponse()
    with unittest.mock.patch.object(
        mock_client, "ReferenceVariableSetValue", return_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut_element_id = elem_msgs.ElementId(id_string="VAR_UNDER_TEST_ID")
        sut = grpcmc.ReferenceDatapin(sut_element_id, engine)
        new_value = atvi.VariableState(set_value, True)

        # Act
        with pytest.raises(atvi.IncompatibleTypesException):
            sut.set_value(new_value)

        # Assert
        mock_grpc_method.assert_not_called()
