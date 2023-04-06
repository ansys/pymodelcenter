from typing import Dict, Optional, Union
import unittest.mock

import ansys.common.variableinterop as acvi
import ansys.engineeringworkflow.api.datatypes
import pytest

import ansys.modelcenter.workflow.api as mc_api
from ansys.modelcenter.workflow.grpc_modelcenter.abstract_workflow_element import (
    AbstractWorkflowElement,
)
from ansys.modelcenter.workflow.grpc_modelcenter.assembly import Assembly
from ansys.modelcenter.workflow.grpc_modelcenter.group import Group
from ansys.modelcenter.workflow.grpc_modelcenter.proto.custom_metadata_messages_pb2 import (
    MetadataGetValueRequest,
    MetadataSetValueRequest,
    MetadataSetValueResponse,
)
from ansys.modelcenter.workflow.grpc_modelcenter.proto.element_messages_pb2 import (
    AddAssemblyRequest,
    AddAssemblyResponse,
    AddAssemblyVariableRequest,
    AddAssemblyVariableResponse,
    AnalysisViewPosition,
    AssemblyIconResponse,
    AssemblyIconSetRequest,
    AssemblyIconSetResponse,
    AssemblyType,
    DeleteAssemblyVariableRequest,
    DeleteAssemblyVariableResponse,
    ElementId,
    ElementIdCollection,
    ElementIndexInParentResponse,
    ElementName,
    RenameRequest,
    RenameResponse,
)
from ansys.modelcenter.workflow.grpc_modelcenter.proto.variable_value_messages_pb2 import (
    VariableType,
    VariableValue,
)
from ansys.modelcenter.workflow.grpc_modelcenter.proto.workflow_messages_pb2 import (
    WorkflowGetElementByNameResponse,
)
from ansys.modelcenter.workflow.grpc_modelcenter.unsupported_var import UnsupportedTypeVariable
from ansys.modelcenter.workflow.grpc_modelcenter.variable import BaseVariable
from tests.grpc_server_test_utils.client_creation_monkeypatch import monkeypatch_client_creation
import tests.test_variable_container as base_tests


class MockWorkflowClientForAssemblyTest:
    def __init__(self) -> None:
        self._name_responses: Dict[str, str] = {}
        self._parent_id_responses: Dict[str, str] = {}
        self._control_type_responses: Dict[str, str] = {}

    @property
    def name_responses(self) -> Dict[str, str]:
        return self._name_responses

    @property
    def parent_id_responses(self) -> Dict[str, str]:
        return self._parent_id_responses

    @property
    def control_type_responses(self) -> Dict[str, str]:
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

    def RegistryGetGroups(self, request: ElementId) -> ElementIdCollection:
        return ElementIdCollection()

    def AssemblyAddVariable(
        self, request: AddAssemblyVariableRequest
    ) -> AddAssemblyVariableResponse:
        return AddAssemblyVariableResponse()

    def AssemblyRename(self, request: RenameRequest) -> RenameResponse:
        return RenameResponse()

    def PropertyOwnerGetPropertyValue(self, request: MetadataGetValueRequest) -> VariableValue:
        return VariableValue()

    def PropertyOwnerSetPropertyValue(
        self, request: MetadataSetValueRequest
    ) -> MetadataSetValueResponse:
        return MetadataSetValueResponse()

    def AssemblyGetIcon(self, request: ElementId) -> AssemblyIconResponse:
        return AssemblyIconResponse()

    def AssemblySetIcon(self, request: AssemblyIconSetRequest) -> AssemblyIconSetResponse:
        return AssemblyIconSetRequest()

    def AssemblyDeleteVariable(self, request: ElementId) -> DeleteAssemblyVariableResponse:
        return DeleteAssemblyVariableResponse()

    def AssemblyGetComponents(self, request: ElementId) -> ElementIdCollection:
        return ElementIdCollection()

    def ElementGetIndexInParent(self, request: ElementId) -> ElementIndexInParentResponse:
        return ElementIndexInParentResponse()

    def WorkflowGetElementByName(self, request: ElementName) -> ElementId:
        return ElementId()

    def AssemblyAddAssembly(self, request: AddAssemblyRequest) -> AddAssemblyResponse:
        return AddAssemblyResponse()


def test_can_get_name(monkeypatch) -> None:
    mock_client = MockWorkflowClientForAssemblyTest()
    mock_client.name_responses["TEST_ID_SHOULD_MATCH"] = "expected_name"
    monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
    sut = Assembly(ElementId(id_string="TEST_ID_SHOULD_MATCH"), None)

    result = sut.name

    assert result == "expected_name"


