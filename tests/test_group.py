# Copyright (C) 2022 - 2024 ANSYS, Inc. and/or its affiliates.
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

from typing import Dict

from ansys.api.modelcenter.v0.element_messages_pb2 import (
    ElementId,
    ElementIdCollection,
    ElementName,
    ElementType,
)
from ansys.api.modelcenter.v0.variable_value_messages_pb2 import VariableType
import pytest

import ansys.modelcenter.workflow.api as mc_api
from ansys.modelcenter.workflow.grpc_modelcenter.abstract_workflow_element import (
    AbstractWorkflowElement,
)
from ansys.modelcenter.workflow.grpc_modelcenter.group import Group
from ansys.modelcenter.workflow.grpc_modelcenter.unsupported_type_datapin import (
    UnsupportedTypeDatapin,
)
from tests.grpc_server_test_utils.client_creation_monkeypatch import monkeypatch_client_creation
import tests.test_abstract_workflow_element as awe_tests
import tests.test_datapin_container as base_tests


class MockWorkflowClientForAssemblyTest:
    def __init__(self) -> None:
        self._name_responses: Dict[str, str] = {}

    @property
    def name_responses(self):
        return self._name_responses

    def ElementGetName(self, request: ElementId) -> ElementName:
        return ElementName(name=self._name_responses[request.id_string])

    def ElementGetFullName(self, request: ElementId) -> ElementName:
        return ElementName(name=self._name_responses[request.id_string])

    def RegistryGetVariables(self, request: ElementId) -> ElementIdCollection:
        return ElementIdCollection()

    def RegistryGetGroups(self, request: ElementId) -> ElementIdCollection:
        return ElementIdCollection()


def test_get_variables_empty(monkeypatch, engine):
    base_tests.do_test_get_datapins_empty(monkeypatch, engine, Group)


@pytest.mark.parametrize(
    "var_type,expected_wrapper_type",
    [
        (VariableType.VARIABLE_TYPE_INTEGER, mc_api.IIntegerDatapin),
        (VariableType.VARIABLE_TYPE_REAL, mc_api.IRealDatapin),
        (VariableType.VARIABLE_TYPE_BOOLEAN, mc_api.IBooleanDatapin),
        (VariableType.VARIABLE_TYPE_STRING, mc_api.IStringDatapin),
        (VariableType.VARIABLE_TYPE_FILE, mc_api.IFileDatapin),
        (VariableType.VARIABLE_TYPE_INTEGER_ARRAY, mc_api.IIntegerArrayDatapin),
        (VariableType.VARIABLE_TYPE_REAL_ARRAY, mc_api.IRealArrayDatapin),
        (VariableType.VARIABLE_TYPE_BOOLEAN_ARRAY, mc_api.IBooleanArrayDatapin),
        (VariableType.VARIABLE_TYPE_STRING_ARRAY, mc_api.IStringArrayDatapin),
        (VariableType.VARIABLE_TYPE_FILE_ARRAY, mc_api.IFileArrayDatapin),
        (VariableType.VARIABLE_TYPE_UNSPECIFIED, UnsupportedTypeDatapin),
    ],
)
def test_get_variables_one_variable(monkeypatch, engine, var_type, expected_wrapper_type):
    base_tests.do_test_get_datapins_one_variable(
        monkeypatch, engine, Group, var_type, expected_wrapper_type
    )


def test_get_variables_multiple_variables(monkeypatch, engine):
    base_tests.do_test_get_datapins_multiple_variables(monkeypatch, engine, Group)


def test_get_groups_empty(monkeypatch, engine):
    base_tests.do_test_get_groups_empty(monkeypatch, engine, Group)


def test_get_groups_one_group(monkeypatch, engine):
    base_tests.do_test_get_groups_one_group(monkeypatch, engine, Group)


def test_get_groups_multiple_groups(monkeypatch, engine):
    base_tests.do_test_get_groups_multiple_groups(monkeypatch, engine, Group)


def test_element_id(monkeypatch, engine) -> None:
    awe_tests.do_test_element_id(monkeypatch, engine, Group, "SUT_TEST_ID")


def test_parent_element_id(monkeypatch, engine) -> None:
    awe_tests.do_test_parent_element_id(monkeypatch, engine, Group)


def test_name(monkeypatch, engine) -> None:
    awe_tests.do_test_name(monkeypatch, engine, Group)


def test_full_name(monkeypatch, engine) -> None:
    awe_tests.do_test_name(monkeypatch, engine, Group)


def test_parent_element(monkeypatch, engine) -> None:
    awe_tests.do_test_parent_element(
        monkeypatch, engine, Group, ElementType.ELEMENT_TYPE_GROUP, Group
    )


def test_get_property_names(monkeypatch, engine) -> None:
    awe_tests.do_test_get_property_names(monkeypatch, engine, Group)


def test_get_properties(monkeypatch, engine) -> None:
    awe_tests.do_test_get_properties(monkeypatch, engine, Group)


def test_can_get_name(monkeypatch, engine):
    mock_client = MockWorkflowClientForAssemblyTest()
    mock_client.name_responses["TEST_ID_SHOULD_MATCH"] = "expected_name"
    monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
    sut = Group(ElementId(id_string="TEST_ID_SHOULD_MATCH"), engine=engine)

    result = sut.name

    assert result == "expected_name"
