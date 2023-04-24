"""Definition of Format."""
from abc import ABC, abstractmethod

from numpy import float64, int64


class IFormat(ABC):
    """Class for formatting values in various string formats \
    (percentage, currency, etc.)."""

    @property
    @abstractmethod
    def format(self) -> str:
        """
        Style to use for formatting.

        Formats, with the exception of Dates, mimic the formatting style
        used in Microsoft Excel. They are not a one-to-one match though,
        there are some differences.
        There are 6 broad categories of formats:

        1. No specific format:
        Specified by 'General', or an empty string, this is the default
        format intended to cover most non-specific cases. It shows a
        limited number of significant figures, and auto-switches between
        number and scientific formats based on the number's scale.

        2. Number:
        Number formats are used for specifying how numeric values will
        be displayed. See Currency for specialized handling of monetary
        values.

        Specification:
        * Zero decimal places indicated by '0'.
        * 1 to 30 decimal places indicated by '0.0' with an extra
        trailing zero for each decimal place.
        * Use of 1000's separator indicated by leading '#,##'.
        * Negative sign can be switched to surrounding braces by
        surrounding entire expression with braces.

        Examples:
        * 0.00 : 2 decimal places
        * (#,##0.00000) : Negative braces, 1000's separator, 5 decimal places

        3. Currency:
        Currency formats are for general monetary values.

        Specification:
        * Follows Number format for specifying digits, but starts with a
        '$' symbol. If negative braces are specified, the symbol should
        be within them.
        * The 1000's separator mark notation is required. If missing will
        be added automatically.

        Examples:
        * $#,##0.00 : 2 decimal places
        * ($#,##0.00000) : Negative braces, 5 decimal places

        3. Percentage:
        Percentage formats multiply the datapin value by 100 and
        display the result with a percent sign.

        Specification:
        * Follows Number format for specifying number of digits, but ends
        with a '%' symbol.
        * No 1000 Separator or Negative braces allowed.

        Examples:
        * 0.00% : 2 decimal places
        * 0.00000% : 5 decimal places

        4. Fraction:
        Fraction formats show the value as a fraction.

        Specification:
        * Only certain arbitrary combinations are allowed. See examples.

        Examples:
        * # ?/? : Up to one digit
        * # ??/?? : Up to two digits
        * # ???/??? : Up to three digits
        * # ?/2 : As halves
        * # ?/4 : As quarters
        * # ?/8 : As eighths
        * # ??/16 : As sixteenths
        * # ?/10 : As tenths
        * # ??/100 : As hundredths

        5. Scientific:
        Scientific formats show the value in scientific notation.

        Specification:
        * Follows Number format for specifying digits, but ends with the
        string: 'E+00'.

        Examples:
        * 0.00E+00 : 2 decimal places
        * 0.00000E+00 : 5 decimal places

        6. Date:
        Date formats show the value as a date.

        Specification:
        * Specified by certain strings, see Examples.

        Examples:
        This list shows each Date format and their example output.
        * Epoch formats:

            * EpSec : 0
            * EpMin : 0.00000
            * EpHr : 0.0000000
            * EpDay : 0.00000000
            * EpYr : 0.00000000000

        * Standard display formats:

            * DD/MM/YYY : 31/21/1971 00:00:00.000
            * YYDDD : 71365.00000000
            * YYYYDDD : 1971365.000000
            * YYYYMMDD : 19711231.00000000
            * YYYY/MM/DD : 1971/12/31 00:00:00.000
            * YYYY:MM:DD : 1971:12:31:00:00:00.000

        * Gregorian formats:

            * GPSG : 30 Dec 1971 23:59:51.000
            * LCLG : 30 Dec 1971 20:00:00.000
            * TAIG : 31 Dec 1971 00:00:10.000
            * TDBG : 31 Dec 1971 00:00:42.184
            * TDTG : 31 Dec 1971 00:00:42.184
            * UTCG : 31 Dec 1971 00:00:00.000

        * Julian formats:

            * JDate : 2441316.50000000
            * JDTDB : 2441316.50048824
            * (Ephemeris Date) JED : 2441316.50048824
            * LCLJ : 364/71 20:00:00.000
            * ModJDate : 41316.00000000
            * TAIJ : 365/71 00:00:10.000
            * UTCJ : 365/71 00:00:00.000
            * UTCJFOUR : 365/1971 00:00:00.000

        * ISO8601 UTC formats:

            * ISO-YD : 1971-365T00:00:00.000
            * ISO-YMD : 1971-12-31T00:00:00.000

        * Other formats:

            * (Earth Canonical Time) EarthEpTU : 0.000
            * (GMT System) GMT : 365/00000 1971
            * (GPS Time) GPS : -0418:172809.000
            * (GPS Z Count) GPSZ : -168652806.000
            * (Mission Elapsed) : MisElap : 0/00:00:00.000
            * (Sun Canonical Time) SunEpTU : 0.000

        Returns
        -------
        str
            The format string used to format values.
        """

    @format.setter
    @abstractmethod
    def format(self, fmt: str) -> None:
        """Setter for format property."""

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
        int64
            The value of the string.
        """

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
        float64
            The value of the string.
        """

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
        str
            The formatted string.
        """

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
        str
            The formatted string.
        """

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
        str
            The formatted string.
        """

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
        str
            The formatted string.
        """

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
        str
            The formatted string.
        """
