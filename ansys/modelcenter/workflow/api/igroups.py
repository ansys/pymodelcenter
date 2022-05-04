from .arrayish import Arrayish
from .igroup import IGroup


class IGroups(Arrayish[IGroup]):
    """A collection of IGroup objects, accessible by name or integer
    ID."""

    def __init__(self, instance) -> None:
        """
        Initialize an arrayish collection of IGroup objects.

        Parameters
        ----------
        instance :
            ModelCenter API IGroups interface object.
        """
        Arrayish.__init__(self, instance, IGroup)
