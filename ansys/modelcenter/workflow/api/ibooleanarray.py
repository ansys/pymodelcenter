"""Boolean array implementation."""
from abc import ABC, abstractmethod

import ansys.common.variableinterop as acvi
from overrides import overrides

from .iarray import IArray


class IBooleanArray(IArray, ABC):
    """Represents a boolean array variable on the workflow."""

    @overrides
    @abstractmethod
    def get_metadata(self) -> acvi.BooleanMetadata:
        ...  # pragma: no cover
