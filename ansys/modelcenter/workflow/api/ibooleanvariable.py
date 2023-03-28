"""Contains definitions for boolean variables."""
from abc import ABC, abstractmethod

import ansys.common.variableinterop as acvi
from overrides import overrides

from .ivariable import IVariable


class IBooleanVariable(IVariable, ABC):
    """Represents a boolean variable on the workflow."""

    # TODO: We probably want type-specific implementations,
    #       but is there any value in type-specific interfaces here?

    @overrides
    @abstractmethod
    def get_metadata(self) -> acvi.BooleanArrayMetadata:
        raise NotImplementedError()
