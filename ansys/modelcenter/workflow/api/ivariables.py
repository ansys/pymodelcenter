from .arrayish import Arrayish
from .ivariable import IVariable


class IVariables(Arrayish[IVariable]):
    """A collection of IVariable objects, accessible by name or \
    integer ID."""

    def __init__(self, instance) -> None:
        """
        Initialize an arrayish collection of IVariable objects.

        Parameters
        ----------
        instance :
            ModelCenter API IVariables interface object.
        """
        Arrayish.__init__(self, instance, IVariable)
