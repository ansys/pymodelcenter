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

from ansys.api.modelcenter.v0.element_messages_pb2 import ElementId
from ansys.api.modelcenter.v0.variable_value_messages_pb2 import VariableState
import ansys.tools.variableinterop as atvi
import pytest

from ansys.modelcenter.workflow.grpc_modelcenter.unsupported_type_datapin import (
    DatapinWithUnsupportedTypeException,
    UnsupportedTypeDatapin,
)

from .grpc_server_test_utils.client_creation_monkeypatch import monkeypatch_client_creation


class MockWorkflowClientForUnsupportedDatapinTest:
    def __init__(self):
        pass


def test_set_metadata(monkeypatch, engine) -> None:
    # Setup
    mock_client = MockWorkflowClientForUnsupportedDatapinTest()
    monkeypatch_client_creation(monkeypatch, UnsupportedTypeDatapin, mock_client)
    sut = UnsupportedTypeDatapin(element_id=ElementId(id_string="VAR_UNDER_TEST_ID"), engine=engine)

    # SUT/Verification
    with pytest.raises(DatapinWithUnsupportedTypeException):
        sut.set_metadata(atvi.BooleanMetadata())


def test_set_state(monkeypatch, engine) -> None:
    # Setup
    mock_client = MockWorkflowClientForUnsupportedDatapinTest()
    monkeypatch_client_creation(monkeypatch, UnsupportedTypeDatapin, mock_client)
    sut = UnsupportedTypeDatapin(element_id=ElementId(id_string="VAR_UNDER_TEST_ID"), engine=engine)

    # SUT/Verification
    with pytest.raises(DatapinWithUnsupportedTypeException):
        sut.set_state(VariableState())


def test_get_metadata(monkeypatch, engine) -> None:
    # Setup
    mock_client = MockWorkflowClientForUnsupportedDatapinTest()
    monkeypatch_client_creation(monkeypatch, UnsupportedTypeDatapin, mock_client)
    sut = UnsupportedTypeDatapin(element_id=ElementId(id_string="VAR_UNDER_TEST_ID"), engine=engine)

    # SUT/Verification
    with pytest.raises(DatapinWithUnsupportedTypeException):
        sut.get_metadata()
