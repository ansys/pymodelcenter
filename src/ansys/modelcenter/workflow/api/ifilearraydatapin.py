"""Contains definition for array file datapin."""
from abc import ABC, abstractmethod

import ansys.tools.variableinterop as atvi
from overrides import overrides

from .idatapin import IDatapin


class IFileArrayDatapin(IDatapin, ABC):
    """Represents a file datapin on the workflow."""

    @overrides
    @abstractmethod
    def get_metadata(self) -> atvi.FileArrayMetadata:
        ...  # pragma: no cover
