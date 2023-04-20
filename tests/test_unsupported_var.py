import ansys.common.variableinterop as acvi
import pytest

from ansys.modelcenter.workflow.grpc_modelcenter.proto.element_messages_pb2 import ElementId
from ansys.modelcenter.workflow.grpc_modelcenter.proto.variable_value_messages_pb2 import (
    VariableState,
)
from ansys.modelcenter.workflow.grpc_modelcenter.unsupported_type_datapin import (
    DatapinWithUnsupportedTypeException,
    UnsupportedTypeDatapin,
)

from .grpc_server_test_utils.client_creation_monkeypatch import monkeypatch_client_creation


class MockWorkflowClientForUnsupportedVarTest:
    def __init__(self):
        pass


def test_set_metadata(monkeypatch) -> None:
    # Setup
    mock_client = MockWorkflowClientForUnsupportedVarTest()
    monkeypatch_client_creation(monkeypatch, UnsupportedTypeDatapin, mock_client)
    sut = UnsupportedTypeDatapin(element_id=ElementId(id_string="VAR_UNDER_TEST_ID"), channel=None)

    # SUT/Verification
    with pytest.raises(DatapinWithUnsupportedTypeException):
        sut.set_metadata(acvi.BooleanMetadata())


def test_set_value(monkeypatch) -> None:
    # Setup
    mock_client = MockWorkflowClientForUnsupportedVarTest()
    monkeypatch_client_creation(monkeypatch, UnsupportedTypeDatapin, mock_client)
    sut = UnsupportedTypeDatapin(element_id=ElementId(id_string="VAR_UNDER_TEST_ID"), channel=None)

    # SUT/Verification
    with pytest.raises(DatapinWithUnsupportedTypeException):
        sut.set_value(VariableState())


def test_get_metadata(monkeypatch) -> None:
    # Setup
    mock_client = MockWorkflowClientForUnsupportedVarTest()
    monkeypatch_client_creation(monkeypatch, UnsupportedTypeDatapin, mock_client)
    sut = UnsupportedTypeDatapin(element_id=ElementId(id_string="VAR_UNDER_TEST_ID"), channel=None)

    # SUT/Verification
    with pytest.raises(DatapinWithUnsupportedTypeException):
        sut.get_metadata()
