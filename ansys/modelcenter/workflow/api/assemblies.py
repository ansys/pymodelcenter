
class Assemblies:
    """
    COM Instance.
    """

    @property
    def count(self):
        """Number of Assemblies."""
        # VARIANT Count;
        raise NotImplementedError

    def item(self, id_: int) -> object:   # Assembly:
        """
        Get a pointer to the specified Assembly.

        Parameters
        ----------
        id_ : int
            ID of the specified Assembly. It can be a name or an index.

        Returns
        -------
        Assembly object.
        """
        # VARIANT Item(VARIANT id);
        raise NotImplementedError
