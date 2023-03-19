from typing import Dict, Optional
import unittest.mock

import pytest

from ansys.modelcenter.workflow.grpc_modelcenter.assembly import Assembly
from ansys.modelcenter.workflow.grpc_modelcenter.proto.element_messages_pb2 import (
    AssemblyType,
    ElementId,
    ElementIdCollection,
    ElementName,
)
from ansys.modelcenter.workflow.grpc_modelcenter.variable import Variable

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

    def RegistryGetAssemblies(self, request: ElementId) -> ElementIdCollection:
        return ElementIdCollection()

    def RegistryGetVariables(self, request: ElementId) -> ElementIdCollection:
        return ElementIdCollection()


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


def test_get_child_assemblies_empty(monkeypatch):
    mock_client = MockWorkflowClientForAssemblyTest()
    no_child_assemblies = ElementIdCollection()
    with unittest.mock.patch.object(
        mock_client, "RegistryGetAssemblies", return_value=no_child_assemblies
    ) as mock_method:
        monkeypatch_client_creation(monkeypatch, Assembly, mock_client)
        sut = Assembly(ElementId(id_string="LEAF_ASSEMBLY"), None)
        result = sut.assemblies
        assert len(result) == 0
        mock_method.assert_called_once_with(ElementId(id_string="LEAF_ASSEMBLY"))


def test_get_child_assemblies_one_child(monkeypatch):
    mock_client = MockWorkflowClientForAssemblyTest()
    child_id = "CHILD_ID_STRING"
    one_child_assembly = ElementIdCollection(ids=[ElementId(id_string=child_id)])
    fake_name = ElementName(name="FAKE_NAME")
    with unittest.mock.patch.object(
        mock_client, "RegistryGetAssemblies", return_value=one_child_assembly
    ) as mock_get_assembly_method:
        with unittest.mock.patch.object(
            mock_client, "ElementGetName", return_value=fake_name
        ) as mock_get_name_method:
            monkeypatch_client_creation(monkeypatch, Assembly, mock_client)
            sut = Assembly(ElementId(id_string="SINGLE_CHILD"), None)
            result = sut.assemblies
            assert len(result) == 1
            assert isinstance(result[0], Assembly)
            mock_get_assembly_method.assert_called_once_with(ElementId(id_string="SINGLE_CHILD"))
            result[0].name
            mock_get_name_method.assert_called_once_with(ElementId(id_string=child_id))


def test_get_child_assemblies_multiple_children(monkeypatch):
    mock_client = MockWorkflowClientForAssemblyTest()
    one_child_assembly = ElementIdCollection(
        ids=[ElementId(id_string="LARRY"), ElementId(id_string="MOE"), ElementId(id_string="CURLY")]
    )
    fake_name = ElementName(name="FAKE_NAME")
    with unittest.mock.patch.object(
        mock_client, "RegistryGetAssemblies", return_value=one_child_assembly
    ) as mock_get_assembly_method:
        with unittest.mock.patch.object(
            mock_client, "ElementGetName", return_value=fake_name
        ) as mock_get_name_method:
            monkeypatch_client_creation(monkeypatch, Assembly, mock_client)
            sut = Assembly(ElementId(id_string="STOOGES"), None)
            result = sut.assemblies
            assert len(result) == 3
            assert isinstance(result[0], Assembly)
            assert isinstance(result[1], Assembly)
            assert isinstance(result[2], Assembly)
            mock_get_assembly_method.assert_called_once_with(ElementId(id_string="STOOGES"))
            result[0].name
            mock_get_name_method.assert_called_once_with(ElementId(id_string="LARRY"))
            mock_get_name_method.reset_mock()
            result[1].name
            mock_get_name_method.assert_called_once_with(ElementId(id_string="MOE"))
            mock_get_name_method.reset_mock()
            result[2].name
            mock_get_name_method.assert_called_once_with(ElementId(id_string="CURLY"))


def test_get_variables_empty(monkeypatch):
    mock_client = MockWorkflowClientForAssemblyTest()
    no_variables = ElementIdCollection()
    with unittest.mock.patch.object(
        mock_client, "RegistryGetVariables", return_value=no_variables
    ) as mock_method:
        monkeypatch_client_creation(monkeypatch, Assembly, mock_client)
        sut = Assembly(ElementId(id_string="NO_VARIABLES"), None)
        result = sut.get_variables()
        assert len(result) == 0
        mock_method.assert_called_once_with(ElementId(id_string="NO_VARIABLES"))


def test_get_variables_one_variable(monkeypatch):
    mock_client = MockWorkflowClientForAssemblyTest()
    variable_id = "VAR_ID_STRING"
    variables = ElementIdCollection(ids=[ElementId(id_string=variable_id)])
    with unittest.mock.patch.object(
        mock_client, "RegistryGetVariables", return_value=variables
    ) as mock_get_variable_method:
        monkeypatch_client_creation(monkeypatch, Assembly, mock_client)
        sut = Assembly(ElementId(id_string="SINGLE_CHILD"), None)
        result = sut.get_variables()
        mock_get_variable_method.assert_called_once_with(ElementId(id_string="SINGLE_CHILD"))
        assert len(result) == 1
        assert isinstance(result[0], Variable)
        assert result[0].element_id == variable_id


def test_get_variables_multiple_variables(monkeypatch):
    mock_client = MockWorkflowClientForAssemblyTest()
    one_child_assembly = ElementIdCollection(
        ids=[ElementId(id_string="LARRY"), ElementId(id_string="MOE"), ElementId(id_string="CURLY")]
    )
    with unittest.mock.patch.object(
        mock_client, "RegistryGetVariables", return_value=one_child_assembly
    ) as mock_get_variable_method:
        monkeypatch_client_creation(monkeypatch, Assembly, mock_client)
        sut = Assembly(ElementId(id_string="STOOGES"), None)
        result = sut.get_variables()
        mock_get_variable_method.assert_called_once_with(ElementId(id_string="STOOGES"))
        assert len(result) == 3
        assert isinstance(result[0], Variable)
        assert result[0].element_id == "LARRY"
        assert isinstance(result[1], Variable)
        assert result[1].element_id == "MOE"
        assert isinstance(result[2], Variable)
        assert result[2].element_id == "CURLY"
