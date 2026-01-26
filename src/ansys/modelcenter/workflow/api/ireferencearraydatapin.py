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
"""Defines the reference array datapin."""

from abc import ABC, abstractmethod
from typing import Mapping, Sequence

from overrides import overrides

from .idatapin import IDatapin
from .idatapinreferencebase import IDatapinReferenceBase
from .ireferenceproperty import IReferenceArrayProperty, IReferencePropertyManager


class IReferenceArrayDatapin(
    IDatapin, Sequence[IDatapinReferenceBase], IReferencePropertyManager, ABC
):
    """Represents a reference array datapin on the workflow.

    Reference array datapins are different than other array datapin types.
    Reference arrays are only allowed to be one-dimensional, and their
    size cannot be changed by resetting their values.

    In particular, because reference arrays may refer to datapins of
    more than one type, getting their values is more complex than with
    other datapin types. Implementations of this interface
    implement ``IDatapin.get_state()`` and ``set_state`` methods in a manner that
    is intended mostly for convenience and feature parity with legacy
    ModelCenter APIs, but if you are attempting to work with reference
    arrays in particular, consider using the ``get_reference_value()`` and
    ``set_refererence_value()`` methods to query and manipulate the values of
    individual referenced datapins.
    """

    @abstractmethod
    @overrides
    def get_reference_properties(self) -> Mapping[str, IReferenceArrayProperty]: ...

    @abstractmethod
    def set_length(self, new_size: int) -> None:
        """Resize the array.

        If smaller than the current size, elements at the end of the array are dropped.
        If larger than the current size, new empty elements are added to the end of the array.

        Parameters
        ----------
        new_size : int
            New size of the array.
        """
        ...