def test_can_get_control_type(monkeypatch) -> None:
    mock_client = MockWorkflowClientForAssemblyTest()
    mock_client.control_type_responses["TEST_ID_SHOULD_MATCH"] = "Sequence"
    monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)

    sut = Assembly(ElementId(id_string="TEST_ID_SHOULD_MATCH"), None)

    result = sut.control_type

    assert result == "Sequence"


@pytest.mark.parametrize("returned_id", [None, ""])
def test_can_get_parent_no_parent(monkeypatch, returned_id: Optional[str]) -> None:
    mock_client = MockWorkflowClientForAssemblyTest()
    test_id_string = "TEST_ID_SHOULD_MATCH"
    mock_client.parent_id_responses[test_id_string] = returned_id if returned_id is not None else ""
    monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)

    sut = Assembly(ElementId(id_string=test_id_string), None)

    result: Assembly = sut.parent_assembly

    assert result is None


def test_can_get_parent_has_parent(monkeypatch) -> None:
    mock_client = MockWorkflowClientForAssemblyTest()
    test_id_string = "TEST_ID_SHOULD_MATCH"
    parent_id_string = "PARENT_ID"
    mock_client.parent_id_responses[test_id_string] = parent_id_string
    monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)

    sut = Assembly(ElementId(id_string=test_id_string), None)

    result = sut.parent_assembly

    assert isinstance(result, Assembly)
    assert result.element_id == parent_id_string


def test_get_child_assemblies_empty(monkeypatch) -> None:
    mock_client = MockWorkflowClientForAssemblyTest()
    no_child_assemblies = ElementIdCollection()
    with unittest.mock.patch.object(
        mock_client, "RegistryGetAssemblies", return_value=no_child_assemblies
    ) as mock_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = Assembly(ElementId(id_string="LEAF_ASSEMBLY"), None)
        result = sut.assemblies
        assert len(result) == 0
        mock_method.assert_called_once_with(ElementId(id_string="LEAF_ASSEMBLY"))


def test_get_child_assemblies_one_child(monkeypatch) -> None:
    mock_client = MockWorkflowClientForAssemblyTest()
    child_id = "CHILD_ID_STRING"
    one_child_assembly = ElementIdCollection(ids=[ElementId(id_string=child_id)])
    fake_name = ElementName(name="FAKE_NAME")
    with unittest.mock.patch.object(
        mock_client, "RegistryGetAssemblies", return_value=one_child_assembly
    ) as mock_get_assembly_method:
        with unittest.mock.patch.object(
            mock_client, "ElementGetFullName", return_value=fake_name
        ) as mock_get_name_method:
            monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
            sut = Assembly(ElementId(id_string="SINGLE_CHILD"), None)
            result = sut.assemblies
            assert len(result) == 1
            assert isinstance(result[0], Assembly)
            mock_get_assembly_method.assert_called_once_with(ElementId(id_string="SINGLE_CHILD"))
            result[0].name
            mock_get_name_method.assert_called_once_with(ElementId(id_string=child_id))


def test_get_child_assemblies_multiple_children(monkeypatch) -> None:
    mock_client = MockWorkflowClientForAssemblyTest()
    one_child_assembly = ElementIdCollection(
        ids=[ElementId(id_string="LARRY"), ElementId(id_string="MOE"), ElementId(id_string="CURLY")]
    )
    fake_name = ElementName(name="FAKE_NAME")
    with unittest.mock.patch.object(
        mock_client, "RegistryGetAssemblies", return_value=one_child_assembly
    ) as mock_get_assembly_method:
        with unittest.mock.patch.object(
            mock_client, "ElementGetFullName", return_value=fake_name
        ) as mock_get_name_method:
            monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
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


def test_get_variables_empty(monkeypatch) -> None:
    base_tests.do_test_get_variables_empty(monkeypatch, Group)


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
def test_get_variables_one_variable(monkeypatch, var_type, expected_wrapper_type) -> None:
    base_tests.do_test_get_variables_one_variable(
        monkeypatch, Group, var_type, expected_wrapper_type
    )


def test_get_variables_multiple_variables(monkeypatch) -> None:
    base_tests.do_test_get_variables_multiple_variables(monkeypatch, Group)


def test_get_groups_empty(monkeypatch) -> None:
    base_tests.do_test_get_groups_empty(monkeypatch, Group)


