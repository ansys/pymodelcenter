"""Contains definitions for double variables."""
from abc import ABC, abstractmethod

import ansys.common.variableinterop as acvi
from overrides import overrides

from .idatapin import IDatapin


class IRealDatapin(IDatapin, ABC):
    """Represents a datapin storing a real on the workflow."""

    @overrides
    @abstractmethod
    def get_metadata(self) -> acvi.RealMetadata:
        ...  # pragma: no cover
