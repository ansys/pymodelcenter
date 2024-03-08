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
"""Defines classes and functions for working with links between variables in
the workflow."""

from abc import ABC, abstractmethod


class IDatapinLink(ABC):
    """Represents a link between two datapins in the workflow."""

    @abstractmethod
    def break_link(self) -> None:
        """Break the link.

        Breaking the link removes the dependencies between the left-hand
        and right-hand side of the link. The object becomes invalid and
        cannot be used after calling this method.
        """

    @abstractmethod
    def suspend(self) -> None:
        """Suspend the link.

        Suspending the link causes the engine to behave as if it is not
        present. This method is idempotent. It is safe to call this
        method multiple times, even if the link is already suspended.
        """

    @abstractmethod
    def resume(self) -> None:
        """Resume the link if it is suspended.

        This method is idempotent. it is safe to call this method
        multiple times, even if the link is already suspended.
        """

    @abstractmethod
    def is_suspended(self) -> bool:
        """Check whether the link is suspended.

        Returns
        -------
        bool
            ``True`` if the link is suspended, and ``False`` otherwise.
        """

    @property
    @abstractmethod
    def lhs(self) -> str:
        """Left-hand side of the link.

        The left-hand side receives a value from the right-hand side
        (analogous to a variable assignment in most languages). This is
        always a simple datapin name, except in cases where the link
        target is a single array index, in which case it is the name of
        the datapin plus an array index.
        """

    @property
    @abstractmethod
    def rhs(self) -> str:
        """Right-hand side (source) of the link equation.

        This is a simple equation containing the names of the other
        datapins that this link depends on.
        """

    @rhs.setter
    @abstractmethod
    def rhs(self, new_rhs: str) -> None:
        """Set the right-hand side (source) of the link equation."""
