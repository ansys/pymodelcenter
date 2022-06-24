import ansys.common.variableinterop as acvi
import clr
from overrides import overrides

from .iarray import IArray

clr.AddReference("phoenix-mocks/Phoenix.Mock.v45")
from Phoenix.Mock import MockBooleanArray  # type: ignore


class IBooleanArray(IArray[MockBooleanArray]):
    """
    Represents a boolean array variable on the workflow.
    """

    @overrides
    def __init__(self, wrapped: MockBooleanArray):
        super().__init__(wrapped)
        self._standard_metadata: acvi.CommonVariableMetadata = acvi.BooleanArrayMetadata()

    # IVariable

    @property  # type: ignore
    @overrides
    def value(self) -> acvi.BooleanArrayValue:
        return acvi.BooleanArrayValue.from_api_string(self._wrapped.toString())

    @value.setter  # type: ignore
    @overrides
    def value(self, new_value: acvi.IVariableValue):
        self._wrapped.fromString(new_value.to_api_string())

    @property  # type: ignore
    @overrides
    def value_absolute(self) -> acvi.BooleanArrayValue:
        return acvi.BooleanArrayValue.from_api_string(self._wrapped.toStringAbsolute())

    @property  # type: ignore
    @overrides
    def standard_metadata(self) -> acvi.BooleanArrayMetadata:
        return self._standard_metadata

    @standard_metadata.setter  # type: ignore
    @overrides
    def standard_metadata(self, new_metadata: acvi.BooleanArrayMetadata) -> None:
        if not isinstance(new_metadata, acvi.BooleanArrayMetadata):
            raise acvi.exceptions.IncompatibleTypesException(
                new_metadata.variable_type.name, self._standard_metadata.variable_type.name
            )
        else:
            self._standard_metadata = new_metadata
