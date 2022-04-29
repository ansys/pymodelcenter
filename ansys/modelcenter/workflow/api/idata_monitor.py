
class IDataMonitor:
    """COM Instance."""

    def get_name(self, row: int) -> str:
        """
        Parameters
        ----------
        row :
            The row number in the Data Monitor of interest (0-based index).

        Returns
        -------
        The name of the row.

        """
        # BSTR getName( long row );
        raise NotImplementedError

    def set_name(self, row: int, name: str) -> None:
        """
        Sets the display name of the specified row in the Data Monitor.

        Parameters
        ----------
        row : int
            The row in the Data Monitor of interest (0-based index).
        name : str
            The new display name.
        """
        # void setName( long row, BSTR name );
        raise NotImplementedError

    def is_renamed(self, row: int) -> bool:
        """
        Determines whether the name of a row in the Data Monitor lines \
        up to the %ModelCenter variable it represents.

        Parameters
        ----------
        row : int
            The row in the Data Monitor of interest (0-based index).

        Returns
        -------
        true or false
        """
        # boolean isRenamed( long row );
        raise NotImplementedError

    def get_link(self, row: int) -> str:
        """
        Retrieves the %ModelCenter variable associated with a given row in the Data Monitor.

        Returns a blank string if the specified row doesn't link to a %ModelCenter variable.

        Parameters
        ----------
        row :
            The row number in the Data Monitor of interest (0-based index).

        Returns
        -------

        """
        # BSTR getLink ( long row );
        raise NotImplementedError

    def set_link(self, row: int, link: str) -> bool:
        """
        Sets the %ModelCenter variable associated with a given row in the Data Monitor.

        Parameters
        ----------
        row :
            The row in the Data Monitor of interest (0-based index).
        link :
            The %ModelCenter variable to associate with a given row in the Data Monitor.

        Returns
        -------

        """
        # boolean setLink( long row, BSTR link );
        raise NotImplementedError

    def add_item(self, name: str, link: str) -> int:
        """
        Add an item to the Data Monitor that links to a variable in the model.

        Parameters
        ----------
        name :
            The name to use for the item in the Data Monitor.
        link :
            The name of the %ModelCenter variable this item links to.

        Returns
        -------

        """
        # int addItem( BSTR name, BSTR link );
        raise NotImplementedError

    def add_unlinked_item(self, name: str) -> int:
        """
        Add an item to the Data Monitor that does not link to a variable within %ModelCenter.

        Parameters
        ----------
        name :
            The name to use for the item in the Data Monitor.

        Returns
        -------

        """
        # int addUnlinkedItem( BSTR name );
        raise NotImplementedError

    def remove_item(self, row: int) -> None:
        """
        Removes the selected row from the Data Monitor.

        Parameters
        ----------
        row : int
            The row in the Data Monitor of interest (0-based index).
        """
        # void removeItem( long row );
        raise NotImplementedError

    def remove_link(self, row: int) -> None:
        """
        Removes the associated link from the row specified in the Data \
        Monitor.

        Parameters
        ----------
        row :
        The row in the Data Monitor of interest (0-based index).
        """
        # void removeLink( long row );
        raise NotImplementedError

    def get_display_full_names(self) -> bool:
        """Get the status of the "Display Full Names" option."""
        # boolean getDisplayFullNames( );
        raise NotImplementedError

    def set_display_full_names(self, display_full_names: bool) -> None:
        """Sets the "Display Full Names" option."""
        # void setDisplayFullNames( boolean );
        raise NotImplementedError

    def get_auto_delete(self) -> bool:
        """Gets the status of the Auto Delete option."""
        # boolean getAutoDelete( );
        raise NotImplementedError

    def set_auto_delete(self, auto_delete: bool) -> None:
        """Sets the status of the Auto Delete option."""
        # void setAutoDelete( boolean );
        raise NotImplementedError

    def get_display_units(self) -> bool:
        """Get the status of the "Display Units" option."""
        # boolean getDisplayUnits( );
        raise NotImplementedError

    def set_display_units(self, display_units) -> None:
        """Sets the "Display Units" option."""
        # void setDisplayUnits( boolean );
        raise NotImplementedError

    def get_col_width(self, col: int) -> int:
        """
        Gets the column width for the specified column.

        Parameters
        ----------
        col : int
            The column number to fetch the width of (0-based index).

        Returns
        -------
        The column width.
        """
        # int getColWidth( long col );
        raise NotImplementedError

    def set_col_width(self, col: int, width: int) -> None:
        """
        Sets the width of the specified column.

        Parameters
        ----------
        col :
            The column in the Data Monitor of interest (0-based index).
        width :
            The new width for the column.
        """
        # void setColWidth( long col, int width );
        raise NotImplementedError

    def is_valid(self) -> bool:
        """Determines whether all the items in the Data Monitor are \
        valid or not."""
        # boolean isValid( );
        raise NotImplementedError

    def get_title(self) -> str:
        """Gets the title of the Data Monitor."""
        # BSTR getTitle( );
        raise NotImplementedError

    def set_title(self, title: str) -> None:
        """
        Sets the title of the Data Monitor.

        Parameters
        ----------
        title :
            The new title of the Data Monitor.
        """
        # void setTitle( BSTR title );
        raise NotImplementedError

    def get_width(self) -> int:
        """Gets the width of the Data Monitor."""
        # int getWidth( );
        raise NotImplementedError

    def get_height(self) -> int:
        """Get the height of the Data Monitor."""
        # int getHeight( );
        raise NotImplementedError

    def set_size(self, width: int, height: int) -> None:
        """
        Sets the height and width of the Data Monitor.

        Parameters
        ----------
        width :
            The new width for the Data Monitor.
        height :
            The new height of the Data Monitor.
        """
        # void setSize( int width, int height );
        raise NotImplementedError

    def get_x(self) -> int:
        """Gets the X position of the Data Monitor."""
        # int getX( );
        raise NotImplementedError

    def get_y(self) -> int:
        """Gets the Y position of the Data Monitor."""
        # int getY( );
        raise NotImplementedError

    def set_location(self, x: int, y: int) -> None:
        """
        Sets the x and y location of the Data Monitor in the Analysis View.

        Parameters
        ----------
        x :
            The new x position.
        y :
            The new y position.
        """
        # void setLocation( int x, int y);
        raise NotImplementedError
