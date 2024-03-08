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
"""Contains classes for representing variables that exist in ModelCenter with
unsupported state types."""
from typing import TYPE_CHECKING

import ansys.tools.variableinterop as atvi
from overrides import overrides

from .base_datapin import BaseDatapin

if TYPE_CHECKING:
    from .engine import Engine
from ansys.api.modelcenter.v0.element_messages_pb2 import ElementId


class DatapinWithUnsupportedTypeException(BaseException):
    """Raised when attempting to interact with a datapin of an unsupported
    type."""

    def __init__(self):
        """Initialize an instance."""
        super(DatapinWithUnsupportedTypeException, self).__init__(
            "The PyModelCenter API does not currently support this interaction on datapins of "
            "this type."
        )


class UnsupportedTypeDatapin(BaseDatapin):
    """Represents a datapin with an unsupported datatype.

    Generally speaking, it is possible to perform interactions that
    don't require retrieving or otherwise interacting with the datapin's
    state or metadata. Attempts to get or set the state or metadata
    raise a ``DatapinWithUnsupportedTypeException``.
    """

    def __init__(self, element_id: ElementId, engine: "Engine"):
        """Initialize an instance."""
        super(BaseDatapin, self).__init__(element_id=element_id, engine=engine)

    @overrides
    def set_metadata(self, new_metadata: atvi.CommonVariableMetadata) -> None:
        raise DatapinWithUnsupportedTypeException()

    @overrides
    def set_state(self, state: atvi.VariableState) -> None:
        raise DatapinWithUnsupportedTypeException()

    @overrides
    def get_metadata(self) -> atvi.CommonVariableMetadata:
        raise DatapinWithUnsupportedTypeException()
