"""Definition of group of variables."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Collection

from ansys.engineeringworkflow.api import IVariableContainer


class IGroup(IVariableContainer, ABC):
    """Represents a variable group in ModelCenter."""

    @property
    @abstractmethod
    def groups(self) -> Collection["IGroup"]:
        """The groups that this group contains."""
        raise NotImplementedError()
