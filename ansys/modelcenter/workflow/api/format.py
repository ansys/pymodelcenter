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

        There are 6 broad categories of formats:
        1. General:
        The General format indicates no specific number format.
        Specified by 'General', or an empty string.

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
        Percentage formats multiply the variable value by 100 and
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
