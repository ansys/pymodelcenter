"""Definition of IComponent."""
from abc import ABC, abstractmethod

import ansys.engineeringworkflow.api as aew_api
import ansys.modelcenter.workflow.api.iassembly as assembly
import ansys.modelcenter.workflow.api.igroup as igroup
import ansys.modelcenter.workflow.api.irenamable_elements as renamable_element


class IComponent(
    renamable_element.IRenamableElement,
    aew_api.IComponent,
    igroup.IGroupOwner,
    assembly.IAssemblyChild,
    ABC,
):
    """Represents a component in a Workflow."""

    # ModelCenter

    @abstractmethod
    def get_source(self) -> str:
        """
        Get the source of the component.

        Returns
        -------
        str
            Source of the component.
        """

    @property
    @abstractmethod
    def control_type(self) -> str:
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
        str
            Type of the component.
        """

    @abstractmethod
    def invoke_method(self, method: str) -> None:
        """
        Invoke one of the component's methods.

        Parameters
        ----------
        method : str
            Name of the method to invoke.
        """

    @abstractmethod
    def invalidate(self) -> None:
        """Invalidate the component and all of its datapins."""

    @property
    @abstractmethod
    def is_connected(self) -> bool:
        """Is this component connected to its source."""

    @abstractmethod
    def reconnect(self) -> None:
        """Reload this component from its source."""

    @abstractmethod
    def download_values(self) -> None:
        """Download the component's datapin values from the server if\
        it is a ModelCenter Remote Execution component."""
