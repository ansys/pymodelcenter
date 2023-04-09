import unittest

import pytest

import ansys.modelcenter.workflow.api as mc_api
from ansys.modelcenter.workflow.grpc_modelcenter.abstract_workflow_element import (
    AbstractWorkflowElement,
)
from ansys.modelcenter.workflow.grpc_modelcenter.assembly import Assembly
from ansys.modelcenter.workflow.grpc_modelcenter.component import Component
from ansys.modelcenter.workflow.grpc_modelcenter.proto.element_messages_pb2 import (
    AnalysisViewPosition,
    ComponentDownloadValuesResponse,
    ComponentInvalidateResponse,
    ComponentInvokeMethodRequest,
    ComponentInvokeMethodResponse,
    ComponentIsConnectedResponse,
    ComponentReconnectResponse,
    ComponentSourceResponse,
    ElementId,
    ElementType,
)
from ansys.modelcenter.workflow.grpc_modelcenter.proto.variable_value_messages_pb2 import (
    VariableType,
)
from ansys.modelcenter.workflow.grpc_modelcenter.unsupported_var import UnsupportedTypeVariable
from tests.grpc_server_test_utils.client_creation_monkeypatch import monkeypatch_client_creation
import tests.test_abstract_workflow_element as awe_tests
import tests.test_variable_container as varcontainer_tests


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


def test_element_id(monkeypatch) -> None:
    awe_tests.do_test_element_id(monkeypatch, Component, "SUT_TEST_ID")


def test_parent_element_id(monkeypatch) -> None:
    awe_tests.do_test_parent_element_id(monkeypatch, Component)


def test_name(monkeypatch) -> None:
    awe_tests.do_test_name(monkeypatch, Component)


def test_full_name(monkeypatch) -> None:
    awe_tests.do_test_name(monkeypatch, Component)


def test_parent_element(monkeypatch) -> None:
    awe_tests.do_test_parent_element(
        monkeypatch, Component, ElementType.ELEMTYPE_ASSEMBLY, Assembly
    )


def test_get_variables_empty(monkeypatch):
    varcontainer_tests.do_test_get_variables_empty(monkeypatch, Component)


@pytest.mark.parametrize(
    "var_type,expected_wrapper_type",
    [
        (VariableType.VARTYPE_INTEGER, mc_api.IIntegerVariable),
        (VariableType.VARTYPE_REAL, mc_api.IDoubleVariable),
        (VariableType.VARTYPE_BOOLEAN, mc_api.IBooleanVariable),
        (VariableType.VARTYPE_STRING, mc_api.IStringVariable),
        (VariableType.VARTYPE_FILE, UnsupportedTypeVariable),
        (VariableType.VARTYPE_INTEGER_ARRAY, mc_api.IIntegerArray),
        (VariableType.VARTYPE_REAL_ARRAY, mc_api.IDoubleArray),
        (VariableType.VARTYPE_BOOLEAN_ARRAY, mc_api.IBooleanArray),
        (VariableType.VARTYPE_STRING_ARRAY, mc_api.IStringArray),
        (VariableType.VARTYPE_FILE_ARRAY, UnsupportedTypeVariable),
        (VariableType.VARTYPE_UNKNOWN, UnsupportedTypeVariable),
    ],
)
def test_get_variables_one_variable(monkeypatch, var_type, expected_wrapper_type):
    varcontainer_tests.do_test_get_variables_one_variable(
        monkeypatch, Component, var_type, expected_wrapper_type
    )


def test_get_variables_multiple_variables(monkeypatch):
    varcontainer_tests.do_test_get_variables_multiple_variables(monkeypatch, Component)


def test_get_groups_empty(monkeypatch):
    varcontainer_tests.do_test_get_groups_empty(monkeypatch, Component)


def test_get_groups_one_group(monkeypatch):
    varcontainer_tests.do_test_get_groups_one_group(monkeypatch, Component)


def test_get_groups_multiple_groups(monkeypatch):
    varcontainer_tests.do_test_get_groups_one_group(monkeypatch, Component)


def test_get_source(monkeypatch):
    mock_client = MockWorkflowClientForComponentTests()
    mock_response = ComponentSourceResponse(source="common:/Quadratic")
    sut_id = ElementId(id_string="SUT_COMPONENT_ID")
    with unittest.mock.patch.object(
        mock_client, "ComponentGetSource", return_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = Component(sut_id, None)

        result = sut.get_source()

        mock_grpc_method.assert_called_once_with(sut_id)
        assert result == "common:/Quadratic", "The result should be what the gRPC client reported."


def test_invoke_method(monkeypatch):
    mock_client = MockWorkflowClientForComponentTests()
    mock_response = ComponentInvokeMethodResponse()
    sut_id = ElementId(id_string="SUT_COMPONENT_ID")
    with unittest.mock.patch.object(
        mock_client, "ComponentInvokeMethod", return_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = Component(sut_id, None)

        sut.invoke_method("CustomComponentMethod()")

        expected_request = ComponentInvokeMethodRequest(
            target=sut_id, method_name="CustomComponentMethod()"
        )
        mock_grpc_method.assert_called_once_with(expected_request)


def test_invalidate(monkeypatch):
    mock_client = MockWorkflowClientForComponentTests()
    mock_response = ComponentInvalidateResponse()
    sut_id = ElementId(id_string="SUT_COMPONENT_ID")
    with unittest.mock.patch.object(
        mock_client, "ComponentInvalidate", return_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = Component(sut_id, None)

        sut.invalidate()

        mock_grpc_method.assert_called_once_with(sut_id)


@pytest.mark.parametrize("value_in_response", [True, False])
def test_is_connected(monkeypatch, value_in_response):

    mock_client = MockWorkflowClientForComponentTests()
    mock_response = ComponentIsConnectedResponse(is_connected=value_in_response)
    sut_id = ElementId(id_string="SUT_COMPONENT_ID")
    with unittest.mock.patch.object(
        mock_client, "ComponentIsConnected", return_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = Component(sut_id, None)

        result = sut.is_connected

        mock_grpc_method.assert_called_once_with(sut_id)
        assert result == value_in_response, "The result should be what the gRPC client reported."


def test_reconnect(monkeypatch):
    mock_client = MockWorkflowClientForComponentTests()
    mock_response = ComponentReconnectResponse()
    sut_id = ElementId(id_string="SUT_COMPONENT_ID")
    with unittest.mock.patch.object(
        mock_client, "ComponentReconnect", return_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = Component(sut_id, None)

        sut.reconnect()

        mock_grpc_method.assert_called_once_with(sut_id)


def test_download_values(monkeypatch):
    mock_client = MockWorkflowClientForComponentTests()
    mock_response = ComponentDownloadValuesResponse()
    sut_id = ElementId(id_string="SUT_COMPONENT_ID")
    with unittest.mock.patch.object(
        mock_client, "ComponentDownloadValues", return_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = Component(sut_id, None)

        sut.download_values()

        mock_grpc_method.assert_called_once_with(sut_id)


def test_get_analysis_view_position(monkeypatch):
    mock_client = MockWorkflowClientForComponentTests()
    mock_response = AnalysisViewPosition(x_pos=47, y_pos=9001)
    sut_id = ElementId(id_string="SUT_COMPONENT_ID")
    with unittest.mock.patch.object(
        mock_client, "AssemblyGetAnalysisViewPosition", return_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = Component(sut_id, None)

        result = sut.get_analysis_view_position()

        mock_grpc_method.assert_called_once_with(sut_id)
        assert result == (47, 9001)
