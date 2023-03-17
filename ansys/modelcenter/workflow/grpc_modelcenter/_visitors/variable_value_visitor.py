from typing import Callable, Type

import ansys.common.variableinterop as acvi
from ansys.common.variableinterop.ivariable_visitor import T
import numpy as np

import ansys.modelcenter.workflow.grpc_modelcenter.proto.element_messages_pb2 as element_msg
from ansys.modelcenter.workflow.grpc_modelcenter.proto.grpc_modelcenter_workflow_pb2_grpc import (
    ModelCenterWorkflowServiceStub,
)
import ansys.modelcenter.workflow.grpc_modelcenter.proto.variable_value_messages_pb2 as var_val_msg


class VariableValueVisitor(acvi.IVariableValueVisitor[bool]):
    """Visitor pattern implementation for use with acvi.IVariableValue."""

    def __init__(self, var_name: str, stub: ModelCenterWorkflowServiceStub):
        """
        Create a new VariableValueVisitor.

        Parameters
        ----------
        varname: str
            Name of variable to set.
        stub: ModelCenterWorkflowServiceStub
            gRPC stub to use.
        """
        self._var_name = var_name
        self._stub = stub

    def visit_integer(self, value: acvi.IntegerValue) -> T:  # noqa D102
        return self._scalar_request(
            value, var_val_msg.SetIntegerValueRequest, int, self._stub.IntegerVariableSetValue
        )

    def visit_real(self, value: acvi.RealValue) -> T:  # noqa D102
        return self._scalar_request(
            value, var_val_msg.SetDoubleValueRequest, float, self._stub.DoubleVariableSetValue
        )

    def visit_boolean(self, value: acvi.BooleanValue) -> T:  # noqa D102
        return self._scalar_request(
            value, var_val_msg.SetBooleanValueRequest, bool, self._stub.BooleanVariableSetValue
        )

    def visit_string(self, value: acvi.StringValue) -> T:  # noqa D102
        return self._scalar_request(
            value, var_val_msg.SetStringValueRequest, str, self._stub.StringVariableSetValue
        )

    def visit_file(self, value: acvi.FileValue) -> T:  # noqa D102
        raise NotImplementedError

    def visit_integer_array(self, value: acvi.IntegerArrayValue) -> T:  # noqa D102
        return self._array_request(
            value,
            var_val_msg.SetIntegerArrayValueRequest,
            var_val_msg.IntegerArrayValue,
            self._stub.IntegerArraySetValue,
        )

    def visit_real_array(self, value: acvi.RealArrayValue) -> T:  # noqa D102
        return self._array_request(
            value,
            var_val_msg.SetDoubleArrayValueRequest,
            var_val_msg.DoubleArrayValue,
            self._stub.DoubleArraySetValue,
        )

    def visit_boolean_array(self, value: acvi.BooleanArrayValue) -> T:  # noqa D102
        return self._array_request(
            value,
            var_val_msg.SetBooleanArrayValueRequest,
            var_val_msg.BooleanArrayValue,
            self._stub.BooleanArraySetValue,
        )

    def visit_string_array(self, value: acvi.StringArrayValue) -> T:  # noqa D102
        return self._array_request(
            value,
            var_val_msg.SetStringArrayValueRequest,
            var_val_msg.StringArrayValue,
            self._stub.StringArraySetValue,
        )

    def visit_file_array(self, value: acvi.FileArrayValue) -> T:  # noqa D102
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
        target = element_msg.ElementId()
        target.id_string = self._var_name
        request = request_type()
        request.target = target
        request.new_value = value_type(value)
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
        target = element_msg.ElementId()
        target.id_string = self._var_name
        set_value = value_type()
        set_value.values = value.flatten()
        set_value.dims = self._dims(value)
        request = request_type()
        request.target = target
        request.new_value = set_value
        response = grpc_call(request)
        return response.was_changed

    @staticmethod
    def _dims(array: acvi.CommonArrayValue) -> var_val_msg.ArrayDimensions:
        """Helper method to get array dimensions (protobuf)."""
        lengths = np.array(array.get_lengths()).flatten()
        dims = var_val_msg.ArrayDimensions()
        dims.dims = lengths
        return dims
