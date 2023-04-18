"""Contains definition for StringVariable and StringArrayVariable."""

import ansys.common.variableinterop as acvi
from grpc import Channel
from overrides import overrides

import ansys.modelcenter.workflow.api as mc_api

from ._visitors.variable_value_visitor import VariableValueVisitor
from .grpc_error_interpretation import (
    WRAP_OUT_OF_BOUNDS,
    WRAP_TARGET_NOT_FOUND,
    interpret_rpc_error,
)
from .proto.element_messages_pb2 import ElementId
from .proto.variable_value_messages_pb2 import SetStringVariableMetadataRequest
from .var_metadata_convert import (
    convert_grpc_string_array_metadata,
    convert_grpc_string_metadata,
    fill_string_metadata_message,
)
from .variable import BaseVariable


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
    def __eq__(self, other):
        return isinstance(other, StringVariable) and self.element_id == other.element_id

    @interpret_rpc_error(WRAP_TARGET_NOT_FOUND)
    @overrides
    def get_metadata(self) -> acvi.StringArrayMetadata:
        response = self._client.StringVariableGetMetadata(self._element_id)
        return convert_grpc_string_metadata(response)

    @interpret_rpc_error(WRAP_TARGET_NOT_FOUND)
    @overrides
    def set_metadata(self, new_metadata: acvi.CommonVariableMetadata) -> None:
        if not isinstance(new_metadata, acvi.StringMetadata):
            raise TypeError(
                f"The provided metadata object is not the correct type."
                f"Expected {acvi.StringArrayMetadata} "
                f"but received {new_metadata.__class__}"
            )
        request = SetStringVariableMetadataRequest(target=self._element_id)
        fill_string_metadata_message(new_metadata, request.new_metadata)
        self._client.StringVariableSetMetadata(request)

    @interpret_rpc_error({**WRAP_TARGET_NOT_FOUND, **WRAP_OUT_OF_BOUNDS})
    @overrides
    def set_value(self, value: acvi.VariableState) -> None:
        self._do_set_value(value.value)

    @acvi.implicit_coerce
    def _do_set_value(self, value: acvi.StringValue) -> None:
        value.accept(VariableValueVisitor(self._element_id, self._client))


class StringArrayVariable(BaseVariable, mc_api.IStringArrayVariable):
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
        super(StringArrayVariable, self).__init__(element_id=element_id, channel=channel)

    @overrides
    def __eq__(self, other):
        return isinstance(other, StringArrayVariable) and self.element_id == other.element_id

    @interpret_rpc_error(WRAP_TARGET_NOT_FOUND)
    @overrides
    def get_metadata(self) -> acvi.StringArrayMetadata:
        response = self._client.StringVariableGetMetadata(self._element_id)
        return convert_grpc_string_array_metadata(response)

    @interpret_rpc_error(WRAP_TARGET_NOT_FOUND)
    @overrides
    def set_metadata(self, new_metadata: acvi.CommonVariableMetadata) -> None:
        if not isinstance(new_metadata, acvi.StringArrayMetadata):
            raise TypeError(
                f"The provided metadata object is not the correct type."
                f"Expected {acvi.StringArrayMetadata} "
                f"but received {new_metadata.__class__}"
            )
        request = SetStringVariableMetadataRequest(target=self._element_id)
        fill_string_metadata_message(new_metadata, request.new_metadata)
        self._client.StringVariableSetMetadata(request)

    @interpret_rpc_error({**WRAP_TARGET_NOT_FOUND, **WRAP_OUT_OF_BOUNDS})
    @overrides
    def set_value(self, value: acvi.VariableState) -> None:
        self._do_set_value(value.value)

    @acvi.implicit_coerce
    def _do_set_value(self, value: acvi.StringArrayValue) -> None:
        value.accept(VariableValueVisitor(self._element_id, self._client))
