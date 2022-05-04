"""Definition of IfComponent."""
import clr

from .icomponent import IComponent

clr.AddReference("phoenix-mocks/Phoenix.Mock.v45")
from Phoenix.Mock import MockIfComponent


class IIfComponent(IComponent):
    """Component for creating branching paths in a process workflow."""

    def __init__(self, instance: MockIfComponent):
        """Initialize."""
        super().__init__(instance)

    @property
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
        return self._instance.exclusive

    @exclusive.setter
    def exclusive(self, value: bool) -> None:
        """
        Setter for the exclusive property.

        Parameters
        ----------
        value : bool
            The new value.
        """
        self._instance.exclusive = value

    @property
    def run_last_branch_by_default(self) -> bool:
        """
        Whether there is an else branch that is run if no conditions \
        are met.

        Returns
        -------
        True if there is an else branch, False otherwise.
        """
        return self._instance.runLastBranchByDefault

    @run_last_branch_by_default.setter
    def run_last_branch_by_default(self, value: bool) -> None:
        """
        Setter for run_last_branch_by_default property.

        Parameters
        ----------
        value: bool
            The new value.
        """
        self._instance.runLastBranchByDefault = value

    @property
    def num_branches(self) -> int:
        """Get the number of branches."""
        return self._instance.getNumBranches()

    def get_branch_condition(self, index: int) -> str:
        """
        Gets the branch condition.

        Parameters
        ----------
        index: int
            Index of the branch.

        Returns
        -------
        The branch condition.
        """
        return self._instance.getBranchCondition(index)

    def set_branch_condition(self, index: int, condition: str) -> None:
        """
        Set the branch condition.

        Parameters
        ----------
        index: int
            Index of the branch.
        condition: str
            The new condition.
        """
        self._instance.setBranchCondition(index, condition)

    def get_branch_name(self, index: int) -> str:
        """
        Return the name of the branch.

        Parameters
        ----------
        index: int
            Index of the branch.

        Returns
        -------
        The name of the branch.
        """
        return self._instance.getBranchName(index)

    def rename_branch(self, index: int, name: str) -> None:
        """
        Rename the branch to the given name.

        Parameters
        ----------
        index: int
            Index of the branch.
        name: str
            New name of the branch.
        """
        return self._instance.renameBranch(index, name)
