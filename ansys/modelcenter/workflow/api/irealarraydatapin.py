"""Definitions for array of doubles variables."""
from abc import ABC, abstractmethod

import ansys.common.variableinterop as acvi
from overrides import overrides

from .idatapin import IDatapin


class IRealArrayDatapin(IDatapin, ABC):
    """Represents a datapin storing an array of reals on the workflow."""

    @overrides
    @abstractmethod
    def get_metadata(self) -> acvi.RealArrayMetadata:
        ...  # pragma: no cover
