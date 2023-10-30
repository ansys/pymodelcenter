"""Contains definitions for a base class for reference datapins."""
from abc import ABC, abstractmethod
from typing import Optional

import ansys.tools.variableinterop as atvi


class IDatapinReferenceBase(ABC):
    """
    Defines methods common to an individual reference to another datapin.

    This could be a single reference datapin or an element in a reference array datapin, etc.
    """

    @property
    @abstractmethod
    def equation(self) -> str:
        """
        Reference equation describing what values this datapin references.

        Returns
        -------
        str
            The reference equation.
        """
        ...

    @equation.setter
    @abstractmethod
    def equation(self, equation: str):
        """
        Setter for the reference equation that describes what this datapin references.

        Parameters
        ----------
        equation : str
            Reference equation
        """
        ...

    @property
    @abstractmethod
    def is_direct(self) -> bool:
        """
        Check whether this datapin is a direct reference.

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
        """
        Set the state of the referenced datapin.

        This method only works if this is a direct reference; that is,
        if the equation is just the name of a single other datapin with no modification.
        If this is not a direct reference, a ValueError is raised.
        A ValueError will additionally be raised if the referenced datapin would not be allowed
        to be set directly in the first place (for example, if it is an output or linked input).
        """