def test_get_groups_one_group(monkeypatch) -> None:
    base_tests.do_test_get_groups_one_group(monkeypatch, Group)


def test_get_groups_multiple_groups(monkeypatch) -> None:
    base_tests.do_test_get_groups_multiple_groups(monkeypatch, Group)


@pytest.mark.parametrize(
    "var_type,expected_var_type_in_request",
    [
        ("int", "int"),
        ("real", "real"),
        (acvi.VariableType.INTEGER, "int"),
        (acvi.VariableType.REAL, "real"),
        (acvi.VariableType.BOOLEAN, "bool"),
        (acvi.VariableType.STRING, "string"),
        (acvi.VariableType.FILE, "file"),
        (acvi.VariableType.INTEGER_ARRAY, "int[]"),
        (acvi.VariableType.REAL_ARRAY, "real[]"),
        (acvi.VariableType.BOOLEAN_ARRAY, "bool[]"),
        (acvi.VariableType.STRING_ARRAY, "string[]"),
        (acvi.VariableType.FILE_ARRAY, "file[]"),
    ],
)
def test_assembly_create_variable(
    monkeypatch, var_type: Union[str, acvi.VariableType], expected_var_type_in_request: str
) -> None:
    mock_client = MockWorkflowClientForAssemblyTest()
    mock_response = AddAssemblyVariableResponse(id=ElementId(id_string="CREATED_VAR"))
    with unittest.mock.patch.object(
        mock_client, "AssemblyAddVariable", return_value=mock_response
    ) as mock_add_var_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = Assembly(ElementId(id_string="ADD_VAR_TARGET"), None)
        result = sut.add_variable("created_variable_name", var_type)
        mock_add_var_method.assert_called_once_with(
            AddAssemblyVariableRequest(
                name=ElementName(name="created_variable_name"),
                target_assembly=ElementId(id_string="ADD_VAR_TARGET"),
                variable_type=expected_var_type_in_request,
            )
        )
        assert result.element_id == "CREATED_VAR"
        assert isinstance(result, BaseVariable)


def test_assembly_create_variable_unknown_type(monkeypatch) -> None:
    mock_client = MockWorkflowClientForAssemblyTest()
    mock_response = AddAssemblyVariableResponse(id=ElementId(id_string="CREATED_VAR"))
    with unittest.mock.patch.object(
        mock_client, "AssemblyAddVariable", return_value=mock_response
    ) as mock_add_var_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = Assembly(ElementId(id_string="ADD_VAR_TARGET"), None)
        with pytest.raises(
            ValueError, match="Cannot determine a ModelCenter type for an unknown variable type."
        ):
            sut.add_variable("created_variable_name", acvi.VariableType.UNKNOWN)
        mock_add_var_method.assert_not_called()


def test_assembly_rename(monkeypatch) -> None:
    mock_client = MockWorkflowClientForAssemblyTest()
    mock_response = RenameResponse()
    with unittest.mock.patch.object(
        mock_client, "AssemblyRename", return_value=mock_response
    ) as mock_rename_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = Assembly(ElementId(id_string="ADD_VAR_TARGET"), None)
        sut.rename("this_is_the_new_assembly_name")
        mock_rename_method.assert_called_once_with(
            RenameRequest(
                target_assembly=ElementId(id_string="ADD_VAR_TARGET"),
                new_name=ElementName(name="this_is_the_new_assembly_name"),
            )
        )


def test_assembly_get_int_metadata_property(monkeypatch) -> None:
    mock_client = MockWorkflowClientForAssemblyTest()
    mock_response = VariableValue(int_value=47)
    with unittest.mock.patch.object(
        mock_client, "PropertyOwnerGetPropertyValue", return_value=mock_response
    ) as mock_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = Assembly(ElementId(id_string="GET_METADATA"), None)
        result = sut.get_property("mock_property_name")
        mock_method.assert_called_once_with(
            MetadataGetValueRequest(
                id=ElementId(id_string="GET_METADATA"), property_name="mock_property_name"
            )
        )
        assert isinstance(result, ansys.engineeringworkflow.api.datatypes.Property)
        assert result.property_name == "mock_property_name"
        assert result.parent_element_id == "GET_METADATA"
        assert result.property_value == acvi.IntegerValue(47)


