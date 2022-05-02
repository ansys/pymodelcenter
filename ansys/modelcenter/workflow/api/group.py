class Group:
    """COM Instance."""

    def variables(self) -> object:
        """The variables in the Group."""
        # VARIANT Variables;
        raise NotImplementedError

    def groups(self) -> object:     # Group
        """The Groups this Group is a member of."""
        # VARIANT Groups;
        raise NotImplementedError

    def icon_id(self) -> int:
        """The ID number of the icon to use for the Group."""
        # int iconID;
        raise NotImplementedError

    def get_name(self) -> str:
        """Gets the name of the Group."""
        # BSTR getName();
        raise NotImplementedError

    def get_full_name(self) -> str:
        """Gets the full %ModelCenter path of the Group."""
        # BSTR getFullName();
        raise NotImplementedError
