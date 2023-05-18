import unittest

import pytest

import ansys.modelcenter.workflow.api as mc_api
from ansys.modelcenter.workflow.grpc_modelcenter.abstract_workflow_element import (
    AbstractWorkflowElement,
)
from ansys.modelcenter.workflow.grpc_modelcenter.component import Component
from ansys.modelcenter.workflow.grpc_modelcenter.proto.element_messages_pb2 import (
    AnalysisViewPosition,
    ComponentDownloadValuesResponse,
    ComponentInvalidateResponse,
    ComponentInvokeMethodRequest,
    ComponentInvokeMethodResponse,
    ComponentIsConnectedResponse,
    ComponentPaczUrlResponse,
    ComponentReconnectResponse,
    ComponentSourceResponse,
    ElementId,
    ElementType,
)
from ansys.modelcenter.workflow.grpc_modelcenter.proto.variable_value_messages_pb2 import (
    VariableType,
)
from ansys.modelcenter.workflow.grpc_modelcenter.unsupported_type_datapin import (
    UnsupportedTypeDatapin,
)
from tests.grpc_server_test_utils.client_creation_monkeypatch import monkeypatch_client_creation
import tests.test_abstract_workflow_element as awe_tests
import tests.test_datapin_container as varcontainer_tests


class MockWorkflowClientForComponentTests:
    def __init__(self):
        pass

    def ComponentGetSource(self, request: ElementId) -> ComponentSourceResponse:
        return ComponentSourceResponse()

    def ComponentInvokeMethod(
        self, request: ComponentInvokeMethodRequest
    ) -> ComponentInvokeMethodResponse:
        return ComponentInvokeMethodResponse()

    def ComponentInvalidate(self, request: ElementId) -> ComponentInvalidateResponse:
        return ComponentInvalidateResponse()

    def ComponentIsConnected(self, request: ElementId) -> ComponentIsConnectedResponse:
        return ComponentIsConnectedResponse()

    def ComponentReconnect(self, request: ElementId) -> ComponentReconnectResponse:
        return ComponentReconnectResponse()

    def ComponentDownloadValues(self, request: ElementId) -> ComponentDownloadValuesResponse:
        return ComponentDownloadValuesResponse()

    def AssemblyGetAnalysisViewPosition(self, request: ElementId) -> AnalysisViewPosition:
        return AnalysisViewPosition()

    def ComponentGetPaczUrl(self, request: ElementId) -> ComponentPaczUrlResponse:
        return ComponentPaczUrlResponse()


def test_element_id(monkeypatch, engine) -> None:
    awe_tests.do_test_element_id(monkeypatch, engine, Component, "SUT_TEST_ID")


def test_parent_element_id(monkeypatch, engine) -> None:
    awe_tests.do_test_parent_element_id(monkeypatch, engine, Component)


def test_name(monkeypatch, engine) -> None:
    awe_tests.do_test_name(monkeypatch, engine, Component)


def test_full_name(monkeypatch, engine) -> None:
    awe_tests.do_test_name(monkeypatch, engine, Component)


def test_parent_element(monkeypatch, engine) -> None:
    awe_tests.do_test_parent_element(
        monkeypatch, engine, Component, ElementType.ELEMTYPE_COMPONENT, Component
    )


def test_get_property_names(monkeypatch, engine) -> None:
    awe_tests.do_test_get_property_names(monkeypatch, engine, Component)


def test_get_properties(monkeypatch, engine) -> None:
    awe_tests.do_test_get_properties(monkeypatch, engine, Component)


def test_get_variables_empty(monkeypatch, engine):
    varcontainer_tests.do_test_get_datapins_empty(monkeypatch, engine, Component)


@pytest.mark.parametrize(
    "var_type,expected_wrapper_type",
    [
        (VariableType.VARTYPE_INTEGER, mc_api.IIntegerDatapin),
        (VariableType.VARTYPE_REAL, mc_api.IRealDatapin),
        (VariableType.VARTYPE_BOOLEAN, mc_api.IBooleanDatapin),
        (VariableType.VARTYPE_STRING, mc_api.IStringDatapin),
        (VariableType.VARTYPE_FILE, UnsupportedTypeDatapin),
        (VariableType.VARTYPE_INTEGER_ARRAY, mc_api.IIntegerArrayDatapin),
        (VariableType.VARTYPE_REAL_ARRAY, mc_api.IRealArrayDatapin),
        (VariableType.VARTYPE_BOOLEAN_ARRAY, mc_api.IBooleanArrayDatapin),
        (VariableType.VARTYPE_STRING_ARRAY, mc_api.IStringArrayDatapin),
        (VariableType.VARTYPE_FILE_ARRAY, UnsupportedTypeDatapin),
        (VariableType.VARTYPE_UNKNOWN, UnsupportedTypeDatapin),
    ],
)
def test_get_variables_one_variable(monkeypatch, engine, var_type, expected_wrapper_type):
    varcontainer_tests.do_test_get_datapins_one_variable(
        monkeypatch, engine, Component, var_type, expected_wrapper_type
    )


