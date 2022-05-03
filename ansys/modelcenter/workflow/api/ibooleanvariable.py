from abc import ABC, abstractmethod
from typing import Optional

from .iarray import IArray


class IBooleanArray(IArray, ABC):
    """
    COM instance.

    Implements IArray.
    """

    @property
    def has_changed(self) -> bool:
        raise NotImplementedError

    @property
    def hide(self) -> bool:
        raise NotImplementedError

    @property
    def owning_component(self) -> object:
        raise NotImplementedError

    @property
    def size(self) -> int:
        raise NotImplementedError

    @property
    def num_dimensions(self) -> int:
        raise NotImplementedError

    @property
    def description(self) -> str:
        """
        Description of the array.
        """
        raise NotImplementedError

    @abstractmethod
    def is_valid(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def validate(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_name(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_full_name(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_type(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def is_input(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def to_string(self) -> str:
        """
        Converts the array to a string, validating it if necessary. The format is of the form
        <c>"true, false, true"</c> for one-dimensional arrays or <c>"bounds[3,3] {true, false,
        true, false, true, false, true, false, true}"</c> for multi-dimensional arrays.

        Returns
        -------
        str
            String representation of the array.
        """
        raise NotImplementedError

    @abstractmethod
    def from_string(self, value: str) -> None:
        """
        Sets the value of the array from a specified string. For \c 1D arrays, the specification
        is of the form <c>'true,false,true'</c>.\n For \c nD arrays, the specification is of the
        form <c>'bounds[2,2,2] {true,false,true,false,true,false,true,false}'</c>.

        Parameters
        ----------
        value
            The new value.
        """
        raise NotImplementedError

    @abstractmethod
    def to_string_absolute(self) -> str:
        """
        Converts the array to a string. The format is of the form <c>"true, false, true"</c> for
        one-dimensional arrays or <c>"bounds[3,3] {true, false, true, false, true, false, true,
        false, true}"</c> for multi-dimensional arrays.

        Returns
        -------
        str
            String representation of the array.
        """
        raise NotImplementedError

    @abstractmethod
    def invalidate(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def direct_precedents(self, follow_suspended: Optional[object],
                          reserved: Optional[object]) -> object:
        raise NotImplementedError

    @abstractmethod
    def direct_dependents(self, follow_suspended: Optional[object],
                          reserved: Optional[object]) -> object:
        raise NotImplementedError

    @abstractmethod
    def precedent_links(self, reserved: Optional[object]) -> object:
        raise NotImplementedError

    @abstractmethod
    def dependent_links(self, reserved: Optional[object]) -> object:
        raise NotImplementedError

    @abstractmethod
    def precedents(self, follow_suspended: Optional[object], reserved: Optional[object]) -> object:
        raise NotImplementedError

    @abstractmethod
    def dependents(self, follow_suspended: Optional[object], reserved: Optional[object]) -> object:
        raise NotImplementedError

    @abstractmethod
    def is_input_to_component(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def is_input_to_model(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def set_metadata(self, name: str, type: MetadataType, value: object, access: MetadataAccess,
                     archive: bool) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_metadata(self, name: str) -> object:
        raise NotImplementedError

    @abstractmethod
    def to_string_ex(self, index: int) -> str:
        raise NotImplementedError

    @abstractmethod
    def from_string_ex(self, value: str, index: int) -> None:
        raise NotImplementedError

    @abstractmethod
    def to_string_absolute_ex(self, index: int) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_length(self, dim: Optional[object]) -> int:
        raise NotImplementedError

    @abstractmethod
    def set_length(self, length: int, dim: Optional[object]) -> None:
        raise NotImplementedError

    @abstractmethod
    def set_dimensions(self, d1: int, d2: Optional[object], d3: Optional[object],
                       d4: Optional[object], d5: Optional[object], d6: Optional[object],
                       d7: Optional[object], d8: Optional[object], d9: Optional[object],
                       d10: Optional[object]) -> None:
        raise NotImplementedError

    @abstractmethod
    def value(self, d1: object, d2: Optional[object], d3: Optional[object], d4: Optional[object],
              d5: Optional[object], d6: Optional[object], d7: Optional[object],
              d8: Optional[object], d9: Optional[object], d10: Optional[object]) -> bool:
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
        bool
            The value.
        """
        raise NotImplementedError

    @abstractmethod
    def value(self, d1: object, d2: Optional[object], d3: Optional[object], d4: Optional[object],
              d5: Optional[object], d6: Optional[object], d7: Optional[object],
              d8: Optional[object], d9: Optional[object], d10: Optional[object],
              new_value: bool) -> None:
        """
        Set the value of an array element.

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
            The new value.
        """
        raise NotImplementedError

    @abstractmethod
    def get_value(self, d1: object, d2: Optional[object], d3: Optional[object],
                  d4: Optional[object], d5: Optional[object], d6: Optional[object],
                  d7: Optional[object], d8: Optional[object], d9: Optional[object],
                  d10: Optional[object]) -> bool:
        """
        Gets the value of an array element.

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
        bool
            The value.
        """
        raise NotImplementedError

    @abstractmethod
    def set_value(self, value: bool, d1: object, d2: Optional[object], d3: Optional[object],
                  d4: Optional[object], d5: Optional[object], d6: Optional[object],
                  d7: Optional[object], d8: Optional[object], d9: Optional[object],
                  d10: Optional[object]) -> None:
        """
        Sets the value of an array element.

        Parameters
        ----------
        value
            The new value.
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
        """
        raise NotImplementedError

    @abstractmethod
    def get_array(self) -> object:
        """
        Get the COM array.

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
    def get_value_absolute(self, d1: object, d2: Optional[object], d3: Optional[object],
                           d4: Optional[object], d5: Optional[object], d6: Optional[object],
                           d7: Optional[object], d8: Optional[object], d9: Optional[object],
                           d10: Optional[object]) -> bool:
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
        bool
            The value.
        """
        raise NotImplementedError
