"""Definition of IComponent."""
from abc import ABC, abstractmethod
from typing import Collection, Tuple

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
    """A component in a Workflow."""

    # ModelCenter

    # TODO/REDUCE: Drop associated files for Phase II.
    @property
    @abstractmethod
    def associated_files(self) -> Collection[str]:
        """Set of files associated with the component."""

    @associated_files.setter
    @abstractmethod
    def associated_files(self, source: Collection[str]):
        """Set of files associated with the component."""

    @abstractmethod
    def get_source(self) -> str:
        """
        Get the source of the component.

        Returns
        -------
        The source of the component.
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
        The type of the component.
        """

    @abstractmethod
    def invoke_method(self, method: str) -> None:
        """
        Invoke one of the component's methods.

        Parameters
        ----------
        method: str
            The name of the method to invoke.
        """

    @abstractmethod
    def invalidate(self) -> None:
        """Invalidate the component and all of its variables."""

    @property
    @abstractmethod
    def is_connected(self) -> bool:
        """Is this component connected to its source."""

    @abstractmethod
    def reconnect(self) -> None:
        """Reload this component from its source."""

    @abstractmethod
    def download_values(self) -> None:
        """Download the component's variable values from the server if\
        it is a ModelCenter Remote Execution component."""

    @abstractmethod
    def get_analysis_view_position(self) -> Tuple[int, int]:
        """
        Get the position on the analysis view.

        Returns
        -------
        A 2-tuple where the first element is the x-coordinate
        and the second element is the y-coordinate.
        """
