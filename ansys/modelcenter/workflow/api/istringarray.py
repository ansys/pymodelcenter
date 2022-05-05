import ansys.common.variableinterop as acvi
import clr
from overrides import overrides

from ansys.modelcenter.workflow.api.iarray import IArray

clr.AddReference('phoenix-mocks/Phoenix.Mock.v45')
from Phoenix.Mock import MockStringArray


class IStringArray(IArray[MockStringArray]):
    """
    Represents a boolean variable on the workflow.
    """

    @property  # type: ignore
    @overrides
    def value(self) -> acvi.StringArrayValue:
        return acvi.StringArrayValue.from_api_string(self._wrapped.toString())

    @value.setter  # type: ignore
    @overrides
    def value(self, new_value: acvi.IVariableValue):
        self._wrapped.fromString(new_value.to_api_string())

    @property  # type: ignore
    @overrides
    def value_absolute(self) -> acvi.StringArrayValue:
        return acvi.StringArrayValue.from_api_string(self._wrapped.toStringAbsolute())

    @property  # type: ignore
    @overrides
    def standard_metadata(self) -> acvi.StringArrayMetadata:
        raise NotImplementedError

    @standard_metadata.setter
    def standard_metadata(self, new_metadata: acvi.CommonVariableMetadata) -> None:
        """
        Get the standard metadata for this variable.
        """
        raise NotImplementedError
