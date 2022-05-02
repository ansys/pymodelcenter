from .arrayish import Arrayish
from .group import Group


class Groups(Arrayish[Group]):
    """A collection of Groups, accessible by name or integer ID."""

    def __init__(self, instance) -> None:
        """
        Initialize an arrayish collection of Group objects.

        Parameters
        ----------
        instance :
            ModelCenter API groups interface object.
        """
        Arrayish.__init__(self, instance, Group)
