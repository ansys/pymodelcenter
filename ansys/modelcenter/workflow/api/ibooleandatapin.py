"""Contains definitions for boolean variables."""
from abc import ABC, abstractmethod

import ansys.common.variableinterop as acvi
from overrides import overrides

from .idatapin import IDatapin


class IBooleanDatapin(IDatapin, ABC):
    """Represents a boolean datapin on the workflow."""

    @overrides
    @abstractmethod
    def get_metadata(self) -> acvi.BooleanArrayMetadata:
        ...  # pragma: no cover
