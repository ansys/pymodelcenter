# Copyright (C) 2022 - 2026 ANSYS, Inc. and/or its affiliates.
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
"""Defines the integer datapin classes.

These classes include ``IntegerDatapin`` and ``IntegerArray``.
"""

from typing import TYPE_CHECKING

import ansys.tools.variableinterop as atvi
from overrides import overrides

import ansys.modelcenter.workflow.api as mc_api

from ._visitors.variable_value_visitor import VariableValueVisitor
from .base_datapin import BaseDatapin

if TYPE_CHECKING:
    from .engine import Engine

from ansys.api.modelcenter.v0.element_messages_pb2 import ElementId
from ansys.api.modelcenter.v0.variable_value_messages_pb2 import SetIntegerVariableMetadataRequest

from .grpc_error_interpretation import (
    WRAP_OUT_OF_BOUNDS,
    WRAP_TARGET_NOT_FOUND,
    interpret_rpc_error,
)
from .var_metadata_convert import (
    convert_grpc_integer_array_metadata,
    convert_grpc_integer_metadata,
    fill_integer_metadata_message,
)


class IntegerDatapin(BaseDatapin, mc_api.IIntegerDatapin):
    """Represents an integer datapin.

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
        engine : Engine
            Engine to use to create the datapin.
        """
        super(IntegerDatapin, self).__init__(element_id=element_id, engine=engine)

    @overrides
    def __eq__(self, other):
        return isinstance(other, IntegerDatapin) and self.element_id == other.element_id

    @interpret_rpc_error(WRAP_TARGET_NOT_FOUND)
    @overrides
    def get_metadata(self) -> atvi.IntegerMetadata:
        response = self._client.IntegerVariableGetMetadata(self._element_id)
        return convert_grpc_integer_metadata(response)

    @interpret_rpc_error(WRAP_TARGET_NOT_FOUND)
    @overrides
    def set_metadata(self, new_metadata: atvi.CommonVariableMetadata) -> None:
        if not isinstance(new_metadata, atvi.IntegerMetadata):
            raise TypeError(
                f"The provided metadata object is not the correct type."
                f"Expected {atvi.IntegerMetadata}. "
                f"but received {new_metadata.__class__}."
            )
        request = SetIntegerVariableMetadataRequest(target=self._element_id)
        fill_integer_metadata_message(new_metadata, request.new_metadata)
        self._client.IntegerVariableSetMetadata(request)

    @interpret_rpc_error({**WRAP_TARGET_NOT_FOUND, **WRAP_OUT_OF_BOUNDS})
    @overrides
    def set_state(self, state: atvi.VariableState) -> None:
        self._do_set_value(state.value)

    @atvi.implicit_coerce
    def _do_set_value(self, value: atvi.IntegerValue) -> None:
        value.accept(VariableValueVisitor(self._element_id, self._client, self._engine.is_local))


class IntegerArrayDatapin(BaseDatapin, mc_api.IIntegerArrayDatapin):
    """Represents an integer array datapin.

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
        engine : Engine
            Engine to use to create the datapin.
        """
        super(IntegerArrayDatapin, self).__init__(element_id=element_id, engine=engine)

    @overrides
    def __eq__(self, other):
        return isinstance(other, IntegerArrayDatapin) and self.element_id == other.element_id

    @overrides
    def get_metadata(self) -> atvi.IntegerArrayMetadata:
        response = self._client.IntegerVariableGetMetadata(self._element_id)
        return convert_grpc_integer_array_metadata(response)

    @overrides
    def set_metadata(self, new_metadata: atvi.CommonVariableMetadata) -> None:
        if not isinstance(new_metadata, atvi.IntegerArrayMetadata):
            raise TypeError(
                f"The provided metadata object is not the correct type."
                f"Expected {atvi.IntegerArrayMetadata}, "
                f"but received {new_metadata.__class__}."
            )
        request = SetIntegerVariableMetadataRequest(target=self._element_id)
        fill_integer_metadata_message(new_metadata, request.new_metadata)
        self._client.IntegerVariableSetMetadata(request)

    @overrides
    def set_state(self, state: atvi.VariableState) -> None:
        self._do_set_value(state.value)

    @atvi.implicit_coerce
    def _do_set_value(self, value: atvi.IntegerArrayValue) -> None:
        value.accept(VariableValueVisitor(self._element_id, self._client, self._engine.is_local))
