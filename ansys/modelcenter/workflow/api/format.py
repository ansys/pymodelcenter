"""Definition of Format."""
import clr
from numpy import float64, int64

clr.AddReference(r"phoenix-mocks\Phoenix.Mock.v45")
from Phoenix.Mock import MockFormatter


class Format:
    """Class for formatting values in various string formats \
    (percentage, currency, etc.)."""

    def __init__(self, instance: MockFormatter):
        """Initialize."""
        self._instance = instance

    @property
    def format(self) -> str:
        """
        Style to use for formatting.

        When setting, you may pass in the empty string to mean "General".
        TODO: Documentation on valid formats, MCD docs not great.

        Returns
        -------
        The format string used to format values.
        """
        return self._instance.getFormat()

    @format.setter
    def format(self, fmt: str) -> None:
        """Setter for format property."""
        self._instance.setFormat(fmt)

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
        return self._instance.stringToLong(string)

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
        return self._instance.stringToDouble(string)

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
        return self._instance.longToString(integer)

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
        return self._instance.doubleToString(real)

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
        return self._instance.stringToString(string)

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
        return self._instance.longToEditableString(integer)

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
        return self._instance.doubleToEditableString(real)
