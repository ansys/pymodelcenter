"""Definitions of common array functionality."""
from abc import ABC, abstractmethod

from .ivariable import IVariable


class IArray(IVariable, ABC):
    """Base class for all array types."""

    @property
    @abstractmethod
    def auto_size(self) -> bool:
        """
        Whether the array is set to automatically size itself.

        If False and the array is the left-hand side of a link, the upstream
        array must be exactly the same size or an error ensues.
        If True, the array will resize itself when such link is validated.
        """

    @auto_size.setter
    @abstractmethod
    def auto_size(self, value: bool) -> None:
        """
        Setter for the auto_size property.

        Parameters
        ----------
        value: bool
            The new value.
        """
