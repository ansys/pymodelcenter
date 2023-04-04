"""Definition of workflow."""
from abc import ABC, abstractmethod
from typing import Collection, Optional, Tuple, Union

import ansys.common.variableinterop as acvi
import ansys.engineeringworkflow.api as aew_api

from ansys.modelcenter.workflow.api.assembly import IAssembly
from ansys.modelcenter.workflow.api.datamonitor import IDataMonitor
from ansys.modelcenter.workflow.api.icomponent import IComponent
from ansys.modelcenter.workflow.api.ivariable import IVariable
from ansys.modelcenter.workflow.api.variable_links import IVariableLink


class IWorkflow(aew_api.IWorkflowInstance, ABC):
    """Represents a ModelCenter workflow."""

    @property
    @abstractmethod
    def workflow_file_name(self) -> str:
        """Full path of the current Workflow."""

    # TODO: We need to come up with a consistent convention (and document)
    #       whether incoming variable values will have their types coerced or not
    #       for this and the actual IVariable objects.
    @abstractmethod
    def set_value(self, var_name: str, value: acvi.IVariableValue) -> None:
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
        raise NotImplementedError()

    @abstractmethod
    def get_value(self, var_name: str) -> acvi.VariableState:
        """
        Get the value of a variable.

        Parameters
        ----------
        var_name :  str
            Full ModelCenter path of the variable.

        Returns
        -------
        The value as a VariableState.
        """
        raise NotImplementedError()

    @abstractmethod
    def get_variable_meta_data(self, name: str) -> acvi.CommonVariableMetadata:
        """
        Get metadata from a variable.

        Throws an exception if the variable is not found.

        Parameters
        ----------
        name : str
            The full name of the variable.

        Returns
        -------
        CommonVariableMetadata :
            The metadata, in the form of a CommonVariableMetadata
            implementation.
        """
        raise NotImplementedError()

    @abstractmethod
    def create_link(self, variable: Union[IVariable, str], equation: Union[str, IVariable]) -> None:
        """
        Create a link to the specified variable based on the specified equation.

        Parameters
        ----------
        variable : Union[IVariable, str]
            The variable that the link should target,
            or its full name.
        equation : Union[str, IVariable]
            Equation of the link. You may also pass an IVariable object here,
            and its name will become the equation.
        """
        raise NotImplementedError()

    @abstractmethod
    def save_workflow(self) -> None:
        """Save the current Model."""
        raise NotImplementedError()

    @abstractmethod
    def save_workflow_as(self, file_name: str) -> None:
        """
        Save the current Model to a specified file.

        Parameters
        ----------
        file_name : str
            Path to save the Model in.
        """
        raise NotImplementedError()

    @abstractmethod
    def close_workflow(self) -> None:
        """Close the current Model."""
        raise NotImplementedError()

    @abstractmethod
    def get_variable(self, name: str) -> IVariable:
        """
        Get variable of given name.

        Parameters
        ----------
        name : str
            Full ModelCenter path of the variable.

        Returns
        -------
        The variable.
        """
        raise NotImplementedError()

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
        The component.
        """
        raise NotImplementedError()

    # TODO/REDUCE: consider dropping for Phase II
    def set_scheduler(self, schedular: str) -> None:
        """
        Set the current active scheduler for the Model.

        Parameters
        ----------
        schedular : str
            The scheduler type. Possible types are:
                * forward
                * backward
                * mixed
                * script
            Note: all scheduler types are case-sensitive.
        """
        self._instance.setScheduler(schedular)

    @abstractmethod
    def remove_component(self, name: str) -> None:
        """
        Remove the specified component from the Model.

        Parameters
        ----------
        name : str
            Full ModelCenter path of the component to remove.
        """
        raise NotImplementedError()

    @abstractmethod
    def create_assembly(
        self, name: str, parent: Union[IAssembly, str], assembly_type: Optional[str] = None
    ):
        """
        Create a new Assembly in the Model.

        Parameters
        ----------
        name : str
            Desired name of the new Assembly.
        parent : Union[IAssembly, str]
            Full ModelCenter path of the parent Assembly, or an IAssembly that represents it.
        assembly_type : str, optional
            Type of the assembly to create.

        Returns
        -------
        Assembly.
        """
        # TODO: document / define enumeration for allowed assembly types.
        raise NotImplementedError()

    @abstractmethod
    def auto_link(self, src_comp: str, dest_comp: str) -> Collection[IVariableLink]:
        """
        Automatically links two components.

        Parameters
        ----------
        src_comp : str
            The source component.
        dest_comp : str
            The destination component.

        Returns
        -------
        A collection of the created links.
        """
        raise NotImplementedError()

    @abstractmethod
    def get_links(self) -> Collection[IVariableLink]:
        """
        Get a list of all links in the model.

        Parameters
        ----------
        reserved
            Parameter reserved for future use.

        Returns
        -------
        Iterable over variable links.
        """
        raise NotImplementedError(0)

    @abstractmethod
    def get_workflow_uuid(self) -> str:
        """Get the unique ID string for the current model."""
        raise NotImplementedError()

    @abstractmethod
    def halt(self) -> None:
        """Stop execution of the Model currently running in ModelCenter."""
        raise NotImplementedError(0)

    # TODO / REDUCE: consider dropping all DataMonitor methods for Phase II.
    # TODO / REDUCE: consider dropping DataMonitor related functionality entirely
    #                (if not, update these methods)
    def get_data_monitor(self, component: Union[IComponent, str], index: int) -> IDataMonitor:
        """
        Get the DataMonitor at the given index for the given component.

        Parameters
        ----------
        component: str
            The name of the component.
        index: int
            The index of the DataMonitor in the component.

        Returns
        -------
        The component's DataMonitor at the given index.
        """
        raise NotImplementedError()

    @abstractmethod
    def create_data_monitor(
        self, component: Union[IComponent, str], name: str, x: int, y: int
    ) -> object:
        """
        Create a DataMonitor associated with the specified component.

        Parameters
        ----------
        component: str
            The name of the component to associate the DataMonitor with.
        name: str
            The name of the DataMonitor.
        x: int
            The x-position of the DataMonitor.
        y: int
            The y-position of the DataMonitor.

        Returns
        -------
        The created DataMonitor.
        """
        raise NotImplementedError()

    @abstractmethod
    def remove_data_monitor(self, component: Union[IComponent, str], index: int) -> bool:
        """
        Remove the DataMonitor at the given index for the given component.

        Parameters
        ----------
        component: str
            The name of the component.
        index: int
            The index of the DataMonitor in the component.

        Returns
        -------
        True if the component had a DataMonitor at the given index.
        """
        raise NotImplementedError()

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
        raise NotImplementedError()

    @abstractmethod
    def get_assembly(self, name: Optional[str] = None) -> IAssembly:
        """
        Gets the named assembly or the top level assembly.

        Parameters
        ----------
        name : Optional[str]
            The full name of the desired assembly.
            If None is passed, the root assembly of the workflow is returned.
        """
        raise NotImplementedError()

    @abstractmethod
    def create_component(
        self,
        server_path: str,
        name: str,
        parent: Union[IAssembly, str],
        *,
        init_string: Optional[str] = None,
        av_position: Optional[Tuple[int, int]] = None,
        insert_before: Optional[Union[IComponent, IAssembly, str]] = None
    ) -> IComponent:
        """
        Creates a new component.

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
        The created component.
        """
        raise NotImplementedError()
