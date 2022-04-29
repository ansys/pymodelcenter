
class IAssemblies:
    """
    COM Instance.
    """

    @property
    def count(self):
        """Number of Assemblies."""
        # VARIANT Count;
        raise NotImplementedError

    def item(self, id: int) -> object:   # IAssembly:
        """
        Gets a pointer to the specified Assembly.

        Parameters
        ----------
        id : int
            ID of the specified Assembly. It can be a name or an index.
        Returns
        -------
        IAssembly object.
        """
        # VARIANT Item(VARIANT id);
        raise NotImplementedError
