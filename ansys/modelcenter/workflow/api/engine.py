"""Definition of Engine and associated classes."""
from abc import ABC, abstractmethod
from enum import Enum
from typing import Collection, Mapping, Union

from ansys.engineeringworkflow.api import IFileBasedWorkflowEngine

from .format import IFormat
from .workflow import IWorkflow


class WorkflowType(Enum):
    """Enumeration of the types of workflows that can be created."""

    DATA = ("dataModel",)
    """Legacy style workflow where execution flow is determined from
    links between components and an execution strategy."""
    PROCESS = "processModel"
    """Modern style workflow where execution flow is explicitly designed
    by the user using flow components."""


class OnConnectionErrorMode(Enum):
    """Enumeration of actions to take on connection error."""

    ERROR = (3,)
    """Abort loading and throw the error back to the caller."""
    # TODO: If we continue to allow connecting without errors,
    #       we need a method on IComponent that allows verifying component connection state.
    IGNORE = (1,)
    """Ignore the error and continue loading."""
    # TODO: This should probably not be allowed on this API.
    DIALOG = -1
    """(UI mode only) Show an error dialog."""


class IEngine(IFileBasedWorkflowEngine, ABC):
    """Engine class used to wrap around MockModelCenter class."""

    @abstractmethod
    def new_workflow(self, name: str, workflow_type: WorkflowType = WorkflowType.DATA) -> IWorkflow:
        """
        Create a new workflow.

        Parameters
        ----------
        name: str
            A filename or path where the new workflow will be made.
        workflow_type: WorkflowType
            The type of workflow to create. Defaults to a data workflow.

        Returns
        -------
        A new Workflow instance.
        """
        raise NotImplementedError()

    # TODO/REDUCE: Drop ignoring connection errors for Phase II.
    #              Will need a connection state getter when implemented as noted below.
    # TODO: this probably doesn't need to be a separate method;
    #     on_connect_error can be an optional kwarg on
    #     the existing load_workflow
    @abstractmethod
    def load_workflow_ex(
        self, file_name: str, on_connect_error: OnConnectionErrorMode = OnConnectionErrorMode.ERROR
    ) -> IWorkflow:
        """
        Load a saved workflow from a file.

        Parameters
        ----------
        file_name: str
            The path to the file to load.
        on_connect_error: OnConnectionErrorMode
            What to do in the event of an error.

        Returns
        -------
        A new Workflow instance.
        """
        raise NotImplementedError()

    @abstractmethod
    def get_formatter(self, fmt: str) -> IFormat:
        """
        Create an instance of a formatter that can be used to format \
        numbers to and from a particular string style.

        Parameters
        ----------
        fmt: str
            Specified string format for the IFormat object.

        Returns
        -------
        A Format object that formats in the given style.
        """
        raise NotImplementedError()

    @abstractmethod
    def get_preference(self, pref: str) -> Union[bool, int, float, str]:
        """
        Get the value of a preference.

        Preferences control how the engine behaves in various ways.
        The value returned may be boolean, integer, real, or string
        typed.

        Parameters
        ----------
        pref: str
            The name of the preference for which to return the value.

        Returns
        -------
        The value of the given preference.
        """
        raise NotImplementedError()

    # TODO: No set_preference? Does this exist on the COM API?

    @abstractmethod
    def get_units(self) -> Mapping[str, Collection[str]]:
        """
        Get available units by category.

        Returns
        -------
        A mapping representing the units available in the engine.
        The keys in the map are the names of unit categories,
        and the values are collections containing all the unit names for that category.
        """

    @abstractmethod
    def get_run_only_mode(self) -> bool:
        """
        Get whether the engine is in Run-Only mode.

        Run-Only mode has lower licensing requirements, but does not
        allow for the workflow to be edited.

        Returns
        -------
        True if in Run-Only mode; otherwise, False.
        """
        raise NotImplementedError()
