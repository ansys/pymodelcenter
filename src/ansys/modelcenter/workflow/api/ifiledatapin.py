"""Contains definition for scalar file datapin."""
from abc import ABC, abstractmethod

import ansys.tools.variableinterop as atvi
from overrides import overrides

from .idatapin import IDatapin


class IFileDatapin(IDatapin, ABC):
    """Represents a file datapin on the workflow."""

    @overrides
    @abstractmethod
    def get_metadata(self) -> atvi.FileMetadata:
        ...  # pragma: no cover
