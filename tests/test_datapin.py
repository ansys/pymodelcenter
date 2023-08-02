import unittest.mock

import ansys.modelcenter.workflow.api as mc_api
from ansys.modelcenter.workflow.grpc_modelcenter.abstract_workflow_element import (
    AbstractWorkflowElement,
)
from ansys.modelcenter.workflow.grpc_modelcenter.base_datapin import BaseDatapin
from ansys.modelcenter.workflow.grpc_modelcenter.proto.element_messages_pb2 import (
    ElementId,
    VariableIsInputResponse,
)
from ansys.modelcenter.workflow.grpc_modelcenter.proto.variable_value_messages_pb2 import (
    GetVariableDependenciesRequest,
    VariableInfo,
    VariableInfoCollection,
    VariableState,
    VariableType,
    VariableTypeResponse,
)
from ansys.modelcenter.workflow.grpc_modelcenter.proto.workflow_messages_pb2 import ElementIdOrName
import ansys.tools.variableinterop as atvi
import pytest

from .grpc_server_test_utils.client_creation_monkeypatch import monkeypatch_client_creation


class MockWorkflowClientForVariableTest:
    def __init__(self):
        pass

    def VariableGetType(self, request: ElementId) -> VariableTypeResponse:
        return VariableTypeResponse()

    def VariableGetState(self, request: ElementIdOrName) -> VariableState:
        return VariableState()

    def VariableGetIsInput(self, request: ElementId) -> VariableIsInputResponse:
        return VariableIsInputResponse()

    def VariableGetDependents(
        self, request: GetVariableDependenciesRequest
    ) -> VariableInfoCollection:
        return VariableInfoCollection()

    def VariableGetPrecedents(
        self, request: GetVariableDependenciesRequest
    ) -> VariableInfoCollection:
        return VariableInfoCollection()


