"""Contains definition for StringVariable."""
from typing import Collection, Optional, Sequence

from ansys.engineeringworkflow.api import Property
from overrides import overrides

import ansys.modelcenter.workflow.api as wfapi
from ansys.modelcenter.workflow.api import VariableLink
import ansys.modelcenter.workflow.grpc_modelcenter.proto.element_messages_pb2 as element_msg
from ansys.modelcenter.workflow.grpc_modelcenter.proto.grpc_modelcenter_workflow_pb2_grpc import (
    ModelCenterWorkflowServiceStub,
)
import ansys.modelcenter.workflow.grpc_modelcenter.proto.variable_value_messages_pb2 as var_val_msg


class StringVariable(wfapi.IStringVariable):
    """Represents a gRPC string variable on the workflow."""

    @overrides
    def __init__(self, id: element_msg.ElementId, stub: ModelCenterWorkflowServiceStub):
        self._id = id
        self._stub = stub

    @property  # type: ignore
    @overrides
    def value(self) -> str:
        response: var_val_msg.VariableState = self._stub.VariableGetState(self._id)
        return response.value.string_value

    @value.setter  # type: ignore
    @overrides
    def value(self, new_value: var_val_msg.DoubleValue):
        raise NotImplementedError

    @overrides
    def get_properties(self) -> Collection[Property]:
        raise NotImplementedError

    @overrides
    def precedent_links(self, reserved: Optional[object] = None) -> Sequence[VariableLink]:
        raise NotImplementedError

    @overrides
    def dependent_links(self, reserved: Optional[object] = None) -> Sequence[VariableLink]:
        raise NotImplementedError
