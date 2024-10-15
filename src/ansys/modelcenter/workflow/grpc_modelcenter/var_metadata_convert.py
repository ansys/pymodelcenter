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
"""Defines functions for converting between ACVI metadata and gRPC messages."""
from typing import Union

from ansys.api.modelcenter.v0.variable_value_messages_pb2 import (
    BaseVariableMetadata,
    BooleanVariableMetadata,
    DoubleVariableMetadata,
    FileVariableMetadata,
    IntegerVariableMetadata,
    NumericVariableMetadata,
    ReferenceVariableMetadata,
    StringVariableMetadata,
    VariableValue,
)
import ansys.tools.variableinterop as atvi

from .reference_datapin_metadata import ReferenceDatapinMetadata
from .var_value_convert import (
    ValueTypeNotSupportedError,
    convert_grpc_value_to_atvi,
    convert_interop_value_to_grpc,
)


class CustomMetadataValueNotSupportedError(ValueTypeNotSupportedError):
    """Raised if a custom metadata item includes an unsupported value type."""


def _extract_base_metadata(
    source: BaseVariableMetadata, target: atvi.CommonVariableMetadata
) -> None:
    """Extract ``atvi.CommonVariableMetadata`` fields from the corresponding
    gRPC message type."""
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
                "The datapin's custom metadata " "contains a value with an unsupported type."
            ) from custom_metadata_value_error


def _extract_numeric_metadata(
    source: NumericVariableMetadata, target: atvi.NumericMetadata
) -> None:
    """Extract ``atvi.NumericVariableMetadata`` fields from the corresponding
    gRPC message type."""
    target.units = source.units
    target.display_format = source.display_format


def convert_grpc_reference_metadata(source: ReferenceVariableMetadata) -> ReferenceDatapinMetadata:
    """Given a gRPC reference datapin metadata message, produce an equivalent \
    ``ReferenceDatapinMetadata`` object."""
    target = ReferenceDatapinMetadata()
    _extract_base_metadata(source.base_metadata, target)
    return target


def convert_grpc_boolean_metadata(source: BooleanVariableMetadata) -> atvi.BooleanMetadata:
    """Given a gRPC Boolean datapin metadata message, produce an equivalent \
    ``atvi.BooleanMetadata`` object."""
    target = atvi.BooleanMetadata()
    _extract_base_metadata(source.base_metadata, target)
    return target


def convert_grpc_boolean_array_metadata(
    source: BooleanVariableMetadata,
) -> atvi.BooleanArrayMetadata:
    """Given a gRPC Boolean array datapin metadata message, produce an
    equivalent ``atvi.BooleanArrayMetadata`` object."""
    target = atvi.BooleanArrayMetadata()
    _extract_base_metadata(source.base_metadata, target)
    return target


def _fill_base_metadata(source: atvi.CommonVariableMetadata, target: BaseVariableMetadata):
    """Fill out a gRPC message representing an ``atvi.CommonVariableMetadata``
    object."""
    target.description = source.description
    # Can't use a dict comprehension here because you can't assign the dict directly.
    for source_key, source_value in source.custom_metadata.items():
        target.custom_metadata[source_key].MergeFrom(convert_interop_value_to_grpc(source_value))


def fill_reference_metadata_message(
    source: ReferenceDatapinMetadata, target: ReferenceVariableMetadata
) -> None:
    """Fill out a gRPC message representing reference datapin metadata."""
    _fill_base_metadata(source, target.base_metadata)


def fill_boolean_metadata_message(
    source: atvi.BooleanMetadata, target: BooleanVariableMetadata
) -> None:
    """Fill out a gRPC message representing an ``atvi.BooleanMetadata`` object.

    The subordinate metadata types are also filled out.
    """
    _fill_base_metadata(source, target.base_metadata)


def _extract_real_metadata(source: DoubleVariableMetadata, target: atvi.RealMetadata) -> None:
    """Extract information for an ``atvi.RealMetadata`` object from a gRPC
    message."""
    _extract_base_metadata(source.base_metadata, target)
    _extract_numeric_metadata(source.numeric_metadata, target)
    target.lower_bound = source.lower_bound if source.HasField("lower_bound") else None
    target.upper_bound = source.upper_bound if source.HasField("upper_bound") else None
    target.enumerated_values = [
        atvi.RealValue(source_enum_value) for source_enum_value in source.enum_values
    ]
    target.enumerated_aliases = [source_alias for source_alias in source.enum_aliases]


def _fill_numeric_metadata(source: atvi.NumericMetadata, target: NumericVariableMetadata) -> None:
    """Fill out a gRPC message representing numeric metadata.

    Note that base metadata is not filled out by this helper. Invoke the
    ``_fill_base_metadata`` helper directly instead.
    """
    target.units = source.units
    target.display_format = source.display_format


