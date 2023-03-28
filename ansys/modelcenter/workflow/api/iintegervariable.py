"""Contains definitions for integer variables."""
from abc import ABC, abstractmethod

import ansys.common.variableinterop as acvi
from overrides import overrides

from .ivariable import IVariable


class IIntegerVariable(IVariable, ABC):
    """Represents an integer variable on the workflow."""

    @overrides
    @abstractmethod
    def get_metadata(self) -> acvi.IntegerMetadata:
        raise NotImplementedError()