def test_assembly_set_int_metadata_property(monkeypatch) -> None:
    mock_client = MockWorkflowClientForAssemblyTest()
    mock_response = MetadataSetValueResponse()
    with unittest.mock.patch.object(
        mock_client, "PropertyOwnerSetPropertyValue", return_value=mock_response
    ) as mock_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = Assembly(ElementId(id_string="SET_METADATA"), None)
        sut.set_property("mock_property_name", acvi.IntegerValue(47))
        mock_method.assert_called_once_with(
            MetadataSetValueRequest(
                id=ElementId(id_string="SET_METADATA"),
                property_name="mock_property_name",
                value=VariableValue(int_value=47),
            )
        )


def test_get_index_in_parent(monkeypatch) -> None:
    mock_client = MockWorkflowClientForAssemblyTest()
    mock_response = ElementIndexInParentResponse(index=3)
    with unittest.mock.patch.object(
        mock_client, "ElementGetIndexInParent", return_value=mock_response
    ) as mock_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = Assembly(ElementId(id_string="INDEX_IN_PARENT"), None)
        result = sut.index_in_parent
        mock_method.assert_called_once_with(ElementId(id_string="INDEX_IN_PARENT"))
        assert result == 3


def test_delete_variable(monkeypatch) -> None:
    mock_client = MockWorkflowClientForAssemblyTest()
    target_assembly_name = "Model.DeleteVarAssembly"
    target_assembly_id = "TARGET_ASSEMBLY"
    mock_client.name_responses[target_assembly_id] = target_assembly_name
    target_variable_name = "Model.DeleteVarAssembly.VarToDelete"
    target_variable_id = "TARGET_VARIABLE"
    target_variable_id_response = WorkflowGetElementByNameResponse(
        id=ElementId(id_string=target_variable_id)
    )
    with unittest.mock.patch.object(
        mock_client, "WorkflowGetElementByName", return_value=target_variable_id_response
    ) as mock_get_by_name:
        with unittest.mock.patch.object(
            mock_client, "AssemblyDeleteVariable", return_value=DeleteAssemblyVariableResponse()
        ) as mock_delete:
            monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
            sut = Assembly(ElementId(id_string=target_assembly_id), None)
            sut.delete_variable("VarToDelete")
            mock_get_by_name.assert_called_once_with(ElementName(name=target_variable_name))
            mock_delete.assert_called_once_with(
                DeleteAssemblyVariableRequest(target=ElementId(id_string=target_variable_id))
            )


def test_add_assembly(monkeypatch) -> None:
    mock_client = MockWorkflowClientForAssemblyTest()
    mock_response = AddAssemblyResponse(id=ElementId(id_string="BRAND_NEW_ASSEMBLY"))
    with unittest.mock.patch.object(
        mock_client, "AssemblyAddAssembly", return_value=mock_response
    ) as mock_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = Assembly(ElementId(id_string="TARGET_ASSEMBLY"), None)
        result = sut.add_assembly("new_assembly_name", 867, 5309, "Assembly")
        mock_method.assert_called_once_with(
            AddAssemblyRequest(
                name=ElementName(name="new_assembly_name"),
                parent=ElementId(id_string="TARGET_ASSEMBLY"),
                assembly_type="Assembly",
                av_pos=AnalysisViewPosition(x_pos=867, y_pos=5309),
            )
        )
        assert isinstance(result, Assembly)
        assert result.element_id == "BRAND_NEW_ASSEMBLY"


@pytest.mark.parametrize(
    "ids_in_response,expected_ids",
    [
        ([], []),
        ([ElementId(id_string="SINGLE_COMP")], ["SINGLE_COMP"]),
        (
            [
                ElementId(id_string="FIRST_COMP"),
                ElementId(id_string="SECOND_COMP"),
                ElementId(id_string="THIRD_COMP"),
            ],
            ["FIRST_COMP", "SECOND_COMP", "THIRD_COMP"],
        ),
    ],
)
def test_get_components(monkeypatch, ids_in_response, expected_ids) -> None:
    mock_client = MockWorkflowClientForAssemblyTest()
    mock_response = ElementIdCollection(ids=ids_in_response)
    with unittest.mock.patch.object(
        mock_client, "AssemblyGetComponents", return_value=mock_response
    ) as mock_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = Assembly(ElementId(id_string="TARGET_ASSEMBLY"), None)

        result = sut.get_components()

        mock_method.assert_called_once_with(ElementId(id_string="TARGET_ASSEMBLY"))
        item: mc_api.IComponent
        assert all([isinstance(item, mc_api.IComponent) for item in result])
        assert [item.element_id for item in result] == expected_ids
