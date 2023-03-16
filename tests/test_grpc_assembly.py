from typing import Dict, Optional

import pytest

from ansys.modelcenter.workflow.grpc_modelcenter.assembly import Assembly
from ansys.modelcenter.workflow.grpc_modelcenter.proto.element_messages_pb2 import (
    AssemblyType,
    ElementId,
    ElementName,
)

from .grpc_server_test_utils.client_creation_monkeypatch import monkeypatch_client_creation


class MockWorkflowClientForAssemblyTest:
    def __init__(self):
        self._name_responses: Dict[str, str] = {}
        self._parent_id_responses: Dict[str, str] = {}
        self._control_type_responses: Dict[str, str] = {}

    @property
    def name_responses(self):
        return self._name_responses

    @property
    def parent_id_responses(self):
        return self._parent_id_responses

    @property
    def control_type_responses(self):
        return self._control_type_responses

    def ElementGetName(self, request: ElementId) -> ElementName:
        return ElementName(name=self._name_responses[request.id_string])

    def ElementGetFullName(self, request: ElementId) -> ElementName:
        return ElementName(name=self._name_responses[request.id_string])

    def RegistryGetControlType(self, request: ElementId) -> ElementName:
        return AssemblyType(type=self._control_type_responses[request.id_string])

    def ElementGetParentElement(self, request: ElementId) -> ElementId:
        return ElementId(id_string=self._parent_id_responses[request.id_string])


def test_can_get_name(monkeypatch):
    mock_client = MockWorkflowClientForAssemblyTest()
    mock_client.name_responses["TEST_ID_SHOULD_MATCH"] = "expected_name"
    monkeypatch_client_creation(monkeypatch, Assembly, mock_client)
    sut = Assembly(ElementId(id_string="TEST_ID_SHOULD_MATCH"), None)

    result = sut.name

    assert result == "expected_name"


def test_can_get_full_name(monkeypatch):
    mock_client = MockWorkflowClientForAssemblyTest()
    mock_client.name_responses["TEST_ID_SHOULD_MATCH"] = "model.expected_name"
    monkeypatch_client_creation(monkeypatch, Assembly, mock_client)
    sut = Assembly(ElementId(id_string="TEST_ID_SHOULD_MATCH"), None)

    result = sut.get_full_name()

    assert result == "model.expected_name"


def test_can_get_control_type(monkeypatch):
    mock_client = MockWorkflowClientForAssemblyTest()
    mock_client.control_type_responses["TEST_ID_SHOULD_MATCH"] = "Sequence"
    monkeypatch_client_creation(monkeypatch, Assembly, mock_client)

    sut = Assembly(ElementId(id_string="TEST_ID_SHOULD_MATCH"), None)

    result = sut.control_type

    assert result == "Sequence"


@pytest.mark.parametrize("returned_id", [None, ""])
def test_can_get_parent_no_parent(monkeypatch, returned_id: Optional[str]):
    mock_client = MockWorkflowClientForAssemblyTest()
    test_id_string = "TEST_ID_SHOULD_MATCH"
    mock_client.parent_id_responses[test_id_string] = returned_id
    monkeypatch_client_creation(monkeypatch, Assembly, mock_client)

    sut = Assembly(ElementId(id_string=test_id_string), None)

    result = sut.parent_assembly

    assert result is None


def test_can_get_parent_has_parent(monkeypatch):
    mock_client = MockWorkflowClientForAssemblyTest()
    test_id_string = "TEST_ID_SHOULD_MATCH"
    parent_id_string = "PARENT_ID"
    mock_client.parent_id_responses[test_id_string] = parent_id_string
    monkeypatch_client_creation(monkeypatch, Assembly, mock_client)

    sut = Assembly(ElementId(id_string=test_id_string), None)

    result = sut.parent_assembly

    assert isinstance(result, Assembly)
    assert result.element_id == parent_id_string
