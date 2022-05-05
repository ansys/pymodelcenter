import ansys.common.variableinterop as acvi
import clr
from overrides import overrides

from ansys.modelcenter.workflow.api.iarray import IArray

clr.AddReference('phoenix-mocks/Phoenix.Mock.v45')
from Phoenix.Mock import MockBooleanArray


class IBooleanArray(IArray[MockBooleanArray]):
    """
    Represents a boolean array variable on the workflow.
    """

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
        raise NotImplementedError

    @standard_metadata.setter
    def standard_metadata(self, new_metadata: acvi.CommonVariableMetadata) -> None:
        """
        Get the standard metadata for this variable.
        """
        raise NotImplementedError
