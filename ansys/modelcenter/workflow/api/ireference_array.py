"""Definition of array reference."""
from abc import ABC, abstractmethod
from typing import Sequence

from .iarray import IArray
from .irefprop import IReferenceArrayProperty, IReferencePropertyOwner
from .ivariable import IVariable


# TODO/REDUCE: Consider dropping this for Phase II.
class IReferenceArray(IArray, IReferencePropertyOwner[IReferenceArrayProperty], ABC):
    """Represents a reference array variable in a ModelCenter workflow."""

    # TODO: consider creating a type to implement indexing, iteration semantics for references?

    @abstractmethod
    def get_reference(self, index: int) -> str:
        """Get the reference equation for this variable at the specified index."""
        raise NotImplementedError()

    @abstractmethod
    def set_reference(self, index: int, new_reference: str):
        """Set the reference equation for this variable at the specified index."""

    @abstractmethod
    def referenced_variables(self, index: int) -> Sequence[IVariable]:
        """
        Get the referenced variables at the specified index.

        Parameters
        ----------
        index
            Index of the array element (0-based index).

        Returns
        -------
        object
            The references variables of the element.
        """
        raise NotImplementedError()
