# Copyright (C) 2022 - 2025 ANSYS, Inc. and/or its affiliates.
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
"""Contains definitions for assemblies."""
from abc import ABC, abstractmethod
from enum import Enum
from typing import Optional, Tuple

import ansys.engineeringworkflow.api as aew_api
import ansys.tools.variableinterop as atvi

import ansys.modelcenter.workflow.api.igroup as igroup
import ansys.modelcenter.workflow.api.irenamable_elements as renamable_element


class AssemblyType(Enum):
    """Represents an allowed assembly type in ModelCenter."""

    ASSEMBLY = "Assembly"
    SEQUENCE = "Sequence"
    IF = "If"
    PARALLEL = "Parallel"
    EMPTY = "Empty"
    LOOP = "Loop"
    FOR_EACH = "ForEach"
    FOR = "For"
    WHILE = "While"
    REPEAT_UNTIL = "RepeatUntil"


class IAssemblyChild(ABC):
    """Defines methods related to being the child element of an assembly."""

    @property
    @abstractmethod
    def index_in_parent(self) -> int:
        """Index of the assembly within its parent assembly."""

    @property
    @abstractmethod
    def parent_assembly(self) -> Optional["IAssembly"]:
        """Parent assembly of the assembly.

        Returns
        -------
        Optional[IAssembly]
            Parent assembly or ``None`` if this assembly is the root of
            the workflow.
        """

    @abstractmethod
    def get_analysis_view_position(self) -> Tuple[int, int]:
        """Get the position of the assembly within the analysis view.

        Returns
        -------
        Tuple[int, int]
            Two-element tuple where the first element is the x coordinate and the
            second element is the y coordinate.
        """


class IAssembly(
    renamable_element.IRenamableElement,
    aew_api.IControlStatement,
    igroup.IGroupOwner,
    IAssemblyChild,
    ABC,
):
    """Represents a ModelCenter assembly.

    Assemblies organize components and other assemblies in the workflow.
    Additionally, assemblies can have datapins appended to themselves,
    allowing them to act as a way to abstract subordinate parts of the
    model.

    Each ModelCenter workflow has an assembly as its root element,
    containing all other assemblies.
    """

    # ModelCenter specific

    @abstractmethod
    def add_assembly(
        self,
        name: str,
        av_pos: Optional[Tuple[int, int]] = None,
        assembly_type: Optional[AssemblyType] = None,
    ) -> "IAssembly":
        """Create a subassembly with a specific type and position.

        Parameters
        ----------
        name : str
            Name of the subassembly.
        av_pos : Tuple[int,int], optional
            Position of the subassembly in the parent assembly's analysis view.
            The default is ``None``.
        assembly_type : AssemblyType, optional
            Type of assembly to create. The default is ``None``, in which case a
            regular data-dependency assembly is created. (This is the same
            as passing ``AssemblyType.ASSEMBLY``.)

        Returns
        -------
        IAssembly
            Created assembly object.
        """

    def add_datapin(self, name: str, mc_type: atvi.VariableType) -> aew_api.IDatapin:
        """Create a datapin on the assembly.

        Parameters
        ----------
        name : str
            Name of the datapin.
        mc_type: atvi.VariableType
            Type for the datapin.

        Returns
        -------
        IDatapin
            Object representing the created datapin.
        """

    @abstractmethod
    def delete_datapin(self, name: str) -> bool:
        """Delete a given datapin.

        Variable objects that represent the given datapin become invalid.
        If there is no datapin with the given name, no error is raised.

        Parameters
        ----------
        name : str
            Name of the datapin.

        Returns
        -------
        bool
            ``True`` if the given datapin was located and deleted,
            ``False`` if it was not and no action was taken.
        """
