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
    VariableType,
    VariableValue,
)


class ValueTypeNotSupportedError(ValueError):
    """Indicates that an attempt was made to convert a value with a known but unsupported type."""


class _ModelCenterTypeStringConverter(acvi.IVariableTypePseudoVisitor):
    def visit_unknown(self) -> T:
        raise ValueError("Cannot determine a ModelCenter type for an unknown variable type.")

    def visit_int(self) -> T:
        return "int"

    def visit_real(self) -> T:
        return "real"

    def visit_boolean(self) -> T:
        return "bool"

    def visit_string(self) -> T:
        return "string"

    def visit_file(self) -> T:
        return "file"

    def visit_int_array(self) -> T:
        return "int[]"

    def visit_real_array(self) -> T:
        return "real[]"

    def visit_bool_array(self) -> T:
        return "bool[]"

    def visit_string_array(self) -> T:
        return "string[]"

    def visit_file_array(self) -> T:
        return "file[]"


def interop_type_to_mc_type_string(original: acvi.VariableType) -> str:
    """Given an acvi interop type, create the corresponding ModelCenter type string."""
    return acvi.vartype_accept(_ModelCenterTypeStringConverter(), original)


__GRPC_TO_INTEROP_TYPE_MAP = {
    VariableType.VARTYPE_INTEGER: acvi.VariableType.INTEGER,
    VariableType.VARTYPE_REAL: acvi.VariableType.REAL,
    VariableType.VARTYPE_BOOLEAN: acvi.VariableType.BOOLEAN,
    VariableType.VARTYPE_STRING: acvi.VariableType.STRING,
    VariableType.VARTYPE_FILE: acvi.VariableType.FILE,
    VariableType.VARTYPE_INTEGER_ARRAY: acvi.VariableType.INTEGER_ARRAY,
    VariableType.VARTYPE_REAL_ARRAY: acvi.VariableType.REAL_ARRAY,
    VariableType.VARTYPE_BOOLEAN_ARRAY: acvi.VariableType.BOOLEAN_ARRAY,
    VariableType.VARTYPE_STRING_ARRAY: acvi.VariableType.STRING_ARRAY,
    VariableType.VARTYPE_FILE_ARRAY: acvi.VariableType.FILE_ARRAY,
}


def grpc_type_enum_to_interop_type(original: VariableType) -> acvi.VariableType:
    """Given a value of the GRPC type enumeration, return the appropriate value of the ACVI enum."""
    return (
        __GRPC_TO_INTEROP_TYPE_MAP[original]
        if original in __GRPC_TO_INTEROP_TYPE_MAP
        else acvi.VariableType.UNKNOWN
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
    # TODO: FileValue missing from gRPC API, need to add, update this case
    elif original.HasField("file_value"):
        raise ValueTypeNotSupportedError(
            "The provided gRPC value has a file type, "
            "but this is not yet supported by the pyModelCenter API."
        )
    else:
        raise ValueError(
            "The provided gRPC value could not be converted to a common variable " "interop value."
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
        raise ValueTypeNotSupportedError(
            "A file value was provided, but pyModelCenter currently does not support this type."
        )

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
        raise ValueTypeNotSupportedError(
            "A file array value was provided, but pyModelCenter currently does not support this "
            "type."
        )


def convert_interop_value_to_grpc(original: acvi.IVariableValue) -> VariableValue:
    """Produce an equivalent gRPC VariableValue message from an IVariableValue."""
    return original.accept(ToGRPCVisitor())
