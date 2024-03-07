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
"""Contains definitions for reference properties and datapins which own
them."""

from abc import ABC, abstractmethod
from typing import Mapping

import ansys.tools.variableinterop as atvi


class IReferencePropertyBase(ABC):
    """Defines common methods for IReferenceProperty and
    IReferenceArrayProperty."""

    @abstractmethod
    def get_value_type(self) -> atvi.VariableType:
        """Get the value type of the property.

        Returns
        -------
        atvi.VariableType
            Type of the property.
        """
        pass

    @abstractmethod
    def get_metadata(self) -> atvi.CommonVariableMetadata:
        """Get the metadata for this property.

        Returns
        -------
        atvi.CommonVariableMetadata
            Value of the metadata.
        """
        pass

    @abstractmethod
    def set_metadata(self, new_value: atvi.CommonVariableMetadata) -> None:
        """Set the metadata for this property.

        Note that this method only has an effect for reference properties where the datatype
        is numeric, in which case the display format passed in is set.

        Parameters
        ----------
        new_value : atvi.CommonVariableMetadata
            New value for the metadata.
        """
        pass

    @property
    @abstractmethod
    def is_input(self) -> bool:
        """Check whether this property is an input or output.

        Returns
        -------
        bool
            ``True`` if this property is an input, ``False`` otherwise.
        """
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """Get the name of this property.

        Returns
        -------
        str
            Name of the property.
        """


class IReferenceProperty(IReferencePropertyBase, ABC):
    """Defines methods for reference properties."""

    @abstractmethod
    def get_state(self) -> atvi.VariableState:
        """Get the state of the property.

        The returned state may be invalid. The engine will not attempt
        to run the workflow to validate this property.

        Returns
        -------
        atvi.VariableState
            State of the property.
        """
        pass

    @abstractmethod
    def set_state(self, new_state: atvi.VariableState) -> None:
        """Set the state of the property.

        Parameters
        ----------
        new_state : atvi.VariableState
            New state of the property.
        """
        pass


class IReferenceArrayProperty(IReferencePropertyBase, ABC):
    """Defines methods for reference array properties."""

    @abstractmethod
    def set_value_at(self, index: int, new_state: atvi.VariableState) -> None:
        """Set the state of a particular index.

        Parameters
        ----------
        index : int
            Index at which to set the state.
        new_state: atvi.VariableState
            New state of the property.
        """

    @abstractmethod
    def get_state_at(self, index: int) -> atvi.VariableState:
        """Get the state of a reference property at a particular index.

        Parameters
        ----------
        index : int
            Index at which to get the state.

        Returns
        -------
        atvi.VariableState
            State of the property at the given index.
        """


class IReferencePropertyManager(ABC):
    """Defines utility methods for getting reference properties from reference
    datapins."""

    @abstractmethod
    def get_reference_properties(self) -> Mapping[str, IReferencePropertyBase]:
        """Get the reference properties on this reference datapin.

        Returns
        -------
        Mapping[str, IReferencePropertyBase]
            Mapping of names to reference properties.
        """
