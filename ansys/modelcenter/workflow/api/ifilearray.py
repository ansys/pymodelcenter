import ansys.common.variableinterop as acvi
import clr
from overrides import overrides
from ansys.modelcenter.workflow.api.iarray import IArray

clr.AddReference('phoenix-mocks/Phoenix.Mock.v45')
from Phoenix.Mock import MockFileArray


class IFileArray(IArray[MockFileArray]):
    """Represents a file array variable in the workflow."""

    @overrides
    def __init__(self, wrapped: MockFileArray):
        super().__init__(wrapped)
        self._standard_metadata: acvi.CommonVariableMetadata = acvi.FileArrayMetadata()

    @property
    @overrides
    def value(self) -> acvi.FileArrayValue:
        """
        Value of the variable.

        Returns
        -------
        FileArrayValue :
            Value of the file array variable.
        """
        string: str = self._wrapped.toString()
        return None
        # TODO: Implement acvi.FileArrayValue.from_api_string().
        # return acvi.FileArrayValue.from_api_string(string)

    @value.setter
    @overrides
    def value(self, new_value: acvi.FileArrayValue):
        """
        Set value of the variable.

        Parameters
        ----------
        new_value : FileArrayValue
            Value of the file array variable.
        """
        if new_value is None:
            self._wrapped.fromString(None)
        else:
            self._wrapped.fromString(new_value.to_api_string())

    @property
    @overrides
    def value_absolute(self) -> acvi.FileArrayValue:
        return self.value

    @value_absolute.setter
    @overrides
    def value_absolute(self, value: acvi.FileArrayValue) -> None:
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

    @property  # type: ignore
    @overrides
    def standard_metadata(self) -> acvi.FileArrayMetadata:
        return self._standard_metadata

    @standard_metadata.setter  # type: ignore
    @overrides
    def standard_metadata(self, new_metadata: acvi.FileArrayMetadata) -> None:
        if not isinstance(new_metadata, acvi.FileArrayMetadata):
            raise acvi.exceptions.IncompatibleTypesException(
                new_metadata.variable_type.name,
                self._standard_metadata.variable_type.name)
        else:
            self._standard_metadata = new_metadata
