from .icomponent import IComponent


class IIfComponent(IComponent):
    """COM Instance.

    @implements IComponent"""

    @property
    def exclusive(self) -> bool:
        """
        The If exclusive mode.

        Returns
        -------
        Yes (TRUE) or no (FALSE)."
        """
        # boolean exclusive;
        raise NotImplementedError

    @property
    def run_last_branch_by_default(self) -> bool:
        """
        The "has default" flag.

        Returns
        -------
        @return    YES (TRUE) or no (FALSE)."
        """
        # boolean runLastBranchByDefault;
        raise NotImplementedError

    def get_num_branches(self) -> int:
        """Gets the number of branches."""
        # int getNumBranches();
        raise NotImplementedError

    def get_branch_condition(self, index: int) -> str:
        """
        "Gets the branch condition.

        Parameters
        ----------
        index :
            Index of the branch.

        Returns
        -------
        The branch condition.

        """
        # BSTR getBranchCondition( int index );
        raise NotImplementedError

    def set_branch_condition(self, index: int, condition: str) -> None:
        """
        Sets the branch condition.

        Parameters
        ----------
        index :
            Index of the branch.
        condition :
            The new condition."
        """
        # void setBranchCondition( int index, BSTR condition );
        raise NotImplementedError

    def get_branch_name(self, index: int) -> str:
        """
        Returns the name of the branch.

        Parameters
        ----------
        index :
            Index of the branch.

        Returns
        -------
        The name of the branch.
        """
        # BSTR getBranchName( int index );
        raise NotImplementedError

    def rename_branch(self, index: int, name: str) -> None:
        """
        Renames the branch to the given name.

        Parameters
        ----------
        index :
            Index of the branch.
        name :
            New name of the branch."
        """
        # void renameBranch( int index, BSTR name );
        raise NotImplementedError
