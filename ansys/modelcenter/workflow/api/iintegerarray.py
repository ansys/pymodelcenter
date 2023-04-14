"""Definition of integer array variable."""
from abc import ABC, abstractmethod

import ansys.common.variableinterop as acvi
from overrides import overrides

from .ivariable import IVariable


class IIntegerArray(IVariable, ABC):
    """Represents an integer array variable on the workflow."""

    @overrides
    @abstractmethod
    def get_metadata(self) -> acvi.IntegerArrayMetadata:
        ...  # pragma: no cover
