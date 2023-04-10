"""Definitions of string array variable."""
from abc import ABC, abstractmethod

import ansys.common.variableinterop as acvi
from overrides import overrides

from .iarray import IArray


class IStringArray(IArray, ABC):
    """Represents a string variable on the workflow."""

    @overrides
    @abstractmethod
    def get_metadata(self) -> acvi.StringArrayMetadata:
        ...  # pragma: no cover
