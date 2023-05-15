"""Contains interface definitions for reference and reference array datapins."""
from abc import ABC, abstractmethod
from typing import Collection, Optional, Sequence, Union

import ansys.engineeringworkflow.api as aew_api
import ansys.tools.variableinterop as atvi
from overrides import overrides

from .idatapin import IDatapin


class IDatapinReferenceBase(ABC):
    """
    Defines methods common to an individual reference to another datapin.

    This could be a single reference datapin or an element in a reference array datapin, etc.
    """

    @abstractmethod
    def get_reference_equation(self) -> str:
        """Get the reference equation for this reference datapin."""

    @abstractmethod
    def set_reference_equation(self, new_equation: Union[str]) -> str:
        """Set the reference equation for this reference datapin."""

    @abstractmethod
    def get_referenced_variables(self) -> Collection[IDatapin]:
        """Get the datapin(s) that appear in this reference datapin's equation."""

    @abstractmethod
    def is_direct_reference(self) -> bool:
        """
        Check whether this datapin is a direct reference.

        Direct reference datapins refer to one specific other datapin exactly; their equations
        are just the name of one other datapin. Only direct-reference datapins that refer
        to a datapin that can be set directly can use set_value to set the referenced datapin.
        """

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


class IReferenceDatapin(aew_api.IDatapin, IDatapinReferenceBase, ABC):
    """
    Represents a reference datapin in the workflow.

    Reference datapins allow components to have configurable connections to other datapins
    without creating a full link relationship.
    """


class IReferenceArrayDatapin(aew_api.IDatapin, Sequence[IDatapinReferenceBase], ABC):
    """
    Represents a reference array datapin in the workflow.

    Reference array datapins are different to other array datapin types. Reference arrays are
    only allowed to be one-dimensional and their size cannot be changed by resetting their values.

    In particular, because reference arrays may refer to datapins of more than one type,
    getting their values is more complex than with other datapin types. Implementations of this
    interface will implement IDatapin.get_value and set_value in a manner that is
    intended mostly for convenience and feature parity with legacy ModelCenter APIs,
    but if you are attempting to work with reference arrays in particular,
    consider using get_reference_value and set_refererence_value to query and manipulate the values
    of individual referenced datapins.
    """

    @abstractmethod
    @overrides
    def get_value(self, hid: Optional[str] = None) -> atvi.VariableState:
        """
        Get the value of the reference equations in the array.

        The returned VariableState has a one-dimensional RealArrayValue. Each element in the array
        corresponds to the actual value for the corresponding reference equation if it is an
        equation for a RealValue, or NaN if it is not.
        """

    @abstractmethod
    @overrides
    def set_value(self, value: atvi.VariableState) -> None:
        """
        Set the value of referenced variables in the array.

        The supplied VariableState must be a valid and contain a one-dimensional RealArrayValue.
        Each element in the array corresponds to the desired value for the corresponding
        reference equation if it is a direct reference to a real-type datapin. Values for all
        other reference equations must be NaN.
        """
