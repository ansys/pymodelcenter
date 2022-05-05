from abc import ABC, abstractmethod
from typing import Optional

from ansys.modelcenter.workflow.api.iarray import IArray


class IFileArray(IArray, ABC):
    """
    COM instance.

    Implements IArray.
    """

    @property
    def is_binary(self) -> bool:
        """
        Whether or not the file is binary.
        """
        raise NotImplementedError

    @property
    def description(self) -> str:
        """
        Description of the array.
        """
        raise NotImplementedError

    @property
    def save_with_model(self) -> bool:
        """
        Flag to indicate whether the file content to be saved with the Model file.
        """
        raise NotImplementedError

    @property
    def direct_transfer(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def get_value(self, d1: object, d2: Optional[object], d3: Optional[object],
                  d4: Optional[object], d5: Optional[object], d6: Optional[object],
                  d7: Optional[object], d8: Optional[object], d9: Optional[object],
                  d10: Optional[object]) -> str:
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
        str
            The value.
        """
        raise NotImplementedError

    @abstractmethod
    def set_value(self, d1: object, d2: Optional[object], d3: Optional[object],
                  d4: Optional[object], d5: Optional[object], d6: Optional[object],
                  d7: Optional[object], d8: Optional[object], d9: Optional[object],
                  d10: Optional[object], new_value: str) -> None:
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
    def get_file_extension(self, d1: object, d2: Optional[object], d3: Optional[object],
                           d4: Optional[object], d5: Optional[object], d6: Optional[object],
                           d7: Optional[object], d8: Optional[object], d9: Optional[object],
                           d10: Optional[object]) -> str:
        """
        Gets the extension used for the file (used to associate the file with an application).

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
            The file extension.
        """
        raise NotImplementedError

    @abstractmethod
    def set_file_extension(self, value: str, d1: object, d2: Optional[object], d3: Optional[object],
                           d4: Optional[object], d5: Optional[object], d6: Optional[object],
                           d7: Optional[object], d8: Optional[object], d9: Optional[object],
                           d10: Optional[object]) -> None:
        """
        Sets the desired file extension for the file.

        Parameters
        ----------
        value
            The file extension.
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
    def to_file(self, file_name: str, encoding: object, d1: object, d2: Optional[object],
                d3: Optional[object], d4: Optional[object], d5: Optional[object],
                d6: Optional[object], d7: Optional[object], d8: Optional[object],
                d9: Optional[object], d10: Optional[object]) -> None:
        """
        Writes out contents to a file.

        Parameters
        ----------
        file_name
            The file to write.
        encoding
            File encoding to be used (ascii, utf-8, binary).
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
    def from_file(self, file_name: str, d1: object, d2: Optional[object], d3: Optional[object],
                  d4: Optional[object], d5: Optional[object], d6: Optional[object],
                  d7: Optional[object], d8: Optional[object], d9: Optional[object],
                  d10: Optional[object]) -> None:
        """
        Reads data from a file.

        Parameters
        ----------
        file_name
            The file to load.
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
    def to_file_absolute(self, file_name: str, encoding: object, d1: object, d2: Optional[object],
                         d3: Optional[object], d4: Optional[object], d5: Optional[object],
                         d6: Optional[object], d7: Optional[object], d8: Optional[object],
                         d9: Optional[object], d10: Optional[object]) -> None:
        """
        Writes out contents to a file without validating the variable.

        Parameters
        ----------
        file_name
            The file to write.
        encoding
            File encoding to be used (ascii, utf-8, binary).
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
