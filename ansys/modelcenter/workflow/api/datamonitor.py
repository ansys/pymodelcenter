"""Definition of DataMonitor."""
from abc import ABC, abstractmethod
from typing import Tuple


# TODO/REDUCE: We almost certainly don't want to support this for Phase II.
class IDataMonitor(ABC):
    """Represents a data monitor on the ModelCenter Analysis View."""

    # TODO: are rows zero-indexed? How do you know how many there are?

    @abstractmethod
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
        raise NotImplementedError()

    @abstractmethod
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
        raise NotImplementedError()

    @abstractmethod
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
        raise NotImplementedError()

    @abstractmethod
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
        raise NotImplementedError()

    @abstractmethod
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
        raise NotImplementedError()

    @abstractmethod
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
        raise NotImplementedError()

    @abstractmethod
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
        raise NotImplementedError()

    @abstractmethod
    def remove_item(self, row: int) -> None:
        """
        Remove the selected row from the DataMonitor.

        Parameters
        ----------
        row : int
            The row in the DataMonitor of interest.
        """
        raise NotImplementedError()

    @abstractmethod
    def remove_link(self, row: int) -> None:
        """
        Remove the associated link from the row specified in the \
        DataMonitor.

        Parameters
        ----------
        row :
            The row in the DataMonitor of interest.
        """
        raise NotImplementedError()

    @property
    @abstractmethod
    def display_full_names(self) -> bool:
        """Get the status of the "Display Full Names" option."""
        raise NotImplementedError()

    @display_full_names.setter
    @abstractmethod
    def display_full_names(self, display_full_names: bool) -> None:
        """Set the "Display Full Names" option."""
        raise NotImplementedError()

    @property
    @abstractmethod
    def auto_delete(self) -> bool:
        """Get the status of the Auto Delete option."""
        raise NotImplementedError()

    @auto_delete.setter
    @abstractmethod
    def auto_delete(self, auto_delete: bool) -> None:
        """Set the status of the Auto Delete option."""
        raise NotImplementedError()

    @property
    @abstractmethod
    def display_units(self) -> bool:
        """Get the status of the "Display Units" option."""
        raise NotImplementedError()

    @display_units.setter
    @abstractmethod
    def display_units(self, display_units) -> None:
        """Set the "Display Units" option."""
        raise NotImplementedError()

    @abstractmethod
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
        raise NotImplementedError()

    @abstractmethod
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
        raise NotImplementedError()

    @property
    @abstractmethod
    def is_valid(self) -> bool:
        """Determine whether all the items in the DataMonitor are \
        valid or not."""
        raise NotImplementedError()

    @property
    def title(self) -> str:
        """Get the title of the DataMonitor."""
        raise NotImplementedError()

    @title.setter
    @abstractmethod
    def title(self, title: str) -> None:
        """
        Set the title of the DataMonitor.

        Parameters
        ----------
        title: str
            The new title.
        """
        raise NotImplementedError()

    @property
    @abstractmethod
    def size(self) -> Tuple[int, int]:
        """
        Get the size of the DataMonitor.

        Returns
        -------
        A Tuple containing the (width, height) of the DataMonitor.
        """
        raise NotImplementedError()

    @size.setter
    @abstractmethod
    def size(self, size: Tuple[int, int]) -> None:
        """
        Set the size of the DataMonitor.

        Parameters
        ----------
        size: Tuple[int, int]
            The new (width, height) of the DataMonitor.
        """
        raise NotImplementedError()

    @property
    @abstractmethod
    def location(self) -> Tuple[int, int]:
        """
        Get the location of the DataMonitor in the Analysis View.

        Returns
        -------
        A tuple containing the (x,y) position of the DataMonitor.
        """
        raise NotImplementedError()

    @location.setter
    @abstractmethod
    def location(self, location: Tuple[int, int]) -> None:
        """
        Set the location of the DataMonitor in the Analysis View.

        Parameters
        ----------
        location: Tuple[int, int]
            The new (x,y) location.
        """
        raise NotImplementedError()
