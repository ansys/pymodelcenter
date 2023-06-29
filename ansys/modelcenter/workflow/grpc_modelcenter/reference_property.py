"""Contains implementations of reference property related classes."""

from typing import Mapping

from ansys.tools import variableinterop as atvi
from overrides import overrides

from ansys.modelcenter.workflow.api import (
    IReferenceArrayProperty,
    IReferenceProperty,
    IReferencePropertyManager,
)


class ReferenceProperty(IReferenceProperty):
    """Represents a reference property."""

    @overrides
    def get_state(self) -> atvi.VariableState:
        pass

    @overrides
    def set_value(self, new_value: atvi.VariableState):
        pass

    @overrides
    def get_value_type(self) -> atvi.VariableType:
        pass

    @overrides
    def get_metadata(self) -> atvi.CommonVariableMetadata:
        pass

    @overrides
    def set_metadata(self, new_value: atvi.CommonVariableMetadata):
        pass

    @property
    @overrides
    def is_input(self) -> bool:
        return False

    @property
    @overrides
    def name(self) -> str:
        return ""


class ReferenceArrayProperty(IReferenceArrayProperty, ReferenceProperty):
    """Represents a reference array property."""

    @overrides
    def set_value_at(self, index: int, new_value: atvi.IVariableValue):
        pass


class ReferencePropertyManager(IReferencePropertyManager):
    """Provides utility methods for getting reference properties from reference datapins."""

    @overrides
    def get_reference_properties(self) -> Mapping[str, IReferenceProperty]:
        return {}
