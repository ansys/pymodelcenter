"""Contains definition for IntegerVariable and IntegerArray."""
import ansys.common.variableinterop as acvi
from grpc import Channel
from overrides import overrides

import ansys.modelcenter.workflow.api as mc_api

from ._visitors.variable_value_visitor import VariableValueVisitor
from .proto.element_messages_pb2 import ElementId
from .proto.variable_value_messages_pb2 import SetIntegerVariableMetadataRequest
from .var_metadata_convert import (
    convert_grpc_integer_array_metadata,
    convert_grpc_integer_metadata,
    fill_integer_metadata_message,
)
from .variable import BaseArray, BaseVariable


class IntegerVariable(BaseVariable, mc_api.IIntegerVariable):
    """Represents a gRPC integer variable on the workflow."""

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
        super(IntegerVariable, self).__init__(element_id=element_id, channel=channel)

    @overrides
    def get_metadata(self) -> acvi.IntegerMetadata:
        response = self._client.IntegerVariableGetMetadata(self._element_id)
        return convert_grpc_integer_metadata(response)

    @overrides
    def set_metadata(self, new_metadata: acvi.CommonVariableMetadata) -> None:
        if not isinstance(new_metadata, acvi.IntegerMetadata):
            raise TypeError()  # TODO: be more informative in this error message
        request = SetIntegerVariableMetadataRequest(target=self._element_id)
        fill_integer_metadata_message(new_metadata, request.new_metadata)
        self._client.IntegerVariableSetMetadata(request)

    @overrides
    def set_value(self, value: acvi.VariableState) -> None:
        self._do_set_value(value.value)

    @acvi.implicit_coerce
    def _do_set_value(self, value: acvi.IntegerValue) -> None:
        value.accept(VariableValueVisitor(self._element_id, self._client))


class IntegerArray(BaseArray, mc_api.IIntegerArray):
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
        super(IntegerArray, self).__init__(element_id=element_id, channel=channel)

    @overrides
    def get_metadata(self) -> acvi.RealArrayMetadata:
        response = self._client.IntegerVariableGetMetadata(self._element_id)
        return convert_grpc_integer_array_metadata(response)

    @overrides
    def set_metadata(self, new_metadata: acvi.CommonVariableMetadata) -> None:
        if not isinstance(new_metadata, acvi.IntegerArrayMetadata):
            raise TypeError()  # TODO: be more informative in this error message
        request = SetIntegerVariableMetadataRequest(target=self._element_id)
        fill_integer_metadata_message(new_metadata, request.new_metadata)
        self._client.IntegerVariableSetMetadata(request)

    @overrides
    def set_value(self, value: acvi.VariableState) -> None:
        self._do_set_value(value.value)

    @acvi.implicit_coerce
    def _do_set_value(self, value: acvi.IntegerArrayValue) -> None:
        value.accept(VariableValueVisitor(self._element_id, self._client))