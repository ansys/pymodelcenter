"""Contains definitions for double variables."""
from abc import ABC, abstractmethod

import ansys.common.variableinterop as acvi
from overrides import overrides

from .ivariable import IVariable


class IDoubleVariable(IVariable, ABC):
    """Represents a double / real variable on the workflow."""

    @overrides
    @abstractmethod
    def get_metadata(self) -> acvi.RealMetadata:
        raise NotImplementedError()
