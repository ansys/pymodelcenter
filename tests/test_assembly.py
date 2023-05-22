from typing import Dict, Optional
import unittest.mock

import ansys.engineeringworkflow.api as aew_api
import ansys.tools.variableinterop as atvi
import pytest

import ansys.modelcenter.workflow.api as mc_api
from ansys.modelcenter.workflow.grpc_modelcenter import Assembly, Component
from ansys.modelcenter.workflow.grpc_modelcenter.abstract_workflow_element import (
    AbstractWorkflowElement,
)
from ansys.modelcenter.workflow.grpc_modelcenter.base_datapin import BaseDatapin
from ansys.modelcenter.workflow.grpc_modelcenter.proto.custom_metadata_messages_pb2 import (
    MetadataGetValueRequest,
    MetadataSetValueRequest,
    MetadataSetValueResponse,
)
from ansys.modelcenter.workflow.grpc_modelcenter.proto.element_messages_pb2 import (
    ELEMTYPE_ASSEMBLY,
    AddAssemblyRequest,
    AddAssemblyResponse,
    AddAssemblyVariableRequest,
    AddAssemblyVariableResponse,
    AnalysisViewPosition,
    AssemblyIconResponse,
    AssemblyIconSetRequest,
    AssemblyIconSetResponse,
    AssemblyType,
    DeleteAssemblyVariableResponse,
    ElementId,
    ElementIdCollection,
    ElementIndexInParentResponse,
    ElementName,
    ElementType,
    RenameRequest,
    RenameResponse,
)
from ansys.modelcenter.workflow.grpc_modelcenter.proto.variable_value_messages_pb2 import (
    VariableType,
    VariableValue,
)
from ansys.modelcenter.workflow.grpc_modelcenter.proto.workflow_messages_pb2 import (
    DeleteAssemblyVariableRequest,
    ElementIdOrName,
    ElementInfo,
    ElementInfoCollection,
    NamedElementInWorkflow,
)
from ansys.modelcenter.workflow.grpc_modelcenter.unsupported_type_datapin import (
    UnsupportedTypeDatapin,
)
from tests.grpc_server_test_utils.client_creation_monkeypatch import monkeypatch_client_creation
import tests.test_abstract_workflow_element as awe_tests
import tests.test_datapin_container as base_tests


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

    def RegistryGetControlType(self, request: ElementId) -> AssemblyType:
        return AssemblyType(type=self._control_type_responses[request.id_string])

    def ElementGetParentElement(self, request: ElementId) -> ElementInfo:
        return ElementInfo(
            id=ElementId(id_string=self._parent_id_responses[request.id_string]),
            type=ELEMTYPE_ASSEMBLY,
        )

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

    def AssemblyGetAnalysisViewPosition(self, request: ElementId) -> AnalysisViewPosition:
        return AnalysisViewPosition()

    def AssemblyGetIcon(self, request: ElementId) -> AssemblyIconResponse:
        return AssemblyIconResponse()

    def AssemblySetIcon(self, request: AssemblyIconSetRequest) -> AssemblyIconSetResponse:
        return AssemblyIconSetResponse()

    def AssemblyDeleteVariable(self, request: ElementId) -> DeleteAssemblyVariableResponse:
        return DeleteAssemblyVariableResponse()

    def AssemblyGetAssembliesAndComponents(self, request: ElementId) -> ElementInfoCollection:
        return ElementInfoCollection()

    def ElementGetIndexInParent(self, request: ElementId) -> ElementIndexInParentResponse:
        return ElementIndexInParentResponse()

    def WorkflowGetElementByName(self, request: ElementName) -> ElementId:
        return ElementId()

    def AssemblyAddAssembly(self, request: AddAssemblyRequest) -> AddAssemblyResponse:
        return AddAssemblyResponse()


def test_element_id(monkeypatch, engine) -> None:
    awe_tests.do_test_element_id(monkeypatch, engine, Assembly, "SUT_TEST_ID")


