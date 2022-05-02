
class IGlobalParameters:
    """
    A set of name/value pairs that can be used for programmatic \
    purposes.

    Values are not stored with Model files. They can optionally be
    passed up to external servers, such as MCRE server.
    """

    def count(self) -> int:
        """The count of the name/value pairs."""
        # long count;
        raise NotImplementedError

    def get_item(self, index) -> object:
        """
        Receives the value of a particular parameter.

        Parameters
        ----------
        index :
            The name of the name/value pair to retrieve.

        Returns
        -------
        The value of the parameter.
        """
        # VARIANT item(VARIANT index);
        raise NotImplementedError

    def set_item(self, index, new_value: object) -> None:
        """
        Receives the value of a particular parameter.

        Parameters
        ----------
        index :
            The name of the name/value pair to retrieve.
        new_value :
            The variable to hold the value of the parameter.
        """
        # void item(VARIANT index, VARIANT newValue);
        raise NotImplementedError

    def set_sxport_to_remote_components(
            self, index, bexport: bool) -> None:
        """
        Sets whether this name/value pair is passed to external \
        servers when a component is run on that server.

        Parameters
        ----------
        index :
            The name of the variable.
        bexport :
            If true, this name/value pair will be sent.
        """
        # void setExportToRemoteComponents(
        #       VARIANT index, boolean bexport);
        raise NotImplementedError

    def remove(self, index) -> None:
        """
        Removes a named parameter.

        Parameters
        ----------
        index :
            The name of the parameter to remove.
        """
        # void Remove(VARIANT index);
        raise NotImplementedError
