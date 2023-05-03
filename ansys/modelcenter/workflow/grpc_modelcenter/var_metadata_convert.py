"""Defines functions for converting between ACVI metadata and gRPC messages."""

import ansys.tools.variableinterop as atvi

from .proto.variable_value_messages_pb2 import (
    BaseVariableMetadata,
    BooleanVariableMetadata,
    DoubleVariableMetadata,
    IntegerVariableMetadata,
    NumericVariableMetadata,
    StringVariableMetadata,
    VariableValue,
)
from .var_value_convert import (
    ValueTypeNotSupportedError,
    convert_grpc_value_to_atvi,
    convert_interop_value_to_grpc,
)


class CustomMetadataValueNotSupportedError(ValueTypeNotSupportedError):
    """Indicates that a custom metadata item included an unsupported value type."""


def _extract_base_metadata(
    source: BaseVariableMetadata, target: atvi.CommonVariableMetadata
) -> None:
    """Extract ACVI CommonVariableMetadata fields from the corresponding gRPC message type."""
    target.description = source.description
    source_custom_key: str
    source_custom_value: VariableValue
    # Can't use a dict comprehension as the custom_metadata property is not settable.
    for source_custom_key, source_custom_value in source.custom_metadata.items():
        try:
            target.custom_metadata[source_custom_key] = convert_grpc_value_to_atvi(
                source_custom_value
            )
        except ValueTypeNotSupportedError as custom_metadata_value_error:
            raise CustomMetadataValueNotSupportedError(
                "The variable's custom metadata " "contains a value with an unsupported type."
            ) from custom_metadata_value_error


def _extract_numeric_metadata(
    source: NumericVariableMetadata, target: atvi.NumericMetadata
) -> None:
    """Extract ACVI NumericVariableMetadata fields from the corresponding gRPC message type."""
    target.units = source.units
    target.display_format = source.display_format


def convert_grpc_boolean_metadata(source: BooleanVariableMetadata) -> atvi.BooleanMetadata:
    """Given a gRPC boolean variable metadata message, produce an equivalent ATVI metadata."""
    target = atvi.BooleanMetadata()
    _extract_base_metadata(source.base_metadata, target)
    return target


def convert_grpc_boolean_array_metadata(
    source: BooleanVariableMetadata,
) -> atvi.BooleanArrayMetadata:
    """Given a gRPC boolean array variable metadata message, produce an equivalent ATVI metadata."""
    target = atvi.BooleanArrayMetadata()
    _extract_base_metadata(source.base_metadata, target)
    return target


def _fill_base_metadata(source: atvi.CommonVariableMetadata, target: BaseVariableMetadata):
    """Fill out a gRPC message representing ATVI common variable metadata."""
    target.description = source.description
    # Can't use a dict comprehension here because you can't assign the dict directly.
    for source_key, source_value in source.custom_metadata.items():
        target.custom_metadata[source_key].MergeFrom(convert_interop_value_to_grpc(source_value))


def fill_boolean_metadata_message(
    source: atvi.BooleanMetadata, target: BooleanVariableMetadata
) -> None:
    """
    Fill out a gRPC message representing ATVI boolean metadata.

    The subordinate metadata types are also filled out.
    """
    _fill_base_metadata(source, target.base_metadata)


def _extract_real_metadata(source: DoubleVariableMetadata, target: atvi.RealMetadata) -> None:
    """Extract information for an ATVI real metadata from a gRPC message."""
    _extract_base_metadata(source.base_metadata, target)
    _extract_numeric_metadata(source.numeric_metadata, target)
    target.lower_bound = source.lower_bound if source.HasField("lower_bound") else None
    target.upper_bound = source.upper_bound if source.HasField("upper_bound") else None
    target.enumerated_values = [
        atvi.RealValue(source_enum_value) for source_enum_value in source.enum_values
    ]
    target.enumerated_aliases = [source_alias for source_alias in source.enum_aliases]


def _fill_numeric_metadata(source: atvi.NumericMetadata, target: NumericVariableMetadata) -> None:
    """
    Fill out a gRPC message representing a numeric metadata.

    Note that base metadata is not filled out by this helper. Invoke the _fill_base_metadata
    helper directly instead.
    """
    target.units = source.units
    target.display_format = source.display_format


