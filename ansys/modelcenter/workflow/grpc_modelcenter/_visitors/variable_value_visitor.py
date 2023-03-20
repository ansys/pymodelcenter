from typing import Callable, Type

import ansys.common.variableinterop as acvi
import numpy as np
from overrides import overrides

import ansys.modelcenter.workflow.grpc_modelcenter.proto.element_messages_pb2 as element_msg
from ansys.modelcenter.workflow.grpc_modelcenter.proto.grpc_modelcenter_workflow_pb2_grpc import (
    ModelCenterWorkflowServiceStub,
)
import ansys.modelcenter.workflow.grpc_modelcenter.proto.variable_value_messages_pb2 as var_val_msg


class VariableValueVisitor(acvi.IVariableValueVisitor[bool]):
    """Visitor for setting variable values via ModelCenter gRPC API."""

    def __init__(self, var_name: str, stub: ModelCenterWorkflowServiceStub):
        """
        Create a new VariableValueVisitor.

        Parameters
        ----------
        var_name: str
            Name of variable to set.
        stub: ModelCenterWorkflowServiceStub
            gRPC stub to use.
        """
        self._var_name = var_name
        self._stub = stub

    @overrides
    def visit_integer(self, value: acvi.IntegerValue) -> bool:
        return self._scalar_request(
            value, var_val_msg.SetIntegerValueRequest, int, self._stub.IntegerVariableSetValue
        )

    @overrides
    def visit_real(self, value: acvi.RealValue) -> bool:
        return self._scalar_request(
            value, var_val_msg.SetDoubleValueRequest, float, self._stub.DoubleVariableSetValue
        )

    @overrides
    def visit_boolean(self, value: acvi.BooleanValue) -> bool:
        return self._scalar_request(
            value, var_val_msg.SetBooleanValueRequest, bool, self._stub.BooleanVariableSetValue
        )

    @overrides
    def visit_string(self, value: acvi.StringValue) -> bool:
        return self._scalar_request(
            value, var_val_msg.SetStringValueRequest, str, self._stub.StringVariableSetValue
        )

    @overrides
    def visit_file(self, value: acvi.FileValue) -> bool:
        raise NotImplementedError

    @overrides
    def visit_integer_array(self, value: acvi.IntegerArrayValue) -> bool:
        return self._array_request(
            value,
            var_val_msg.SetIntegerArrayValueRequest,
            var_val_msg.IntegerArrayValue,
            self._stub.IntegerArraySetValue,
        )

    @overrides
    def visit_real_array(self, value: acvi.RealArrayValue) -> bool:
        return self._array_request(
            value,
            var_val_msg.SetDoubleArrayValueRequest,
            var_val_msg.DoubleArrayValue,
            self._stub.DoubleArraySetValue,
        )

    @overrides
    def visit_boolean_array(self, value: acvi.BooleanArrayValue) -> bool:
        return self._array_request(
            value,
            var_val_msg.SetBooleanArrayValueRequest,
            var_val_msg.BooleanArrayValue,
            self._stub.BooleanArraySetValue,
        )

    @overrides
    def visit_string_array(self, value: acvi.StringArrayValue) -> bool:
        return self._array_request(
            value,
            var_val_msg.SetStringArrayValueRequest,
            var_val_msg.StringArrayValue,
            self._stub.StringArraySetValue,
        )

    @overrides
    def visit_file_array(self, value: acvi.FileArrayValue) -> bool:
        raise NotImplementedError

    def _scalar_request(
        self, value: acvi.IVariableValue, request_type: Type, value_type: Type, grpc_call: Callable
    ) -> bool:
        """
        Helper method to send a gRPC request for setting scalar values.

        Parameters
        ----------
        value: acvi.IVariableValue
            The new value to set.
        request_type: Type
            The type of request (e.g. SetIntegerValueRequest)
        value_type: Type
            The type of value to set, from protobuf (e.g. int, float, etc.)
        grpc_call: Callable
            The method used to make the gRPC call (e.g. IntegerVariableSetValue)

        Returns
        -------
        bool
            was_changed from the response message.
        """
        target = element_msg.ElementId(id_string=self._var_name)
        request = request_type(target=target, new_value=value_type(value))
        response = grpc_call(request)
        return response.was_changed

    def _array_request(
        self,
        value: acvi.CommonArrayValue,
        request_type: Type,
        value_type: Type,
        grpc_call: Callable,
    ):
        """
        Helper method to send a gRPC request for setting array values.

        Parameters
        ----------
        value: acvi.CommonArrayValue
            The new value to set.
        request_type: Type
            The type of request (e.g. SetIntegerArrayValueRequest)
        value_type: Type
            The type of value to set, from protobuf (e.g. IntegerArrayValue, DoubleArrayValue, etc.)
        grpc_call: Callable
            The method used to make the gRPC call (e.g. IntegerArraySetValue)

        Returns
        -------
        bool
            was_changed from the response message.
        """
        target = element_msg.ElementId(id_string=self._var_name)
        set_value = value_type(values=value.flatten(), dims=self._dims(value))
        request = request_type(target=target, new_value=set_value)
        response = grpc_call(request)
        return response.was_changed

    @staticmethod
    def _dims(array: acvi.CommonArrayValue) -> var_val_msg.ArrayDimensions:
        """Helper method to get array dimensions (protobuf)."""
        return var_val_msg.ArrayDimensions(dims=np.array(array.get_lengths()).flatten())
