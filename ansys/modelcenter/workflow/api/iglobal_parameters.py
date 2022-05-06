"""Definition of GlobalParameters."""
from typing import Union

import clr

clr.AddReference(r"phoenix-mocks\Phoenix.Mock.v45")
from Phoenix.Mock import MockGlobalParameters


class IGlobalParameters:
    """
    A set of name/value pairs that can be used for programmatic \
    purposes.

    Values are not stored with the open workflow. They can optionally be
    passed up to external servers, such as a ModelCenter Remote
    Execution server.
    """

    def __init__(self, instance: MockGlobalParameters):
        """Initialize."""
        self._instance = instance

    @property
    def count(self) -> int:
        """Count of the name/value pairs."""
        return self._instance.Count

    def get_item(self, index: Union[int, str]) -> object:
        """
        Receives the value of a particular parameter.

        Parameters
        ----------
        index : object
            The name of the name/value pair to retrieve.

        Returns
        -------
        The value of the parameter.
        """
        return self._instance[index]

    def set_item(self, index: Union[int, str], new_value: object) -> None:
        """
        Receives the value of a particular parameter.

        Parameters
        ----------
        index :
            The name of the name/value pair to retrieve.
        new_value :
            The variable to hold the value of the parameter.
        """
        self._instance[index] = new_value

    def set_export_to_remote_components(
            self, index: Union[int, str], export: bool) -> None:
        """
        Set whether this name/value pair is passed to external \
        servers when a component is run on that server.

        Parameters
        ----------
        index :
            The name of the variable.
        export :
            If true, this name/value pair will be sent.
        """
        self._instance.setExportToRemoteComponents(index, export)

    def remove(self, index: Union[int, str]) -> None:
        """
        Remove a named parameter.

        Parameters
        ----------
        index :
            The name of the parameter to remove.
        """
        self._instance.Remove(index)
