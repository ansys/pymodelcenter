"""Contains common base class for all variables."""
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Collection, Sequence

import ansys.common.variableinterop as acvi
import ansys.engineeringworkflow.api as aew_api

from .ivariable_link import IVariableLink

if TYPE_CHECKING:
    import ansys.modelcenter.workflow.api.icomponent as icomponent


class IVariable(aew_api.IVariable, ABC):
    """Represents a variable in the workflow."""

    @abstractmethod
    def set_metadata(self, new_metadata: acvi.CommonVariableMetadata) -> None:
        """Get the standard metadata for this variable."""

    @property
    @abstractmethod
    def owning_component(self) -> "icomponent.IComponent":
        """
        The component that owns this variable.

        Returns
        -------
        IComponent :
            Owning IComponent object.
        """

    @abstractmethod
    def invalidate(self) -> None:
        """
        Marks the variable as invalid (needs to be computed).

        This will set all dependent variables invalid also.
        """

    @abstractmethod
    def direct_precedents(self, follow_suspended: bool = False) -> Collection["IVariable"]:
        """
        Returns a list of variables that are immediate precedents to the value of this variable.

        This function returns all variables that influence this variable and are directly
        connected via a link to it.

        For scalar variables, the returned list will only ever contain up to one element.
        For array variables, the returned list may contain multiple elements
        when individual indices are linked.

        Parameters
        ----------
        follow_suspended
            When True, suspended links are followed when determining precedents.

        Returns
        -------
        A Collection of IVariables that are immediate precedents of this variable.
        """

    @abstractmethod
    def direct_dependents(self, follow_suspended: bool = False) -> Collection["IVariable"]:
        """
        Returns a list of variables that are immediate dependents of the value of this variable.

        This function returns all variables that are influenced by this variable and are
        directly connected via a link to it.

        Parameters
        ----------
        follow_suspended
            When True, suspended links are followed when determining dependents.

        Returns
        -------
        A Collection of IVariables that are immediate dependents of this variable.
        """

    @abstractmethod
    def precedent_links(self) -> Collection[IVariableLink]:
        """
        Returns a list of links that are immediate precedents to the value of this variable.

        All the returned links will have this variable as the LHS of the equation.
        The returned collection may have more than one element in the case where
        there are direct links to a single variable index.

        Returns
        -------
        A Collection of IVariable links that are immediate precedents of this variable.
        """

    @abstractmethod
    def dependent_links(self) -> Collection[IVariableLink]:
        """
        Returns a list of links that immediately depend on the value of this variable.

        All the returned links will have this variable in the RHS of the equation.

        Returns
        -------
        A Collection of IVariableLinks that are immediate dependents of this variable.
        """

    @abstractmethod
    def precedents(self, follow_suspended: bool = False) -> Sequence["IVariable"]:
        """
        Returns a list of variables that are precedents to the value of this variable.

        This function returns all variables that influence this variable,
        not just directly connected ones.

        Parameters
        ----------
        follow_suspended
            When True, suspended links are followed when determining precedents.

        Returns
        -------
        A Collection of IVariables that influence the value of this variable.
        """

    @abstractmethod
    def dependents(self, follow_suspended: bool = False) -> Sequence["IVariable"]:
        """
        Returns a list of variables that are dependent upon the value of this variable.

        This function returns all variables that are influenced by this variable,
        not just directly connected ones.

        Parameters
        ----------
        follow_suspended
            When True, suspended links are followed when determining dependents.

        Returns
        -------
        A Collection of IVariables that are influenced by the value of this variable.
        """
