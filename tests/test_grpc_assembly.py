from typing import Dict

from ansys.modelcenter.workflow.grpc_modelcenter.assembly import Assembly
from ansys.modelcenter.workflow.grpc_modelcenter.proto.element_messages_pb2 import (
    ElementId,
    ElementName,
)

from .grpc_server_test_utils.client_creation_monkeypatch import monkeypatch_client_creation


class MockWorkflowClientForAssemblyTest:
    def __init__(self):
        self._name_responses: Dict[str, str] = {}

    @property
    def name_responses(self):
        return self._name_responses

    def ElementGetName(self, request: ElementId) -> ElementName:
        return ElementName(name=self._name_responses[request.id_string])

    def ElementGetFullName(self, request: ElementId) -> ElementName:
        return ElementName(name=self._name_responses[request.id_string])


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
