import unittest

import pytest

from ansys.modelcenter.workflow.grpc_modelcenter import DatapinLink
from ansys.modelcenter.workflow.grpc_modelcenter.proto.element_messages_pb2 import ElementId
from ansys.modelcenter.workflow.grpc_modelcenter.proto.grpc_modelcenter_workflow_pb2_grpc import (
    ModelCenterWorkflowServiceStub,
)
import ansys.modelcenter.workflow.grpc_modelcenter.proto.workflow_messages_pb2 as workflow_msg


class MockWorkflowClientForLinkTest(ModelCenterWorkflowServiceStub):
    # noinspection PyMissingConstructor
    def __init__(self) -> None:
        pass

    def WorkflowBreakLink(
        self, request: workflow_msg.WorkflowBreakLinkRequest
    ) -> workflow_msg.WorkflowBreakLinkResponse:
        return workflow_msg.WorkflowBreakLinkResponse()

    def WorkflowSuspendOrResumeLink(
        self, request: workflow_msg.WorkflowSuspendOrResumeLinkRequest
    ) -> workflow_msg.WorkflowLinkSuspension:
        return workflow_msg.WorkflowLinkSuspension()


def test_break_existing_link(monkeypatch) -> None:
    # Setup
    mock_client = MockWorkflowClientForLinkTest()
    mock_response = workflow_msg.WorkflowBreakLinkResponse(existed=True)
    mock_lhs = "TEST_LHS"
    mock_rhs = "TEST_RHS"
    with unittest.mock.patch.object(
        mock_client, "WorkflowBreakLink", return_value=mock_response
    ) as mock_grpc_method:
        sut = DatapinLink(mock_client, mock_lhs, mock_rhs)

        # SUT
        sut.break_link()

        # Verification
        expected_request = workflow_msg.WorkflowBreakLinkRequest(
            target_var=ElementId(id_string=mock_lhs)
        )
        mock_grpc_method.assert_called_once_with(expected_request)


def test_break_missing_link(monkeypatch) -> None:
    # Setup
    mock_client = MockWorkflowClientForLinkTest()
    mock_response = workflow_msg.WorkflowBreakLinkResponse(existed=False)
    mock_lhs = "TEST_LHS"
    mock_rhs = "TEST_RHS"
    with unittest.mock.patch.object(
        mock_client, "WorkflowBreakLink", return_value=mock_response
    ) as mock_grpc_method:
        sut = DatapinLink(mock_client, mock_lhs, mock_rhs)

        # SUT
        with pytest.raises(ValueError):
            sut.break_link()

        # Verification
        expected_request = workflow_msg.WorkflowBreakLinkRequest(
            target_var=ElementId(id_string=mock_lhs)
        )
        mock_grpc_method.assert_called_once_with(expected_request)


def test_suspend_link(monkeypatch) -> None:
    # Setup
    mock_client = MockWorkflowClientForLinkTest()
    mock_response = workflow_msg.WorkflowLinkSuspension()
    mock_lhs = "TEST_LHS"
    mock_rhs = "TEST_RHS"
    with unittest.mock.patch.object(
        mock_client, "WorkflowSuspendOrResumeLink", return_value=mock_response
    ) as mock_grpc_method:
        sut = DatapinLink(mock_client, mock_lhs, mock_rhs)

        sut.suspend()

        expected_request = workflow_msg.WorkflowSuspendOrResumeLinkRequest(
            target_link_lhs=ElementId(id_string=mock_lhs), suspend=True
        )
        mock_grpc_method.assert_called_once_with(expected_request)


def test_resume_link(monkeypatch) -> None:
    # Setup
    mock_client = MockWorkflowClientForLinkTest()
    mock_response = workflow_msg.WorkflowLinkSuspension()
    mock_lhs = "TEST_LHS"
    mock_rhs = "TEST_RHS"
    with unittest.mock.patch.object(
        mock_client, "WorkflowSuspendOrResumeLink", return_value=mock_response
    ) as mock_grpc_method:
        sut = DatapinLink(mock_client, mock_lhs, mock_rhs)

        sut.resume()

        expected_request = workflow_msg.WorkflowSuspendOrResumeLinkRequest(
            target_link_lhs=ElementId(id_string=mock_lhs), suspend=False
        )
        mock_grpc_method.assert_called_once_with(expected_request)
