"""Contains definition for IntegerVariable and IntegerArray."""

from typing import Collection, Optional, Sequence

import ansys.common.variableinterop as acvi
from ansys.engineeringworkflow.api import Property
import grpc
import numpy as np
from overrides import overrides

import ansys.modelcenter.workflow.api as wfapi
from ansys.modelcenter.workflow.api import VariableLink
import ansys.modelcenter.workflow.grpc_modelcenter.proto.element_messages_pb2 as element_msg
from ansys.modelcenter.workflow.grpc_modelcenter.proto.grpc_modelcenter_workflow_pb2_grpc import (
    ModelCenterWorkflowServiceStub,
)
import ansys.modelcenter.workflow.grpc_modelcenter.proto.variable_value_messages_pb2 as var_val_msg

from ._visitors import VariableValueVisitor


class IntegerVariable(wfapi.IIntegerVariable):
    """Represents a gRPC integer variable on the workflow."""

    @overrides
    def __init__(self, id: element_msg.ElementId, channel: grpc.Channel):
        self._id = id
        self._channel = channel
        self._stub = ModelCenterWorkflowServiceStub(channel)

    @property  # type: ignore
    @overrides
    def value(self) -> acvi.IntegerValue:
        response: var_val_msg.VariableState = self._stub.VariableGetState(self._id)
        return acvi.IntegerValue(response.value.int_value)

    @value.setter  # type: ignore
    @overrides
    def value(self, new_value: acvi.IntegerValue):
        new_value.accept(VariableValueVisitor(var_id=self._id, stub=self._stub))

    @overrides
    def get_properties(self) -> Collection[Property]:
        raise NotImplementedError

    @overrides
    def precedent_links(self, reserved: Optional[object] = None) -> Sequence[VariableLink]:
        raise NotImplementedError

    @overrides
    def dependent_links(self, reserved: Optional[object] = None) -> Sequence[VariableLink]:
        raise NotImplementedError


class IntegerArray(wfapi.IIntegerArray):
    """Represents a gRPC double / real array variable on the workflow."""

    @overrides
    def __init__(self, id: element_msg.ElementId, channel: grpc.Channel):
        self._id = id
        self._channel = channel
        self._stub = ModelCenterWorkflowServiceStub(channel)

    @property  # type: ignore
    @overrides
    def value(self) -> acvi.IntegerArrayValue:
        response: var_val_msg.VariableState = self._stub.VariableGetState(self._id)
        grpc_value = response.value.int_array_value
        values = np.array(grpc_value.values).flatten()
        dims = grpc_value.dims.dims
        return acvi.IntegerArrayValue(shape_=dims, values=values)

    @value.setter  # type: ignore
    @overrides
    def value(self, new_value: acvi.IntegerArrayValue):
        new_value.accept(VariableValueVisitor(var_id=self._id, stub=self._stub))

    @overrides
    def get_properties(self) -> Collection[Property]:
        raise NotImplementedError

    @overrides
    def precedent_links(self, reserved: Optional[object] = None) -> Sequence[VariableLink]:
        raise NotImplementedError

    @overrides
    def dependent_links(self, reserved: Optional[object] = None) -> Sequence[VariableLink]:
        raise NotImplementedError
