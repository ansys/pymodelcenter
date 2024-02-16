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
"""Contains definitions for a base class for reference datapins."""
from abc import ABC, abstractmethod
from typing import Optional

import ansys.tools.variableinterop as atvi


class IDatapinReferenceBase(ABC):
    """Defines methods common to an individual reference to another datapin.

    This could be a single reference datapin or an element in a
    reference array datapin, etc.
    """

    @property
    @abstractmethod
    def equation(self) -> str:
        """Reference equation describing what values this datapin references.

        Returns
        -------
        str
            The reference equation.
        """
        ...

    @equation.setter
    @abstractmethod
    def equation(self, equation: str):
        """Setter for the reference equation that describes what this datapin
        references.

        Parameters
        ----------
        equation : str
            Reference equation
        """
        ...

    @property
    @abstractmethod
    def is_direct(self) -> bool:
        """Check whether this datapin is a direct reference.

        Direct reference datapins refer to one specific other datapin exactly; their equations
        are just the name of one other datapin. Only direct-reference datapins that refer
        to a datapin that can be set directly can use set_state to set the referenced datapin.

        Return
        ------
        bool
            ``True`` if the datapin is a direct reference.
        """
        ...

    @abstractmethod
    def get_state(self, hid: Optional[str] = None) -> atvi.VariableState:
        """Get the state of the reference equation."""

    @abstractmethod
    def set_state(self, state: atvi.VariableState) -> None:
        """Set the state of the referenced datapin.

        This method only works if this is a direct reference; that is,
        if the equation is just the name of a single other datapin with
        no modification. If this is not a direct reference, a ValueError
        is raised. A ValueError will additionally be raised if the
        referenced datapin would not be allowed to be set directly in
        the first place (for example, if it is an output or linked
        input).
        """
