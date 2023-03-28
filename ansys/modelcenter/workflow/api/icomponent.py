"""Definition of IComponent."""
from abc import ABC, abstractmethod
from typing import Collection, List, Tuple, Union

import ansys.engineeringworkflow.api as aew_api

import ansys.modelcenter.workflow.api.assembly as assembly
import ansys.modelcenter.workflow.api.custom_metadata_owner as custom_mo
import ansys.modelcenter.workflow.api.igroup as igroup
import ansys.modelcenter.workflow.api.ivariable as ivariable


class IComponent(assembly.IAssemblyChild, custom_mo.ICustomMetadataOwner, aew_api.IComponent, ABC):
    """A component in a Workflow."""

    # ModelCenter

    # TODO: Shared with assembly, groups
    @property
    @abstractmethod
    def groups(self) -> Collection[igroup.IGroup]:
        """All groups in the component."""
        raise NotImplementedError()

    # TODO: Deleted "user data" field - although this does exist separately on the COM API,
    #       the functionality seems to be no better than the custom metadata feature;
    #       need to see if this is critical to users for some reason.

    @property
    @abstractmethod
    def associated_files(self) -> Collection[str]:
        """Set of files associated with the component."""
        raise NotImplementedError()

    @associated_files.setter
    @abstractmethod
    def associated_files(self, source: Union[str, List[str]]):
        """Set of files associated with the component."""
        raise NotImplementedError()

    @abstractmethod
    def get_source(self) -> str:
        """
        Get the source of the component.

        Returns
        -------
        The source of the component.
        """
        raise NotImplementedError()

    # TODO: should be on base variable container
    @abstractmethod
    def get_variable(self, name: str) -> ivariable.IVariable:
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
        raise NotImplementedError()

    # TODO: shared with assembly
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
        return self._wrapped.getType()

    # TODO: Do we want to continue to support running individual components like this?
    @abstractmethod
    def run(self) -> None:
        """Run the component."""
        raise NotImplementedError()

    @abstractmethod
    def invoke_method(self, method: str) -> None:
        """
        Invoke one of the component's methods.

        Parameters
        ----------
        method: str
            The name of the method to invoke.
        """
        raise NotImplementedError()

    @abstractmethod
    def invalidate(self) -> None:
        """Invalidate the component and all of its variables."""
        raise NotImplementedError()

    @abstractmethod
    def reconnect(self) -> None:
        """Reload this component from its source."""
        raise NotImplementedError()

    @abstractmethod
    def download_values(self) -> None:
        """Download the component's variable values from the server if\
        it is a ModelCenter Remote Execution component."""
        raise NotImplementedError()

    # TODO: Shared with at least assembly, possibly anything with a name
    @abstractmethod
    def rename(self, name: str) -> None:
        """
        Rename the current component.

        Parameters
        ----------
        name: str
            The new name of the component.
        """
        self._wrapped.rename(name)

    @abstractmethod
    def get_analysis_view_position(self) -> Tuple[int, int]:
        """
        Get the position on the analysis view.

        Returns
        -------
        A 2-tuple where the first element is the x-coordinate
        and the second element is the y-coordinate.
        """
        raise NotImplementedError()
