"""Contains definitions for double variables."""
from abc import ABC, abstractmethod

import ansys.common.variableinterop as acvi
from overrides import overrides

from .ivariable import IVariable


class IRealVariable(IVariable, ABC):
    """Represents a variable storing a real on the workflow."""

    @overrides
    @abstractmethod
    def get_metadata(self) -> acvi.RealMetadata:
        ...  # pragma: no cover
