"""Contains definition for FileDatapin and FileArrayDatapin."""
from typing import TYPE_CHECKING

import ansys.tools.variableinterop as atvi
from overrides import overrides

import ansys.modelcenter.workflow.api as mc_api

from ._visitors.variable_value_visitor import VariableValueVisitor
from .base_datapin import BaseDatapin

if TYPE_CHECKING:
    from .engine import Engine

from .grpc_error_interpretation import (
    WRAP_OUT_OF_BOUNDS,
    WRAP_TARGET_NOT_FOUND,
    interpret_rpc_error,
)
from .proto.element_messages_pb2 import ElementId
from .proto.variable_value_messages_pb2 import SetFileVariableMetadataRequest
from .var_metadata_convert import (
    convert_grpc_file_array_metadata,
    convert_grpc_file_metadata,
    fill_file_metadata_message,
)


class FileDatapin(BaseDatapin, mc_api.IFileDatapin):
    """
    Represents a file datapin.

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
        super(FileDatapin, self).__init__(element_id=element_id, engine=engine)

    @overrides
    def __eq__(self, other):
        return isinstance(other, FileDatapin) and self.element_id == other.element_id

    @interpret_rpc_error(WRAP_TARGET_NOT_FOUND)
    @overrides
    def get_metadata(self) -> atvi.FileMetadata:
        response = self._client.FileVariableGetMetadata(self._element_id)
        return convert_grpc_file_metadata(response)

    @interpret_rpc_error(WRAP_TARGET_NOT_FOUND)
    @overrides
    def set_metadata(self, new_metadata: atvi.CommonVariableMetadata) -> None:
        if not isinstance(new_metadata, atvi.FileMetadata):
            raise TypeError(
                f"The provided metadata object is not the correct type."
                f"Expected {atvi.FileMetadata} "
                f"but received {new_metadata.__class__}"
            )
        request = SetFileVariableMetadataRequest(target=self._element_id)
        fill_file_metadata_message(new_metadata, request.new_metadata)
        self._client.FileVariableSetMetadata(request)

    @interpret_rpc_error({**WRAP_TARGET_NOT_FOUND, **WRAP_OUT_OF_BOUNDS})
    @overrides
    def set_value(self, value: atvi.VariableState) -> None:
        if not isinstance(value.value, atvi.FileValue):
            raise atvi.IncompatibleTypesException(value.value.variable_type, atvi.VariableType.FILE)
        set_visitor: VariableValueVisitor = VariableValueVisitor(self._element_id, self._client)
        value.value.accept(set_visitor)


class FileArrayDatapin(BaseDatapin, mc_api.IFileArrayDatapin):
    """
    Represents a file array datapin.

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
        super(FileArrayDatapin, self).__init__(element_id=element_id, engine=engine)

    @overrides
    def __eq__(self, other):
        return isinstance(other, FileArrayDatapin) and self.element_id == other.element_id

    @interpret_rpc_error(WRAP_TARGET_NOT_FOUND)
    @overrides
    def get_metadata(self) -> atvi.FileArrayMetadata:
        response = self._client.FileVariableGetMetadata(self._element_id)
        return convert_grpc_file_array_metadata(response)

    @interpret_rpc_error(WRAP_TARGET_NOT_FOUND)
    @overrides
    def set_metadata(self, new_metadata: atvi.CommonVariableMetadata) -> None:
        if not isinstance(new_metadata, atvi.FileArrayMetadata):
            raise TypeError(
                f"The provided metadata object is not the correct type."
                f"Expected {atvi.FileArrayMetadata} "
                f"but received {new_metadata.__class__}"
            )
        request = SetFileVariableMetadataRequest(target=self._element_id)
        fill_file_metadata_message(new_metadata, request.new_metadata)
        self._client.FileVariableSetMetadata(request)

    @interpret_rpc_error({**WRAP_TARGET_NOT_FOUND, **WRAP_OUT_OF_BOUNDS})
    @overrides
    def set_value(self, value: atvi.VariableState) -> None:
        if not isinstance(value.value, atvi.FileArrayValue):
            raise atvi.IncompatibleTypesException(
                value.value.variable_type, atvi.VariableType.FILE_ARRAY
            )
        set_visitor: VariableValueVisitor = VariableValueVisitor(self._element_id, self._client)
        value.value.accept(set_visitor)
