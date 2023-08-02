"""Contains definitions for assemblies."""
from abc import ABC, abstractmethod
from enum import Enum
from typing import Optional, Tuple

import ansys.engineeringworkflow.api as aew_api
import ansys.modelcenter.workflow.api.igroup as igroup
import ansys.modelcenter.workflow.api.irenamable_elements as renamable_element
import ansys.tools.variableinterop as atvi


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
        """Get the index of the assembly within its parent assembly."""

    @property
    @abstractmethod
    def parent_assembly(self) -> Optional["IAssembly"]:
        """
        Get the parent assembly of this assembly.

        Returns
        -------
        Optional[IAssembly]
            The parent assembly or None if this assembly is the root of the workflow.
        """

    @abstractmethod
    def get_analysis_view_position(self) -> Tuple[int, int]:
        """
        Get the position on the analysis view.

        Returns
        -------
        Tuple[int, int]
            A 2-tuple where the first element is the x-coordinate and the second element is the
            y-coordinate.
        """


class IAssembly(
    renamable_element.IRenamableElement,
    aew_api.IControlStatement,
    igroup.IGroupOwner,
    IAssemblyChild,
    ABC,
):
    """
    A ModelCenter assembly organizes components and other assemblies in a workflow.

    Additionally, assemblies can have datapins appended to themselves,
    allowing them to act as a way to abstract subordinate parts of the model.

    Each ModelCenter workflow has an assembly as its root element, containing all other assemblies.
    """

    # ModelCenter specific

    @abstractmethod
    def add_assembly(
        self,
        name: str,
        av_pos: Optional[Tuple[int, int]] = None,
        assembly_type: Optional[AssemblyType] = None,
    ) -> "IAssembly":
        """
        Create a sub-Assembly in the current Assembly with a specific type and position.

        Parameters
        ----------
        name : str
            the name of the subassembly
        av_pos : Optional[Tuple[int,int]]
            the position of the subassembly in the parent assembly's analysis view
        assembly_type : AssemblyType
            the type of assembly to create. If None is passed, a regular data-dependency assembly
            is created (same as passing AssemblyType.ASSEMBLY).
        Returns
        -------
        IAssembly
            The created assembly object.
        """

    def add_datapin(self, name: str, mc_type: atvi.VariableType) -> aew_api.IDatapin:
        """
        Create a datapin on this assembly.

        Parameters
        ----------
        name : str
            Name of the new datapin to create.

        mc_type
            The type for the new datapin.

        Returns
        -------
        IDatapin
            An object representing the created datapin.
        """

    @abstractmethod
    def delete_datapin(self, name: str) -> bool:
        """
        Delete the specified datapin.

        Variable objects that represent the specified datapin will become invalid.
        If there is no datapin with the specified name, no error will be thrown.

        Parameters
        ----------
        name : str
            Name of the datapin to be deleted.

        Returns
        -------
        bool
            True if the specified datapin was located and deleted,
            False if it was not and no action was taken.
        """