def do_get_type_test(monkeypatch, engine, sut_type, type_in_response, expected_acvi_type) -> None:
    """Perform a test of interop_type on a particular base variable."""

    mock_client = MockWorkflowClientForVariableTest()
    sut_element_id = ElementId(id_string="VAR_UNDER_TEST_ID")
    mock_response = VariableTypeResponse(var_type=type_in_response)
    with unittest.mock.patch.object(
        mock_client, "VariableGetType", return_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = sut_type(element_id=sut_element_id, engine=engine)

        # Execute
        result: atvi.VariableType = sut.value_type

        # Verify
        mock_grpc_method.assert_called_once_with(sut_element_id)
        assert result == expected_acvi_type, "The type returned by interop_type should be correct."


def do_get_state_test(monkeypatch, engine, sut_type, mock_response, expected_acvi_state) -> None:
    """Perform a test of get_state on a particular base variable."""

    mock_client = MockWorkflowClientForVariableTest()
    sut_element_id = ElementId(id_string="VAR_UNDER_TEST_ID")
    with unittest.mock.patch.object(
        mock_client, "VariableGetState", return_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = sut_type(element_id=sut_element_id, engine=engine)

        result: atvi.VariableState = sut.get_value()

        mock_grpc_method.assert_called_once_with(ElementIdOrName(target_id=sut_element_id))
        assert result.value == expected_acvi_state.value
        assert result.is_valid == expected_acvi_state.is_valid


def do_get_state_test_with_hid(monkeypatch, engine, sut_type) -> None:
    """Perform a test of get_state on a particular base variable."""

    mock_client = MockWorkflowClientForVariableTest()
    sut_element_id = ElementId(id_string="VAR_UNDER_TEST_ID")
    with unittest.mock.patch.object(
        mock_client, "VariableGetState", return_value=VariableState()
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = sut_type(element_id=sut_element_id, engine=engine)

        with pytest.raises(ValueError, match="does not yet support HIDs."):
            sut.get_value("some_hid")

        mock_grpc_method.assert_not_called()


def do_test_is_input_component(monkeypatch, engine, sut_type, flag_in_response) -> None:
    mock_client = MockWorkflowClientForVariableTest()
    sut_element_id = ElementId(id_string="VAR_UNDER_TEST_ID")
    mock_response = VariableIsInputResponse(
        is_input_in_component=flag_in_response, is_input_in_workflow=False
    )
    with unittest.mock.patch.object(
        mock_client, "VariableGetIsInput", return_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = sut_type(element_id=sut_element_id, engine=engine)

        result: bool = sut.is_input_to_component

        mock_grpc_method.assert_called_once_with(sut_element_id)
        assert result == flag_in_response


def do_test_is_input_workflow(monkeypatch, engine, sut_type, flag_in_response) -> None:
    mock_client = MockWorkflowClientForVariableTest()
    sut_element_id = ElementId(id_string="VAR_UNDER_TEST_ID")
    mock_response = VariableIsInputResponse(
        is_input_in_component=False, is_input_in_workflow=flag_in_response
    )
    with unittest.mock.patch.object(
        mock_client, "VariableGetIsInput", return_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = sut_type(element_id=sut_element_id, engine=engine)

        result: bool = sut.is_input_to_workflow

        mock_grpc_method.assert_called_once_with(sut_element_id)
        assert result == flag_in_response


class MockVariable(BaseDatapin):
    """Mock variable for generic tests."""

    def set_metadata(self, new_metadata: atvi.CommonVariableMetadata) -> None:
        pass

    def get_metadata(self) -> atvi.CommonVariableMetadata:
        pass

    def set_value(self, value: VariableState) -> None:
        pass


def test_get_state_conversion_failure(monkeypatch, engine) -> None:
    """Perform a test of get_state on a particular base variable."""

    # Setup
    mock_client = MockWorkflowClientForVariableTest()
    sut_element_id = ElementId(id_string="VAR_UNDER_TEST_ID")
    with unittest.mock.patch.object(
        mock_client, "VariableGetState", return_value=VariableState(value=None, is_valid=True)
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = MockVariable(element_id=sut_element_id, engine=engine)

        with pytest.raises(Exception) as err:
            # SUT
            result: atvi.VariableState = sut.get_value(None)

        # Verification
        assert err.value.args[0] == "Unexpected failure converting gRPC value response"
        mock_grpc_method.assert_called_once_with(ElementIdOrName(target_id=sut_element_id))


@pytest.mark.parametrize(
    "only_fetch_direct_dependencies, follow_suspended",
    [(True, True), (True, False), (False, True), (False, False)],
)
def test_get_dependents(
    monkeypatch, engine, only_fetch_direct_dependencies: bool, follow_suspended: bool
) -> None:
    """Perform a test of get_dependents on a base datapin."""
    # Setup
    mock_client = MockWorkflowClientForVariableTest()
    sut_element_id = ElementId(id_string="VAR_UNDER_TEST_ID")
    return_variables = VariableInfoCollection(
        variables=[
            VariableInfo(
                id=ElementId(id_string="IDVAR_LARRY"),
                value_type=VariableType.VARTYPE_INTEGER,
                short_name="larry",
            ),
            VariableInfo(
                id=ElementId(id_string="IDVAR_MOE"),
                value_type=VariableType.VARTYPE_STRING,
                short_name="moe",
            ),
            VariableInfo(
                id=ElementId(id_string="IDVAR_CURLY"),
                value_type=VariableType.VARTYPE_REAL,
                short_name="curly",
            ),
        ]
    )
    with unittest.mock.patch.object(
        mock_client, "VariableGetDependents", return_value=return_variables
    ) as mock_get_variable_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = MockVariable(element_id=sut_element_id, engine=engine)

        # SUT
        result = sut.get_dependents(only_fetch_direct_dependencies, follow_suspended)

        # Verify
        mock_get_variable_method.assert_called_once_with(
            GetVariableDependenciesRequest(
                id=sut_element_id,
                onlyFetchDirectDependencies=only_fetch_direct_dependencies,
                followSuspended=follow_suspended,
            )
        )

        assert len(result) == 3

        # Verify: Different variable types are properly converted from VariableInfo to Datapin types
        assert isinstance(result[0], mc_api.IIntegerDatapin)
        assert result[0].element_id == "IDVAR_LARRY"
        assert isinstance(result[1], mc_api.IStringDatapin)
        assert result[1].element_id == "IDVAR_MOE"
        assert isinstance(result[2], mc_api.IRealDatapin)
        assert result[2].element_id == "IDVAR_CURLY"


@pytest.mark.parametrize(
    "only_fetch_direct_dependencies, follow_suspended",
    [(True, True), (True, False), (False, True), (False, False)],
)
def test_get_precedents(
    monkeypatch, engine, only_fetch_direct_dependencies: bool, follow_suspended: bool
) -> None:
    """Perform a test of get_precedents on a base datapin."""
    # Setup
    mock_client = MockWorkflowClientForVariableTest()
    sut_element_id = ElementId(id_string="VAR_UNDER_TEST_ID")
    return_variables = VariableInfoCollection(
        variables=[
            VariableInfo(
                id=ElementId(id_string="IDVAR_LARRY"),
                value_type=VariableType.VARTYPE_INTEGER,
                short_name="larry",
            ),
            VariableInfo(
                id=ElementId(id_string="IDVAR_MOE"),
                value_type=VariableType.VARTYPE_STRING,
                short_name="moe",
            ),
            VariableInfo(
                id=ElementId(id_string="IDVAR_CURLY"),
                value_type=VariableType.VARTYPE_REAL,
                short_name="curly",
            ),
        ]
    )
    with unittest.mock.patch.object(
        mock_client, "VariableGetPrecedents", return_value=return_variables
    ) as mock_get_variable_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = MockVariable(element_id=sut_element_id, engine=engine)

        # SUT
        result = sut.get_precedents(only_fetch_direct_dependencies, follow_suspended)

        # Verify
        mock_get_variable_method.assert_called_once_with(
            GetVariableDependenciesRequest(
                id=sut_element_id,
                onlyFetchDirectDependencies=only_fetch_direct_dependencies,
                followSuspended=follow_suspended,
            )
        )

        assert len(result) == 3

        # Verify: Different variable types are properly converted from VariableInfo to Datapin types
        assert isinstance(result[0], mc_api.IIntegerDatapin)
        assert result[0].element_id == "IDVAR_LARRY"
        assert isinstance(result[1], mc_api.IStringDatapin)
        assert result[1].element_id == "IDVAR_MOE"
        assert isinstance(result[2], mc_api.IRealDatapin)
        assert result[2].element_id == "IDVAR_CURLY"
