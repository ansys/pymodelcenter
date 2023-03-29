"""Definition of group of variables."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Collection

from ansys.engineeringworkflow.api import IVariableContainer


class IGroupOwner(IVariableContainer, ABC):
    """Represents a workflow element which has groups in ModelCenter."""

    @property
    @abstractmethod
    def groups(self) -> Collection["IGroup"]:
        """The groups that this item contains."""


class IGroup(IGroupOwner, ABC):
    """Represents a variable group in ModelCenter."""

    pass
