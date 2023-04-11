"""Contains definition for StringVariable and StringArray."""

import ansys.common.variableinterop as acvi
from grpc import Channel
from overrides import overrides

import ansys.modelcenter.workflow.api as mc_api

from ._visitors.variable_value_visitor import VariableValueVisitor
from .proto.element_messages_pb2 import ElementId
from .proto.variable_value_messages_pb2 import SetStringVariableMetadataRequest
from .var_metadata_convert import (
    convert_grpc_string_array_metadata,
    convert_grpc_string_metadata,
    fill_string_metadata_message,
)
from .variable import BaseArray, BaseVariable


class StringVariable(BaseVariable, mc_api.IStringVariable):
    """Represents a gRPC string variable on the workflow."""

    def __init__(self, element_id: ElementId, channel: Channel):
        """
        Initialize a new instance.

        Parameters
        ----------
        element_id: ElementId
            The id of the variable.
        channel: Channel
            The gRPC channel to use.
        """
        super(StringVariable, self).__init__(element_id=element_id, channel=channel)

    @overrides
    def get_metadata(self) -> acvi.StringArrayMetadata:
        response = self._client.StringVariableGetMetadata(self._element_id)
        return convert_grpc_string_metadata(response)

    @overrides
    def set_metadata(self, new_metadata: acvi.CommonVariableMetadata) -> None:
        if not isinstance(new_metadata, acvi.StringMetadata):
            raise TypeError()  # TODO: be more informative in this error message
        request = SetStringVariableMetadataRequest(target=self._element_id)
        fill_string_metadata_message(new_metadata, request.new_metadata)
        self._client.StringVariableSetMetadata(request)

    @overrides
    def set_value(self, value: acvi.VariableState) -> None:
        self._do_set_value(value.value)

    @acvi.implicit_coerce
    def _do_set_value(self, value: acvi.StringValue) -> None:
        value.accept(VariableValueVisitor(self._element_id, self._client))


class StringArray(BaseArray, mc_api.IStringArray):
    """Represents a gRPC double / real array variable on the workflow."""

    def __init__(self, element_id: ElementId, channel: Channel):
        """
        Initialize a new instance.

        Parameters
        ----------
        element_id: ElementId
            The id of the variable.
        channel: Channel
            The gRPC channel to use.
        """
        super(StringArray, self).__init__(element_id=element_id, channel=channel)

    @overrides
    def get_metadata(self) -> acvi.StringArrayMetadata:
        response = self._client.StringVariableGetMetadata(self._element_id)
        return convert_grpc_string_array_metadata(response)

    @overrides
    def set_metadata(self, new_metadata: acvi.CommonVariableMetadata) -> None:
        if not isinstance(new_metadata, acvi.StringArrayMetadata):
            raise TypeError()  # TODO: be more informative in this error message
        request = SetStringVariableMetadataRequest(target=self._element_id)
        fill_string_metadata_message(new_metadata, request.new_metadata)
        self._client.StringVariableSetMetadata(request)

    @overrides
    def set_value(self, value: acvi.VariableState) -> None:
        self._do_set_value(value.value)

    @acvi.implicit_coerce
    def _do_set_value(self, value: acvi.StringArrayValue) -> None:
        value.accept(VariableValueVisitor(self._element_id, self._client))