"""Definition of integer array variable."""
from abc import ABC, abstractmethod

import ansys.common.variableinterop as acvi
from overrides import overrides

from .idatapin import IDatapin


class IIntegerArray(IDatapin, ABC):
    """Represents an integer array datapin on the workflow."""

    @overrides
    @abstractmethod
    def get_metadata(self) -> acvi.IntegerArrayMetadata:
        ...  # pragma: no cover