def test_parent_element_id(monkeypatch, engine) -> None:
    awe_tests.do_test_parent_element_id(monkeypatch, engine, Assembly)


def test_name(monkeypatch, engine) -> None:
    awe_tests.do_test_name(monkeypatch, engine, Assembly)


def test_full_name(monkeypatch, engine) -> None:
    awe_tests.do_test_name(monkeypatch, engine, Assembly)


def test_parent_element(monkeypatch, engine) -> None:
    awe_tests.do_test_parent_element(
        monkeypatch, engine, Assembly, ElementType.ELEMTYPE_ASSEMBLY, Assembly
    )


def test_parent_element_root(monkeypatch, engine) -> None:
    mock_client = MockWorkflowClientForAssemblyTest()
    id_in_response = ""
    sut_element_id = ElementId(id_string="SUT_ELEMENT")
    mock_response = ElementInfo(
        id=ElementId(id_string=id_in_response), type=ElementType.ELEMTYPE_ASSEMBLY
    )
    with unittest.mock.patch.object(
        mock_client, "ElementGetParentElement", return_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = Assembly(sut_element_id, engine=engine)

        result = sut.get_parent_element()

        assert result is None
        mock_grpc_method.assert_called_once_with(sut_element_id)


def test_get_property_names(monkeypatch, engine) -> None:
    awe_tests.do_test_get_property_names(monkeypatch, engine, Assembly)


def test_get_properties(monkeypatch, engine) -> None:
    awe_tests.do_test_get_properties(monkeypatch, engine, Assembly)


def test_can_get_control_type(monkeypatch, engine) -> None:
    mock_client = MockWorkflowClientForAssemblyTest()
    mock_client.control_type_responses["TEST_ID_SHOULD_MATCH"] = "Sequence"
    monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)

    sut = Assembly(ElementId(id_string="TEST_ID_SHOULD_MATCH"), engine=engine)

    result = sut.control_type

    assert result == "Sequence"


@pytest.mark.parametrize("returned_id", [None, ""])
def test_can_get_parent_no_parent(monkeypatch, engine, returned_id: Optional[str]) -> None:
    mock_client = MockWorkflowClientForAssemblyTest()
    test_id_string = "TEST_ID_SHOULD_MATCH"
    mock_client.parent_id_responses[test_id_string] = returned_id if returned_id is not None else ""
    monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)

    sut = Assembly(ElementId(id_string=test_id_string), engine=engine)

    result: Optional[Assembly] = sut.parent_assembly

    assert result is None


def test_can_get_parent_has_parent(monkeypatch, engine) -> None:
    mock_client = MockWorkflowClientForAssemblyTest()
    test_id_string = "TEST_ID_SHOULD_MATCH"
    parent_id_string = "PARENT_ID"
    mock_client.parent_id_responses[test_id_string] = parent_id_string
    monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)

    sut = Assembly(ElementId(id_string=test_id_string), engine=engine)

    result = sut.parent_assembly

    assert isinstance(result, Assembly)
    assert result.element_id == parent_id_string


