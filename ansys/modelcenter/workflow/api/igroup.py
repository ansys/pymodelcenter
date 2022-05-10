from __future__ import annotations

from typing import Sequence

import clr

from ansys.modelcenter.workflow.api.arrayish import Arrayish
import ansys.modelcenter.workflow.api.ivariable as ivariable

clr.AddReference("phoenix-mocks/Interop.ModelCenter")
from ModelCenter import IGroup as mcapiIGroup


class IGroup:
    """COM Instance."""

    def __init__(self, group: mcapiIGroup):
        """Initialize."""
        self._instance = group

    @property
    def variables(self) -> 'Sequence[ivariable.IVariable]':
        """The variables in the Group."""
        return Arrayish(self._instance.Variables, ivariable.IVariable)

    @property
    def groups(self) -> 'Sequence[IGroup]':
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
