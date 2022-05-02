class RefProp:
    """COM Instance."""

    @property
    def enum_values(self) -> str:
        """Enumerated values of the reference property."""
        # BSTR enumValues;
        raise NotImplementedError

    @property
    def is_input(self) -> bool:
        """Whether or not the reference property is an input."""
        # boolean isInput;
        raise NotImplementedError

    @property
    def title(self) -> str:
        """Title of the reference property."""
        # BSTR title;
        raise NotImplementedError

    @property
    def description(self) -> str:
        """Description of the reference property."""
        # BSTR description;
        raise NotImplementedError

    def get_name(self) -> str:
        """
        Name of the reference property.

        Returns
        -------
        The name of the reference property.
        """
        # BSTR getName();
        raise NotImplementedError

    def get_type(self) -> str:
        """
        Type of the reference property.

        Returns
        -------
        The type of the reference property.
        """
        # BSTR getType();
        raise NotImplementedError
