from typing import Callable, Type

import ansys.tools.variableinterop as atvi
import numpy as np
from overrides import overrides

import ansys.modelcenter.workflow.grpc_modelcenter.proto.element_messages_pb2 as element_msg
from ansys.modelcenter.workflow.grpc_modelcenter.proto.grpc_modelcenter_workflow_pb2_grpc import (
    ModelCenterWorkflowServiceStub,
)
import ansys.modelcenter.workflow.grpc_modelcenter.proto.variable_value_messages_pb2 as var_val_msg


class VariableValueVisitor(atvi.IVariableValueVisitor[bool]):
    """Visitor for setting variable values via ModelCenter gRPC API."""

    def __init__(self, var_id: element_msg.ElementId, stub: ModelCenterWorkflowServiceStub):
        """
        Create a new VariableValueVisitor.

        Parameters
        ----------
        var_id: str
            Name of variable to set.
        stub: ModelCenterWorkflowServiceStub
            gRPC stub to use.
        """
        self._var_id = var_id
        self._stub = stub

    @overrides
    def visit_integer(self, value: atvi.IntegerValue) -> bool:
        return self._scalar_request(
            value, var_val_msg.SetIntegerValueRequest, int, self._stub.IntegerVariableSetValue
        )

    @overrides
    def visit_real(self, value: atvi.RealValue) -> bool:
        return self._scalar_request(
            value, var_val_msg.SetDoubleValueRequest, float, self._stub.DoubleVariableSetValue
        )

    @overrides
    def visit_boolean(self, value: atvi.BooleanValue) -> bool:
        return self._scalar_request(
            value, var_val_msg.SetBooleanValueRequest, bool, self._stub.BooleanVariableSetValue
        )

    @overrides
    def visit_string(self, value: atvi.StringValue) -> bool:
        return self._scalar_request(
            value, var_val_msg.SetStringValueRequest, str, self._stub.StringVariableSetValue
        )

    @overrides
    def visit_file(self, value: atvi.FileValue) -> bool:
        with value.get_reference_to_actual_content_file() as local_pin:
            value_in_request = var_val_msg.FileValue()
            if local_pin.content_path is not None:
                value_in_request.content_path = str(local_pin.content_path)
            request = var_val_msg.SetFileValueRequest(
                target=self._var_id, new_value=value_in_request
            )
            response = self._stub.FileVariableSetValue(request)
            return response.was_changed

    @overrides
    def visit_integer_array(self, value: atvi.IntegerArrayValue) -> bool:
        return self._array_request(
            value,
            var_val_msg.SetIntegerArrayValueRequest,
            var_val_msg.IntegerArrayValue,
            self._stub.IntegerArraySetValue,
        )

    @overrides
    def visit_real_array(self, value: atvi.RealArrayValue) -> bool:
        return self._array_request(
            value,
            var_val_msg.SetDoubleArrayValueRequest,
            var_val_msg.DoubleArrayValue,
            self._stub.DoubleArraySetValue,
        )

    @overrides
    def visit_boolean_array(self, value: atvi.BooleanArrayValue) -> bool:
        return self._array_request(
            value,
            var_val_msg.SetBooleanArrayValueRequest,
            var_val_msg.BooleanArrayValue,
            self._stub.BooleanArraySetValue,
        )

    @overrides
    def visit_string_array(self, value: atvi.StringArrayValue) -> bool:
        return self._array_request(
            value,
            var_val_msg.SetStringArrayValueRequest,
            var_val_msg.StringArrayValue,
            self._stub.StringArraySetValue,
        )

    @overrides
    def visit_file_array(self, value: atvi.FileArrayValue) -> bool:
        raise NotImplementedError  # pragma: no cover

    def _scalar_request(
        self, value: atvi.IVariableValue, request_type: Type, value_type: Type, grpc_call: Callable
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
        request = request_type(target=self._var_id, new_value=value_type(value))
        response = grpc_call(request)
        return response.was_changed

    def _array_request(
        self,
        value: atvi.CommonArrayValue,
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
        set_value = value_type(values=value.flatten(), dims=self._dims(value))
        request = request_type(target=self._var_id, new_value=set_value)
        response = grpc_call(request)
        return response.was_changed

    @staticmethod
    def _dims(array: atvi.CommonArrayValue) -> var_val_msg.ArrayDimensions:
        """Helper method to get array dimensions (protobuf)."""
        return var_val_msg.ArrayDimensions(dims=np.array(array.get_lengths()).flatten())
