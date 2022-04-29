class IRefArrayProp:
    """COM Instance."""

    @property
    def enum_values(self) -> str:
        """Enumerated values of the reference array property."""
        # BSTR enumValues;
        raise NotImplementedError

    @property
    def is_input(self) -> bool:
        """Enumerated values of the reference array property."""
        # boolean isInput;
        raise NotImplementedError

    @property
    def title(self) -> str:
        """Title of the reference array property."""
        # BSTR title;
        raise NotImplementedError

    @property
    def description(self) -> str:
        """Description of the reference array property."""
        # BSTR description;

    def get_name(self) -> str:
        """
        Name of the reference array property.

        Returns
        -------
        The name of the reference array property.
        """
        # BSTR getName();
        raise NotImplementedError

    def get_type(self) -> str:
        """
        Type of the reference array property.

        Returns
        -------
        The type of the reference array property.
        """
        # BSTR getType();
        raise NotImplementedError
