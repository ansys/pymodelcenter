"""Definition of group of variables."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Mapping

from ansys.engineeringworkflow.api import IDatapinContainer


class IGroupOwner(IDatapinContainer, ABC):
    """Represents a workflow element which has groups in ModelCenter."""

    @property
    @abstractmethod
    def groups(self) -> Mapping[str, "IGroup"]:
        """The groups that this item contains."""


class IGroup(IGroupOwner, ABC):
    """Represents a variable group in ModelCenter."""

    ...  # pragma: no cover
