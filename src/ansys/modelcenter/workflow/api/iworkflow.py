"""Definition of workflow."""
from abc import ABC, abstractmethod
from typing import Collection, Optional, Tuple, Union

import ansys.engineeringworkflow.api as aew_api
import ansys.tools.variableinterop as atvi

from ansys.modelcenter.workflow.api.iassembly import AssemblyType, IAssembly
from ansys.modelcenter.workflow.api.icomponent import IComponent
from ansys.modelcenter.workflow.api.idatapin import IDatapin
from ansys.modelcenter.workflow.api.idatapin_link import IDatapinLink


class IWorkflow(aew_api.IWorkflowInstance, ABC):
    """Represents a ModelCenter workflow."""

    @property
    @abstractmethod
    def workflow_file_name(self) -> str:
        """Full path of the current Workflow."""

    @abstractmethod
    def set_value(self, var_name: str, value: atvi.IVariableValue) -> None:
        """
        Set the value of a datapin.

        Parameters
        ----------
        var_name : str
            Full ModelCenter path of the datapin.
        value : atvi.IVariableValue
            New value to set.

        Raises
        ------
        InvalidInstanceError
            If a datapin with the given name does not exist.
        """

    @abstractmethod
    def get_datapin_state(self, var_name: str) -> atvi.VariableState:
        """
        Get the state of a datapin.

        Parameters
        ----------
        var_name :  str
            Full ModelCenter path of the datapin.

        Returns
        -------
        VariableState
            Value as a ``VariableState``.

        Raises
        ------
        InvalidInstanceError
            If a datapin with the given name does not exist.
        """

    @abstractmethod
    def get_datapin_meta_data(self, name: str) -> atvi.CommonVariableMetadata:
        """
        Get metadata from a datapin.

        Parameters
        ----------
        name : str
            Full name of the datapin.

        Returns
        -------
        atvi.CommonVariableMetadata
            Metadata of the datapin.

        Raises
        ------
        InvalidInstanceError
            If a datapin with the given name does not exist.
        """

    @abstractmethod
    def create_link(self, datapin: Union[IDatapin, str], equation: Union[str, IDatapin]) -> None:
        """
        Create a link to the specified datapin based on the specified equation.

        Parameters
        ----------
        datapin : Union[IDatapin, str]
            The datapin that the link should target, or its full name.
        equation : Union[str, IDatapin]
            Equation of the link. You may also pass an ``IDatapin``
            object here, and its name will become the equation.

        Raises
        ------
        InvalidInstanceError
            If either the target or equation datapin does not exist.
        """

    @abstractmethod
    def save_workflow(self) -> None:
        """Save the current workflow."""

    @abstractmethod
    def save_workflow_as(self, file_name: str) -> None:
        """
        Save the current workflow to a specified file.

        Parameters
        ----------
        file_name : str
            Path to save the workflow in.
        """

    @abstractmethod
    def close_workflow(self) -> None:
        """Close the current workflow."""

    @abstractmethod
    def get_datapin(self, name: str) -> IDatapin:
        """
        Get a datapin with a given name.

        Parameters
        ----------
        name : str
            Full ModelCenter path of the datapin.

        Returns
        -------
        IDatapin
            Datapin with the given name.

        Raises
        ------
        InvalidInstanceError
            If a datapin with the given name does not exist.
        """

    @abstractmethod
    def get_component(self, name: str) -> IComponent:
        """
        Get a component from the workflow.

        Parameters
        ----------
        name : str
            The full path to the component.

        Returns
        -------
        IComponent
            Component with the given name.

        Raises
        ------
        InvalidInstanceError
            If a component with the given name does not exist.
        """

    @abstractmethod
    def remove_component(self, name: str) -> None:
        """
        Remove the specified component from the workflow.

        Parameters
        ----------
        name : str
            Full ModelCenter path of the component to remove.

        Raises
        ------
        InvalidInstanceError
            If a component with the given name does not exist.
        """

    @abstractmethod
    def create_assembly(
        self, name: str, parent: Union[IAssembly, str], assembly_type: Optional[AssemblyType] = None
    ) -> IAssembly:
        """
        Create a new Assembly in the workflow.

        Parameters
        ----------
        name : str
            Desired name of the new Assembly.
        parent : Union[IAssembly, str]
            Full ModelCenter path of the parent ``IAssembly``, or an
            ``IAssembly`` that represents it.
        assembly_type : AssemblyType, optional
            Type of the assembly to create. Pass ``None`` to create a
            regular data-dependency assembly (equivalent to passing
            ``AssemblyType.ASSEMBLY``).

        Returns
        -------
        IAssembly
            Created assembly.
        """

    @abstractmethod
    def auto_link(
        self, src_comp: Union[IComponent, str], dest_comp: Union[IComponent, str]
    ) -> Collection[IDatapinLink]:
        """
        Automatically links two components.

        Parameters
        ----------
        src_comp : str
            Source component, or the full name of the component desired.
        dest_comp : str
            Destination component, or the full name of the component desired.

        Returns
        -------
        Collection[IDatapinLink]
            Collection of the created links.

        Raises
        ------
        InvalidInstanceError
            If either the source or destination component does not exist.
        """

    @abstractmethod
    def get_links(self) -> Collection[IDatapinLink]:
        """
        Get a list of all links in the workflow.

        Returns
        -------
        Collection[IDatapinLink]
            Iterable over datapin links.
        """

    @abstractmethod
    def get_workflow_uuid(self) -> str:
        """Get the unique ID string for the current workflow."""

    @abstractmethod
    def halt(self) -> None:
        """Stop execution of the workflow currently running in ModelCenter."""

    @abstractmethod
    def move_component(
        self,
        component: Union[IComponent, str],
        parent: Union[aew_api.IControlStatement, str],
        index: int = -1,
    ) -> None:
        """
        Move the component to the parent at the given index.

        Parameters
        ----------
        component : Union[IComponent, str]
            Component to move.
        parent : str
            Owning object of the component.
        index : int, optional
            Position in the parent.

        Raises
        ------
        InvalidInstanceError
            If the target component does not exist.
        """

    @abstractmethod
    def get_assembly(self, name: Optional[str] = None) -> IAssembly:
        """
        Get the named assembly or the top level assembly.

        Parameters
        ----------
        name : str, optional
            The full name of the desired assembly.
            If ``None`` is passed, the root assembly of the workflow is
            returned.

        Raises
        ------
        InvalidInstanceError
            If an assembly with the given name does not exist.
        """

    @abstractmethod
    def create_component(
        self,
        server_path: str,
        name: str,
        parent: Union[aew_api.IControlStatement, str],
        *,
        init_string: Optional[str] = None,
        av_position: Optional[Tuple[int, int]] = None,
        insert_before: Optional[Union[IComponent, IAssembly, str]] = None,
    ) -> IComponent:
        """
        Create a new component.

        Parameters
        ----------
        server_path : str
            Source path of the new component, such as the url to the
            component in ModelCenter Remote Execution.
        name : str
            Name of the new component.
        parent : Union[aew_api.IControlStatement, str]
            Parent assembly of the component.
        init_string: str, optional
            Initialization string.
        av_position: Tuple[int, int], optional
            Position in the analysis view at which to insert the component.
        insert_before: Union[IComponent, IAssembly, str], optional
            Component before which this component should be inserted.
        Returns
        -------
        IComponent
            Created component.
        """
