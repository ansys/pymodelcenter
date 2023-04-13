"""Contains definitions for boolean variables."""
from abc import ABC, abstractmethod

import ansys.common.variableinterop as acvi
from overrides import overrides

from .ivariable import IVariable


class IBooleanVariable(IVariable, ABC):
    """Represents a boolean variable on the workflow."""

    @overrides
    @abstractmethod
    def get_metadata(self) -> acvi.BooleanArrayMetadata:
        ...  # pragma: no cover
