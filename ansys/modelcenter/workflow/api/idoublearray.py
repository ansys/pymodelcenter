"""Definitions for array of doubles variables."""
from abc import ABC, abstractmethod

import ansys.common.variableinterop as acvi
from overrides import overrides

from .iarray import IArray


class IDoubleArray(IArray, ABC):
    """Represents a double array variable on the workflow."""

    @overrides
    @abstractmethod
    def get_metadata(self) -> acvi.RealArrayMetadata:
        raise NotImplementedError()
