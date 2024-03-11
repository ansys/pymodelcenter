# Copyright (C) 2022 - 2024 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from contextlib import ExitStack
from typing import Callable, Type

import ansys.api.modelcenter.v0.element_messages_pb2 as element_msg
from ansys.api.modelcenter.v0.grpc_modelcenter_workflow_pb2_grpc import (
    ModelCenterWorkflowServiceStub,
)
import ansys.api.modelcenter.v0.variable_value_messages_pb2 as var_val_msg
import ansys.engineeringworkflow.api as aew_api
import ansys.tools.variableinterop as atvi
import numpy as np
from overrides import overrides

from ansys.modelcenter.workflow.grpc_modelcenter.var_value_convert import ValueTypeNotSupportedError


class VariableValueVisitor(atvi.IVariableValueVisitor[bool]):
    """Provides the visitor for setting datapin values with the ModelCenter gRPC
    API."""

    def __init__(
        self,
        var_id: element_msg.ElementId,
        stub: ModelCenterWorkflowServiceStub,
        engine_is_local: bool,
    ):
        """Create a VariableValueVisitor.

        Parameters
        ----------
        var_id : element_msg.ElementId
            ID of the datapin to set.
        stub : ModelCenterWorkflowServiceStub
            gRPC stub to use.
        engine_is_local : bool
            Whether the engine is running locally or on a remote machine.
        """
        self._var_id = var_id
        self._stub = stub
        self._engine_is_local = engine_is_local

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
        if self._engine_is_local:
            with value.get_reference_to_actual_content_file() as local_pin:
                value_in_request = var_val_msg.FileValue()
                if local_pin.content_path is not None:
                    value_in_request.content_path = str(local_pin.content_path)
                request = var_val_msg.SetFileValueRequest(
                    target=self._var_id, new_value=value_in_request
                )
                response = self._stub.FileVariableSetValue(request)
                return response.was_changed
        else:
            raise ValueTypeNotSupportedError(
                "Setting file values is not currently supported for " "remote engines."
            )

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
        if self._engine_is_local:
            with ExitStack() as local_content_copy_stack:
                request = var_val_msg.SetFileArrayValueRequest(
                    target=self._var_id,
                    new_value=var_val_msg.FileArrayValue(
                        dims=var_val_msg.ArrayDimensions(dims=value.get_lengths())
                    ),
                )
                one_file_value: atvi.FileValue
                for one_file_value in value.flatten():
                    one_local_content: atvi.LocalFileContentContext = (
                        local_content_copy_stack.enter_context(
                            one_file_value.get_reference_to_actual_content_file()
                        )
                    )
                    one_grpc_file_value = var_val_msg.FileValue()
                    if one_local_content.content_path is not None:
                        one_grpc_file_value.content_path = str(one_local_content.content_path)
                    request.new_value.values.add(content_path=one_local_content.content_path)
                response = self._stub.FileArraySetValue(request)
                return response.was_changed
            # This line should only be reachable if one of the context managers in
            # local_content_copy_stack suppress an exception, which they should not
            # be doing.
            raise aew_api.EngineInternalError(
                "Reached an unexpected state. A local file content context may be suppressing an "
                "exception. Report this error on the PyModelCenter repository's Issues page."
            )
        else:
            raise ValueTypeNotSupportedError(
                "Setting file array values is not currently " "supported for remote engines."
            )

    def _scalar_request(
        self, value: atvi.IVariableValue, request_type: Type, value_type: Type, grpc_call: Callable
    ) -> bool:
        """Use this helper method to send a gRPC request for setting scalar
        values.

        Parameters
        ----------
        value : acvi.IVariableValue
            New value to set.
        request_type : Type
            Type of the request. For example, ``SetIntegerValueRequest``.
        value_type : Type
            Type of the value to set, from protobuf. For example, ``int`` or
            ``float``.
        grpc_call : Callable
            Method to use to make the gRPC call. For example,
            ``IntegerVariableSetValue``.

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
        """Use this helper method to send a gRPC request for setting array
        values.

        Parameters
        ----------
        value: acvi.CommonArrayValue
            New value to set.
        request_type: Type
            Type of the request. For example, ``SetIntegerArrayValueRequest``.
        value_type: Type
            Type of the value to set, from protobuf. For example,
            ``IntegerArrayValue`` or ``DoubleArrayValue``.
        grpc_call: Callable
            Method to use to make the gRPC call. For example,
            ``IntegerArraySetValue``.

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
        """Use this helper method to get array dimensions (protobuf)."""
        return var_val_msg.ArrayDimensions(dims=np.array(array.get_lengths()).flatten())
