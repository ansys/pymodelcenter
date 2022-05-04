from typing import Optional

from ansys.modelcenter.workflow.api.iarray import IArray


class IDoubleArray(IArray):
    """
    An array of double (real) values.

    Implements IArray.
    """

    @property
    def lower_bound(self) -> float:
        """
        Lower bound of the array.
        """
        raise NotImplementedError

    @property
    def upper_bound(self) -> float:
        """
        Upper bound of the array.
        """
        raise NotImplementedError

    @property
    def description(self) -> str:
        """
        Description of the array.
        """
        raise NotImplementedError

    @property
    def units(self) -> str:
        """
        Units of the array.
        """
        raise NotImplementedError

    @property
    def enum_aliases(self) -> str:
        """
        Enumerated aliases of the array.
        """
        raise NotImplementedError

    @property
    def enum_values(self) -> str:
        """
        Enumerated values of the array.
        """
        raise NotImplementedError

    @property
    def format(self) -> str:
        """
        Format of the variable.
        """
        raise NotImplementedError

    def has_lower_bound(self) -> bool:
        """
        Finds out whether or not the array has a lower bound.

        Returns
        -------
        bool
            Yes (TRUE) or no (FALSE).
        """
        raise NotImplementedError

    def has_upper_bound(self) -> bool:
        """
        Finds out whether or not the array has an upper bound.

        Returns
        -------
        bool
            Yes (TRUE) or no (FALSE).
        """
        raise NotImplementedError

    def get_value(self, d1: object, d2: Optional[object], d3: Optional[object],
                  d4: Optional[object], d5: Optional[object], d6: Optional[object],
                  d7: Optional[object], d8: Optional[object], d9: Optional[object],
                  d10: Optional[object]) -> float:
        """
        Gets the value of an array element.

        Parameters
        ----------
        d1
            index in the 1st dimension (0-based index)
        d2
            index in the 2nd dimension (0-based index)
        d3
            index in the 3rd dimension (0-based index)
        d4
            index in the 4th dimension (0-based index)
        d5
            index in the 5th dimension (0-based index)
        d6
            index in the 6th dimension (0-based index)
        d7
            index in the 7th dimension (0-based index)
        d8
            index in the 8th dimension (0-based index)
        d9
            index in the 9th dimension (0-based index)
        d10
            index in the 10th dimension (0-based index)

        Returns
        -------
        float
            The value.
        """
        raise NotImplementedError

    def set_value(self, value: float, d1: object, d2: Optional[object], d3: Optional[object],
                  d4: Optional[object], d5: Optional[object], d6: Optional[object],
                  d7: Optional[object], d8: Optional[object], d9: Optional[object],
                  d10: Optional[object]) -> None:
        """
        Sets the value of an array element.  You must set the array size first.

        Parameters
        ----------
        value
            New value.
        d1
            position in the 1st dimension of the array (or full index string) (0-based index)
        d2
            position in the 2nd dimension of the array (0-based index)
        d3
            position in the 3rd dimension of the array (0-based index)
        d4
            position in the 4th dimension of the array (0-based index)
        d5
            position in the 5th dimension of the array (0-based index)
        d6
            position in the 6th dimension of the array (0-based index)
        d7
            position in the 7th dimension of the array (0-based index)
        d8
            position in the 8th dimension of the array (0-based index)
        d9
            position in the 9th dimension of the array (0-based index)
        d10
            position in the 10th dimension of the array (0-based index)
        """
        raise NotImplementedError

    def get_array(self) -> object:
        """
        Gets the whole array as a single primitive array object in the language's native array
        format. This is typically faster than calling individual array elements.

        Returns
        -------
        object
            The primitive array
        """
        raise NotImplementedError

    def set_array(self, array: object) -> None:
        """
        Sets the whole array at once using a single primitive array object in the language's
        native array format. This is typically faster than calling individual array elements.
        The array will take on the size and dimensions of the passed in array.

        Parameters
        ----------
        array
            The primitive source array
        """
        raise NotImplementedError

    def to_formatted_string_ex(self, index: int) -> str:
        """
        Converts the value to a formatted string.

        Parameters
        ----------
        index
            Position in the array (0-based index).

        Returns
        -------
        str
            Formatted string.
        """
        raise NotImplementedError

    def from_formatted_string_ex(self, value: str, index: int) -> None:
        """
        Loads a formatted string.

        Parameters
        ----------
        value
            Formatted value to load.
        index
            Position in the array (0-based index).
        """
        raise NotImplementedError

    def to_formatted_string_absolute_ex(self, index: int) -> str:
        """
        Converts the value to an absolute formatted string.

        Parameters
        ----------
        index
            Position in the array (0-based index).

        Returns
        -------
        str
            An absolute formatted string.
        """
        raise NotImplementedError

    def clear_upper_bound(self) -> None:
        """
        Clears the upper bound property of the array if it has previously been set.
        """
        raise NotImplementedError

    def clear_lower_bound(self) -> None:
        """
        Clears the lower bound property of the array if it has previously been set.
        """
        raise NotImplementedError

    def get_value_absolute(self, d1: object, d2: Optional[object], d3: Optional[object],
                           d4: Optional[object], d5: Optional[object], d6: Optional[object],
                           d7: Optional[object], d8: Optional[object], d9: Optional[object],
                           d10: Optional[object]) -> float:
        """
        Gets the value of an array element without validating.

        Parameters
        ----------
        d1
            index in the 1st dimension (0-based index)
        d2
            index in the 2nd dimension (0-based index)
        d3
            index in the 3rd dimension (0-based index)
        d4
            index in the 4th dimension (0-based index)
        d5
            index in the 5th dimension (0-based index)
        d6
            index in the 6th dimension (0-based index)
        d7
            index in the 7th dimension (0-based index)
        d8
            index in the 8th dimension (0-based index)
        d9
            index in the 9th dimension (0-based index)
        d10
            index in the 10th dimension (0-based index)

        Returns
        -------
        float
            The value.
        """
        raise NotImplementedError
