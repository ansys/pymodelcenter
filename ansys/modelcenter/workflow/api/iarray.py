from abc import ABC, abstractmethod
from typing import Optional


class IArray(ABC):
    """
    Base class for all array types.  Has common functionality for getting/setting array
    sizes and getting/setting values as strings.

    Arrays start at 0 length by default.  So you must set the size before you can
    assign individual array elements.

    Implements IVariable
    """

    @property
    def has_changed(self) -> bool:
        raise NotImplementedError

    @property
    def hide(self) -> bool:
        raise NotImplementedError

    @property
    def owning_component(self) -> LPDISPATCH:
        raise NotImplementedError

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
    def is_valid(self) -> bool:
        """
        Finds out whether or not the array is valid.

        Returns
        -------
        yes(TRUE) or no(FALSE).
        """
        raise NotImplementedError

    @abstractmethod
    def validate(self) -> None:
        """
        Causes the array to validate itself.
        """
        raise NotImplementedError

    @abstractmethod
    def get_name(self) -> str:
        """
        Gets the name of the array.

        Returns
        -------
        The name of the array.
        """
        raise NotImplementedError

    @abstractmethod
    def get_full_name(self) -> str:
        """
        Gets the full %ModelCenter path of the array.

        Returns
        -------
        The full %ModelCenter path of the array.
        """
        raise NotImplementedError

    @abstractmethod
    def get_type(self) -> str:
        """
        Gets the type of the array.

        Returns
        -------
        The type of the array as a string.
        """
        raise NotImplementedError

    @abstractmethod
    def is_input(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def to_string(self) -> str:
        """
        Converts the array to a string, validating the array if necessary. If the variable is an
        array, it will to be of the form <c>"1, 2, 3"</c> for one-dimensional arrays or
        <c>"bounds[3,3] {1, 2, 3, 4, 5, 6, 7, 8, 9}"</c> for multi-dimensional arrays.

        Returns
        -------
        The converted string value of the array.
        """
        raise NotImplementedError

    @abstractmethod
    def from_string(self, value: str) -> None:
        """
        Sets the value of the array from a specified string. For \c 1D arrays, the specification
        is of the form <c>'1,2,3'</c>.\n For \c nD arrays, the specification is of the form
        <c>'bounds[2,2,2] {1,2,3,4,5,6,7,8}'</c>.\n String arrays may optionally have the
        elements quoted in the form <c>'bounds[2,3] {"a", "b,c", "d", "", "e", "f"}'</c>

        Parameters
        ----------
        value
            New value.
        """
        raise NotImplementedError

    @abstractmethod
    def to_string_absolute(self) -> str:
        """
        Converts the array to a string. If the variable is an array, it will to be of the form
        <c>"1, 2, 3"</c> for one-dimensional arrays or <c>"bounds[3,3] {1, 2, 3, 4, 5, 6, 7, 8,
        9}"</c> for multi-dimensional arrays.

        Returns
        -------
        The converted string value of the array.
        """
        raise NotImplementedError

    @abstractmethod
    def invalidate(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def direct_precedents(self, follow_suspended: Optional[VARIANT],
                          reserved: Optional[VARIANT]) -> LPDISPATCH:
        raise NotImplementedError

    @abstractmethod
    def direct_dependents(self, follow_suspended: Optional[VARIANT],
                          reserved: Optional[VARIANT]) -> LPDISPATCH:
        raise NotImplementedError

    @abstractmethod
    def precedent_links(self, reserved: Optional[VARIANT]) -> LPDISPATCH:
        raise NotImplementedError

    @abstractmethod
    def dependent_links(self, reserved: Optional[VARIANT]) -> LPDISPATCH:
        raise NotImplementedError

    @abstractmethod
    def precedents(self, follow_suspended: Optional[VARIANT],
                   reserved: Optional[VARIANT]) -> LPDISPATCH:
        raise NotImplementedError

    @abstractmethod
    def dependents(self, follow_suspended: Optional[VARIANT],
                   reserved: Optional[VARIANT]) -> LPDISPATCH:
        raise NotImplementedError

    @abstractmethod
    def is_input_to_component(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def is_input_to_model(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def set_metadata(self, name: str, type: MetadataType, value: VARIANT, access: MetadataAccess,
                     archive: bool) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_metadata(self, name: str) -> VARIANT:
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
        The value of the element as a string.
        """
        raise NotImplementedError

    @abstractmethod
    def get_length(self, dim: Optional[VARIANT]) -> int:
        """
        Get the length of the n'th dimension of the array.

        Parameters
        ----------
        dim
            Dimension of the array to query.  This uses a 0 based index, so 0 will give you the
            first dimension, 1 the second, etc.  If omitted, gives the first dimension

        Returns
        -------
        Length(size) of the array.
        """
        raise NotImplementedError

    @abstractmethod
    def set_length(self, length: int, dim: Optional[VARIANT]) -> None:
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
    def set_dimensions(self, d1: int, d2: Optional[VARIANT], d3: Optional[VARIANT],
                       d4: Optional[VARIANT], d5: Optional[VARIANT], d6: Optional[VARIANT],
                       d7: Optional[VARIANT], d8: Optional[VARIANT], d9: Optional[VARIANT],
                       d10: Optional[VARIANT]) -> None:
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
    def get_size(self, dim: Optional[VARIANT]) -> int:
        """
        Alias for the getLength() call

        Parameters
        ----------
        dim
            Dimension of the array to query(0-based index).

        Returns
        -------
        Size of the dimension
        """
        raise NotImplementedError

    @abstractmethod
    def set_size(self, length: int, dim: Optional[VARIANT]) -> None:
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
    def get_dimensions(self) -> VARIANT:
        """
        Gets the dimensions of the array.

        Returns
        -------
        Variant - either a single integer, in the case of a 1D array,
        or an array of integers, in the case of multi-dimensional arrays.
        """
        raise NotImplementedError

