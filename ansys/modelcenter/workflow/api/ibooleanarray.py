"""Boolean array implementation."""
from abc import ABC, abstractmethod

import ansys.common.variableinterop as acvi
from overrides import overrides

from .ivariable import IVariable


class IBooleanArray(IVariable, ABC):
    """Represents a boolean array variable on the workflow."""

    @overrides
    @abstractmethod
    def get_metadata(self) -> acvi.BooleanMetadata:
        ...  # pragma: no cover
