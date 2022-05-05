from abc import abstractmethod, ABC
from typing import Optional

from ansys.modelcenter.workflow.api.iarray import IArray


class IStringArray(IArray, ABC):
    """
    COM instance.

    Implements IArray.
    """

    @property
    def description(self) -> str:
        """
        Description of the array.
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

    @abstractmethod
    def get_value(self, d1: object, d2: Optional[object], d3: Optional[object],
                  d4: Optional[object], d5: Optional[object], d6: Optional[object],
                  d7: Optional[object], d8: Optional[object], d9: Optional[object],
                  d10: Optional[object]) -> str:
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
        str
            The value.
        """
        raise NotImplementedError

    @abstractmethod
    def set_value(self, value: str, d1: object, d2: Optional[object], d3: Optional[object],
                  d4: Optional[object], d5: Optional[object], d6: Optional[object],
                  d7: Optional[object], d8: Optional[object], d9: Optional[object],
                  d10: Optional[object]) -> None:
        """
        Sets the value of an array element.

        Parameters
        ----------
        value
            New value.
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
    def get_value_absolute(self, d1: object, d2: Optional[object], d3: Optional[object],
                           d4: Optional[object], d5: Optional[object], d6: Optional[object],
                           d7: Optional[object], d8: Optional[object], d9: Optional[object],
                           d10: Optional[object]) -> str:
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
        str
            The value.
        """
        raise NotImplementedError
