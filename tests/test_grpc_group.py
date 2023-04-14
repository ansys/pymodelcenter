from typing import Dict

import pytest

import ansys.modelcenter.workflow.api as mc_api
from ansys.modelcenter.workflow.grpc_modelcenter.abstract_workflow_element import (
    AbstractWorkflowElement,
)
from ansys.modelcenter.workflow.grpc_modelcenter.group import Group
from ansys.modelcenter.workflow.grpc_modelcenter.proto.element_messages_pb2 import (
    ElementId,
    ElementIdCollection,
    ElementName,
    ElementType,
)
from ansys.modelcenter.workflow.grpc_modelcenter.proto.variable_value_messages_pb2 import (
    VariableType,
)
from ansys.modelcenter.workflow.grpc_modelcenter.unsupported_var import UnsupportedTypeDatapin
from tests.grpc_server_test_utils.client_creation_monkeypatch import monkeypatch_client_creation
import tests.test_abstract_workflow_element as awe_tests
import tests.test_variable_container as base_tests


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


def test_get_variables_empty(monkeypatch):
    base_tests.do_test_get_datapins_empty(monkeypatch, Group)


@pytest.mark.parametrize(
    "var_type,expected_wrapper_type",
    [
        (VariableType.VARTYPE_INTEGER, mc_api.IIntegerDatapin),
        (VariableType.VARTYPE_REAL, mc_api.IRealDatapin),
        (VariableType.VARTYPE_BOOLEAN, mc_api.IBooleanDatapin),
        (VariableType.VARTYPE_STRING, mc_api.IStringDatapin),
        (VariableType.VARTYPE_FILE, UnsupportedTypeDatapin),
        (VariableType.VARTYPE_INTEGER_ARRAY, mc_api.IIntegerArray),
        (VariableType.VARTYPE_REAL_ARRAY, mc_api.IRealArrayDatapin),
        (VariableType.VARTYPE_BOOLEAN_ARRAY, mc_api.IBooleanArrayDatapin),
        (VariableType.VARTYPE_STRING_ARRAY, mc_api.IStringArrayDatapin),
        (VariableType.VARTYPE_FILE_ARRAY, UnsupportedTypeDatapin),
        (VariableType.VARTYPE_UNKNOWN, UnsupportedTypeDatapin),
    ],
)
def test_get_variables_one_variable(monkeypatch, var_type, expected_wrapper_type):
    base_tests.do_test_get_datapins_one_variable(
        monkeypatch, Group, var_type, expected_wrapper_type
    )


def test_get_variables_multiple_variables(monkeypatch):
    base_tests.do_test_get_datapins_multiple_variables(monkeypatch, Group)


def test_get_groups_empty(monkeypatch):
    base_tests.do_test_get_groups_empty(monkeypatch, Group)


def test_get_groups_one_group(monkeypatch):
    base_tests.do_test_get_groups_one_group(monkeypatch, Group)


def test_get_groups_multiple_groups(monkeypatch):
    base_tests.do_test_get_groups_multiple_groups(monkeypatch, Group)


def test_element_id(monkeypatch) -> None:
    awe_tests.do_test_element_id(monkeypatch, Group, "SUT_TEST_ID")


def test_parent_element_id(monkeypatch) -> None:
    awe_tests.do_test_parent_element_id(monkeypatch, Group)


def test_name(monkeypatch) -> None:
    awe_tests.do_test_name(monkeypatch, Group)


def test_full_name(monkeypatch) -> None:
    awe_tests.do_test_name(monkeypatch, Group)


def test_parent_element(monkeypatch) -> None:
    awe_tests.do_test_parent_element(monkeypatch, Group, ElementType.ELEMTYPE_GROUP, Group)


def test_get_property_names(monkeypatch) -> None:
    awe_tests.do_test_get_property_names(monkeypatch, Group)


def test_get_properties(monkeypatch) -> None:
    awe_tests.do_test_get_properties(monkeypatch, Group)


def test_can_get_name(monkeypatch):
    mock_client = MockWorkflowClientForAssemblyTest()
    mock_client.name_responses["TEST_ID_SHOULD_MATCH"] = "expected_name"
    monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
    sut = Group(ElementId(id_string="TEST_ID_SHOULD_MATCH"), None)

    result = sut.name

    assert result == "expected_name"
