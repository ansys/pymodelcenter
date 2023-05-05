import unittest

import ansys.engineeringworkflow.api as aew_api
import ansys.tools.variableinterop as atvi

from ansys.modelcenter.workflow.grpc_modelcenter.abstract_workflow_element import (
    AbstractWorkflowElement,
)
from ansys.modelcenter.workflow.grpc_modelcenter.proto.custom_metadata_messages_pb2 import (
    MetadataGetValueRequest,
    MetadataPropertyNamesResponse,
)
from ansys.modelcenter.workflow.grpc_modelcenter.proto.element_messages_pb2 import (
    ElementId,
    ElementName,
    ElementType,
)
from ansys.modelcenter.workflow.grpc_modelcenter.proto.variable_value_messages_pb2 import (
    VariableValue,
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

    def PropertyOwnerGetProperties(self, request: ElementId) -> MetadataPropertyNamesResponse:
        return MetadataPropertyNamesResponse()

    def PropertyOwnerGetPropertyValue(self, request: MetadataGetValueRequest) -> VariableValue:
        return VariableValue()


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


def do_test_get_property_names(monkeypatch, sut_type) -> None:
    names_in_response = {
        "Model.Internals.Widgets.sut.lowerBound",
        "Model.Internals.Widgets.sut.upperBound",
    }
    mock_client = MockWorkflowClientForAbstractWorkflowElementTest()
    mock_response = MetadataPropertyNamesResponse(names=names_in_response)
    sut_get_prop_names = ElementId(id_string="SUT_ELEMENT_ID")
    with unittest.mock.patch.object(
        mock_client, "PropertyOwnerGetProperties", return_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = sut_type(sut_get_prop_names, None)

        result = sut.get_property_names()

        assert result == names_in_response
        mock_grpc_method.assert_called_once_with(sut_get_prop_names)


def do_test_get_properties(monkeypatch, sut_type) -> None:
    names_in_response = {
        "Model.Internals.Widgets.sut.lowerBound",
        "Model.Internals.Widgets.sut.upperBound",
    }
    value_response = VariableValue(int_value=-2)
    mock_client = MockWorkflowClientForAbstractWorkflowElementTest()
    mock_response = MetadataPropertyNamesResponse(names=names_in_response)
    sut_get_prop_names = ElementId(id_string="SUT_ELEMENT_ID")

    with unittest.mock.patch.object(
        mock_client, "PropertyOwnerGetProperties", return_value=mock_response
    ) as mock_grpc_method:
        with unittest.mock.patch.object(
            mock_client, "PropertyOwnerGetPropertyValue", return_value=value_response
        ):
            monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
            sut = sut_type(sut_get_prop_names, None)

            result = sut.get_properties()

            assert result == {
                name: aew_api.Property(
                    parent_element_id=sut_get_prop_names.id_string,
                    property_name=name,
                    property_value=atvi.IntegerValue(value_response.int_value),
                )
                for name in names_in_response
            }
            mock_grpc_method.assert_called_once_with(sut_get_prop_names)


def test_parent_element(monkeypatch) -> None:
    do_test_parent_element(
        monkeypatch, AbstractWorkflowElement, ElementType.ELEMTYPE_UNKNOWN, AbstractWorkflowElement
    )
