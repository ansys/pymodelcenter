"""Definitions for array of doubles variables."""
from abc import ABC, abstractmethod

import ansys.tools.variableinterop as atvi
from overrides import overrides

from .idatapin import IDatapin


class IRealArrayDatapin(IDatapin, ABC):
    """Represents a datapin storing an array of reals on the workflow."""

    @overrides
    @abstractmethod
    def get_metadata(self) -> atvi.RealArrayMetadata:
        ...  # pragma: no cover
