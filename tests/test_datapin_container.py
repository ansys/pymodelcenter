from typing import Dict
import unittest.mock

from ansys.api.modelcenter.v0.element_messages_pb2 import (
    ElementId,
    ElementIdCollection,
    ElementName,
)
from ansys.api.modelcenter.v0.variable_value_messages_pb2 import (
    VariableInfo,
    VariableInfoCollection,
    VariableType,
)

import ansys.modelcenter.workflow.api as mc_api
from ansys.modelcenter.workflow.grpc_modelcenter.abstract_workflow_element import (
    AbstractWorkflowElement,
)
from ansys.modelcenter.workflow.grpc_modelcenter.group import Group

from .grpc_server_test_utils.client_creation_monkeypatch import monkeypatch_client_creation


class MockWorkflowClientForAbstractDatapinContainerTest:
    def __init__(self) -> None:
        self._name_responses: Dict[str, str] = {}
        self._full_name_responses: Dict[str, str] = {}

    @property
    def name_responses(self) -> Dict[str, str]:
        return self._name_responses

    @property
    def full_name_responses(self) -> Dict[str, str]:
        return self._full_name_responses

    def ElementGetName(self, request: ElementId) -> ElementName:
        return ElementName(name=self._name_responses[request.id_string])

    def ElementGetFullName(self, request: ElementId) -> ElementName:
        return ElementName(name=self._full_name_responses[request.id_string])

    def RegistryGetVariables(self, request: ElementId) -> ElementIdCollection:
        return ElementIdCollection()

    def RegistryGetGroups(self, request: ElementId) -> ElementIdCollection:
        return ElementIdCollection()


def do_test_get_datapins_empty(monkeypatch, engine, sut_type) -> None:
    mock_client = MockWorkflowClientForAbstractDatapinContainerTest()
    no_variables = VariableInfoCollection()
    with unittest.mock.patch.object(
        mock_client, "RegistryGetVariables", return_value=no_variables
    ) as mock_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = sut_type(ElementId(id_string="NO_VARIABLES"), engine=engine)
        result = sut.get_datapins()
        assert len(result) == 0
        mock_method.assert_called_once_with(ElementId(id_string="NO_VARIABLES"))


def do_test_get_datapins_one_variable(
    monkeypatch, engine, sut_type, var_type, expected_wrapper_type
) -> None:
    mock_client = MockWorkflowClientForAbstractDatapinContainerTest()
    mock_client.name_responses["VAR_ID_STRING"] = "child_var"
    variable_id = ElementId(id_string="VAR_ID_STRING")
    variables = VariableInfoCollection(
        variables=[VariableInfo(id=variable_id, value_type=var_type)]
    )
    with unittest.mock.patch.object(
        mock_client, "RegistryGetVariables", return_value=variables
    ) as mock_get_variable_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = sut_type(ElementId(id_string="SINGLE_CHILD"), engine=engine)
        result = sut.get_datapins()
        mock_get_variable_method.assert_called_once_with(ElementId(id_string="SINGLE_CHILD"))
        assert len(result) == 1
        assert isinstance(result["child_var"], expected_wrapper_type)
        assert result["child_var"].element_id == variable_id.id_string


def do_test_get_datapins_multiple_variables(monkeypatch, engine, sut_type) -> None:
    mock_client = MockWorkflowClientForAbstractDatapinContainerTest()
    mock_client.name_responses["IDVAR_LARRY"] = "larry"
    mock_client.name_responses["IDVAR_MOE"] = "moe"
    mock_client.name_responses["IDVAR_CURLY"] = "curly"
    one_child_assembly = VariableInfoCollection(
        variables=[
            VariableInfo(
                id=ElementId(id_string="IDVAR_LARRY"),
                value_type=VariableType.VARIABLE_TYPE_INTEGER,
                short_name="larry",
            ),
            VariableInfo(
                id=ElementId(id_string="IDVAR_MOE"),
                value_type=VariableType.VARIABLE_TYPE_STRING,
                short_name="moe",
            ),
            VariableInfo(
                id=ElementId(id_string="IDVAR_CURLY"),
                value_type=VariableType.VARIABLE_TYPE_REAL,
                short_name="curly",
            ),
        ]
    )
    with unittest.mock.patch.object(
        mock_client, "RegistryGetVariables", return_value=one_child_assembly
    ) as mock_get_variable_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = sut_type(ElementId(id_string="STOOGES"), engine=engine)
        result = sut.get_datapins()
        mock_get_variable_method.assert_called_once_with(ElementId(id_string="STOOGES"))
        assert len(result) == 3
        assert isinstance(result["larry"], mc_api.IIntegerDatapin)
        assert result["larry"].element_id == "IDVAR_LARRY"
        assert isinstance(result["moe"], mc_api.IStringDatapin)
        assert result["moe"].element_id == "IDVAR_MOE"
        assert isinstance(result["curly"], mc_api.IRealDatapin)
        assert result["curly"].element_id == "IDVAR_CURLY"


def do_test_get_groups_empty(monkeypatch, engine, sut_type) -> None:
    mock_client = MockWorkflowClientForAbstractDatapinContainerTest()
    no_variables = ElementIdCollection()
    with unittest.mock.patch.object(
        mock_client, "RegistryGetGroups", return_value=no_variables
    ) as mock_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = sut_type(ElementId(id_string="NO_GROUPS"), engine=engine)
        result = sut.get_groups()
        assert len(result) == 0
        mock_method.assert_called_once_with(ElementId(id_string="NO_GROUPS"))


def do_test_get_groups_one_group(monkeypatch, engine, sut_type) -> None:
    mock_client = MockWorkflowClientForAbstractDatapinContainerTest()
    group_id = "GRP_ID_STRING"
    mock_client.name_responses[group_id] = "child_group"
    variables = ElementIdCollection(ids=[ElementId(id_string=group_id)])
    with unittest.mock.patch.object(
        mock_client, "RegistryGetGroups", return_value=variables
    ) as mock_get_group_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = sut_type(ElementId(id_string="SINGLE_CHILD"), engine=engine)
        result = sut.get_groups()
        mock_get_group_method.assert_called_once_with(ElementId(id_string="SINGLE_CHILD"))
        assert len(result) == 1
        assert isinstance(result["child_group"], Group)
        assert result["child_group"].element_id == group_id


def do_test_get_groups_multiple_groups(monkeypatch, engine, sut_type) -> None:
    mock_client = MockWorkflowClientForAbstractDatapinContainerTest()
    mock_client.name_responses["IDGROUP_LARRY"] = "larry"
    mock_client.name_responses["IDGROUP_MOE"] = "moe"
    mock_client.name_responses["IDGROUP_CURLY"] = "curly"
    one_child_assembly = ElementIdCollection(
        ids=[
            ElementId(id_string="IDGROUP_LARRY"),
            ElementId(id_string="IDGROUP_MOE"),
            ElementId(id_string="IDGROUP_CURLY"),
        ]
    )
    with unittest.mock.patch.object(
        mock_client, "RegistryGetGroups", return_value=one_child_assembly
    ) as mock_get_group_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = sut_type(ElementId(id_string="STOOGES"), engine=engine)
        result = sut.get_groups()
        mock_get_group_method.assert_called_once_with(ElementId(id_string="STOOGES"))
        assert len(result) == 3
        assert isinstance(result["larry"], Group)
        assert result["larry"].element_id == "IDGROUP_LARRY"
        assert isinstance(result["moe"], Group)
        assert result["moe"].element_id == "IDGROUP_MOE"
        assert isinstance(result["curly"], Group)
        assert result["curly"].element_id == "IDGROUP_CURLY"
