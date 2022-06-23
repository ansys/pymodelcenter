import ansys.common.variableinterop as acvi
import clr
from overrides import overrides

from .iarray import IArray
from .ivariable import FormattableVariable

clr.AddReference('phoenix-mocks/Phoenix.Mock.v45')
from Phoenix.Mock import MockDoubleArray  # type: ignore


class IDoubleArray(IArray[MockDoubleArray], FormattableVariable[MockDoubleArray]):
    """
    Represents a double array variable on the workflow.
    """

    @overrides
    def __init__(self, wrapped: MockDoubleArray):
        super().__init__(wrapped)
        self._standard_metadata: acvi.CommonVariableMetadata = acvi.RealArrayMetadata()

    # IVariable

    @property  # type: ignore
    @overrides
    def value(self) -> acvi.RealArrayValue:
        return acvi.RealArrayValue.from_api_string(self._wrapped.toString())

    @value.setter  # type: ignore
    @overrides
    def value(self, new_value: acvi.IVariableValue):
        self._wrapped.fromString(new_value.to_api_string())

    @property  # type: ignore
    @overrides
    def value_absolute(self) -> acvi.RealArrayValue:
        return acvi.RealArrayValue.from_api_string(self._wrapped.toStringAbsolute())

    @property  # type: ignore
    @overrides
    def standard_metadata(self) -> acvi.RealArrayMetadata:
        return self._standard_metadata

    @standard_metadata.setter  # type: ignore
    @overrides
    def standard_metadata(self, new_metadata: acvi.RealArrayMetadata) -> None:
        if not isinstance(new_metadata, acvi.RealArrayMetadata):
            raise acvi.exceptions.IncompatibleTypesException(
                new_metadata.variable_type.name,
                self._standard_metadata.variable_type.name)
        else:
            self._standard_metadata = new_metadata
