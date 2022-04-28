"""Defines classes and functions for working with VariableLinks."""


class VariableLink:

    def __init__(self, link):
        self._link = link

    def suspend_link(self) -> None:
        self._link.suspendLink()

    def resume_link(self) -> None:
        self._link.resumeLink()

    def break_link(self) -> None:
        self._link.breakLink()

    @property
    def lhs(self) -> str:
        """
        The left-hand side of the
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
        self._link.RHS = rhs
