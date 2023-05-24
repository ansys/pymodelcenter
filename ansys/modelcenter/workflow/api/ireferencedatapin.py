"""Contains definitions for scalar reference datapins."""
from abc import ABC, abstractmethod

import ansys.tools.variableinterop as atvi
from overrides import overrides

from .idatapin import IDatapin


class IReferenceDatapin(IDatapin, ABC):
    """Represents a reference datapin on the workflow."""

    @overrides
    @abstractmethod
    def get_metadata(self) -> atvi.CommonVariableMetadata:  # TODO: reference metadata
        ...  # pragma: no cover

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

    @property
    @abstractmethod
    def is_direct(self) -> bool:
        """
        The directness of the equation.

        A reference equation is considered direct if it refers to only a single variable.

        Returns
        -------
        True if the reference is direct, False otherwise.
        """
        ...
