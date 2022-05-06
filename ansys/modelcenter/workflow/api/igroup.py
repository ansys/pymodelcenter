from __future__ import annotations

from typing import List, Sequence

import clr

import ansys.modelcenter.workflow.api.dot_net_utils as utils
import ansys.modelcenter.workflow.api.ivariable as ivariable

clr.AddReference(r"phoenix-mocks\Phoenix.Mock.v45")
from Phoenix.Mock import MockGroup, MockGroups, MockVariables


class IGroup:
    """COM Instance."""

    def __init__(self, group: MockGroup):
        """Initialize."""
        self._instance = group

    @property
    def variables(self) -> Sequence[ivariable.IVariable]:  # TODO: Variable
        """The variables in the Group."""
        return utils.create_dot_net_variable_sequence(self._instance.Variables)

    @property
    def groups(self) -> Sequence[IGroup]:
        """The Groups this Group is a member of."""
        result: List[IGroup] = []
        groups: MockGroups = self._instance.Groups
        for i in range(groups.Count):
            result.append(IGroup(groups.Item(i)))
        return result

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
