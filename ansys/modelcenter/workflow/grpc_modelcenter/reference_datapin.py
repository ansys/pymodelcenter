"""Contains definition for ReferenceDatapin and ReferenceArrayDatapin."""
from typing import TYPE_CHECKING

import ansys.tools.variableinterop as atvi
from overrides import overrides

import ansys.modelcenter.workflow.api as mc_api

from .base_datapin import BaseDatapin

if TYPE_CHECKING:
    from .engine import Engine
from .grpc_error_interpretation import (
    WRAP_OUT_OF_BOUNDS,
    WRAP_TARGET_NOT_FOUND,
    interpret_rpc_error,
)
from .proto.element_messages_pb2 import ElementId


class ReferenceDatapin(BaseDatapin, mc_api.IReferenceDatapin):
    """
    Represents a reference datapin.

    .. note::
        This class should not be directly instantiated by clients. Get a Workflow object from
        an instantiated Engine, and use it to get a valid instance of this object.
    """

    def __init__(self, element_id: ElementId, engine: "Engine"):
        """
        Initialize a new instance.

        Parameters
        ----------
        element_id: ElementId
            The id of the variable.
        engine: Engine
            The Engine that created this datapin.
        """
        super(ReferenceDatapin, self).__init__(element_id=element_id, engine=engine)

    @overrides
    def __eq__(self, other):
        return isinstance(other, ReferenceDatapin) and self.element_id == other.element_id

    @interpret_rpc_error(WRAP_TARGET_NOT_FOUND)
    @overrides
    def get_metadata(self) -> atvi.CommonVariableMetadata:  # TODO: reference metadata
        # response = self._client.BooleanVariableGetMetadata(self._element_id)
        # return convert_grpc_boolean_metadata(response)
        pass

    @interpret_rpc_error(WRAP_TARGET_NOT_FOUND)
    @overrides
    def set_metadata(self, new_metadata: atvi.CommonVariableMetadata) -> None:
        # if not isinstance(new_metadata, atvi.BooleanMetadata):
        #     raise TypeError(
        #         f"The provided metadata object is not the correct type."
        #         f"Expected {atvi.BooleanMetadata} "
        #         f"but received {new_metadata.__class__}"
        #     )
        # request = SetBooleanVariableMetadataRequest(target=self._element_id)
        # fill_boolean_metadata_message(new_metadata, request.new_metadata)
        # self._client.BooleanVariableSetMetadata(request)
        pass

    @interpret_rpc_error({**WRAP_TARGET_NOT_FOUND, **WRAP_OUT_OF_BOUNDS})
    @overrides
    def set_value(self, value: atvi.VariableState) -> None:
        # if not isinstance(value.value, atvi.BooleanValue):
        #     raise atvi.IncompatibleTypesException(
        #         value.value.variable_type, atvi.VariableType.BOOLEAN
        #     )
        # set_visitor: VariableValueVisitor = VariableValueVisitor(self._element_id, self._client)
        # value.value.accept(set_visitor)
        pass


class ReferenceArrayDatapin(BaseDatapin, mc_api.IReferenceArrayDatapin):
    """
    Represents a reference array datapin.

    .. note::
        This class should not be directly instantiated by clients. Get a Workflow object from
        an instantiated Engine, and use it to get a valid instance of this object.
    """

    @overrides
    def __init__(self, element_id: ElementId, engine: "Engine"):
        """
        Initialize a new instance.

        Parameters
        ----------
        element_id: ElementId
            The id of the variable.
        engine: Engine
            The Engine that created this datapin.
        """
        super(ReferenceArrayDatapin, self).__init__(element_id=element_id, engine=engine)

    @overrides
    def __eq__(self, other):
        return isinstance(other, ReferenceArrayDatapin) and self.element_id == other.element_id

    @interpret_rpc_error(WRAP_TARGET_NOT_FOUND)
    @overrides
    def get_metadata(self) -> atvi.CommonVariableMetadata:  # TODO: reference metadata
        # response = self._client.BooleanVariableGetMetadata(self._element_id)
        # return convert_grpc_boolean_array_metadata(response)
        pass

    @interpret_rpc_error(WRAP_TARGET_NOT_FOUND)
    @overrides
    def set_metadata(self, new_metadata: atvi.CommonVariableMetadata) -> None:
        # if not isinstance(new_metadata, atvi.BooleanArrayMetadata):
        #     raise TypeError(
        #         f"The provided metadata object is not the correct type."
        #         f"Expected {atvi.BooleanArrayMetadata} "
        #         f"but received {new_metadata.__class__}"
        #     )
        # request = SetBooleanVariableMetadataRequest(target=self._element_id)
        # fill_boolean_metadata_message(new_metadata, request.new_metadata)
        # self._client.BooleanVariableSetMetadata(request)
        pass

    @interpret_rpc_error({**WRAP_TARGET_NOT_FOUND, **WRAP_OUT_OF_BOUNDS})
    @overrides
    def set_value(self, value: atvi.VariableState) -> None:
        # if not isinstance(value.value, atvi.BooleanArrayValue):
        #     raise atvi.IncompatibleTypesException(
        #         value.value.variable_type, atvi.VariableType.BOOLEAN_ARRAY
        #     )
        # set_visitor: VariableValueVisitor = VariableValueVisitor(self._element_id, self._client)
        # value.value.accept(set_visitor)
        pass
