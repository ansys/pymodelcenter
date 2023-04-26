"""Contains definition for StringDatapin and StringArrayDatapin."""

import ansys.common.variableinterop as acvi
from grpc import Channel
from overrides import overrides

import ansys.modelcenter.workflow.api as mc_api

from ._visitors.variable_value_visitor import VariableValueVisitor
from .base_datapin import BaseDatapin
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


class StringDatapin(BaseDatapin, mc_api.IStringDatapin):
    """
    Represents a gRPC string variable on the workflow.

    .. note::
        This class should not be directly instantiated by clients. Get a Workflow object from
        an instantiated Engine, and use it to get a valid instance of this object.
    """

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
        super(StringDatapin, self).__init__(element_id=element_id, channel=channel)

    @overrides
    def __eq__(self, other):
        return isinstance(other, StringDatapin) and self.element_id == other.element_id

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


class StringArrayDatapin(BaseDatapin, mc_api.IStringArrayDatapin):
    """
    Represents a gRPC double / real array variable on the workflow.

    .. note::
        This class should not be directly instantiated by clients. Get a Workflow object from
        an instantiated Engine, and use it to get a valid instance of this object.
    """

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
        super(StringArrayDatapin, self).__init__(element_id=element_id, channel=channel)

    @overrides
    def __eq__(self, other):
        return isinstance(other, StringArrayDatapin) and self.element_id == other.element_id

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
