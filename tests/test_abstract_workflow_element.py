import unittest

from ansys.modelcenter.workflow.grpc_modelcenter.abstract_workflow_element import (
    AbstractWorkflowElement,
)
from ansys.modelcenter.workflow.grpc_modelcenter.proto.element_messages_pb2 import (
    ElementId,
    ElementName,
)
from ansys.modelcenter.workflow.grpc_modelcenter.proto.workflow_messages_pb2 import ElementInfo
from tests.grpc_server_test_utils.client_creation_monkeypatch import monkeypatch_client_creation


class MockWorkflowClientForAbstractWorkflowElementTest:
    def __init__(self):
        pass

    def ElementGetParentElement(self, request: ElementId) -> ElementInfo:
        return ElementInfo()

    def ElementGetName(self, request: ElementId) -> ElementName:
        return ElementName()

    def ElementGetFullName(self, request: ElementId) -> ElementName:
        return ElementName()


def do_test_element_id(monkeypatch, sut_type, element_id: str):
    monkeypatch_client_creation(
        monkeypatch, AbstractWorkflowElement, MockWorkflowClientForAbstractWorkflowElementTest()
    )
    sut = sut_type(ElementId(id_string=element_id), None)

    result = sut.element_id

    assert result == element_id


def do_test_parent_element_id(monkeypatch, sut_type):
    element_id_in_response = "PARENT_ELEMENT_OF_SUT"
    mock_client = MockWorkflowClientForAbstractWorkflowElementTest()
    mock_response = ElementInfo(id=ElementId(id_string=element_id_in_response))
    sut_element_id = ElementId(id_string="SUT_ELEMENT")
    with unittest.mock.patch.object(
        mock_client, "ElementGetParentElement", return_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = sut_type(sut_element_id, None)

        result = sut.parent_element_id

        assert result == element_id_in_response
        mock_grpc_method.assert_called_once_with(sut_element_id)


def do_test_name(monkeypatch, sut_type):
    name_in_response = "sut"
    mock_client = MockWorkflowClientForAbstractWorkflowElementTest()
    mock_response = ElementName(name=name_in_response)
    sut_element_id = ElementId(id_string="SUT_ELEMENT")
    with unittest.mock.patch.object(
        mock_client, "ElementGetName", return_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = sut_type(sut_element_id, None)

        result = sut.name

        assert result == name_in_response
        mock_grpc_method.assert_called_once_with(sut_element_id)


def do_test_full_name(monkeypatch, sut_type):
    name_in_response = "Model.Internals.Widgets.sut"
    mock_client = MockWorkflowClientForAbstractWorkflowElementTest()
    mock_response = ElementName(name=name_in_response)
    sut_element_id = ElementId(id_string="SUT_ELEMENT_ID")
    with unittest.mock.patch.object(
        mock_client, "ElementGetFullName", return_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = sut_type(sut_element_id, None)

        result = sut.full_name

        assert result == name_in_response
        mock_grpc_method.assert_called_once_with(sut_element_id)


def do_test_parent_element(monkeypatch, sut_type, type_in_response, expected_parent_wrapper_type):
    mock_client = MockWorkflowClientForAbstractWorkflowElementTest()
    id_in_response = "PARENT_OF_SUT_ELEMENT"
    sut_element_id = ElementId(id_string="SUT_ELEMENT_ID")
    mock_response = ElementInfo(id=ElementId(id_string=id_in_response), type=type_in_response)
    with unittest.mock.patch.object(
        mock_client, "ElementGetParentElement", return_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = sut_type(sut_element_id, None)

        result = sut.get_parent_element()

        assert result.element_id == id_in_response
        assert isinstance(result, expected_parent_wrapper_type)
        mock_grpc_method.assert_called_once_with(sut_element_id)
