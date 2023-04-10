"""Definition of IfComponent."""
from abc import ABC, abstractmethod

from .icomponent import IComponent


class IIfComponent(IComponent, ABC):
    """Component for creating branching paths in a process workflow."""

    @property
    @abstractmethod
    def exclusive(self) -> bool:
        """
        Whether the branching condition is exclusive.

        In exclusive mode only the first branch that evaluates to True
        is executed. In inclusive mode all branches that evaluate to
        True are executed.

        Returns
        -------
        True if in exclusive mode, False if in inclusive mode.
        """

    @exclusive.setter
    @abstractmethod
    def exclusive(self, value: bool) -> None:
        """
        Setter for the exclusive property.

        Parameters
        ----------
        value : bool
            The new value.
        """

    @property
    @abstractmethod
    def run_last_branch_by_default(self) -> bool:
        """
        Whether there is an else branch that is run if no conditions \
        are met.

        Returns
        -------
        True if there is an else branch, False otherwise.
        """

    @run_last_branch_by_default.setter
    @abstractmethod
    def run_last_branch_by_default(self, value: bool) -> None:
        """
        Setter for run_last_branch_by_default property.

        Parameters
        ----------
        value : bool
            The new value.
        """

    @property
    @abstractmethod
    def num_branches(self) -> int:
        """Get the number of branches."""

    @abstractmethod
    def get_branch_condition(self, index: int) -> str:
        """
             Get the branch condition.

             Parameters
             ----------
             index : int
                 Index of the branch.

             Returns
             -------
        str :
             The branch condition.
        """

    @abstractmethod
    def set_branch_condition(self, index: int, condition: str) -> None:
        """
        Set the branch condition.

        Parameters
        ----------
        index : int
            Index of the branch.
        condition : str
            The new condition.
        """

    @abstractmethod
    def get_branch_name(self, index: int) -> str:
        """
        Return the name of the branch.

        Parameters
        ----------
        index : int
            Index of the branch.

        Returns
        -------
        The name of the branch.
        """

    @abstractmethod
    def rename_branch(self, index: int, name: str) -> None:
        """
        Rename the branch to the given name.

        Parameters
        ----------
        index : int
            Index of the branch.
        name : str
            New name of the branch.
        """
