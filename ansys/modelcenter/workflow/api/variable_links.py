"""Defines classes and functions for working with links between variables in the workflow."""

from abc import ABC, abstractmethod


class IVariableLink(ABC):
    """Represents a link between two variables in the workflow."""

    # TODO/REDUCE: consider dropping link suspension for Phase II.
    #              When it is implemented, we need to add a getter for suspension state.
    @abstractmethod
    def suspend_link(self) -> None:
        """Causes the link to be suspended."""
        raise NotImplementedError()

    # TODO/REDUCE: consider dropping link suspension for Phase II.
    @abstractmethod
    def resume_link(self) -> None:
        """Resumes the link if it was suspended."""
        raise NotImplementedError()

    @abstractmethod
    def break_link(self) -> None:
        """
        Break the link.

        Breaking the link removes the dependencies between the left-hand and right-hand side of the
        link. This object becomes invalid and cannot be used after calling this method.
        """
        raise NotImplementedError()

    @property
    @abstractmethod
    def lhs(self) -> str:
        """
        The left-hand side of the link.

        The left-hand side receives a value from the right-hand
        side (analogous to a variable assignment in most languages). This will always be
        a simple variable name, except in cases where the link targets a single array index,
        in which case it will be the name of the variable plus an array index.
        """
        raise NotImplementedError()

    @property
    @abstractmethod
    def rhs(self) -> str:
        """
        Get the right-hand side (source) of the link equation.

        This will be a simple equation containing the names of
        the other variables on which this link depends.
        """
        raise NotImplementedError()

    @rhs.setter
    @abstractmethod
    def rhs(self, new_rhs: str) -> None:
        """Set the right-hand side (source) of the link equation."""
        raise NotImplementedError()