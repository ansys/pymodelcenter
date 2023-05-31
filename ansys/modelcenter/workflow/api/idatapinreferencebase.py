"""Contains definitions for a base class for reference datapins."""
from abc import ABC, abstractmethod

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
        The reference equation describing what values this variable references.

        Returns
        -------
        The reference equation.
        """
        ...

    @equation.setter
    @abstractmethod
    def equation(self, equation: str):
        """
        Setter for the reference equation that describes what this variable references.

        Parameters
        ----------
        equation: str
            The reference equation
        """
        ...

    @property
    @abstractmethod
    def is_direct(self) -> bool:
        """
        Check whether this datapin is a direct reference.

        Direct reference datapins refer to one specific other datapin exactly; their equations
        are just the name of one other datapin. Only direct-reference datapins that refer
        to a datapin that can be set directly can use set_value to set the referenced datapin.

        Return
        ------
        True if the datapin is a direct reference.
        """
        ...

    @abstractmethod
    def get_value(self) -> atvi.VariableState:
        """Get the value of the reference equation."""

    @abstractmethod
    def set_value(self, value: atvi.VariableState) -> None:
        """
        Set the value of the referenced datapin.

        This method only works if this is a direct reference; that is,
        if the equation is just the name of a single other variable with no modification.
        If this is not a direct reference, a ValueError is raised.
        A ValueError will additionally be raised if the referenced datapin would not be allowed
        to be set directly in the first place (for example, if it is an output or linked input).
        """
