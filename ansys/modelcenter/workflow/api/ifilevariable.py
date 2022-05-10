import ansys.common.variableinterop as acvi
import clr

from overrides import overrides
from typing import Optional
from ansys.modelcenter.workflow.api.ivariable import IVariable

clr.AddReference('phoenix-mocks/Phoenix.Mock.v45')
from Phoenix.Mock import MockFileVariable


class IFileVariable(IVariable[MockFileVariable]):
    """Represents a file variable in the workflow."""

    @overrides
    def __init__(self, wrapped: MockFileVariable):
        super().__init__(wrapped)
        self._standard_metadata: acvi.CommonVariableMetadata = acvi.FileMetadata()

    @property
    @overrides
    def value(self) -> acvi.FileValue:
        """
        Value of the variable.

        Returns
        -------
        FileValue :
            Value of the file variable.
        """
        contents: str = self._wrapped.value
        mime: str = acvi.FileValue.BINARY_MIMETYPE
        encoding = None
        # Create FileValue from string.
        if not self._wrapped.isBinary:
            mime: str = acvi.FileValue.TEXT_MIMETYPE
            encoding: str = 'utf-8'
        raise NotImplementedError  # TODO: Implement FileScope.read_from_string()
        return acvi.FileScope.read_from_string(contents, mime, encoding)

    @value.setter
    @overrides
    def value(self, value: acvi.FileValue) -> None:
        """
        Value of the variable.

        Parameters
        ----------
        value : FileValue
            Value of the file variable.
        """
        self._wrapped.value = value.get_contents()

    @property
    def is_binary(self) -> bool:
        """
        Whether the file is binary.

        Returns
        -------
        bool :
            `True` if file is binary.
        """
        return self._wrapped.isBinary

    @is_binary.setter
    def is_binary(self, value: bool) -> None:
        """
        Whether the file is binary.

        Parameters
        ----------
        value : bool
            Set the value to `True` if file is binary.
        """
        self._wrapped.isBinary = value

    @property
    def file_extension(self) -> str:
        """
        File extension of the variable. Used when opening the file in ModelCenter.

        Returns
        -------
        str :
            Returns the extension of the file value held if known, including the period '.'.
            If the extension is not known, '.tmp' is returned.
        """
        return self._wrapped.fileExtension

    @property
    def save_with_model(self) -> bool:
        """
        Flag to indicate whether the file content to be saved with the Model file.

        Returns
        -------
        bool :
            `True` if the file content to be saved with the Model file.
        """
        return self._wrapped.saveWithModel

    @save_with_model.setter
    def save_with_model(self, value: bool) -> None:
        """
        Flag to indicate whether the file content to be saved with the Model file.

        Parameters
        ----------
        value : bool
            Set to `True` if the file content is to be saved with the Model file.
        """
        self._wrapped.saveWithModel = value

    @property
    def direct_transfer(self) -> bool:
        """
        Flag to indicate whether direct file transfer is used for incoming link.

        Returns
        -------
        bool :
            `True` if direct file transfer is used for incoming link.
        """
        return self._wrapped.directTransfer

    @direct_transfer.setter
    def direct_transfer(self, value: bool) -> None:
        """
        Flag to indicate whether direct file transfer is used for incoming link.

        Parameters
        ----------
        value : bool
            Set to `True` if direct file transfer is used for incoming link.
        """
        self._wrapped.directTransfer = value

    def to_file(self, file_name: str, encoding: Optional[str]) -> None:
        """
        Writes the value of the variable to a file. Optional parameter to specify the
        encoding as ASCII, UTF-8 or binary. If no encoding is specified, will default to ASCII
        for text files and binary for binary files. Will throw an exception if binary encoding
        is used on a text file or if ascii or utf-8 encoding is used on a binary file.

        Parameters
        ----------
        file_name : str
            Path of the file.
        encoding
            The desired encoding of the file. Can be: 'ascii', 'utf-8', or 'binary'.
        """
        self._wrapped.toFile(file_name, encoding)

    def from_file(self, file_name: str) -> None:
        """
        Sets the value of the variable from a specified file.

        Parameters
        ----------
        file_name : str
            Path of the file.
        """
        self._wrapped.fromFile(file_name)

    @property  # type: ignore
    @overrides
    def standard_metadata(self) -> acvi.FileMetadata:
        return self._standard_metadata

    @standard_metadata.setter  # type: ignore
    @overrides
    def standard_metadata(self, new_metadata: acvi.FileMetadata) -> None:
        if not isinstance(new_metadata, acvi.FileMetadata):
            raise acvi.exceptions.IncompatibleTypesException(
                new_metadata.variable_type.name,
                self._standard_metadata.variable_type.name)
        else:
            self._standard_metadata = new_metadata
