import ansys.common.variableinterop as acvi
import clr
from overrides import overrides

from ansys.modelcenter.workflow.api.ivariable import ScalarVariable

clr.AddReference('phoenix-mocks/Phoenix.Mock.v45')
from Phoenix.Mock import MockDoubleVariable


class IDoubleVariable(ScalarVariable[MockDoubleVariable]):
    """
    Represents a double / real variable on the workflow.
    """

    @overrides
    def __init__(self, wrapped: MockDoubleVariable):
        super().__init__(wrapped)
        self._standard_metadata: acvi.CommonVariableMetadata = acvi.RealMetadata()

    @property  # type: ignore
    @overrides
    def value(self) -> acvi.RealValue:
        return acvi.RealValue(self._wrapped.value)

    @value.setter  # type: ignore
    @overrides
    def value(self, new_value: acvi.IVariableValue):
        self._wrapped.fromString(new_value.to_api_string())

    @property  # type: ignore
    @overrides
    def value_absolute(self) -> acvi.RealValue:
        return acvi.RealValue(self._wrapped.valueAbsolute)

    @overrides
    def set_initial_value(self, value: acvi.IVariableValue) -> None:
        self._wrapped.setInitialValue(float(acvi.to_real_value(value)))

    @property  # type: ignore
    @overrides
    def standard_metadata(self) -> acvi.RealMetadata:
        return self._standard_metadata

    @standard_metadata.setter  # type: ignore
    @overrides
    def standard_metadata(self, new_metadata: acvi.RealMetadata) -> None:
        if not isinstance(new_metadata, acvi.RealMetadata):
            raise acvi.exceptions.IncompatibleTypesException(
                new_metadata.variable_type.name,
                self._standard_metadata.variable_type.name)
        else:
            self._standard_metadata = new_metadata
