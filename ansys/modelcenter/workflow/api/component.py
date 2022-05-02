"""Definition of Component."""
from abc import ABC, abstractmethod
from typing import List, Union


class Component(ABC):
    """A component in a Workflow."""

    @property
    @abstractmethod
    def variables(self) -> object:  # IVariables
        """Variables in the component."""
        raise NotImplementedError

    @property
    @abstractmethod
    def groups(self) -> object:  # Groups
        """All groups in the component."""
        raise NotImplementedError

    @property
    @abstractmethod
    def user_data(self) -> object:  # VARIANT
        """Arbitrary object which is not used internally, but can \
        store data for programmatic purposes.

        The value is not stored across save/load operations.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def associated_files(self) -> Union[str, List[str]]:
        """Set of files associated with the component."""
        raise NotImplementedError

    @property
    @abstractmethod
    def index_in_parent(self) -> int:
        """Position of this component in its parent assembly."""
        raise NotImplementedError

    @property
    @abstractmethod
    def parent_assembly(self) -> object: # Assembly
        """Parent assembly of this component."""
        raise NotImplementedError

    @abstractmethod
    def get_name(self) -> str:
        """
        Get the name of the component.

        Returns
        -------
        The name of the component.
        """
        raise NotImplementedError

    @abstractmethod
    def get_full_name(self) -> str:
        """
        Get the full path of the component.

        Returns
        -------
        The full path of the component.
        """
        raise NotImplementedError

    @abstractmethod
    def get_source(self) -> str:
        """
        Get the source of the component.

        Returns
        -------
        The source of the component.
        """
        raise NotImplementedError

    @abstractmethod
    def get_variable(self, name: str) -> object:  # IVariable
        """
        Get a variable in this component by name.

        Parameters
        ----------
        name: str
            The name of the variable, in dotted notation relative to
            the component.

        Returns
        -------
        The variable object.
        """
        raise NotImplementedError

    @abstractmethod
    def get_type(self) -> str:
        """
        Get the type of the component.

        Valid values include:
        * Component
        * Assembly
        * Sequence
        * If
        * Parallel
        * Empty
        * ForEach

        Returns
        -------
        The type of the component.
        """
        raise NotImplementedError

    @abstractmethod
    def get_metadata(self, name: str) -> object:  # VARIANT
        """
        Get the metadata value of the given metadata key name.

        Parameters
        ----------
        name: str
            The key name of the metadata to retrieve.

        Returns
        -------
        The value of the metadata key.
        """
        raise NotImplementedError

    @abstractmethod
    def set_metadata(self, name: str, type_: object, value: object, access: object,
                     archive: bool) -> None:  # MetadataType, VARIANT, MetadataAccess
        """
        Set the metadata value of a given key.

        Parameters
        ----------
        name: str
            The key name of the metadata to set.
        type_: object
            The type of metadata to set.
        value: object
            The metadata value to set.
        access: object
            The access permissions of the metadata.
        archive: bool
            Whether this property should be archived.
        """
        raise NotImplementedError

    @abstractmethod
    def run(self) -> None:
        """Run the component."""
        raise NotImplementedError

    @abstractmethod
    def invoke_method(self, method: str) -> None:
        """
        Invoke one of the component's methods.

        Parameters
        ----------
        method: str
            The name of the method to invoke.
        """
        raise NotImplementedError

    @abstractmethod
    def invalidate(self) -> None:
        """Invalidate the component and all of its variables."""
        raise NotImplementedError

    @abstractmethod
    def reconnect(self) -> None:
        """Reload this component from its source."""
        raise NotImplementedError

    @abstractmethod
    def download_values(self) -> None:
        """Download the component's variable values from the server if\
        it is a ModelCenter Remote Execution component."""
        raise NotImplementedError

    @abstractmethod
    def rename(self, name: str) -> None:
        """
        Rename the current component.

        Parameters
        ----------
        name: str
            The new name of the component.
        """
        raise NotImplementedError

    @abstractmethod
    def show(self) -> None:
        """Show the component's GUI, if it has one."""
        raise NotImplementedError
