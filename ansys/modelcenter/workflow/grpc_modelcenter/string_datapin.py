"""Contains definition for StringDatapin and StringArrayDatapin."""
from typing import TYPE_CHECKING

import ansys.modelcenter.workflow.api as mc_api
import ansys.tools.variableinterop as atvi
from overrides import overrides

from ._visitors.variable_value_visitor import VariableValueVisitor
from .base_datapin import BaseDatapin

if TYPE_CHECKING:
    from .engine import Engine

from ansys.api.modelcenter.v0.element_messages_pb2 import ElementId
from ansys.api.modelcenter.v0.variable_value_messages_pb2 import SetStringVariableMetadataRequest

from .grpc_error_interpretation import (
    WRAP_OUT_OF_BOUNDS,
    WRAP_TARGET_NOT_FOUND,
    interpret_rpc_error,
)
from .var_metadata_convert import (
    convert_grpc_string_array_metadata,
    convert_grpc_string_metadata,
    fill_string_metadata_message,
)


class StringDatapin(BaseDatapin, mc_api.IStringDatapin):
    """
    Represents a gRPC string datapin in the workflow.

    .. note::
        This class should not be directly instantiated by clients. Get a ``Workflow`` object from
        an instantiated ``Engine``, and use it to get a valid instance of this object.
    """

    def __init__(self, element_id: ElementId, engine: "Engine"):
        """
        Initialize a new instance.

        Parameters
        ----------
        element_id : ElementId
            ID of the datapin.
        engine: Engine
            ``Engine`` that created this datapin.
        """
        super(StringDatapin, self).__init__(element_id=element_id, engine=engine)

    @overrides
    def __eq__(self, other):
        return isinstance(other, StringDatapin) and self.element_id == other.element_id

    @interpret_rpc_error(WRAP_TARGET_NOT_FOUND)
    @overrides
    def get_metadata(self) -> atvi.StringMetadata:
        response = self._client.StringVariableGetMetadata(self._element_id)
        return convert_grpc_string_metadata(response)

    @interpret_rpc_error(WRAP_TARGET_NOT_FOUND)
    @overrides
    def set_metadata(self, new_metadata: atvi.CommonVariableMetadata) -> None:
        if not isinstance(new_metadata, atvi.StringMetadata):
            raise TypeError(
                f"The provided metadata object is not the correct type."
                f"Expected {atvi.StringArrayMetadata} "
                f"but received {new_metadata.__class__}"
            )
        request = SetStringVariableMetadataRequest(target=self._element_id)
        fill_string_metadata_message(new_metadata, request.new_metadata)
        self._client.StringVariableSetMetadata(request)

    @interpret_rpc_error({**WRAP_TARGET_NOT_FOUND, **WRAP_OUT_OF_BOUNDS})
    @overrides
    def set_state(self, state: atvi.VariableState) -> None:
        self._do_set_value(state.value)

    @atvi.implicit_coerce
    def _do_set_value(self, value: atvi.StringValue) -> None:
        value.accept(VariableValueVisitor(self._element_id, self._client, self._engine.is_local))


class StringArrayDatapin(BaseDatapin, mc_api.IStringArrayDatapin):
    """
    Represents a gRPC double / real array datapin on the workflow.

    .. note::
        This class should not be directly instantiated by clients. Get a ``Workflow`` object from
        an instantiated ``Engine``, and use it to get a valid instance of this object.
    """

    def __init__(self, element_id: ElementId, engine: "Engine"):
        """
        Initialize a new instance.

        Parameters
        ----------
        element_id : ElementId
            ID of the datapin.
        engine : Engine
            ``Engine`` that created this datapin.
        """
        super(StringArrayDatapin, self).__init__(element_id=element_id, engine=engine)

    @overrides
    def __eq__(self, other):
        return isinstance(other, StringArrayDatapin) and self.element_id == other.element_id

    @interpret_rpc_error(WRAP_TARGET_NOT_FOUND)
    @overrides
    def get_metadata(self) -> atvi.StringArrayMetadata:
        response = self._client.StringVariableGetMetadata(self._element_id)
        return convert_grpc_string_array_metadata(response)

    @interpret_rpc_error(WRAP_TARGET_NOT_FOUND)
    @overrides
    def set_metadata(self, new_metadata: atvi.CommonVariableMetadata) -> None:
        if not isinstance(new_metadata, atvi.StringArrayMetadata):
            raise TypeError(
                f"The provided metadata object is not the correct type."
                f"Expected {atvi.StringArrayMetadata} "
                f"but received {new_metadata.__class__}"
            )
        request = SetStringVariableMetadataRequest(target=self._element_id)
        fill_string_metadata_message(new_metadata, request.new_metadata)
        self._client.StringVariableSetMetadata(request)

    @interpret_rpc_error({**WRAP_TARGET_NOT_FOUND, **WRAP_OUT_OF_BOUNDS})
    @overrides
    def set_state(self, state: atvi.VariableState) -> None:
        self._do_set_value(state.value)

    @atvi.implicit_coerce
    def _do_set_value(self, value: atvi.StringArrayValue) -> None:
        value.accept(VariableValueVisitor(self._element_id, self._client, self._engine.is_local))
