# Copyright (C) 2022 - 2024 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
"""Contains the definitions for the ``FileDatapin`` and ``FileArrayDatapin``
classes."""
from typing import TYPE_CHECKING

import ansys.tools.variableinterop as atvi
from overrides import overrides

import ansys.modelcenter.workflow.api as mc_api

from ._visitors.variable_value_visitor import VariableValueVisitor
from .base_datapin import BaseDatapin

if TYPE_CHECKING:
    from .engine import Engine

from ansys.api.modelcenter.v0.element_messages_pb2 import ElementId
from ansys.api.modelcenter.v0.variable_value_messages_pb2 import SetFileVariableMetadataRequest

from .grpc_error_interpretation import (
    WRAP_OUT_OF_BOUNDS,
    WRAP_TARGET_NOT_FOUND,
    interpret_rpc_error,
)
from .var_metadata_convert import (
    convert_grpc_file_array_metadata,
    convert_grpc_file_metadata,
    fill_file_metadata_message,
)


class FileDatapin(BaseDatapin, mc_api.IFileDatapin):
    """Represents a file datapin.

    .. note::
        This class should not be directly instantiated by clients. Get a ``Workflow`` object from
        an instantiated ``Engine`` instance and use it to get a valid instance of this object.
    """

    def __init__(self, element_id: ElementId, engine: "Engine"):
        """Initialize an instance.

        Parameters
        ----------
        element_id : ElementId
            ID of the datapin.
        engine: Engine
            Engine to use to create the datapin.
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
    def set_state(self, state: atvi.VariableState) -> None:
        if not isinstance(state.value, atvi.FileValue):
            raise atvi.IncompatibleTypesException(state.value.variable_type, atvi.VariableType.FILE)
        set_visitor: VariableValueVisitor = VariableValueVisitor(
            self._element_id, self._client, self._engine.is_local
        )
        state.value.accept(set_visitor)


class FileArrayDatapin(BaseDatapin, mc_api.IFileArrayDatapin):
    """Represents a file array datapin.

    .. note::
        This class should not be directly instantiated by clients. Get a ``Workflow`` object from
        an instantiated ``Engine`` instance and use it to get a valid instance of this object.
    """

    @overrides
    def __init__(self, element_id: ElementId, engine: "Engine"):
        """Initialize an instance.

        Parameters
        ----------
        element_id : ElementId
            ID of the datapin.
        engine : Engine
            Engine to use to create the datapin.
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
                f"Expected {atvi.FileArrayMetadata}, "
                f"but received {new_metadata.__class__}."
            )
        request = SetFileVariableMetadataRequest(target=self._element_id)
        fill_file_metadata_message(new_metadata, request.new_metadata)
        self._client.FileVariableSetMetadata(request)

    @interpret_rpc_error({**WRAP_TARGET_NOT_FOUND, **WRAP_OUT_OF_BOUNDS})
    @overrides
    def set_state(self, state: atvi.VariableState) -> None:
        if not isinstance(state.value, atvi.FileArrayValue):
            raise atvi.IncompatibleTypesException(
                state.value.variable_type, atvi.VariableType.FILE_ARRAY
            )
        set_visitor: VariableValueVisitor = VariableValueVisitor(
            self._element_id, self._client, self._engine.is_local
        )
        state.value.accept(set_visitor)
