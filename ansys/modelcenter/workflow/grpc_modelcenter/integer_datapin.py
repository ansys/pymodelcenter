"""Contains definition for IntegerDatapin and IntegerArray."""
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
from .proto.variable_value_messages_pb2 import SetIntegerVariableMetadataRequest
from .var_metadata_convert import (
    convert_grpc_integer_array_metadata,
    convert_grpc_integer_metadata,
    fill_integer_metadata_message,
)


class IntegerDatapin(BaseDatapin, mc_api.IIntegerDatapin):
    """Represents an integer datapin."""

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
        super(IntegerDatapin, self).__init__(element_id=element_id, channel=channel)

    @overrides
    def __eq__(self, other):
        return isinstance(other, IntegerDatapin) and self.element_id == other.element_id

    @interpret_rpc_error(WRAP_TARGET_NOT_FOUND)
    @overrides
    def get_metadata(self) -> acvi.IntegerMetadata:
        response = self._client.IntegerVariableGetMetadata(self._element_id)
        return convert_grpc_integer_metadata(response)

    @interpret_rpc_error(WRAP_TARGET_NOT_FOUND)
    @overrides
    def set_metadata(self, new_metadata: acvi.CommonVariableMetadata) -> None:
        if not isinstance(new_metadata, acvi.IntegerMetadata):
            raise TypeError(
                f"The provided metadata object is not the correct type."
                f"Expected {acvi.IntegerMetadata} "
                f"but received {new_metadata.__class__}"
            )
        request = SetIntegerVariableMetadataRequest(target=self._element_id)
        fill_integer_metadata_message(new_metadata, request.new_metadata)
        self._client.IntegerVariableSetMetadata(request)

    @interpret_rpc_error({**WRAP_TARGET_NOT_FOUND, **WRAP_OUT_OF_BOUNDS})
    @overrides
    def set_value(self, value: acvi.VariableState) -> None:
        self._do_set_value(value.value)

    @acvi.implicit_coerce
    def _do_set_value(self, value: acvi.IntegerValue) -> None:
        value.accept(VariableValueVisitor(self._element_id, self._client))


class IntegerArrayDatapin(BaseDatapin, mc_api.IIntegerArrayDatapin):
    """Represents an integer array datapin."""

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
        super(IntegerArrayDatapin, self).__init__(element_id=element_id, channel=channel)

    @overrides
    def __eq__(self, other):
        return isinstance(other, IntegerArrayDatapin) and self.element_id == other.element_id

    @overrides
    def get_metadata(self) -> acvi.RealArrayMetadata:
        response = self._client.IntegerVariableGetMetadata(self._element_id)
        return convert_grpc_integer_array_metadata(response)

    @overrides
    def set_metadata(self, new_metadata: acvi.CommonVariableMetadata) -> None:
        if not isinstance(new_metadata, acvi.IntegerArrayMetadata):
            raise TypeError(
                f"The provided metadata object is not the correct type."
                f"Expected {acvi.IntegerArrayMetadata} "
                f"but received {new_metadata.__class__}"
            )
        request = SetIntegerVariableMetadataRequest(target=self._element_id)
        fill_integer_metadata_message(new_metadata, request.new_metadata)
        self._client.IntegerVariableSetMetadata(request)

    @overrides
    def set_value(self, value: acvi.VariableState) -> None:
        self._do_set_value(value.value)

    @acvi.implicit_coerce
    def _do_set_value(self, value: acvi.IntegerArrayValue) -> None:
        value.accept(VariableValueVisitor(self._element_id, self._client))
