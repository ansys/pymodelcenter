"""Contains definition for IntegerVariable."""

import ansys.common.variableinterop as acvi
from overrides import overrides

import ansys.modelcenter.workflow.api as wfapi
import ansys.modelcenter.workflow.grpc_modelcenter.proto.element_messages_pb2 as element_msg
from ansys.modelcenter.workflow.grpc_modelcenter.proto.grpc_modelcenter_workflow_pb2_grpc import (
    ModelCenterWorkflowServiceStub,
)
import ansys.modelcenter.workflow.grpc_modelcenter.proto.variable_value_messages_pb2 as var_val_msg


class IntegerVariable(wfapi.IIntegerVariable):
    """Represents a gRPC integer variable on the workflow."""

    @overrides
    def __init__(self, id: element_msg.ElementId, stub: ModelCenterWorkflowServiceStub):
        self._id = id
        self._stub = stub

    @property  # type: ignore
    @overrides
    def value(self) -> acvi.IntegerValue:
        response: var_val_msg.VariableState = self._stub.VariableGetState(self._id)
        return acvi.IntegerValue(response.value.int_value)

    @value.setter  # type: ignore
    @overrides
    def value(self, new_value: acvi.IntegerValue):
        request = var_val_msg.SetIntegerValueRequest(target=self._id, new_value=new_value)
        self._stub.IntegerVariableSetValue(request)