def test_get_variables_multiple_variables(monkeypatch, engine):
    varcontainer_tests.do_test_get_datapins_multiple_variables(monkeypatch, engine, Component)


def test_get_groups_empty(monkeypatch, engine):
    varcontainer_tests.do_test_get_groups_empty(monkeypatch, engine, Component)


def test_get_groups_one_group(monkeypatch, engine):
    varcontainer_tests.do_test_get_groups_one_group(monkeypatch, engine, Component)


def test_get_groups_multiple_groups(monkeypatch, engine):
    varcontainer_tests.do_test_get_groups_one_group(monkeypatch, engine, Component)


def test_get_source(monkeypatch, engine):
    mock_client = MockWorkflowClientForComponentTests()
    mock_response = ComponentSourceResponse(source="common:/Quadratic")
    sut_id = ElementId(id_string="SUT_COMPONENT_ID")
    with unittest.mock.patch.object(
        mock_client, "ComponentGetSource", return_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = Component(sut_id, engine=engine)

        result = sut.get_source()

        mock_grpc_method.assert_called_once_with(sut_id)
        assert result == "common:/Quadratic", "The result should be what the gRPC client reported."


def test_invoke_method(monkeypatch, engine):
    mock_client = MockWorkflowClientForComponentTests()
    mock_response = ComponentInvokeMethodResponse()
    sut_id = ElementId(id_string="SUT_COMPONENT_ID")
    with unittest.mock.patch.object(
        mock_client, "ComponentInvokeMethod", return_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = Component(sut_id, engine=engine)

        sut.invoke_method("CustomComponentMethod()")

        expected_request = ComponentInvokeMethodRequest(
            target=sut_id, method_name="CustomComponentMethod()"
        )
        mock_grpc_method.assert_called_once_with(expected_request)


def test_invalidate(monkeypatch, engine):
    mock_client = MockWorkflowClientForComponentTests()
    mock_response = ComponentInvalidateResponse()
    sut_id = ElementId(id_string="SUT_COMPONENT_ID")
    with unittest.mock.patch.object(
        mock_client, "ComponentInvalidate", return_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = Component(sut_id, engine=engine)

        sut.invalidate()

        mock_grpc_method.assert_called_once_with(sut_id)


@pytest.mark.parametrize("value_in_response", [True, False])
def test_is_connected(monkeypatch, engine, value_in_response):

    mock_client = MockWorkflowClientForComponentTests()
    mock_response = ComponentIsConnectedResponse(is_connected=value_in_response)
    sut_id = ElementId(id_string="SUT_COMPONENT_ID")
    with unittest.mock.patch.object(
        mock_client, "ComponentIsConnected", return_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = Component(sut_id, engine=engine)

        result = sut.is_connected

        mock_grpc_method.assert_called_once_with(sut_id)
        assert result == value_in_response, "The result should be what the gRPC client reported."


def test_reconnect(monkeypatch, engine):
    mock_client = MockWorkflowClientForComponentTests()
    mock_response = ComponentReconnectResponse()
    sut_id = ElementId(id_string="SUT_COMPONENT_ID")
    with unittest.mock.patch.object(
        mock_client, "ComponentReconnect", return_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = Component(sut_id, engine=engine)

        sut.reconnect()

        mock_grpc_method.assert_called_once_with(sut_id)


def test_download_values(monkeypatch, engine):
    mock_client = MockWorkflowClientForComponentTests()
    mock_response = ComponentDownloadValuesResponse()
    sut_id = ElementId(id_string="SUT_COMPONENT_ID")
    with unittest.mock.patch.object(
        mock_client, "ComponentDownloadValues", return_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = Component(sut_id, engine=engine)

        sut.download_values()

        mock_grpc_method.assert_called_once_with(sut_id)


def test_get_analysis_view_position(monkeypatch, engine):
    mock_client = MockWorkflowClientForComponentTests()
    mock_response = AnalysisViewPosition(x_pos=47, y_pos=9001)
    sut_id = ElementId(id_string="SUT_COMPONENT_ID")
    with unittest.mock.patch.object(
        mock_client, "AssemblyGetAnalysisViewPosition", return_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = Component(sut_id, engine=engine)

        result = sut.get_analysis_view_position()

        mock_grpc_method.assert_called_once_with(sut_id)
        assert result == (47, 9001)


@pytest.mark.parametrize(
    "url_in_response,url_set_in_response,expected_result",
    [
        ("file://C/component.pacz", True, "file://C/component.pacz"),
        ("common:/Quadratic", False, None),
    ],
)
def test_pacz_url(monkeypatch, engine, url_in_response, url_set_in_response, expected_result):
    mock_client = MockWorkflowClientForComponentTests()
    mock_response = ComponentPaczUrlResponse()
    if url_set_in_response:
        mock_response.pacz_url = url_in_response
    sut_id = ElementId(id_string="SUT_COMPONENT_ID")
    with unittest.mock.patch.object(
        mock_client, "ComponentGetPaczUrl", return_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = Component(sut_id, engine=engine)

        result = sut.pacz_url

        assert result == expected_result
        mock_grpc_method.assert_called_once_with(sut_id)
