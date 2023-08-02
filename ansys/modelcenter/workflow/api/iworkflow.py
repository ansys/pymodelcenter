"""Definition of workflow."""
from abc import ABC, abstractmethod
from typing import Collection, Optional, Tuple, Union

import ansys.engineeringworkflow.api as aew_api
from ansys.modelcenter.workflow.api.iassembly import AssemblyType, IAssembly
from ansys.modelcenter.workflow.api.icomponent import IComponent
from ansys.modelcenter.workflow.api.idatapin import IDatapin
from ansys.modelcenter.workflow.api.idatapin_link import IDatapinLink
import ansys.tools.variableinterop as atvi


class IWorkflow(aew_api.IWorkflowInstance, ABC):
    """Represents a ModelCenter workflow."""

    @property
    @abstractmethod
    def workflow_file_name(self) -> str:
        """Full path of the current Workflow."""

    @abstractmethod
    def set_value(self, var_name: str, value: atvi.IVariableValue) -> None:
        """
        Set the value of a variable.

        A wrapper around the
        IModelCenter.setValue(BSTR varName, BSTR value) method.

        Parameters
        ----------
        var_name : str
            Full ModelCenter path of the variable.
        value : acvi.IVariableValue
            The new value to set.
        """

    @abstractmethod
    def get_value(self, var_name: str) -> atvi.VariableState:
        """
        Get the value of a variable.

        Parameters
        ----------
        var_name :  str
            Full ModelCenter path of the variable.

        Returns
        -------
        VariableState
            The value as a VariableState.
        """

    @abstractmethod
    def get_variable_meta_data(self, name: str) -> atvi.CommonVariableMetadata:
        """
        Get metadata from a variable.

        Throws an exception if the variable is not found.

        Parameters
        ----------
        name : str
            The full name of the variable.

        Returns
        -------
        CommonVariableMetadata
            The metadata, in the form of a CommonVariableMetadata
            implementation.
        """

    @abstractmethod
    def create_link(self, variable: Union[IDatapin, str], equation: Union[str, IDatapin]) -> None:
        """
        Create a link to the specified datapin based on the specified equation.

        Parameters
        ----------
        variable : Union[IDatapin, str]
            The variable that the link should target,
            or its full name.
        equation : Union[str, IDatapin]
            Equation of the link. You may also pass an IDatapin object here,
            and its name will become the equation.
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
    def get_variable(self, name: str) -> IDatapin:
        """
        Get variable of given name.

        Parameters
        ----------
        name : str
            Full ModelCenter path of the variable.

        Returns
        -------
        IDatapin
            The variable.
        """

    @abstractmethod
    def get_component(self, name: str) -> IComponent:
        """
        Get a component from the workflow.

        Parameters
        ----------
        name: str
            The full path to the component.

        Returns
        -------
        IComponent
            The component.
        """

    @abstractmethod
    def remove_component(self, name: str) -> None:
        """
        Remove the specified component from the workflow.

        Parameters
        ----------
        name : str
            Full ModelCenter path of the component to remove.
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
            Full ModelCenter path of the parent Assembly, or an IAssembly that represents it.
        assembly_type : str, optional
            Type of the assembly to create. Pass None to create a regular data-dependency assembly
            (equivalent to passing AssemblyType.ASSEMBLY).

        Returns
        -------
        IAssembly
        """
        # TODO: document / define enumeration for allowed assembly types.

    @abstractmethod
    def auto_link(
        self, src_comp: Union[IComponent, str], dest_comp: Union[IComponent, str]
    ) -> Collection[IDatapinLink]:
        """
        Automatically links two components.

        Parameters
        ----------
        src_comp : str
            The source component or the full name of the component desired.
        dest_comp : str
            The destination component or the full name of the component desired.

        Returns
        -------
        Collection[IDatapinLink]
            A collection of the created links.
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
        self, component: Union[IComponent, str], parent: Union[IAssembly, str], index: int = -1
    ) -> None:
        """
        Move the component to the parent at the given index.

        Parameters
        ----------
        component : Union[IComponent, str]
            The component to move.
        parent : str
            Owning object of the component.
        index
            Position in the parent.
        """

    @abstractmethod
    def get_assembly(self, name: Optional[str] = None) -> IAssembly:
        """
        Get the named assembly or the top level assembly.

        Parameters
        ----------
        name : Optional[str]
            The full name of the desired assembly.
            If None is passed, the root assembly of the workflow is returned.
        """

    @abstractmethod
    def create_component(
        self,
        server_path: str,
        name: str,
        parent: Union[IAssembly, str],
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
            The MCRE source path of the new component.
        name : str
            Name of the new component.
        parent : str
            Parent assembly of the component.
        init_string: Optional[str]
            The initialization string.
        av_position: Optional[Tuple[int, int]]
            The position on the analysis view at which to insert the component.
        insert_before: Optional[Union[IComponent, IAssembly, str]]
            The component before which this component should be inserted.
        Returns
        -------
        IComponent
            The created component.
        """
