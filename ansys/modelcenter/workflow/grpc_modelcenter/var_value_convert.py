"""Methods to convert between gRPC messages and Ansys Common Variable Interop's IVariableValue."""

import ansys.common.variableinterop as acvi
from ansys.common.variableinterop.ivariable_visitor import T
import numpy as np
from overrides import overrides

from .proto.variable_value_messages_pb2 import (
    ArrayDimensions,
    BooleanArrayValue,
    DoubleArrayValue,
    IntegerArrayValue,
    StringArrayValue,
    VariableValue,
)


def convert_grpc_value_to_acvi(original: VariableValue) -> acvi.IVariableValue:
    """
    Produce an equivalent IVariableValue from Ansys Common Variable Interop from a gRPC message.

    @param original: the original gRPC message
    @return the converted value
    """
    if original.HasField("int_value"):
        return acvi.IntegerValue(original.int_value)
    elif original.HasField("double_value"):
        return acvi.RealValue(original.double_value)
    elif original.HasField("bool_value"):
        return acvi.BooleanValue(original.bool_value)
    elif original.HasField("string_value"):
        return acvi.StringValue(original.string_value)
    elif original.HasField("int_array_value"):
        return acvi.IntegerArrayValue(
            original.int_array_value.dims.dims,
            np.reshape(original.int_array_value.values, original.int_array_value.dims.dims),
        )
    elif original.HasField("double_array_value"):
        return acvi.RealArrayValue(
            original.double_array_value.dims.dims,
            np.reshape(original.double_array_value.values, original.double_array_value.dims.dims),
        )
    elif original.HasField("bool_array_value"):
        return acvi.BooleanArrayValue(
            original.bool_array_value.dims.dims,
            np.reshape(original.bool_array_value.values, original.bool_array_value.dims.dims),
        )
    elif original.HasField("string_array_value"):
        return acvi.StringArrayValue(
            original.string_array_value.dims.dims,
            np.reshape(original.string_array_value.values, original.string_array_value.dims.dims),
        )


class ToGRPCVisitor(acvi.IVariableValueVisitor[VariableValue]):
    """Produces a gRPC VariableValue message for a given IVariableValue."""

    @overrides
    def visit_integer(self, value: acvi.IntegerValue) -> VariableValue:
        return VariableValue(int_value=int(value))

    @overrides
    def visit_real(self, value: acvi.RealValue) -> VariableValue:
        return VariableValue(double_value=float(value))

    @overrides
    def visit_boolean(self, value: acvi.BooleanValue) -> VariableValue:
        return VariableValue(bool_value=bool(value))

    @overrides
    def visit_string(self, value: acvi.StringValue) -> T:
        return VariableValue(string_value=str(value))

    @overrides
    def visit_integer_array(self, value: acvi.IntegerArrayValue) -> T:
        return VariableValue(
            int_array_value=IntegerArrayValue(
                values=value.flatten(), dims=ArrayDimensions(dims=value.shape)
            )
        )

    @overrides
    def visit_file(self, value: acvi.FileValue) -> T:
        raise NotImplementedError()

    @overrides
    def visit_real_array(self, value: acvi.RealArrayValue) -> T:
        return VariableValue(
            double_array_value=DoubleArrayValue(
                values=value.flatten(), dims=ArrayDimensions(dims=value.shape)
            )
        )

    @overrides
    def visit_boolean_array(self, value: acvi.BooleanArrayValue) -> T:
        return VariableValue(
            bool_array_value=BooleanArrayValue(
                values=value.flatten(), dims=ArrayDimensions(dims=value.shape)
            )
        )

    @overrides
    def visit_string_array(self, value: acvi.StringArrayValue) -> T:
        return VariableValue(
            string_array_value=StringArrayValue(
                values=value.flatten(), dims=ArrayDimensions(dims=value.shape)
            )
        )

    @overrides
    def visit_file_array(self, value: acvi.FileArrayValue) -> T:
        raise NotImplementedError()


def convert_interop_value_to_grpc(original: acvi.IVariableValue) -> VariableValue:
    """Produce an equivalent gRPC VariableValue message from an IVariableValue."""
    return original.accept(ToGRPCVisitor())
