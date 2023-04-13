"""Contains definition for RealVariable and RealArrayVariable."""
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
from .proto.variable_value_messages_pb2 import SetDoubleVariableMetadataRequest
from .var_metadata_convert import (
    convert_grpc_real_array_metadata,
    convert_grpc_real_metadata,
    fill_real_metadata_message,
)
from .variable import BaseVariable


class RealVariable(BaseVariable, mc_api.IRealVariable):
    """Represents a gRPC double / real variable on the workflow."""

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
        super(RealVariable, self).__init__(element_id=element_id, channel=channel)

    @interpret_rpc_error(WRAP_TARGET_NOT_FOUND)
    @overrides
    def get_metadata(self) -> acvi.RealMetadata:
        response = self._client.DoubleVariableGetMetadata(self._element_id)
        return convert_grpc_real_metadata(response)

    @interpret_rpc_error(WRAP_TARGET_NOT_FOUND)
    @overrides
    def set_metadata(self, new_metadata: acvi.CommonVariableMetadata) -> None:
        if not isinstance(new_metadata, acvi.RealMetadata):
            raise TypeError()  # TODO: be more informative in this error message
        request = SetDoubleVariableMetadataRequest(target=self._element_id)
        fill_real_metadata_message(new_metadata, request.new_metadata)
        self._client.DoubleVariableSetMetadata(request)

    @interpret_rpc_error({**WRAP_TARGET_NOT_FOUND, **WRAP_OUT_OF_BOUNDS})
    @overrides
    def set_value(self, value: acvi.VariableState) -> None:
        self._do_set_value(value.value)

    @acvi.implicit_coerce
    def _do_set_value(self, value: acvi.RealValue) -> None:
        value.accept(VariableValueVisitor(self._element_id, self._client))


class RealArrayVariable(BaseVariable, mc_api.IRealArrayVariable):
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
        super(RealArrayVariable, self).__init__(element_id=element_id, channel=channel)

    @interpret_rpc_error(WRAP_TARGET_NOT_FOUND)
    @overrides
    def get_metadata(self) -> acvi.RealArrayMetadata:
        response = self._client.DoubleVariableGetMetadata(self._element_id)
        return convert_grpc_real_array_metadata(response)

    @interpret_rpc_error(WRAP_TARGET_NOT_FOUND)
    @overrides
    def set_metadata(self, new_metadata: acvi.CommonVariableMetadata) -> None:
        if not isinstance(new_metadata, acvi.RealArrayMetadata):
            raise TypeError()  # TODO: be more informative in this error message
        request = SetDoubleVariableMetadataRequest(target=self._element_id)
        fill_real_metadata_message(new_metadata, request.new_metadata)
        self._client.DoubleVariableSetMetadata(request)

    @interpret_rpc_error({**WRAP_TARGET_NOT_FOUND, **WRAP_OUT_OF_BOUNDS})
    @overrides
    def set_value(self, value: acvi.VariableState) -> None:
        self._do_set_value(value.value)

    @acvi.implicit_coerce
    def _do_set_value(self, value: acvi.RealArrayValue) -> None:
        value.accept(VariableValueVisitor(self._element_id, self._client))
