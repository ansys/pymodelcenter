class IGroups:
    """COM Instance."""

    def count(self):
        """Number of Groups."""
        # VARIANT Count;
        raise NotImplementedError

    def item(self, id_) -> object:
        """
        Gets a pointer to the specified Group.

        Parameters
        ----------
        id_ :
            ID of the specified Group. It can be a name or an index
            (0-based index).

        Returns
        -------
        An IGroup object.
        """
        # VARIANT Item(VARIANT id);
        raise NotImplementedError
