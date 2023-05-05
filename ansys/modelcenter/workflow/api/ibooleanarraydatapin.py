"""Boolean array implementation."""
from abc import ABC, abstractmethod

import ansys.tools.variableinterop as atvi
from overrides import overrides

from .idatapin import IDatapin


class IBooleanArrayDatapin(IDatapin, ABC):
    """Represents a boolean array datapin on the workflow."""

    @overrides
    @abstractmethod
    def get_metadata(self) -> atvi.BooleanMetadata:
        ...  # pragma: no cover
