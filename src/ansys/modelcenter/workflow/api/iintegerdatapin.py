"""Contains definitions for integer variables."""
from abc import ABC, abstractmethod

import ansys.tools.variableinterop as atvi
from overrides import overrides

from .idatapin import IDatapin


class IIntegerDatapin(IDatapin, ABC):
    """Represents an integer datapin on the workflow."""

    @overrides
    @abstractmethod
    def get_metadata(self) -> atvi.IntegerMetadata:
        ...  # pragma: no cover
