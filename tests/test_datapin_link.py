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

import unittest

from ansys.api.modelcenter.v0.element_messages_pb2 import ElementId
from ansys.api.modelcenter.v0.grpc_modelcenter_workflow_pb2_grpc import (
    ModelCenterWorkflowServiceStub,
)
import ansys.api.modelcenter.v0.workflow_messages_pb2 as workflow_msg
import pytest

from ansys.modelcenter.workflow.grpc_modelcenter import DatapinLink


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

    def WorkflowGetLinkSuspensionState(
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


@pytest.mark.parametrize(["is_suspended"], [(True,), (False,)])
def test_get_link_suspension_state(monkeypatch, is_suspended: bool) -> None:
    # Setup
    mock_client = MockWorkflowClientForLinkTest()
    mock_response = workflow_msg.WorkflowLinkSuspension(is_suspended=is_suspended)
    mock_lhs = "TEST_LHS"
    mock_rhs = "TEST_RHS"
    with unittest.mock.patch.object(
        mock_client, "WorkflowGetLinkSuspensionState", return_value=mock_response
    ) as mock_grpc_method:
        sut = DatapinLink(mock_client, mock_lhs, mock_rhs)

        result = sut.is_suspended()

        assert result == is_suspended
        expected_request = workflow_msg.WorkflowBreakLinkRequest(
            target_var=ElementId(id_string=mock_lhs)
        )
        mock_grpc_method.assert_called_once_with(expected_request)
