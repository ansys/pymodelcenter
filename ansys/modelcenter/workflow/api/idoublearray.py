"""Definitions for array of doubles variables."""
from abc import ABC, abstractmethod

import ansys.common.variableinterop as acvi
from overrides import overrides

from .ivariable import IVariable


class IDoubleArray(IVariable, ABC):
    """Represents a double array variable on the workflow."""

    @overrides
    @abstractmethod
    def get_metadata(self) -> acvi.RealArrayMetadata:
        ...  # pragma: no cover
