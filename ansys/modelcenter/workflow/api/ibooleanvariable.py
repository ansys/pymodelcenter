from typing import Optional

import ansys.common.variableinterop as acvi
import clr
from overrides import overrides

from ansys.modelcenter.workflow.api.ivariable import ScalarVariable

clr.AddReference('phoenix-mocks/Phoenix.Mock.v45')
from Phoenix.Mock import MockBooleanVariable


class IBooleanVariable(ScalarVariable[MockBooleanVariable]):
    """Represents a boolean variable on the workflow."""

    @overrides
    def __init__(self, wrapped: MockBooleanVariable):
        super().__init__(wrapped)
        self._standard_metadata: acvi.CommonVariableMetadata = acvi.BooleanMetadata()

    # ansys.engineeringworkflow.api.IVariable

    @overrides
    def get_value(self, hid: Optional[str]) -> acvi.VariableState:
        return acvi.VariableState(
            acvi.BooleanValue(self._wrapped.value),
            self._wrapped.isValid())

    # @property  # type: ignore
    # @overrides
    # def value(self) -> acvi.BooleanValue:
    #     return acvi.BooleanValue(self._wrapped.value)
    #
    # @value.setter  # type: ignore
    # @overrides
    # def value(self, new_value: acvi.IVariableValue):
    #     self._wrapped.fromString(new_value.to_api_string())

    @property  # type: ignore
    @overrides
    def value_absolute(self) -> acvi.BooleanValue:
        return acvi.BooleanValue(self._wrapped.valueAbsolute)

    @overrides
    def set_initial_value(self, value: acvi.IVariableValue) -> None:
        self._wrapped.setInitialValue(bool(acvi.to_boolean_value(value)))

    @property  # type: ignore
    @overrides
    def standard_metadata(self) -> acvi.BooleanMetadata:
        return self._standard_metadata

    @standard_metadata.setter  # type: ignore
    @overrides
    def standard_metadata(self, new_metadata: acvi.BooleanMetadata) -> None:
        if not isinstance(new_metadata, acvi.BooleanMetadata):
            raise acvi.exceptions.IncompatibleTypesException(
                new_metadata.variable_type.name,
                self._standard_metadata.variable_type.name)
        else:
            self._standard_metadata = new_metadata
