"""Contains definitions for assemblies."""
from abc import ABC, abstractmethod
from typing import Optional, Sequence, Union

import ansys.common.variableinterop as acvi
import ansys.engineeringworkflow.api as aew_api

import ansys.modelcenter.workflow.api.custom_metadata_owner as custom_mo
import ansys.modelcenter.workflow.api.igroup as igroup
import ansys.modelcenter.workflow.api.renamable_element as renamable_element


class IAssemblyChild(ABC):
    """Defines methods related to being the child element of an assembly."""

    @property
    @abstractmethod
    def index_in_parent(self) -> int:
        """Get the index of the assembly within its parent assembly."""
        raise NotImplementedError()

    @property
    @abstractmethod
    def parent_assembly(self) -> Optional["IAssembly"]:
        """
        Get the parent assembly of this assembly.

        Returns
        -------
        The parent assembly or None if this assembly is the root of the workflow.
        """
        raise NotImplementedError()


class IAssembly(
    renamable_element.IRenamableElement,
    custom_mo.ICustomMetadataOwner,
    aew_api.IControlStatement,
    igroup.IGroupOwner,
    IAssemblyChild,
    ABC,
):
    """
    A ModelCenter assembly organizes components and other assemblies in a workflow.

    Additionally, assemblies can have variables appended to themselves,
    allowing them to act as a way to abstract subordinate parts of the model.

    Each ModelCenter workflow has an assembly as its root element, containing all other assemblies.
    """

    # ModelCenter specific

    @property
    @abstractmethod
    def assemblies(self) -> Sequence["IAssembly"]:
        """Get a list of child assemblies of this assembly."""
        raise NotImplementedError()

    @abstractmethod
    def add_assembly(
        self,
        name: str,
        x_pos: Optional[int],
        y_pos: Optional[int],
        assembly_type: Optional[str] = None,
    ) -> "IAssembly":
        """
        This method creates a sub-Assembly in the current Assembly \
        with a specific type and position.

        Parameters
        ----------
        name : str
            the name of the subassembly
        x_pos : Optional[int]
            the position of the sub-assembly on the x axis. Ignored if y_pos is not also specified.
        y_pos : Optional[int]
            the position of the sub-assembly on the y axis. Ignored if x_pos is not also specified.
        assembly_type :

        Returns
        -------
        The created assembly object.
        """
        raise NotImplementedError()

    # TODO: add constants / enum for ModelCenter type strings?
    def add_variable(self, name: str, mc_type: Union[acvi.VariableType, str]) -> aew_api.IVariable:
        """
        Create a variable on this assembly.

        Parameters
        ----------
        name : str
            Name of the new variable to create.

        mc_type
            The type for the new variable.
            The caller may either specify a type from the Ansys Common Variable Interop library,
            or a string for a particular ModelCenter type.
            In addition to the standard Ansys Common Variable Interop types
            ModelCenter supports some additional internal geometry types.
            The following string values are acceptable:
               - double
               - int
               - boolean
               - string
               - file
               - double[]
               - int[]
               - boolean[]
               - string[]
               - quadfacet
               - surfaceofrevolution
               - nurbs
               - bspline
               - ruled
               - skinned
               - vrml
               - node

        Returns
        -------
        An object representing the created variable.
        """
        raise NotImplementedError()

    @abstractmethod
    def delete_variable(self, name: str) -> bool:
        """
        Delete the specified variable.

        Variable objects that represent the specified variable will become invalid.
        If there is no variable with the specified name, no error will be thrown.

        Parameters
        ----------
        name : str
            Name of the variable to be deleted.

        Returns
        -------
        True if the specified variable was located and deleted,
        False if it was not and no action was taken.
        """
        raise NotImplementedError()
