"""Definitions of string array datapin."""
from abc import ABC, abstractmethod

import ansys.tools.variableinterop as atvi
from overrides import overrides

from .idatapin import IDatapin


class IStringArrayDatapin(IDatapin, ABC):
    """Represents a string datapin on the workflow."""

    @overrides
    @abstractmethod
    def get_metadata(self) -> atvi.StringArrayMetadata:
        ...  # pragma: no cover
