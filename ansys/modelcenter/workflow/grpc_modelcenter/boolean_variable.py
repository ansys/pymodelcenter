"""Contains definition for BooleanVariable and BooleanArray."""

import ansys.common.variableinterop as acvi
from grpc import Channel
from overrides import overrides

import ansys.modelcenter.workflow.api as mc_api

from ._visitors.variable_value_visitor import VariableValueVisitor
from .proto.element_messages_pb2 import ElementId
from .proto.variable_value_messages_pb2 import SetBooleanVariableMetadataRequest
from .var_metadata_convert import (
    convert_grpc_boolean_array_metadata,
    convert_grpc_boolean_metadata,
    fill_boolean_metadata_message,
)
from .variable import BaseArray, BaseVariable


class BooleanVariable(BaseVariable, mc_api.IBooleanVariable):
    """Represents a gRPC boolean variable on the workflow."""

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
        super(BooleanVariable, self).__init__(element_id=element_id, channel=channel)

    @overrides
    def get_metadata(self) -> acvi.BooleanArrayMetadata:
        response = self._client.BooleanVariableGetMetadata(self._element_id)
        return convert_grpc_boolean_metadata(response)

    @overrides
    def set_metadata(self, new_metadata: acvi.CommonVariableMetadata) -> None:
        if not isinstance(new_metadata, acvi.BooleanMetadata):
            raise TypeError()  # TODO: be more informative in this error message
        request = SetBooleanVariableMetadataRequest(target=self._element_id)
        fill_boolean_metadata_message(new_metadata, request.new_metadata)
        self._client.BooleanVariableSetMetadata(request)

    @overrides
    def set_value(self, value: acvi.VariableState) -> None:
        if not isinstance(value.value, acvi.BooleanValue):
            raise acvi.IncompatibleTypesException(
                value.value.variable_type, acvi.VariableType.BOOLEAN
            )
        set_visitor: VariableValueVisitor = VariableValueVisitor(self._element_id, self._client)
        value.value.accept(set_visitor)


class BooleanArray(BaseArray, mc_api.IBooleanArray):
    """Represents a gRPC boolean array variable on the workflow."""

    @overrides
    def get_metadata(self) -> acvi.BooleanArrayMetadata:
        response = self._client.BooleanVariableGetMetadata(self._element_id)
        return convert_grpc_boolean_array_metadata(response)

    @overrides
    def set_metadata(self, new_metadata: acvi.CommonVariableMetadata) -> None:
        if not isinstance(new_metadata, acvi.BooleanArrayMetadata):
            raise TypeError()  # TODO: be more informative in this error message
        request = SetBooleanVariableMetadataRequest(target=self._element_id)
        fill_boolean_metadata_message(new_metadata, request.new_metadata)
        self._client.BooleanVariableSetMetadata(request)

    @overrides
    def set_value(self, value: acvi.VariableState) -> None:
        if not isinstance(value.value, acvi.BooleanArrayValue):
            raise acvi.IncompatibleTypesException(
                value.value.variable_type, acvi.VariableType.BOOLEAN_ARRAY
            )
        set_visitor: VariableValueVisitor = VariableValueVisitor(self._element_id, self._client)
        value.value.accept(set_visitor)

    @overrides
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
        super(BooleanArray, self).__init__(element_id=element_id, channel=channel)
