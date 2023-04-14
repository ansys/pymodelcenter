"""Contains definition for BooleanDatapin and BooleanArrayDatapin."""

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
from .proto.variable_value_messages_pb2 import SetBooleanVariableMetadataRequest
from .var_metadata_convert import (
    convert_grpc_boolean_array_metadata,
    convert_grpc_boolean_metadata,
    fill_boolean_metadata_message,
)


class BooleanDatapin(BaseDatapin, mc_api.IBooleanDatapin):
    """Represents a boolean datapin."""

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
        super(BooleanDatapin, self).__init__(element_id=element_id, channel=channel)

    @interpret_rpc_error(WRAP_TARGET_NOT_FOUND)
    @overrides
    def get_metadata(self) -> acvi.BooleanArrayMetadata:
        response = self._client.BooleanVariableGetMetadata(self._element_id)
        return convert_grpc_boolean_metadata(response)

    @interpret_rpc_error(WRAP_TARGET_NOT_FOUND)
    @overrides
    def set_metadata(self, new_metadata: acvi.CommonVariableMetadata) -> None:
        if not isinstance(new_metadata, acvi.BooleanMetadata):
            raise TypeError(
                f"The provided metadata object is not the correct type."
                f"Expected {acvi.BooleanMetadata} "
                f"but received {new_metadata.__class__}"
            )
        request = SetBooleanVariableMetadataRequest(target=self._element_id)
        fill_boolean_metadata_message(new_metadata, request.new_metadata)
        self._client.BooleanVariableSetMetadata(request)

    @interpret_rpc_error({**WRAP_TARGET_NOT_FOUND, **WRAP_OUT_OF_BOUNDS})
    @overrides
    def set_value(self, value: acvi.VariableState) -> None:
        if not isinstance(value.value, acvi.BooleanValue):
            raise acvi.IncompatibleTypesException(
                value.value.variable_type, acvi.VariableType.BOOLEAN
            )
        set_visitor: VariableValueVisitor = VariableValueVisitor(self._element_id, self._client)
        value.value.accept(set_visitor)


class BooleanArrayDatapin(BaseDatapin, mc_api.IBooleanArrayDatapin):
    """Represents a boolean array datapin."""

    @interpret_rpc_error(WRAP_TARGET_NOT_FOUND)
    @overrides
    def get_metadata(self) -> acvi.BooleanArrayMetadata:
        response = self._client.BooleanVariableGetMetadata(self._element_id)
        return convert_grpc_boolean_array_metadata(response)

    @interpret_rpc_error(WRAP_TARGET_NOT_FOUND)
    @overrides
    def set_metadata(self, new_metadata: acvi.CommonVariableMetadata) -> None:
        if not isinstance(new_metadata, acvi.BooleanArrayMetadata):
            raise TypeError(
                f"The provided metadata object is not the correct type."
                f"Expected {acvi.BooleanArrayMetadata} "
                f"but received {new_metadata.__class__}"
            )
        request = SetBooleanVariableMetadataRequest(target=self._element_id)
        fill_boolean_metadata_message(new_metadata, request.new_metadata)
        self._client.BooleanVariableSetMetadata(request)

    @interpret_rpc_error({**WRAP_TARGET_NOT_FOUND, **WRAP_OUT_OF_BOUNDS})
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
        super(BooleanArrayDatapin, self).__init__(element_id=element_id, channel=channel)