def fill_real_metadata_message(source: atvi.RealMetadata, target: DoubleVariableMetadata) -> None:
    """
    Fill out a gRPC message representing real metadata.

    All subordinate metadata fields are filled out by this method.
    """
    _fill_base_metadata(source, target.base_metadata)
    _fill_numeric_metadata(source, target.numeric_metadata)
    if source.lower_bound is not None:
        target.lower_bound = source.lower_bound
    if source.upper_bound is not None:
        target.upper_bound = source.upper_bound
    # Can't use list comps as gRPC repeated fields can't be directly assigned.
    for source_enum_value in source.enumerated_values:
        target.enum_values.append(float(source_enum_value))
    for source_enum_alias in source.enumerated_aliases:
        target.enum_aliases.append(source_enum_alias)


def convert_grpc_real_metadata(source: DoubleVariableMetadata) -> atvi.RealMetadata:
    """Create an ATVI metadata object for a real variable from a gRPC message."""
    target = atvi.RealMetadata()
    _extract_real_metadata(source, target)
    return target


def convert_grpc_real_array_metadata(source: DoubleVariableMetadata) -> atvi.RealArrayMetadata:
    """Create an ATVI metadata object for a real array variable from a gRPC message."""
    target = atvi.RealArrayMetadata()
    _extract_real_metadata(source, target)
    return target


def _extract_integer_metadata(
    source: IntegerVariableMetadata, target: atvi.IntegerMetadata
) -> None:
    """Extract information from an integer metadata gRPC message onto an ATVI metadata object."""
    _extract_base_metadata(source.base_metadata, target)
    _extract_numeric_metadata(source.numeric_metadata, target)
    target.lower_bound = source.lower_bound if source.HasField("lower_bound") else None
    target.upper_bound = source.upper_bound if source.HasField("upper_bound") else None
    target.enumerated_values = [
        atvi.IntegerValue(source_enum_value) for source_enum_value in source.enum_values
    ]
    target.enumerated_aliases = [source_alias for source_alias in source.enum_aliases]


def fill_integer_metadata_message(
    source: atvi.IntegerMetadata, target: IntegerVariableMetadata
) -> None:
    """
    Fill out a gRPC message representing integer metadata.

    All subordinate metadata fields are filled out by this method.
    """
    _fill_base_metadata(source, target.base_metadata)
    _fill_numeric_metadata(source, target.numeric_metadata)
    if source.lower_bound is not None:
        target.lower_bound = source.lower_bound
    if source.upper_bound is not None:
        target.upper_bound = source.upper_bound
    # Can't use list comps as gRPC repeated fields can't be directly assigned.
    for source_enum_value in source.enumerated_values:
        target.enum_values.append(int(source_enum_value))
    for source_enum_alias in source.enumerated_aliases:
        target.enum_aliases.append(source_enum_alias)


def convert_grpc_integer_metadata(source: IntegerVariableMetadata) -> atvi.IntegerMetadata:
    """Create an ATVI metadata object for an integer variable from a gRPC message."""
    target = atvi.IntegerMetadata()
    _extract_integer_metadata(source, target)
    return target


def convert_grpc_integer_array_metadata(
    source: IntegerVariableMetadata,
) -> atvi.IntegerArrayMetadata:
    """Create an ATVI metadata object for an integer array variable from a gRPC message."""
    target = atvi.IntegerArrayMetadata()
    _extract_integer_metadata(source, target)
    return target


def _extract_string_metadata(source: StringVariableMetadata, target: atvi.StringMetadata) -> None:
    """Extract information from a string metadata gRPC message onto an ATVI metadata object."""
    _extract_base_metadata(source.base_metadata, target)
    target.enumerated_values = [
        atvi.StringValue(source_enum_value) for source_enum_value in source.enum_values
    ]
    target.enumerated_aliases = [source_alias for source_alias in source.enum_aliases]


def fill_string_metadata_message(
    source: atvi.StringMetadata, target: StringVariableMetadata
) -> None:
    """
    Fill out a gRPC message representing string metadata.

    All subordinate metadata fields are filled out by this method.
    """
    # Can't use list comps as gRPC repeated fields can't be directly assigned.
    for source_enum_value in source.enumerated_values:
        target.enum_values.append(str(source_enum_value))
    for source_enum_alias in source.enumerated_aliases:
        target.enum_aliases.append(source_enum_alias)
    _fill_base_metadata(source, target.base_metadata)


def convert_grpc_string_metadata(source: StringVariableMetadata) -> atvi.StringMetadata:
    """Create an ATVI metadata object for a string variable from a gRPC message."""
    target = atvi.StringMetadata()
    _extract_string_metadata(source, target)
    return target


def convert_grpc_string_array_metadata(source: StringVariableMetadata) -> atvi.StringArrayMetadata:
    """Create an ATVI metadata object for a string array variable from a gRPC message."""
    target = atvi.StringArrayMetadata()
    _extract_string_metadata(source, target)
    return target