def test_can_get_parent_grpc_reports_nonassembly(monkeypatch, engine) -> None:
    """
    Verify that an error is raised if a nonassembly is ever found by parent_assembly.

    This case should not happen in production;
    if it does, it indicates a serious internal error.
    """
    mock_client = MockWorkflowClientForAssemblyTest()
    id_in_response = "VAR_ID"
    sut_element_id = ElementId(id_string="SUT_ELEMENT")
    mock_response = ElementInfo(
        id=ElementId(id_string=id_in_response),
        type=ElementType.ELEMTYPE_VARIABLE,
        var_type=VariableType.VARTYPE_INTEGER,
    )
    with unittest.mock.patch.object(
        mock_client, "ElementGetParentElement", return_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = Assembly(sut_element_id, engine=engine)

        with pytest.raises(aew_api.EngineInternalError):
            assembly = sut.parent_assembly

        mock_grpc_method.assert_called_once_with(sut_element_id)


def test_get_child_elements_empty(monkeypatch, engine) -> None:
    mock_client = MockWorkflowClientForAssemblyTest()
    no_child_assemblies = ElementInfoCollection()
    with unittest.mock.patch.object(
        mock_client, "AssemblyGetAssembliesAndComponents", return_value=no_child_assemblies
    ) as mock_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = Assembly(ElementId(id_string="LEAF_ASSEMBLY"), engine=engine)
        result = sut.get_elements()
        assert len(result) == 0
        mock_method.assert_called_once_with(ElementId(id_string="LEAF_ASSEMBLY"))


@pytest.mark.parametrize(
    "type_in_response,expected_wrapper_type",
    [(ElementType.ELEMTYPE_ASSEMBLY, Assembly), (ElementType.ELEMTYPE_COMPONENT, Component)],
)
def test_get_child_elements_one_child(
    monkeypatch, engine, type_in_response: ElementType, expected_wrapper_type
) -> None:
    mock_client = MockWorkflowClientForAssemblyTest()
    child_id = "CHILD_ID_STRING"
    mock_client.name_responses[child_id] = "child"
    one_child_assembly = ElementInfo(id=ElementId(id_string=child_id), type=type_in_response)
    response = ElementInfoCollection(elements=[one_child_assembly])
    fake_name = ElementName(name="FAKE_NAME")
    with unittest.mock.patch.object(
        mock_client, "AssemblyGetAssembliesAndComponents", return_value=response
    ) as mock_get_assembly_method:
        with unittest.mock.patch.object(
            mock_client, "ElementGetFullName", return_value=fake_name
        ) as mock_get_name_method:
            monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
            sut = Assembly(ElementId(id_string="SINGLE_CHILD"), engine=engine)
            result = sut.get_elements()
            assert len(result) == 1
            assert isinstance(result["child"], expected_wrapper_type)
            mock_get_assembly_method.assert_called_once_with(ElementId(id_string="SINGLE_CHILD"))
            name = result["child"].full_name
            mock_get_name_method.assert_called_once_with(ElementId(id_string=child_id))


def test_get_child_assemblies_multiple_children(monkeypatch, engine) -> None:
    mock_client = MockWorkflowClientForAssemblyTest()
    larry_assembly_info = ElementInfo(
        id=ElementId(id_string="IDASSEMBLY_LARRY"), type=ElementType.ELEMTYPE_ASSEMBLY
    )
    mock_client.name_responses["IDASSEMBLY_LARRY"] = "larry"
    moe_comp_info = ElementInfo(
        id=ElementId(id_string="IDCOMP_MOE"), type=ElementType.ELEMTYPE_COMPONENT
    )
    mock_client.name_responses["IDCOMP_MOE"] = "moe"
    curly_assembly_info = ElementInfo(
        id=ElementId(id_string="IDASSEMBLY_CURLY"), type=ElementType.ELEMTYPE_ASSEMBLY
    )
    mock_client.name_responses["IDASSEMBLY_CURLY"] = "curly"
    response = ElementInfoCollection(
        elements=[larry_assembly_info, moe_comp_info, curly_assembly_info]
    )
    fake_name = ElementName(name="FAKE_NAME")
    with unittest.mock.patch.object(
        mock_client, "AssemblyGetAssembliesAndComponents", return_value=response
    ) as mock_get_assembly_method:
        with unittest.mock.patch.object(
            mock_client, "ElementGetFullName", return_value=fake_name
        ) as mock_get_name_method:
            monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
            sut = Assembly(ElementId(id_string="STOOGES"), engine=engine)
            result = sut.get_elements()
            assert len(result) == 3
            assert isinstance(result["larry"], Assembly)
            assert isinstance(result["moe"], Component)
            assert isinstance(result["curly"], Assembly)
            mock_get_assembly_method.assert_called_once_with(ElementId(id_string="STOOGES"))
            name = result["larry"].full_name
            mock_get_name_method.assert_called_once_with(ElementId(id_string="IDASSEMBLY_LARRY"))
            mock_get_name_method.reset_mock()
            name = result["moe"].full_name
            mock_get_name_method.assert_called_once_with(ElementId(id_string="IDCOMP_MOE"))
            mock_get_name_method.reset_mock()
            name = result["curly"].full_name
            mock_get_name_method.assert_called_once_with(ElementId(id_string="IDASSEMBLY_CURLY"))


def test_get_variables_empty(monkeypatch, engine) -> None:
    base_tests.do_test_get_datapins_empty(monkeypatch, engine, Assembly)


@pytest.mark.parametrize(
    "var_type,expected_wrapper_type",
    [
        (VariableType.VARTYPE_INTEGER, mc_api.IIntegerDatapin),
        (VariableType.VARTYPE_REAL, mc_api.IRealDatapin),
        (VariableType.VARTYPE_BOOLEAN, mc_api.IBooleanDatapin),
        (VariableType.VARTYPE_STRING, mc_api.IStringDatapin),
        (VariableType.VARTYPE_FILE, mc_api.IFileDatapin),
        (VariableType.VARTYPE_INTEGER_ARRAY, mc_api.IIntegerArrayDatapin),
        (VariableType.VARTYPE_REAL_ARRAY, mc_api.IRealArrayDatapin),
        (VariableType.VARTYPE_BOOLEAN_ARRAY, mc_api.IBooleanArrayDatapin),
        (VariableType.VARTYPE_STRING_ARRAY, mc_api.IStringArrayDatapin),
        (VariableType.VARTYPE_FILE_ARRAY, mc_api.IFileArrayDatapin),
        (VariableType.VARTYPE_UNKNOWN, UnsupportedTypeDatapin),
    ],
)
def test_get_variables_one_variable(monkeypatch, engine, var_type, expected_wrapper_type) -> None:
    base_tests.do_test_get_datapins_one_variable(
        monkeypatch, engine, Assembly, var_type, expected_wrapper_type
    )


def test_get_variables_multiple_variables(monkeypatch, engine) -> None:
    base_tests.do_test_get_datapins_multiple_variables(monkeypatch, engine, Assembly)


def test_get_groups_empty(monkeypatch, engine) -> None:
    base_tests.do_test_get_groups_empty(monkeypatch, engine, Assembly)


def test_get_groups_one_group(monkeypatch, engine) -> None:
    base_tests.do_test_get_groups_one_group(monkeypatch, engine, Assembly)


def test_get_groups_multiple_groups(monkeypatch, engine) -> None:
    base_tests.do_test_get_groups_multiple_groups(monkeypatch, engine, Assembly)


@pytest.mark.parametrize(
    "var_type,expected_var_type_in_request",
    [
        (atvi.VariableType.INTEGER, "int"),
        (atvi.VariableType.REAL, "real"),
        (atvi.VariableType.BOOLEAN, "bool"),
        (atvi.VariableType.STRING, "string"),
        (atvi.VariableType.FILE, "file"),
        (atvi.VariableType.INTEGER_ARRAY, "int[]"),
        (atvi.VariableType.REAL_ARRAY, "real[]"),
        (atvi.VariableType.BOOLEAN_ARRAY, "bool[]"),
        (atvi.VariableType.STRING_ARRAY, "string[]"),
        (atvi.VariableType.FILE_ARRAY, "file[]"),
    ],
)
def test_assembly_create_variable(
    monkeypatch, engine, var_type: atvi.VariableType, expected_var_type_in_request: str
) -> None:
    mock_client = MockWorkflowClientForAssemblyTest()
    mock_response = AddAssemblyVariableResponse(id=ElementId(id_string="CREATED_VAR"))
    with unittest.mock.patch.object(
        mock_client, "AssemblyAddVariable", return_value=mock_response
    ) as mock_add_var_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = Assembly(ElementId(id_string="ADD_VAR_TARGET"), engine=engine)
        result = sut.add_datapin("created_variable_name", var_type)
        mock_add_var_method.assert_called_once_with(
            AddAssemblyVariableRequest(
                name=ElementName(name="created_variable_name"),
                target_assembly=ElementId(id_string="ADD_VAR_TARGET"),
                variable_type=expected_var_type_in_request,
            )
        )
        assert result.element_id == "CREATED_VAR"
        assert isinstance(result, BaseDatapin)


def test_assembly_create_variable_unknown_type(monkeypatch, engine) -> None:
    mock_client = MockWorkflowClientForAssemblyTest()
    mock_response = AddAssemblyVariableResponse(id=ElementId(id_string="CREATED_VAR"))
    with unittest.mock.patch.object(
        mock_client, "AssemblyAddVariable", return_value=mock_response
    ) as mock_add_var_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = Assembly(ElementId(id_string="ADD_VAR_TARGET"), engine=engine)
        with pytest.raises(
            ValueError, match="Cannot determine a ModelCenter type for an unknown variable type."
        ):
            sut.add_datapin("created_variable_name", atvi.VariableType.UNKNOWN)
        mock_add_var_method.assert_not_called()


def test_assembly_rename(monkeypatch, engine) -> None:
    mock_client = MockWorkflowClientForAssemblyTest()
    mock_response = RenameResponse()
    with unittest.mock.patch.object(
        mock_client, "AssemblyRename", return_value=mock_response
    ) as mock_rename_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = Assembly(ElementId(id_string="ADD_VAR_TARGET"), engine=engine)
        sut.rename("this_is_the_new_assembly_name")
        mock_rename_method.assert_called_once_with(
            RenameRequest(
                target_assembly=ElementId(id_string="ADD_VAR_TARGET"),
                new_name=ElementName(name="this_is_the_new_assembly_name"),
            )
        )


def test_assembly_get_int_metadata_property(monkeypatch, engine) -> None:
    mock_client = MockWorkflowClientForAssemblyTest()
    mock_response = VariableValue(int_value=47)
    with unittest.mock.patch.object(
        mock_client, "PropertyOwnerGetPropertyValue", return_value=mock_response
    ) as mock_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = Assembly(ElementId(id_string="GET_METADATA"), engine=engine)
        result = sut.get_property("mock_property_name")
        mock_method.assert_called_once_with(
            MetadataGetValueRequest(
                id=ElementId(id_string="GET_METADATA"), property_name="mock_property_name"
            )
        )
        assert isinstance(result, aew_api.Property)
        assert result.property_name == "mock_property_name"
        assert result.parent_element_id == "GET_METADATA"
        assert result.property_value == atvi.IntegerValue(47)


def test_assembly_set_int_metadata_property(monkeypatch, engine) -> None:
    mock_client = MockWorkflowClientForAssemblyTest()
    mock_response = MetadataSetValueResponse()
    with unittest.mock.patch.object(
        mock_client, "PropertyOwnerSetPropertyValue", return_value=mock_response
    ) as mock_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = Assembly(ElementId(id_string="SET_METADATA"), engine=engine)
        sut.set_property("mock_property_name", atvi.IntegerValue(47))
        mock_method.assert_called_once_with(
            MetadataSetValueRequest(
                id=ElementId(id_string="SET_METADATA"),
                property_name="mock_property_name",
                value=VariableValue(int_value=47),
            )
        )


def test_get_index_in_parent(monkeypatch, engine) -> None:
    mock_client = MockWorkflowClientForAssemblyTest()
    mock_response = ElementIndexInParentResponse(index=3)
    with unittest.mock.patch.object(
        mock_client, "ElementGetIndexInParent", return_value=mock_response
    ) as mock_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = Assembly(ElementId(id_string="INDEX_IN_PARENT"), engine=engine)
        result = sut.index_in_parent
        mock_method.assert_called_once_with(ElementId(id_string="INDEX_IN_PARENT"))
        assert result == 3


def test_delete_variable(monkeypatch, engine) -> None:
    mock_client = MockWorkflowClientForAssemblyTest()
    target_assembly_name = "Model.DeleteVarAssembly"
    target_assembly_id = "TARGET_ASSEMBLY"
    mock_client.name_responses[target_assembly_id] = target_assembly_name
    target_variable_name = NamedElementInWorkflow(
        element_full_name=ElementName(name="Model.DeleteVarAssembly.VarToDelete")
    )
    with unittest.mock.patch.object(
        mock_client, "AssemblyDeleteVariable", return_value=DeleteAssemblyVariableResponse()
    ) as mock_delete:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = Assembly(ElementId(id_string=target_assembly_id), engine=engine)
        sut.delete_datapin("VarToDelete")
        mock_delete.assert_called_once_with(
            DeleteAssemblyVariableRequest(target=ElementIdOrName(target_name=target_variable_name))
        )


@pytest.mark.parametrize(
    "assembly_type_in_call,expected_type_in_request",
    [
        (None, "Assembly"),
        *((assembly_type, assembly_type.value) for assembly_type in mc_api.AssemblyType),
    ],
)
def test_add_assembly(monkeypatch, engine, assembly_type_in_call, expected_type_in_request) -> None:
    mock_client = MockWorkflowClientForAssemblyTest()
    mock_response = AddAssemblyResponse(id=ElementId(id_string="BRAND_NEW_ASSEMBLY"))
    with unittest.mock.patch.object(
        mock_client, "AssemblyAddAssembly", return_value=mock_response
    ) as mock_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = Assembly(ElementId(id_string="TARGET_ASSEMBLY"), engine=engine)
        result = sut.add_assembly("new_assembly_name", (867, 5309), assembly_type_in_call)
        mock_method.assert_called_once_with(
            AddAssemblyRequest(
                name=ElementName(name="new_assembly_name"),
                parent=ElementId(id_string="TARGET_ASSEMBLY"),
                assembly_type=expected_type_in_request,
                av_pos=AnalysisViewPosition(x_pos=867, y_pos=5309),
            )
        )
        assert isinstance(result, Assembly)
        assert result.element_id == "BRAND_NEW_ASSEMBLY"


def test_add_assembly_no_position(monkeypatch, engine) -> None:
    mock_client = MockWorkflowClientForAssemblyTest()
    mock_response = AddAssemblyResponse(id=ElementId(id_string="BRAND_NEW_ASSEMBLY"))
    with unittest.mock.patch.object(
        mock_client, "AssemblyAddAssembly", return_value=mock_response
    ) as mock_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = Assembly(ElementId(id_string="TARGET_ASSEMBLY"), engine=engine)
        result = sut.add_assembly("new_assembly_name")
        mock_method.assert_called_once_with(
            AddAssemblyRequest(
                name=ElementName(name="new_assembly_name"),
                parent=ElementId(id_string="TARGET_ASSEMBLY"),
                assembly_type="Assembly",
            )
        )
        assert isinstance(result, Assembly)
        assert result.element_id == "BRAND_NEW_ASSEMBLY"


def test_get_analysis_view_position(monkeypatch, engine):
    mock_client = MockWorkflowClientForAssemblyTest()
    mock_response = AnalysisViewPosition(x_pos=47, y_pos=9001)
    sut_id = ElementId(id_string="SUT_TEST_ID")
    with unittest.mock.patch.object(
        mock_client, "AssemblyGetAnalysisViewPosition", return_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = Assembly(sut_id, engine=engine)

        result = sut.get_analysis_view_position()

        mock_grpc_method.assert_called_once_with(sut_id)
        assert result == (47, 9001)
