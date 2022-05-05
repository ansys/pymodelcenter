from abc import ABC, abstractmethod
from typing import Optional

from ansys.modelcenter.workflow.api.iarray import IArray


class IIntegerArray(IArray, ABC):
    """
    COM instance.

    Implements IArray.
    """

    @property
    def lower_bound(self) -> int:
        """
        Lower bound of the array.
        """
        raise NotImplementedError

    @property
    def upper_bound(self) -> int:
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

    @abstractmethod
    def get_value(self, d1: object, d2: Optional[object], d3: Optional[object],
                  d4: Optional[object], d5: Optional[object], d6: Optional[object],
                  d7: Optional[object], d8: Optional[object], d9: Optional[object],
                  d10: Optional[object]) -> int:
        """
        Get the value of an array element.

        Parameters
        ----------
        d1
            Index in the 1st dimension (0-based index).
        d2
            Index in the 2nd dimension (0-based index).
        d3
            Index in the 3rd dimension (0-based index).
        d4
            Index in the 4th dimension (0-based index).
        d5
            Index in the 5th dimension (0-based index).
        d6
            Index in the 6th dimension (0-based index).
        d7
            Index in the 7th dimension (0-based index).
        d8
            Index in the 8th dimension (0-based index).
        d9
            Index in the 9th dimension (0-based index).
        d10
            Index in the 10th dimension (0-based index).

        Returns
        -------
        int
            The value.
        """
        raise NotImplementedError

    @abstractmethod
    def set_value(self, d1: object, d2: Optional[object], d3: Optional[object],
                  d4: Optional[object], d5: Optional[object], d6: Optional[object],
                  d7: Optional[object], d8: Optional[object], d9: Optional[object],
                  d10: Optional[object], new_value: int) -> None:
        """
        Sets the value of an array element.

        Parameters
        ----------
        d1
            Index in the 1st dimension (0-based index).
        d2
            Index in the 2nd dimension (0-based index).
        d3
            Index in the 3rd dimension (0-based index).
        d4
            Index in the 4th dimension (0-based index).
        d5
            Index in the 5th dimension (0-based index).
        d6
            Index in the 6th dimension (0-based index).
        d7
            Index in the 7th dimension (0-based index).
        d8
            Index in the 8th dimension (0-based index).
        d9
            Index in the 9th dimension (0-based index).
        d10
            Index in the 10th dimension (0-based index).
        new_value
            New value.
        """
        raise NotImplementedError

    @abstractmethod
    def has_lower_bound(self) -> bool:
        """
        Whether or not the array has an lower bound.

        Returns
        -------
        bool
            yes(TRUE) or no(FALSE).
        """
        raise NotImplementedError

    @abstractmethod
    def has_upper_bound(self) -> bool:
        """
        Whether or not the array has an upper bound.

        Returns
        -------
        bool
            yes(TRUE) or no(FALSE).
        """
        raise NotImplementedError

    @abstractmethod
    def get_array(self) -> object:
        """
        Gets the COM array.

        Returns
        -------
        object
            The COM array.
        """
        raise NotImplementedError

    @abstractmethod
    def set_array(self, array: object) -> None:
        """
        Sets the COM array.

        Parameters
        ----------
        array
            The COM array.
        """
        raise NotImplementedError

    @abstractmethod
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
            The formatted string.
        """
        raise NotImplementedError

    @abstractmethod
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

    @abstractmethod
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
            The formatted string.
        """
        raise NotImplementedError

    @abstractmethod
    def clear_upper_bound(self) -> None:
        """
        Clears the upper bound property of the array if it has previously been set.
        """
        raise NotImplementedError

    @abstractmethod
    def clear_lower_bound(self) -> None:
        """
        Clears the lower bound property of the array if it has previously been set.
        """
        raise NotImplementedError

    @abstractmethod
    def get_value_absolute(self, d1: object, d2: Optional[object], d3: Optional[object],
                           d4: Optional[object], d5: Optional[object], d6: Optional[object],
                           d7: Optional[object], d8: Optional[object], d9: Optional[object],
                           d10: Optional[object]) -> int:
        """
        Gets the value of an array element without validating.

        Parameters
        ----------
        d1
            Index in the 1st dimension (0-based index).
        d2
            Index in the 2nd dimension (0-based index).
        d3
            Index in the 3rd dimension (0-based index).
        d4
            Index in the 4th dimension (0-based index).
        d5
            Index in the 5th dimension (0-based index).
        d6
            Index in the 6th dimension (0-based index).
        d7
            Index in the 7th dimension (0-based index).
        d8
            Index in the 8th dimension (0-based index).
        d9
            Index in the 9th dimension (0-based index).
        d10
            Index in the 10th dimension (0-based index).

        Returns
        -------
        int
            The value.
        """
        raise NotImplementedError
