import ansys.common.variableinterop as acvi
import clr
from overrides import overrides

from ansys.modelcenter.workflow.api.ivariable import ScalarVariable

clr.AddReference('phoenix-mocks/Phoenix.Mock.v45')
from Phoenix.Mock import MockIntegerVariable


class IIntegerVariable(ScalarVariable[MockIntegerVariable]):
    """
    Represents an integer variable on the workflow.
    """

    @property  # type: ignore
    @overrides
    def value(self) -> acvi.IntegerValue:
        return acvi.IntegerValue(self._wrapped.value)

    @value.setter  # type: ignore
    @overrides
    def value(self, new_value: acvi.IVariableValue):
        self._wrapped.fromString(new_value.to_api_string())

    @property  # type: ignore
    @overrides
    def value_absolute(self) -> acvi.IntegerValue:
        return acvi.IntegerValue(self._wrapped.valueAbsolute)

    @overrides
    def set_initial_value(self, value: acvi.IVariableValue) -> None:
        self._wrapped.setInitialValue(int(acvi.to_integer_value(value)))

    @property  # type: ignore
    @overrides
    def standard_metadata(self) -> acvi.IntegerMetadata:
        raise NotImplementedError

    @standard_metadata.setter
    def standard_metadata(self, new_metadata: acvi.CommonVariableMetadata) -> None:
        """
        Get the standard metadata for this variable.
        """
        raise NotImplementedError
