"""Contains definitions for reference variables."""
from abc import ABC, abstractmethod
from typing import Sequence

from .irefprop import IReferenceProperty, IReferencePropertyOwner
from .ivariable import IVariable


# TODO/REDUCE: Consider dropping this for Phase II.
# TODO: Need to understand use requirements for reference variables / arrays in general.
class IReferenceVariable(IVariable, IReferencePropertyOwner[IReferenceProperty], ABC):
    """Represents a reference variable in a ModelCenter workflow."""

    @property
    @abstractmethod
    def reference(self) -> str:
        """Get the reference equation for this variable."""
        raise NotImplementedError()

    @reference.setter
    @abstractmethod
    def reference(self, value: str) -> None:
        """Set the reference for this variable."""
        raise NotImplementedError()

    @property
    @abstractmethod
    def referenced_variables(self) -> Sequence[IVariable]:
        """Get the variables referenced by this variable."""
        raise NotImplementedError()
