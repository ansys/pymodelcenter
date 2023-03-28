"""Definition of GlobalParameters."""
from abc import ABC, abstractmethod
from typing import Union


class IGlobalParameters(ABC):
    """
    A set of name/value pairs that can be used for programmatic \
    purposes.

    Values are not stored with the open workflow. They can optionally be
    passed up to external servers, such as a ModelCenter Remote
    Execution server.
    """

    @property
    @abstractmethod
    def count(self) -> int:
        """Count of the name/value pairs."""
        raise NotImplementedError()

    @abstractmethod
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
        raise NotImplementedError()

    @abstractmethod
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
        raise NotImplementedError()

    @abstractmethod
    def set_export_to_remote_components(self, index: Union[int, str], export: bool) -> None:
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
        raise NotImplementedError()

    @abstractmethod
    def remove(self, index: Union[int, str]) -> None:
        """
        Remove a named parameter.

        Parameters
        ----------
        index :
            The name of the parameter to remove.
        """
        raise NotImplementedError()
