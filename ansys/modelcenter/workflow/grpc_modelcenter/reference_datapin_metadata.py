"""Contains a definition for reference datapin metadata."""

from typing import TypeVar

import ansys.tools.variableinterop as atvi
from overrides import overrides

T = TypeVar("T")


class ReferenceDatapinMetadata(atvi.CommonVariableMetadata):
    """Metadata for a reference datapin."""

    @overrides
    def accept(self, visitor: atvi.IVariableMetadataVisitor[T]) -> T:
        raise NotImplementedError(
            "This is a nonstandard metadata type and cannot accept standard " "metadata visitors."
        )

    @property
    @overrides
    def variable_type(self) -> atvi.VariableType:
        return atvi.VariableType.UNKNOWN
