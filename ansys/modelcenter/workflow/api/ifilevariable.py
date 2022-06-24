from typing import Optional

import ansys.common.variableinterop as acvi
import clr
from overrides import overrides

from .i18n import i18n
from .ivariable import IVariable

clr.AddReference('phoenix-mocks/Phoenix.Mock.v45')
from Phoenix.Mock import MockFileVariable  # type: ignore


class IFileVariable(IVariable[MockFileVariable]):
    """Represents a file variable in the workflow."""

    @overrides
    def __init__(self, wrapped: MockFileVariable):
        super().__init__(wrapped)
        self._standard_metadata: acvi.CommonVariableMetadata = acvi.FileMetadata()

    @overrides
    def get_value(self, hid: Optional[str]) -> acvi.VariableState:
        if hid is not None:
            raise NotImplemented(i18n('Exceptions', 'ERROR_METADATA_TYPE_NOT_ALLOWED'))

        return None
        # return acvi.VariableState(self.value, self._wrapped.isValid())

    @overrides
    def set_value(self, value: acvi.VariableState) -> None:
        if value is None:
            self._wrapped.value = None
        else:
            self.value = value.value

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
        return None
        # TODO: Implement acvi.FileValue.from_api_string().
        # return acvi.FileValue.from_api_string(self._wrapped.toString())
        # Or:
        # TODO: Actual implementation might require async.
        # This should not be a property then, according to PEP8:
        #   Avoid using properties for computationally expensive operations;
        #   the attribute notation makes the caller believe that access is (relatively) cheap.
        # TODO: Implement FileScope.read_from_string()
        # return acvi.FileScope.read_from_string(contents, mime, encoding)

    @value.setter
    @overrides
    def value(self, new_value: acvi.FileValue) -> None:
        """
        Set value of the variable.

        Parameters
        ----------
        new_value : FileValue
            Value of the file variable.
        """
        if new_value is None:
            self._wrapped.value = None
        else:
            # TODO: Get save context.
            self._wrapped.fromString(new_value.to_api_string(None))
        # Or:
        # TODO: Actual implementation might require async.
        # See notes for the get property.
        # self._wrapped.value = await new_value.get_contents(new_value.file_encoding)

    @property
    @overrides
    def value_absolute(self) -> acvi.FileValue:
        return self.value

    @value_absolute.setter
    @overrides
    def value_absolute(self, value: acvi.FileValue) -> None:
        self.value = value

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
