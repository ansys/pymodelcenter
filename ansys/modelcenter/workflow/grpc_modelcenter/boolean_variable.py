"""Contains definition for BooleanVariable and BooleanArray."""

from typing import Collection, Optional, Sequence

import ansys.common.variableinterop as acvi
from ansys.engineeringworkflow.api import Property
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


class BooleanVariable(wfapi.IBooleanVariable):
    """Represents a gRPC boolean variable on the workflow."""

    @overrides
    def __init__(self, id: element_msg.ElementId, stub: ModelCenterWorkflowServiceStub):
        self._id = id
        self._stub = stub

    @property  # type: ignore
    @overrides
    def value(self) -> acvi.BooleanValue:
        response: var_val_msg.VariableState = self._stub.VariableGetState(self._id)
        return acvi.BooleanValue(response.value.bool_value)

    @value.setter  # type: ignore
    @overrides
    def value(self, new_value: acvi.BooleanValue):
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


class BooleanArray(wfapi.IBooleanArray):
    """Represents a gRPC boolean array variable on the workflow."""

    @overrides
    def __init__(self, id: element_msg.ElementId, stub: ModelCenterWorkflowServiceStub):
        self._id = id
        self._stub = stub

    @property  # type: ignore
    @overrides
    def value(self) -> acvi.BooleanArrayValue:
        response: var_val_msg.VariableState = self._stub.VariableGetState(self._id)
        grpc_value = response.value.bool_array_value
        values = np.array(grpc_value.values).flatten()
        dims = grpc_value.dims.dims
        return acvi.BooleanArrayValue(shape_=dims, values=values)

    @value.setter  # type: ignore
    @overrides
    def value(self, new_value: acvi.BooleanArrayValue):
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
