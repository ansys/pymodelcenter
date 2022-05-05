from __future__ import annotations

from typing import List, Sequence

import clr

clr.AddReference(r"phoenix-mocks\Phoenix.Mock.v45")
from Phoenix.Mock import MockGroup, MockGroups, MockVariables


class IGroup:
    """COM Instance."""

    def __init__(self, group: MockGroup):
        """Initialize."""
        self._instance = group

    @property
    def variables(self) -> Sequence[object]:  # TODO: Variable
        """The variables in the Group."""
        result: List[object] = []  # TODO: Variable
        variables: MockVariables = self._instance.Variables
        for i in range(variables.Count):
            result.append(variables.Item(i))  # TODO: wrap in Variable
        return result

    @property
    def groups(self) -> 'IGroups':
        """The Groups this Group is a member of."""
        from .igroups import IGroups
        return IGroups(self._instance.Groups)

    @property
    def icon_id(self) -> int:
        """The ID number of the icon to use for the Group."""
        return self._instance.iconId

    @icon_id.setter
    def icon_id(self, id: int) -> None:
        """The ID number of the icon to use for the Group."""
        self._instance.iconId = id

    def get_name(self) -> str:
        """Gets the name of the Group."""
        return self._instance.getName()

    def get_full_name(self) -> str:
        """Gets the full %ModelCenter path of the Group."""
        return self._instance.getFullName()
