from typing import Optional

from ansys.modelcenter.workflow.api.ivariable import IVariable


class IFileVariable(IVariable):
    """
    COM instance.

    Implements IVariable.
    """

    @property
    def value(self) -> str:
        """
        Value of the variable.
        """
        raise NotImplementedError

    @property
    def is_binary(self) -> bool:
        """
        Whether or not the file is binary.
        """
        raise NotImplementedError

    @property
    def file_extension(self) -> str:
        """
        File extension of the variable. Used when opening the file in ModelCenter.
        """
        raise NotImplementedError

    @property
    def description(self) -> str:
        """
        The description of the variable.
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
        """
        Flag to indicate whether direct file transfer is used for incoming link.
        """
        raise NotImplementedError

    def to_file(self, file_name: str, encoding: Optional[object]) -> None:
        """
        Writes the value of the variable to a file.

        Parameters
        ----------
        file_name
            Path of the file.
        encoding
            File encoding to be used (ascii, utf-8, binary).
        """
        raise NotImplementedError

    def from_file(self, file_name: str) -> None:
        """
        Sets the value of the variable from a specified file.

        Parameters
        ----------
        file_name
            Path of the file.
        """
        raise NotImplementedError

    def write_file(self, file_name: str) -> None:
        """
        Writes the value of the variable to a file.

        Parameters
        ----------
        file_name
            Path of the file.
        """
        raise NotImplementedError

    def read_file(self, file_name: str) -> None:
        """
        Sets the value of the variable from a specified file.

        Parameters
        ----------
        file_name
            Path of the file.
        """
        raise NotImplementedError

    def to_file_absolute(self, file_name: str, encoding: Optional[object]) -> None:
        """
        Writes the absolute value of the variable to a file. Optional parameter to specify the
        encoding as ASCII, UTF-8 or binary. If no encoding is specified, will default to ASCII
        for text files and binary for binary files. Will throw an exception if binary encoding
        is used on a text file or if ascii or utf-8 encoding is used on a binary file.

        Parameters
        ----------
        file_name
            Path of the file.
        encoding
            The desired encoding of the file. Can be: 'ascii', 'utf-8',
            or 'binary'.
        """
        raise NotImplementedError

    def write_file_absolute(self, file_name: str) -> None:
        """
        Writes the absolute value of the variable to a file.

        Parameters
        ----------
        file_name
            Path of the file.
        """
        raise NotImplementedError
