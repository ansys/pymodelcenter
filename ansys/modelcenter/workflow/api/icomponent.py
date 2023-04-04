"""Definition of IComponent."""
from abc import ABC, abstractmethod
from typing import Collection, List, Tuple, Union

import ansys.engineeringworkflow.api as aew_api

import ansys.modelcenter.workflow.api.assembly as assembly
import ansys.modelcenter.workflow.api.custom_metadata_owner as custom_mo
import ansys.modelcenter.workflow.api.igroup as igroup
import ansys.modelcenter.workflow.api.ivariable as ivariable
import ansys.modelcenter.workflow.api.renamable_element as renamable_element


class IComponent(
    renamable_element.IRenamableElement,
    assembly.IAssemblyChild,
    igroup.IGroupOwner,
    custom_mo.ICustomMetadataOwner,
    aew_api.IComponent,
    ABC,
):
    """A component in a Workflow."""

    # ModelCenter

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
