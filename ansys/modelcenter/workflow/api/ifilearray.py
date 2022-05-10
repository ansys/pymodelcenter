import ansys.common.variableinterop as acvi
from typing import Optional
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

    @property  # type: ignore
    @overrides
    def value(self) -> acvi.FileArrayValue:
        return acvi.FileArrayValue.from_api_string(self._wrapped.toString())

    @value.setter  # type: ignore
    @overrides
    def value(self, new_value: acvi.IVariableValue):
        self._wrapped.fromString(new_value.to_api_string())

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
