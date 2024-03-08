# Copyright (C) 2022 - 2024 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
"""Contains the definition for the engine and associated classes."""
from abc import ABC, abstractmethod
from enum import Enum
from typing import Collection, Mapping, Union

from ansys.engineeringworkflow.api import IFileBasedWorkflowEngine

from .iformat import IFormat
from .iworkflow import IWorkflow


class WorkflowType(Enum):
    """Enumeration of the types of workflows that can be created."""

    DATA = ("dataModel",)
    """Legacy style workflow where execution flow is determined from links
    between components and an execution strategy."""
    PROCESS = "processModel"
    """Modern style workflow where execution flow is explicitly designed by the
    user using flow components."""


class IEngine(IFileBasedWorkflowEngine, ABC):
    """Manages creating and running engineering workflows."""

    @abstractmethod
    def new_workflow(self, name: str, workflow_type: WorkflowType = WorkflowType.DATA) -> IWorkflow:
        """Create a workflow.

        Parameters
        ----------
        name : str
            Filename or path for creating the workflow.
        workflow_type : WorkflowType, optional
            Type of workflow. The default is a data workflow.

        Returns
        -------
        IWorkflow
            Created ``IWorkflow`` instance.
        """

    @abstractmethod
    def get_formatter(self, fmt: str) -> IFormat:
        """Create an instance of a formatter that can be used to format numbers
        to and from a particular string style.

        Parameters
        ----------
        fmt : str
            Specified string format for the ``IFormat`` object.

        Returns
        -------
        IFormat
            Format object that formats in the given style.
        """

    @abstractmethod
    def get_preference(self, pref: str) -> Union[bool, int, float, str]:
        """Get the value of a preference.

        Preferences control how the engine behaves in various ways.
        The data type of the value may be ``bool``, ``float``,
        ``int``, or ``str``.

        Parameters
        ----------
        pref : str
            Name of the preference for the data type to return the value in.

        Returns
        -------
        Union[bool, int, float, str]
            Value of the given preference.
        """

    @abstractmethod
    def set_preference(self, pref: str, value: Union[bool, int, float, str]) -> None:
        """Set the value of a preference.

        Preferences control how the engine behaves in various ways.
        The data type of the value may be ``bool``, ``float``,
        ``int``, or ``str``.

        Parameters
        ----------
        pref : str
            Name of the preference to set.
        value: Union[bool, int, float, str]
            Value to set.
        """

    @abstractmethod
    def get_units(self) -> Mapping[str, Collection[str]]:
        """Get available units by category.

        Returns
        -------
        Mapping[str, Collection[str]]
            Mapping representing the units available in the engine.
            The keys in the map are the names of unit categories,
            and the values are collections containing all the unit names for that category.
        """

    @abstractmethod
    def get_run_only_mode(self) -> bool:
        """Get whether the engine is in run-only mode.

        Run-only mode has lower licensing requirements, but it does not
        allow for the workflow to be edited.

        Returns
        -------
        bool
            ``True`` if in run-only mode, ``False`` otherwise.
        """
