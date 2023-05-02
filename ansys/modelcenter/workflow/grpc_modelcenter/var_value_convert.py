"""Methods to convert between gRPC messages and Ansys Common Variable Interop's IVariableValue."""

import ansys.tools.variableinterop as atvi
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


class _ModelCenterTypeStringConverter(atvi.IVariableTypePseudoVisitor[str]):
    def visit_unknown(self) -> str:
        raise ValueError("Cannot determine a ModelCenter type for an unknown variable type.")

    def visit_int(self) -> str:
        return "int"

    def visit_real(self) -> str:
        return "real"

    def visit_boolean(self) -> str:
        return "bool"

    def visit_string(self) -> str:
        return "string"

    def visit_file(self) -> str:
        return "file"

    def visit_int_array(self) -> str:
        return "int[]"

    def visit_real_array(self) -> str:
        return "real[]"

    def visit_bool_array(self) -> str:
        return "bool[]"

    def visit_string_array(self) -> str:
        return "string[]"

    def visit_file_array(self) -> str:
        return "file[]"


def interop_type_to_mc_type_string(original: atvi.VariableType) -> str:
    """Given an atvi interop type, create the corresponding ModelCenter type string."""
    return atvi.vartype_accept(_ModelCenterTypeStringConverter(), original)


__MCDSTR_TO_INTEROP_TYPE_MAP = {
    "int": atvi.VariableType.INTEGER,
    "real": atvi.VariableType.REAL,
    "bool": atvi.VariableType.BOOLEAN,
    "string": atvi.VariableType.STRING,
    "file": atvi.VariableType.FILE,
    "int[]": atvi.VariableType.INTEGER_ARRAY,
    "real[]": atvi.VariableType.REAL_ARRAY,
    "bool[]": atvi.VariableType.BOOLEAN_ARRAY,
    "string[]": atvi.VariableType.STRING_ARRAY,
    "file[]": atvi.VariableType.FILE_ARRAY,
}


def mc_type_string_to_interop_type(original: str) -> atvi.VariableType:
    """Given a ModelCenter type string, create the corresponding atvi interop type."""
    return (
        __MCDSTR_TO_INTEROP_TYPE_MAP[original]
        if original in __MCDSTR_TO_INTEROP_TYPE_MAP
        else atvi.VariableType.UNKNOWN
    )


__GRPC_TO_INTEROP_TYPE_MAP = {
    VariableType.VARTYPE_INTEGER: atvi.VariableType.INTEGER,
    VariableType.VARTYPE_REAL: atvi.VariableType.REAL,
    VariableType.VARTYPE_BOOLEAN: atvi.VariableType.BOOLEAN,
    VariableType.VARTYPE_STRING: atvi.VariableType.STRING,
    VariableType.VARTYPE_FILE: atvi.VariableType.FILE,
    VariableType.VARTYPE_INTEGER_ARRAY: atvi.VariableType.INTEGER_ARRAY,
    VariableType.VARTYPE_REAL_ARRAY: atvi.VariableType.REAL_ARRAY,
    VariableType.VARTYPE_BOOLEAN_ARRAY: atvi.VariableType.BOOLEAN_ARRAY,
    VariableType.VARTYPE_STRING_ARRAY: atvi.VariableType.STRING_ARRAY,
    VariableType.VARTYPE_FILE_ARRAY: atvi.VariableType.FILE_ARRAY,
}


def grpc_type_enum_to_interop_type(original: VariableType) -> atvi.VariableType:
    """Given a value of the GRPC type enumeration, return the appropriate value of the ACVI enum."""
    return (
        __GRPC_TO_INTEROP_TYPE_MAP[original]
        if original in __GRPC_TO_INTEROP_TYPE_MAP
        else atvi.VariableType.UNKNOWN
    )


