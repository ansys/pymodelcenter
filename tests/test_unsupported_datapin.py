from ansys.api.modelcenter.v0.element_messages_pb2 import ElementId
from ansys.api.modelcenter.v0.variable_value_messages_pb2 import VariableState
from ansys.modelcenter.workflow.grpc_modelcenter.unsupported_type_datapin import (
    DatapinWithUnsupportedTypeException,
    UnsupportedTypeDatapin,
)
import ansys.tools.variableinterop as atvi
import pytest

from .grpc_server_test_utils.client_creation_monkeypatch import monkeypatch_client_creation


class MockWorkflowClientForUnsupportedDatapinTest:
    def __init__(self):
        pass


def test_set_metadata(monkeypatch, engine) -> None:
    # Setup
    mock_client = MockWorkflowClientForUnsupportedDatapinTest()
    monkeypatch_client_creation(monkeypatch, UnsupportedTypeDatapin, mock_client)
    sut = UnsupportedTypeDatapin(element_id=ElementId(id_string="VAR_UNDER_TEST_ID"), engine=engine)

    # SUT/Verification
    with pytest.raises(DatapinWithUnsupportedTypeException):
        sut.set_metadata(atvi.BooleanMetadata())


def test_set_state(monkeypatch, engine) -> None:
    # Setup
    mock_client = MockWorkflowClientForUnsupportedDatapinTest()
    monkeypatch_client_creation(monkeypatch, UnsupportedTypeDatapin, mock_client)
    sut = UnsupportedTypeDatapin(element_id=ElementId(id_string="VAR_UNDER_TEST_ID"), engine=engine)

    # SUT/Verification
    with pytest.raises(DatapinWithUnsupportedTypeException):
        sut.set_state(VariableState())


def test_get_metadata(monkeypatch, engine) -> None:
    # Setup
    mock_client = MockWorkflowClientForUnsupportedDatapinTest()
    monkeypatch_client_creation(monkeypatch, UnsupportedTypeDatapin, mock_client)
    sut = UnsupportedTypeDatapin(element_id=ElementId(id_string="VAR_UNDER_TEST_ID"), engine=engine)

    # SUT/Verification
    with pytest.raises(DatapinWithUnsupportedTypeException):
        sut.get_metadata()
