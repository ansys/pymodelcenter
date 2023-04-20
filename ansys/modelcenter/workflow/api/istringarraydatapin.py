"""Definitions of string array variable."""
from abc import ABC, abstractmethod

import ansys.common.variableinterop as acvi
from overrides import overrides

from .idatapin import IDatapin


class IStringArrayDatapin(IDatapin, ABC):
    """Represents a string datapin on the workflow."""

    @overrides
    @abstractmethod
    def get_metadata(self) -> acvi.StringArrayMetadata:
        ...  # pragma: no cover
