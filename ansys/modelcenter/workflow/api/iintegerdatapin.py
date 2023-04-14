"""Contains definitions for integer variables."""
from abc import ABC, abstractmethod

import ansys.common.variableinterop as acvi
from overrides import overrides

from .idatapin import IDatapin


class IIntegerDatapin(IDatapin, ABC):
    """Represents an integer datapin on the workflow."""

    @overrides
    @abstractmethod
    def get_metadata(self) -> acvi.IntegerMetadata:
        ...  # pragma: no cover
