"""Definition of IDataMonitor."""
from typing import Tuple

import clr

clr.AddReference(r"phoenix-mocks\Phoenix.Mock.v45")
import Phoenix.Mock as phxmock


class DataMonitor:
    """Maps a COM MockDataMonitor to the IDataMonitor interface."""

    def __init__(self, monitor: phxmock.MockDataMonitor):
        """
        Initialize.

        Parameters
        ----------
        monitor: phxmock.MockDataMonitor
            The COM DataMonitor to wrap.
        """
        self._instance = monitor

    def get_name(self, row: int) -> str:
        """
        Get the name of a row in the DataMonitor.

        Parameters
        ----------
        row :
            The row number in the DataMonitor of interest.

        Returns
        -------
        The name of the row.
        """
        return self._instance.getName(row)

    def set_name(self, row: int, name: str) -> None:
        """
        Set the display name of the specified row in the DataMonitor.

        Parameters
        ----------
        row : int
            The row in the DataMonitor of interest.
        name : str
            The new display name.
        """
        self._instance.setName(row, name)

    def is_renamed(self, row: int) -> bool:
        """
        Determine whether the name of a row in the DataMonitor lines \
        up to the variable it represents.

        Parameters
        ----------
        row : int
            The row in the DataMonitor of interest.

        Returns
        -------
        True or False
        """
        return self._instance.isRenamed(row)

    def get_link(self, row: int) -> str:
        """
        Retrieve the variable associated with a row in the DataMonitor.

        Returns a blank string if the specified row doesn't link to a
        variable.

        Parameters
        ----------
        row :
            The row number in the DataMonitor of interest.

        Returns
        -------
        The full name of the variable, or a blank string.
        """
        return self._instance.getLink(row)

    def set_link(self, row: int, link: str) -> bool:
        """
        Set the variable associated with a given row in the DataMonitor.

        Parameters
        ----------
        row :
            The row in the DataMonitor of interest.
        link :
            The variable to associate with a given row in the
            DataMonitor.

        Returns
        -------
        True if the link was set, False if the variable or row was not
        valid.
        """
        return self._instance.setLink(row, link)

    def add_item(self, name: str, link: str) -> int:
        """
        Add an item to the DataMonitor that links to a variable in \
        the model.

        Parameters
        ----------
        name :
            The name to use for the item in the DataMonitor.
        link :
            The name of the variable this item links to.

        Returns
        -------
        The index of the new item in the DataMonitor.
        """
        return self._instance.addItem(name, link)

    def add_unlinked_item(self, name: str) -> int:
        """
        Add an item to the DataMonitor that does not link to a \
        variable.

        Parameters
        ----------
        name :
            The name to use for the item in the DataMonitor.

        Returns
        -------
            The index of the new item in the DataMonitor.
        """
        return self._instance.addUnlinkedItem(name)

    def remove_item(self, row: int) -> None:
        """
        Remove the selected row from the DataMonitor.

        Parameters
        ----------
        row : int
            The row in the DataMonitor of interest.
        """
        return self._instance.removeItem(row)

    def remove_link(self, row: int) -> None:
        """
        Remove the associated link from the row specified in the \
        DataMonitor.

        Parameters
        ----------
        row :
            The row in the DataMonitor of interest.
        """
        return self._instance.removeLink(row)

    @property
    def display_full_names(self) -> bool:
        """Get the status of the "Display Full Names" option."""
        return self._instance.getDisplayFullNames()

    @display_full_names.setter
    def display_full_names(self, display_full_names: bool) -> None:
        """Set the "Display Full Names" option."""
        self._instance.setDisplayFullNames(display_full_names)

    @property
    def auto_delete(self) -> bool:
        """Get the status of the Auto Delete option."""
        return self._instance.getAutoDelete()

    @auto_delete.setter
    def auto_delete(self, auto_delete: bool) -> None:
        """Set the status of the Auto Delete option."""
        self._instance.setAutoDelete(auto_delete)

    @property
    def display_units(self) -> bool:
        """Get the status of the "Display Units" option."""
        return self._instance.getDisplayUnits()

    @display_units.setter
    def display_units(self, display_units) -> None:
        """Set the "Display Units" option."""
        self._instance.setDisplayUnits(display_units)

    def get_col_width(self, col: int) -> int:
        """
        Get the column width for the specified column.

        Parameters
        ----------
        col : int
            The column in the DataMonitor of interest.

        Returns
        -------
        The column width.
        """
        return self._instance.getColWidth(col)

    def set_col_width(self, col: int, width: int) -> None:
        """
        Set the width of the specified column.

        Parameters
        ----------
        col :
            The column in the DataMonitor of interest.
        width :
            The new width for the column.
        """
        self._instance.setColWidth(col, width)

    def is_valid(self) -> bool:
        """Determine whether all the items in the DataMonitor are \
        valid or not."""
        return self._instance.isValid()

    @property
    def title(self) -> str:
        """Get the title of the DataMonitor."""
        return self._instance.getTitle()

    @title.setter
    def title(self, title: str) -> None:
        """
        Set the title of the DataMonitor.

        Parameters
        ----------
        title: str
            The new title.
        """
        self._instance.setTitle(title)

    @property
    def size(self) -> Tuple[int, int]:
        """
        Get the size of the DataMonitor.

        Returns
        -------
        A Tuple containing the (width, height) of the DataMonitor.
        """
        return self._instance.getWidth(), self._instance.getHeight()

    @size.setter
    def size(self, size: Tuple[int, int]) -> None:
        """
        Set the size of the DataMonitor.

        Parameters
        ----------
        size: Tuple[int, int]
            The new (width, height) of the DataMonitor.
        """
        self._instance.setSize(size[0], size[1])

    @property
    def location(self) -> Tuple[int, int]:
        """
        Get the location of the DataMonitor in the Analysis View.

        Returns
        -------
        A tuple containing the (x,y) position of the DataMonitor.
        """
        return self._instance.getX(), self._instance.getY()

    @location.setter
    def location(self, location: Tuple[int, int]) -> None:
        """
        Set the location of the DataMonitor in the Analysis View.

        Parameters
        ----------
        location: Tuple[int, int]
            The new (x,y) location.
        """
        self._instance.setLocation(location[0], location[1])
