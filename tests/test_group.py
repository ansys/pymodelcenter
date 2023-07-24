from typing import Dict

import pytest

import ansys.modelcenter.workflow.api as mc_api
import tests.test_abstract_workflow_element as awe_tests
import tests.test_datapin_container as base_tests
from ansys.modelcenter.workflow.grpc_modelcenter.abstract_workflow_element import \
    AbstractWorkflowElement
from ansys.modelcenter.workflow.grpc_modelcenter.group import Group
from ansys.modelcenter.workflow.grpc_modelcenter.proto.element_messages_pb2 import (
    ElementId, ElementIdCollection, ElementName, ElementType)
from ansys.modelcenter.workflow.grpc_modelcenter.proto.variable_value_messages_pb2 import \
    VariableType
from ansys.modelcenter.workflow.grpc_modelcenter.unsupported_type_datapin import \
    UnsupportedTypeDatapin
from tests.grpc_server_test_utils.client_creation_monkeypatch import \
    monkeypatch_client_creation


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
        (VariableType.VARTYPE_INTEGER, mc_api.IIntegerDatapin),
        (VariableType.VARTYPE_REAL, mc_api.IRealDatapin),
        (VariableType.VARTYPE_BOOLEAN, mc_api.IBooleanDatapin),
        (VariableType.VARTYPE_STRING, mc_api.IStringDatapin),
        (VariableType.VARTYPE_FILE, mc_api.IFileDatapin),
        (VariableType.VARTYPE_INTEGER_ARRAY, mc_api.IIntegerArrayDatapin),
        (VariableType.VARTYPE_REAL_ARRAY, mc_api.IRealArrayDatapin),
        (VariableType.VARTYPE_BOOLEAN_ARRAY, mc_api.IBooleanArrayDatapin),
        (VariableType.VARTYPE_STRING_ARRAY, mc_api.IStringArrayDatapin),
        (VariableType.VARTYPE_FILE_ARRAY, mc_api.IFileArrayDatapin),
        (VariableType.VARTYPE_UNKNOWN, UnsupportedTypeDatapin),
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
    awe_tests.do_test_parent_element(monkeypatch, engine, Group, ElementType.ELEMTYPE_GROUP, Group)


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
