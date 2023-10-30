"""Definition of integer array datapin."""
from abc import ABC, abstractmethod

import ansys.tools.variableinterop as atvi
from overrides import overrides

from .idatapin import IDatapin


class IIntegerArrayDatapin(IDatapin, ABC):
    """Represents an integer array datapin on the workflow."""

    @overrides
    @abstractmethod
    def get_metadata(self) -> atvi.IntegerArrayMetadata:
        ...  # pragma: no cover
