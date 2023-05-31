"""Contains definitions for array reference datapins."""
from abc import ABC, abstractmethod

import ansys.tools.variableinterop as atvi
from overrides import overrides

from .idatapin import IDatapin


class IReferenceArrayDatapin(IDatapin, ABC):
    """Represents a boolean array datapin on the workflow."""

    @overrides
    @abstractmethod
    def get_metadata(self) -> atvi.CommonVariableMetadata:  # TODO: reference metadata
        ...  # pragma: no cover
