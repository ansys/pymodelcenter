import ansys.modelcenter.workflow.api.arrayish as arrayish
import ansys.modelcenter.workflow.api.igroup as igroup


class IGroups(arrayish.Arrayish['igroup.IGroup']):
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
        arrayish.Arrayish.__init__(self, instance, igroup.IGroup)
