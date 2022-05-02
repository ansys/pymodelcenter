"""Definition of Format."""
from abc import ABC, abstractmethod

from numpy import float64, int64


class Format(ABC):
    """
    Interface that defines operations for formatting values in various
    string formats (percentage, currency, etc.).
    """

    @abstractmethod
    def set_format(self, fmt: str) -> None:
        """
        Set the format string to use in this object.

        You may pass in the empty string to mean "General".
        TODO: Documentation on valid formats, MCD docs not great.

        Parameters
        ----------
        fmt: str
            The format string to use.
        """
        raise NotImplementedError

    @abstractmethod
    def string_to_integer(self, string: str) -> int64:
        """
        Convert a formatted string to an integer.

        The string must be in the correct format for the style being
        used.

        Parameters
        ----------
        string: str
            The formatted string.

        Returns
        -------
        The value of the string.
        """
        raise NotImplementedError

    @abstractmethod
    def string_to_real(self, string: str) -> float64:
        """
        Convert a formatted string to a real.

        The string must be in the correct format for the style being
        used.

        Parameters
        ----------
        string: str
            The formatted string.

        Returns
        -------
        The value of the string.
        """
        raise NotImplementedError

    @abstractmethod
    def integer_to_string(self, integer: int64) -> str:
        """
        Convert an integer to a formatted string.

        Parameters
        ----------
        integer: int64
            The value to format.

        Returns
        -------
        The formatted string.
        """
        raise NotImplementedError

    @abstractmethod
    def real_to_string(self, real: float64) -> str:
        """
        Convert a real to a formatted string.

        Parameters
        ----------
        real: float64
            The value to format.

        Returns
        -------
        The formatted string.
        """
        raise NotImplementedError

    @abstractmethod
    def get_format(self) -> str:
        """
        Get the current format style.

        Returns
        -------
        The format string used to format values.
        """
        raise NotImplementedError

    @abstractmethod
    def string_to_string(self, string: str) -> str:
        """
        Convert an unformatted string into a formatted string.

        Parameters
        ----------
        string: str
            The unformatted string.

        Returns
        -------
        The formatted string.
        """
        raise NotImplementedError

    @abstractmethod
    def integer_to_editable_string(self, integer: int64) -> str:
        """
        Convert an integer to its formatted string representation, but \
        with full precision for editing.

        Parameters
        ----------
        integer: int64
            The value to format.

        Returns
        -------
        The formatted string.
        """
        raise NotImplementedError

    @abstractmethod
    def real_to_editable_string(self, real: float64) -> str:
        """
        Convert a real to its formatted string representation, but \
        with full precision for editing.

        Parameters
        ----------
        real: float64
            The value to format.

        Returns
        -------
        The formatted string.
        """
        raise NotImplementedError
