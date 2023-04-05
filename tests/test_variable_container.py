from typing import Dict
import unittest.mock

import ansys.modelcenter.workflow.api as mc_api
from ansys.modelcenter.workflow.grpc_modelcenter.abstract_workflow_element import (
    AbstractWorkflowElement,
)
from ansys.modelcenter.workflow.grpc_modelcenter.group import Group
from ansys.modelcenter.workflow.grpc_modelcenter.proto.element_messages_pb2 import (
    ElementId,
    ElementIdCollection,
    ElementName,
)
from ansys.modelcenter.workflow.grpc_modelcenter.proto.variable_value_messages_pb2 import (
    VariableInfo,
    VariableInfoCollection,
    VariableType,
)

from .grpc_server_test_utils.client_creation_monkeypatch import monkeypatch_client_creation


class MockWorkflowClientForAbstractVariableContainerTest:
    def __init__(self):
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


def do_test_get_variables_empty(monkeypatch, sut_type):
    mock_client = MockWorkflowClientForAbstractVariableContainerTest()
    no_variables = VariableInfoCollection()
    with unittest.mock.patch.object(
        mock_client, "RegistryGetVariables", return_value=no_variables
    ) as mock_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = sut_type(ElementId(id_string="NO_VARIABLES"), None)
        result = sut.get_variables()
        assert len(result) == 0
        mock_method.assert_called_once_with(ElementId(id_string="NO_VARIABLES"))


def do_test_get_variables_one_variable(monkeypatch, sut_type, var_type, expected_wrapper_type):
    mock_client = MockWorkflowClientForAbstractVariableContainerTest()
    variable_id = ElementId(id_string="VAR_ID_STRING")
    variables = VariableInfoCollection(
        variables=[VariableInfo(id=variable_id, value_type=var_type)]
    )
    with unittest.mock.patch.object(
        mock_client, "RegistryGetVariables", return_value=variables
    ) as mock_get_variable_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = sut_type(ElementId(id_string="SINGLE_CHILD"), None)
        result = sut.get_variables()
        mock_get_variable_method.assert_called_once_with(ElementId(id_string="SINGLE_CHILD"))
        assert len(result) == 1
        assert isinstance(result[0], expected_wrapper_type)
        assert result[0].element_id == variable_id.id_string


def do_test_get_variables_multiple_variables(monkeypatch, sut_type):
    mock_client = MockWorkflowClientForAbstractVariableContainerTest()
    one_child_assembly = VariableInfoCollection(
        variables=[
            VariableInfo(id=ElementId(id_string="LARRY"), value_type=VariableType.VARTYPE_INTEGER),
            VariableInfo(id=ElementId(id_string="MOE"), value_type=VariableType.VARTYPE_STRING),
            VariableInfo(id=ElementId(id_string="CURLY"), value_type=VariableType.VARTYPE_REAL),
        ]
    )
    with unittest.mock.patch.object(
        mock_client, "RegistryGetVariables", return_value=one_child_assembly
    ) as mock_get_variable_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = sut_type(ElementId(id_string="STOOGES"), None)
        result = sut.get_variables()
        mock_get_variable_method.assert_called_once_with(ElementId(id_string="STOOGES"))
        assert len(result) == 3
        assert isinstance(result[0], mc_api.IIntegerVariable)
        assert result[0].element_id == "LARRY"
        assert isinstance(result[1], mc_api.IStringVariable)
        assert result[1].element_id == "MOE"
        assert isinstance(result[2], mc_api.IDoubleVariable)
        assert result[2].element_id == "CURLY"


def do_test_get_groups_empty(monkeypatch, sut_type):
    mock_client = MockWorkflowClientForAbstractVariableContainerTest()
    no_variables = ElementIdCollection()
    with unittest.mock.patch.object(
        mock_client, "RegistryGetGroups", return_value=no_variables
    ) as mock_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = sut_type(ElementId(id_string="NO_GROUPS"), None)
        result = sut.groups
        assert len(result) == 0
        mock_method.assert_called_once_with(ElementId(id_string="NO_GROUPS"))


def do_test_get_groups_one_group(monkeypatch, sut_type):
    mock_client = MockWorkflowClientForAbstractVariableContainerTest()
    group_id = "GRP_ID_STRING"
    variables = ElementIdCollection(ids=[ElementId(id_string=group_id)])
    with unittest.mock.patch.object(
        mock_client, "RegistryGetGroups", return_value=variables
    ) as mock_get_group_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = sut_type(ElementId(id_string="SINGLE_CHILD"), None)
        result = sut.groups
        mock_get_group_method.assert_called_once_with(ElementId(id_string="SINGLE_CHILD"))
        assert len(result) == 1
        assert isinstance(result[0], Group)
        assert result[0].element_id == group_id


def do_test_get_groups_multiple_groups(monkeypatch, sut_type):
    mock_client = MockWorkflowClientForAbstractVariableContainerTest()
    one_child_assembly = ElementIdCollection(
        ids=[ElementId(id_string="LARRY"), ElementId(id_string="MOE"), ElementId(id_string="CURLY")]
    )
    with unittest.mock.patch.object(
        mock_client, "RegistryGetGroups", return_value=one_child_assembly
    ) as mock_get_group_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = sut_type(ElementId(id_string="STOOGES"), None)
        result = sut.groups
        mock_get_group_method.assert_called_once_with(ElementId(id_string="STOOGES"))
        assert len(result) == 3
        assert isinstance(result[0], Group)
        assert result[0].element_id == "LARRY"
        assert isinstance(result[1], Group)
        assert result[1].element_id == "MOE"
        assert isinstance(result[2], Group)
        assert result[2].element_id == "CURLY"
