"""Definitions for array of doubles variables."""
from abc import ABC, abstractmethod

import ansys.common.variableinterop as acvi
from overrides import overrides

from .ivariable import IVariable


class IRealArrayVariable(IVariable, ABC):
    """Represents a variable storing an array of reals on the workflow."""

    @overrides
    @abstractmethod
    def get_metadata(self) -> acvi.RealArrayMetadata:
        ...  # pragma: no cover
