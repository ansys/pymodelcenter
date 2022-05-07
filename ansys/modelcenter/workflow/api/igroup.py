from __future__ import annotations

import clr

from ansys.modelcenter.workflow.api.arrayish import Arrayish
from ansys.modelcenter.workflow.api.ivariable import IVariable

clr.AddReference("phoenix-mocks/Interop.ModelCenter")
from ModelCenter import IGroup as mcapiIGroup


class IGroup:
    """COM Instance."""

    def __init__(self, group: mcapiIGroup):
        """Initialize."""
        self._instance = group

    @property
    def variables(self) -> Sequencial[IVariable]:
        """The variables in the Group."""
        return Arrayish(self._instance.Variables, IVariable)

    @property
    def groups(self) -> Sequencial[IGroup]:
        """The Groups this Group is a member of."""
        return Arrayish(self._instance.Groups, IGroup)

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
