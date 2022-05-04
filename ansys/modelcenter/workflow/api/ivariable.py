class IVariable:
    """A PLACE HOLDER IMPLEMENTATION TO BE REPLACED BY ACTUAL \
    IMPLEMENTATION WHEN MERGED.

    WHEN RESOLVING MERGE CONFLICT TAKE OTHER, SAVE POSSIBLY THE __init__
    METHOD.
    """

    def __init__(self, instance) -> None:
        """
        Initializer.

        Parameters
        ----------
        instance :
            ModelCenter API IVariable interface object.
        """
        self._instance = instance

    def get_name(self) -> str:
        return self._instance.getName()
