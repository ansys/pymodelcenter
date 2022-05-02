from abc import ABC, abstractmethod
from typing import Optional

from .ivariable import IVariable


class IArray(IVariable, ABC):
    """
    Base class for all array types.  Has common functionality for getting/setting array
    sizes and getting/setting values as strings.

    Arrays start at 0 length by default.  So you must set the size before you can
    assign individual array elements.

    Implements IVariable
    """

    @property
    def size(self) -> int:
        """
        Alias for length property
        """
        raise NotImplementedError

    @property
    def auto_size(self) -> bool:
        """
        Whether or not the array is set to automatically size itself.  If false and the
        array is linked from upstream, the upstream array must be exactly the same size
        or an error ensues.  If true, the array will resize itself when the link is validated.
        """
        raise NotImplementedError

    @property
    def num_dimensions(self) -> int:
        """
        Number of dimensions this array has.  Defaults to 1.  Changing the number of dimensions
        will lose all previous data in the array.
        """
        raise NotImplementedError

    @property
    def length(self) -> int:
        """
        Size of the array.  Alias for the length property.  Only useful if the array is 1
        dimensional. Use the getLength(), setLength(), numDimensions, or setDimensions() methods
        and properties for multi-dimensional arrays On initialization, the array is 0 length by
        default.  To fill in values on a newly created array, set the size/length first.
        """
        raise NotImplementedError

    @abstractmethod
    def to_string_ex(self, index: int) -> str:
        """
        Converts the value of an array element to a string, validating the array if necessary.

        Parameters
        ----------
        index
            Index of the array element (0-based index).

        Returns
        -------
        str
            The value of the element as a string.
        """
        raise NotImplementedError

    @abstractmethod
    def from_string_ex(self, value: str, index: int) -> None:
        """
        Sets the value of an array element from a specified string.

        Parameters
        ----------
        value
            New value.
        index
            Index of the array element (0-based index).
        """
        raise NotImplementedError

    @abstractmethod
    def to_string_absolute_ex(self, index: int) -> str:
        """
        Converts the value of an array element to a string.

        Parameters
        ----------
        index
            Index of the array element (0-based index).

        Returns
        -------
        str
            The value of the element as a string.
        """
        raise NotImplementedError

    @abstractmethod
    def get_length(self, dim: Optional[object]) -> int:
        """
        Get the length of the n'th dimension of the array.

        Parameters
        ----------
        dim
            Dimension of the array to query.  This uses a 0 based index, so 0 will give you the
            first dimension, 1 the second, etc.  If omitted, gives the first dimension

        Returns
        -------
        int
            Length(size) of the array.
        """
        raise NotImplementedError

    @abstractmethod
    def set_length(self, length: int, dim: Optional[object]) -> None:
        """
        Sets the length of the n'th dimension of the array

        Parameters
        ----------
        length
            New length of the n'th dimension of the array
        dim
            The dimension to set.  This uses a 0 based index, so 0 will set the
            first dimension, 1 the second, etc.  If omitted, sets the first dimension
        """
        raise NotImplementedError

    @abstractmethod
    def set_dimensions(self, d1: int, d2: Optional[object], d3: Optional[object],
                       d4: Optional[object], d5: Optional[object], d6: Optional[object],
                       d7: Optional[object], d8: Optional[object], d9: Optional[object],
                       d10: Optional[object]) -> None:
        """
        Sets the number of dimensions of an array and the length of each dimension in one call.  An
        array initializes to 0 length.  If any dimension of the array has 0 length, the whole array
        contains no data.  You must set the array size before filling in values unless you are using
        the setArray() call.

        Parameters
        ----------
        d1
            length of the 1st dimension of the array
        d2
            length of the 2nd dimension of the array.  If omitted, the array is 1 dimensional
        d3
            length of the 3rd dimension of the array.  If omitted, the array is 2 dimensional
        d4
            length of the 4th dimension of the array.  If omitted, the array is 3 dimensional
        d5
            length of the 5th dimension of the array.  If omitted, the array is 4 dimensional
        d6
            length of the 6th dimension of the array.  If omitted, the array is 5 dimensional
        d7
            length of the 7th dimension of the array.  If omitted, the array is 6 dimensional
        d8
            length of the 8th dimension of the array.  If omitted, the array is 7 dimensional
        d9
            length of the 9th dimension of the array.  If omitted, the array is 8 dimensional
        d10
            length of the 10th dimension of the array.  If omitted, the array is 9 dimensional
        """
        raise NotImplementedError

    @abstractmethod
    def get_size(self, dim: Optional[object]) -> int:
        """
        Alias for the getLength() call

        Parameters
        ----------
        dim
            Dimension of the array to query(0-based index).

        Returns
        -------
        int
            Size of the dimension
        """
        raise NotImplementedError

    @abstractmethod
    def set_size(self, length: int, dim: Optional[object]) -> None:
        """
        Alias for the setLength() call

        Parameters
        ----------
        length
            Length of the specified dimension
        dim
            The dimension to set (0-based index).
        """
        raise NotImplementedError

    @abstractmethod
    def get_dimensions(self) -> object:
        """
        Gets the dimensions of the array.

        Returns
        -------
        object
            Variant - either a single integer, in the case of a 1D array,
            or an array of integers, in the case of multi-dimensional arrays.
        """
        raise NotImplementedError