def fill_real_metadata_message(source: atvi.RealMetadata, target: DoubleVariableMetadata) -> None:
    """Fill out a gRPC message representing real metadata.

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
    """Create an ``atvi.RealMetadata`` object for a real datapin from a gRPC
    message."""
    target = atvi.RealMetadata()
    _extract_real_metadata(source, target)
    return target


def convert_grpc_real_array_metadata(source: DoubleVariableMetadata) -> atvi.RealArrayMetadata:
    """Create an ``atvi.RealArrayMetadata`` object for a real array datapin
    from a gRPC message."""
    target = atvi.RealArrayMetadata()
    _extract_real_metadata(source, target)
    return target


def _extract_integer_metadata(
    source: IntegerVariableMetadata, target: atvi.IntegerMetadata
) -> None:
    """Extract information from an integer metadata gRPC message onto an
    ``atvi.IntegerMetadata`` object."""
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
    """Fill out a gRPC message representing integer metadata.

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
    """Create an ``atvi.IntegerMetadata`` object for an integer datapin from a
    gRPC message."""
    target = atvi.IntegerMetadata()
    _extract_integer_metadata(source, target)
    return target


def convert_grpc_integer_array_metadata(
    source: IntegerVariableMetadata,
) -> atvi.IntegerArrayMetadata:
    """Create an ``atvi.IntegerArrayMetadata`` object for an integer array
    datapin from a gRPC message."""
    target = atvi.IntegerArrayMetadata()
    _extract_integer_metadata(source, target)
    return target


def _extract_string_metadata(source: StringVariableMetadata, target: atvi.StringMetadata) -> None:
    """Extract information from a string metadata gRPC message onto an
    ``atvi.StringMetadata`` object."""
    _extract_base_metadata(source.base_metadata, target)
    target.enumerated_values = [
        atvi.StringValue(source_enum_value) for source_enum_value in source.enum_values
    ]
    target.enumerated_aliases = [source_alias for source_alias in source.enum_aliases]


def fill_string_metadata_message(
    source: atvi.StringMetadata, target: StringVariableMetadata
) -> None:
    """Fill out a gRPC message representing string metadata.

    All subordinate metadata fields are filled out by this method.
    """
    # Can't use list comps as gRPC repeated fields can't be directly assigned.
    for source_enum_value in source.enumerated_values:
        target.enum_values.append(str(source_enum_value))
    for source_enum_alias in source.enumerated_aliases:
        target.enum_aliases.append(source_enum_alias)
    _fill_base_metadata(source, target.base_metadata)


def convert_grpc_string_metadata(source: StringVariableMetadata) -> atvi.StringMetadata:
    """Create an ``atvi.StringMetadata`` object for a string datapin from a
    gRPC message."""
    target = atvi.StringMetadata()
    _extract_string_metadata(source, target)
    return target


def convert_grpc_string_array_metadata(source: StringVariableMetadata) -> atvi.StringArrayMetadata:
    """Create an ``atvi.StringArrayMetadata`` object for a string array datapin
    from a gRPC message."""
    target = atvi.StringArrayMetadata()
    _extract_string_metadata(source, target)
    return target


def convert_grpc_file_metadata(source: FileVariableMetadata) -> atvi.FileMetadata:
    """Given a gRPC file datapin metadata message, produce an equivalent
    ``atvi.FileMetadata`` object."""
    target = atvi.FileMetadata()
    _extract_base_metadata(source.base_metadata, target)
    return target


def convert_grpc_file_array_metadata(source: FileVariableMetadata) -> atvi.FileArrayMetadata:
    """Given a gRPC file array datapin metadata message, produce an equivalent
    ``atvi.FileMetadata`` object."""
    target = atvi.FileArrayMetadata()
    _extract_base_metadata(source.base_metadata, target)
    return target


def fill_file_metadata_message(source: atvi.FileMetadata, target: FileVariableMetadata) -> None:
    """Fill out a gRPC message representing an ``atvi.FileMetadata`` object.

    The subordinate metadata types are also filled out.
    """
    _fill_base_metadata(source, target.base_metadata)


def convert_grpc_metadata(
    source: Union[
        FileVariableMetadata,
        StringVariableMetadata,
        BooleanVariableMetadata,
        DoubleVariableMetadata,
        IntegerVariableMetadata,
    ],
    is_array: bool = False,
) -> atvi.CommonVariableMetadata:
    """Use a generic method to convert any type of variable m.Metadata.

    Parameters
    ----------
    source : FileVariableMetadata | StringVariableMetadata | BooleanVariableMetadata |
    DoubleVariableMetadata | IntegerVariableMetadata
        gRPC representation of a datapin metadata.

    is_array : bool, optional
        Whether the metadata i for an array datapin.

    Returns
    -------
    atvi.CommonVariableMetadata
        Equivalent ATVI metadata object.
    """
    source_type = type(source)
    if source_type is FileVariableMetadata:
        return (
            convert_grpc_file_array_metadata(source)
            if is_array
            else convert_grpc_file_metadata(source)
        )
    elif source_type is StringVariableMetadata:
        return (
            convert_grpc_string_array_metadata(source)
            if is_array
            else convert_grpc_string_metadata(source)
        )
    elif source_type is BooleanVariableMetadata:
        return (
            convert_grpc_boolean_array_metadata(source)
            if is_array
            else convert_grpc_boolean_metadata(source)
        )
    elif source_type is DoubleVariableMetadata:
        return (
            convert_grpc_real_array_metadata(source)
            if is_array
            else convert_grpc_real_metadata(source)
        )
    elif source_type is IntegerVariableMetadata:
        return (
            convert_grpc_integer_array_metadata(source)
            if is_array
            else convert_grpc_integer_metadata(source)
        )
    else:
        raise ValueTypeNotSupportedError(
            f"Generic conversion of metadata with type {type(source)} is not supported."
        )
