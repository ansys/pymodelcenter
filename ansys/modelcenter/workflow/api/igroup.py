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

    # TODO / REDUCE: Consider dropping for Phase II or entirely
    @property
    @abstractmethod
    def icon_id(self) -> int:
        """The ID number of the icon to use for the Group."""
        raise NotImplementedError()

    # TODO / REDUCE: Consider dropping for Phase II or entirely
    @icon_id.setter
    @abstractmethod
    def icon_id(self, id: int) -> None:
        """The ID number of the icon to use for the Group."""
        raise NotImplementedError()
