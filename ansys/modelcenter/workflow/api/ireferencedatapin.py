"""Contains definitions for scalar reference datapins."""
from abc import ABC, abstractmethod

import ansys.tools.variableinterop as atvi
from overrides import overrides

from .idatapin import IDatapin


class IReferenceDatapin(IDatapin, ABC):
    """Represents a reference datapin on the workflow."""

    @overrides
    @abstractmethod
    def get_metadata(self) -> atvi.CommonVariableMetadata:  # TODO: reference metadata
        ...  # pragma: no cover
