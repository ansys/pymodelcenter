"""Implementation of IVariables class."""

import ansys.modelcenter.workflow.api.ivariable as ivariable

from .arrayish import Arrayish


class IVariables(Arrayish['ivariable.IVariable']):
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
        Arrayish.__init__(self, instance, ivariable.IVariable)
