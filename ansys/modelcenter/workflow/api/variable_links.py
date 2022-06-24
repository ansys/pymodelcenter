"""Defines classes and functions for working with VariableLinks."""
from typing import Sequence


class VariableLink:
    """Represents a link between two variables in the workflow."""

    def __init__(self, link):
        """
        Construct a new instance.

        Parameters
        ----------
        link :
            Currently, the mock link object to wrap.
        """
        self._link = link

    def suspend_link(self) -> None:
        """Causes the link to be suspended."""
        self._link.suspendLink()

    def resume_link(self) -> None:
        """Resumes the link if it was suspended."""
        self._link.resumeLink()

    def break_link(self) -> None:
        """
        Break the link.

        Breaking the link removes the dependencies between the left-hand and right-hand side of the
        link. This object becomes invalid and cannot be used after calling this method.
        """
        self._link.breakLink()

    @property
    def lhs(self) -> str:
        """
        The left-hand side of the link. The left-hand side receives a value from the right-hand
        side (analagous to a variable assignment in most languages). This will aloways be
        a simple variable name.
        """
        return self._link.LHS

    @property
    def rhs(self) -> str:
        """
        The right-hand side of the link equation.

        You can change the link by changing this value.
        """
        return self._link.RHS

    @rhs.setter
    def rhs(self, rhs: str) -> None:
        """
        The right-hand side of the link equation.

        You can change the link by changing this value.

        Parameters
        ----------
        rhs: str
            the new value for the link's right-hand side.
        """
        self._link.RHS = rhs


def dotnet_links_to_iterable(dotnet_links) -> Sequence[VariableLink]:
    """
    Convert a list of mock links to a Python iterable.

    This currently just wraps every link in the passed-in list, producing a Python list of wrappers.
    A more nuanced approach will be necessary when we switch to a real backend.

    Parameters
    ----------
    dotnet_links:
        An IVariableLinks object from the mock ModelCenter.

    Returns
    -------
    A sequence of variable link objects.
    """
    return [
        VariableLink(dotnet_links.Item(var_index)) for var_index in range(0, dotnet_links.Count)
    ]
