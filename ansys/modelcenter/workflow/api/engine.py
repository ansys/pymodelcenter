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
