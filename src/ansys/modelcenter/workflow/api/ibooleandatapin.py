"""Contains definitions for boolean variables."""
from abc import ABC, abstractmethod

import ansys.tools.variableinterop as atvi
from overrides import overrides

from .idatapin import IDatapin


class IBooleanDatapin(IDatapin, ABC):
    """Represents a boolean datapin on the workflow."""

    @overrides
    @abstractmethod
    def get_metadata(self) -> atvi.BooleanArrayMetadata:
        ...  # pragma: no cover
