from unittest.mock import MagicMock

import ansys.modelcenter.workflow.grpc_modelcenter as grpcmc
import ansys.modelcenter.workflow.grpc_modelcenter.proto.element_messages_pb2 as elem_msgs
import ansys.modelcenter.workflow.grpc_modelcenter.proto.variable_value_messages_pb2 as var_msgs

from ansys.modelcenter.workflow.grpc_modelcenter.reference_property import (
    ReferenceProperty
)
from .grpc_server_test_utils.client_creation_monkeypatch import monkeypatch_client_creation


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
        reference_var=sut_id,
        prop_name=sut_name
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
    expected_target = var_msgs.ReferencePropertyIdentifier(
        reference_var=sut_id,
        prop_name=sut_name
    )
    expected_request = var_msgs.ReferencePropertySetIsInputRequest(target=expected_target,
                                                                   new_value=True)
    mock_client.ReferencePropertySetIsInput.assert_called_once_with(expected_request)