def convert_grpc_value_to_acvi(original: VariableValue) -> atvi.IVariableValue:
    """
    Produce an equivalent IVariableValue from Ansys Common Variable Interop from a gRPC message.

    @param original: the original gRPC message
    @return the converted value
    """
    if original.HasField("int_value"):
        return atvi.IntegerValue(original.int_value)
    elif original.HasField("double_value"):
        return atvi.RealValue(original.double_value)
    elif original.HasField("bool_value"):
        return atvi.BooleanValue(original.bool_value)
    elif original.HasField("string_value"):
        return atvi.StringValue(original.string_value)
    elif original.HasField("int_array_value"):
        return atvi.IntegerArrayValue(
            original.int_array_value.dims.dims,
            np.reshape(original.int_array_value.values, original.int_array_value.dims.dims),
        )
    elif original.HasField("double_array_value"):
        return atvi.RealArrayValue(
            original.double_array_value.dims.dims,
            np.reshape(original.double_array_value.values, original.double_array_value.dims.dims),
        )
    elif original.HasField("bool_array_value"):
        return atvi.BooleanArrayValue(
            original.bool_array_value.dims.dims,
            np.reshape(original.bool_array_value.values, original.bool_array_value.dims.dims),
        )
    elif original.HasField("string_array_value"):
        return atvi.StringArrayValue(
            original.string_array_value.dims.dims,
            np.reshape(original.string_array_value.values, original.string_array_value.dims.dims),
        )
    # TODO: FileValue missing from gRPC API, need to add, update this case
    elif original.HasField("file_value"):
        raise ValueTypeNotSupportedError(
            "The provided gRPC value has a file type, "
            "but this is not yet supported by the pyModelCenter API."
        )
    elif original.HasField("file_array_value"):
        raise ValueTypeNotSupportedError(
            "The provided gRPC value has a file type, "
            "but this is not yet supported by the pyModelCenter API."
        )
    else:
        raise ValueError(
            "The provided gRPC value could not be converted to a common variable " "interop value."
        )


class ToGRPCVisitor(atvi.IVariableValueVisitor[VariableValue]):
    """Produces a gRPC VariableValue message for a given IVariableValue."""

    @overrides
    def visit_integer(self, value: atvi.IntegerValue) -> VariableValue:
        return VariableValue(int_value=int(value))

    @overrides
    def visit_real(self, value: atvi.RealValue) -> VariableValue:
        return VariableValue(double_value=float(value))

    @overrides
    def visit_boolean(self, value: atvi.BooleanValue) -> VariableValue:
        return VariableValue(bool_value=bool(value))

    @overrides
    def visit_string(self, value: atvi.StringValue) -> VariableValue:
        return VariableValue(string_value=str(value))

    @overrides
    def visit_integer_array(self, value: atvi.IntegerArrayValue) -> VariableValue:
        return VariableValue(
            int_array_value=IntegerArrayValue(
                values=value.flatten(), dims=ArrayDimensions(dims=value.shape)
            )
        )

    @overrides
    def visit_file(self, value: atvi.FileValue) -> VariableValue:
        raise ValueTypeNotSupportedError(
            "A file value was provided, but pyModelCenter currently does not support this type."
        )

    @overrides
    def visit_real_array(self, value: atvi.RealArrayValue) -> VariableValue:
        return VariableValue(
            double_array_value=DoubleArrayValue(
                values=value.flatten(), dims=ArrayDimensions(dims=value.shape)
            )
        )

    @overrides
    def visit_boolean_array(self, value: atvi.BooleanArrayValue) -> VariableValue:
        return VariableValue(
            bool_array_value=BooleanArrayValue(
                values=value.flatten(), dims=ArrayDimensions(dims=value.shape)
            )
        )

    @overrides
    def visit_string_array(self, value: atvi.StringArrayValue) -> VariableValue:
        return VariableValue(
            string_array_value=StringArrayValue(
                values=value.flatten(), dims=ArrayDimensions(dims=value.shape)
            )
        )

    @overrides
    def visit_file_array(self, value: atvi.FileArrayValue) -> VariableValue:
        raise ValueTypeNotSupportedError(
            "A file array value was provided, but pyModelCenter currently does not support this "
            "type."
        )


def convert_interop_value_to_grpc(original: atvi.IVariableValue) -> VariableValue:
    """Produce an equivalent gRPC VariableValue message from an IVariableValue."""
    return original.accept(ToGRPCVisitor())
