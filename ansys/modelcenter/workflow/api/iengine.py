"""Definition of Engine and associated classes."""
from abc import ABC, abstractmethod
from enum import Enum
from typing import Collection, Mapping, Union

from ansys.engineeringworkflow.api import IFileBasedWorkflowEngine

from .iformat import IFormat
from .iworkflow import IWorkflow


class WorkflowType(Enum):
    """Enumeration of the types of workflows that can be created."""

    DATA = ("dataModel",)
    """Legacy style workflow where execution flow is determined from
    links between components and an execution strategy."""
    PROCESS = "processModel"
    """Modern style workflow where execution flow is explicitly designed
    by the user using flow components."""


class IEngine(IFileBasedWorkflowEngine, ABC):
    """Manages creating and running engineering workflows."""

    @abstractmethod
    def new_workflow(self, name: str, workflow_type: WorkflowType = WorkflowType.DATA) -> IWorkflow:
        """
        Create a new workflow.

        Parameters
        ----------
        name: str
            Filename or path where the new workflow will be made.
        workflow_type: WorkflowType, optional
            Type of workflow to create. Defaults to a data workflow.

        Returns
        -------
        IWorkflow
            Created ``IWorkflow`` instance.
        """

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
        IFormat
            Format object that formats in the given style.
        """

    @abstractmethod
    def get_preference(self, pref: str) -> Union[bool, int, float, str]:
        """
        Get the value of a preference.

        Preferences control how the engine behaves in various ways.
        The value returned may be ``bool``, ``int``, ``float``, or
        ``str`` typed.

        Parameters
        ----------
        pref: str
            Name of the preference for which to return the value.

        Returns
        -------
        Union[bool, int, float, str]
            Value of the given preference.
        """

    @abstractmethod
    def set_preference(self, pref: str, value: Union[bool, int, float, str]) -> None:
        """
        Set the value of a preference.

        Preferences control how the engine behaves in various ways.
        The value may be ``bool`, ``int`, ``float``, or ``str`` typed.

        Parameters
        ----------
        pref: str
            Name of the preference to set.
        value: Union[bool, int, float, str]
            Value to set.
        """

    @abstractmethod
    def get_units(self) -> Mapping[str, Collection[str]]:
        """
        Get available units by category.

        Returns
        -------
        Mapping[str, Collection[str]]
            Mapping representing the units available in the engine.
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
        bool
            ``True`` if in Run-Only mode; otherwise, ``False``.
        """
