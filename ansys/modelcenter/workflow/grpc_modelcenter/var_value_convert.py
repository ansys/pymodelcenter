"""Methods to convert between gRPC messages and Ansys Common Variable Interop's IVariableValue."""

from contextlib import ExitStack
from typing import Optional

import ansys.tools.variableinterop as atvi
import numpy as np
from overrides import overrides

from .proto.variable_value_messages_pb2 import (
    ArrayDimensions,
    BooleanArrayValue,
    DoubleArrayValue,
    FileArrayValue,
    FileValue,
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
    """Given a ModelCenter type string, create the corresponding ATVI interop type."""
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
    """Given a value of the GRPC type enumeration, return the appropriate value of the ATVI enum."""
    return (
        __GRPC_TO_INTEROP_TYPE_MAP[original]
        if original in __GRPC_TO_INTEROP_TYPE_MAP
        else atvi.VariableType.UNKNOWN
    )


def interop_type_to_grpc_type_enum(original: atvi.VariableType) -> VariableType:
    """
    Given a value of the ATVI type enum, return the appropriate GRPC type enumeration.

    NOTE: This does not handle reference types, as they map to atvi.VariableType.UNKNOWN, and are
    thus indistinguishable from actual unknown types.
    """
    for key, value in __GRPC_TO_INTEROP_TYPE_MAP.items():
        if value == original:
            return key
    return VariableType.VARTYPE_UNKNOWN


def convert_grpc_value_to_atvi(
    original: VariableValue, engine_is_local: bool = True
) -> atvi.IVariableValue:
    """
    Produce an IVariableValue from the Python variable interop library from a grpc message.

    Parameters
    ----------
    original: VariableValue
        The original gRPC message.
    engine_is_local: bool
        True if the Engine that created the file is running on the local machine, False if it is
        remote.

    Returns
    -------
    The converted value.
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
    elif original.HasField("file_value"):
        if not engine_is_local:
            raise ValueTypeNotSupportedError(
                "Requesting file values from a remote Engine is currently not supported."
            )
        scope = atvi.NonManagingFileScope()
        value: atvi.FileValue = scope.read_from_file(
            to_read=original.file_value.content_path, mime_type=None, encoding=None
        )
        return value
    elif original.HasField("file_array_value"):
        if not engine_is_local:
            raise ValueTypeNotSupportedError(
                "Requesting file values from a remote Engine is currently not supported."
            )
        scope = atvi.NonManagingFileScope()
        values = [
            scope.read_from_file(to_read=value.content_path, mime_type=None, encoding=None)
            for value in original.file_array_value.values
        ]
        return atvi.FileArrayValue(
            original.file_array_value.dims.dims,
            np.reshape(values, original.file_array_value.dims.dims),
        )
    else:
        raise ValueTypeNotSupportedError(
            "The provided gRPC value could not be converted to a common variable interop value."
        )


class ToGRPCVisitor(atvi.IVariableValueVisitor[VariableValue]):
    """Produces a gRPC VariableValue message for a given IVariableValue."""

    def __init__(self, local_file_context_stack: Optional[ExitStack], engine_is_local: bool):
        """
        Initialize a new instance.

        Parameters
        ==========
        local_file_context_stack : Optional[ExitStack]
            An exit stack into which local file content contexts will be opened.
            It is the caller's responsibility to close / exit this object.
            If None is passed, any attempt to convert a file value
            raises a ValueTypeNotSupportedError.
        engine_is_local : bool
            A flag indicating whether the ModelCenter engine is local.
            This may impact how or whether file value conversion is supported.
        """
        self._local_file_context_stack = local_file_context_stack
        self._engine_is_local = engine_is_local

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
        if self._local_file_context_stack is None:
            raise ValueTypeNotSupportedError(
                "File values are currently not supported for this operation."
            )
        if not self._engine_is_local:
            raise ValueTypeNotSupportedError(
                "Sending file values to remote engines is currently not supported."
            )
        local_file_context: atvi.LocalFileContentContext = (
            self._local_file_context_stack.enter_context(
                value.get_reference_to_actual_content_file()
            )
        )
        return VariableValue(file_value=FileValue(content_path=local_file_context.content_path))

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
        converted = FileArrayValue(dims=ArrayDimensions(dims=value.shape))
        if self._local_file_context_stack is None:
            raise ValueTypeNotSupportedError(
                "File array values are not currently supported for this operation."
            )
        if not self._engine_is_local:
            raise ValueTypeNotSupportedError(
                "Sending file values to remote engines is currently not supported."
            )
        each_file_value: atvi.FileValue
        for each_file_value in value.flatten():
            each_local_file_context: atvi.LocalFileContentContext = (
                self._local_file_context_stack.enter_context(
                    each_file_value.get_reference_to_actual_content_file()
                )
            )
            converted.values.add(content_path=each_local_file_context.content_path)
        return VariableValue(file_array_value=converted)


def convert_interop_value_to_grpc(
    original: atvi.IVariableValue,
    local_file_context_stack: Optional[ExitStack] = None,
    engine_is_local=False,
) -> VariableValue:
    """Produce an equivalent gRPC VariableValue message from an IVariableValue."""
    return original.accept(ToGRPCVisitor(local_file_context_stack, engine_is_local))
