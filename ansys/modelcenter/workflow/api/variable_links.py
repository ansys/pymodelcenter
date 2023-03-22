"""Defines classes and functions for working with VariableLinks."""


class VariableLink:
    """Represents a link between two variables in the workflow."""

    def __init__(self, lhs_id: str, rhs: str):
        """
        Construct a new instance.

        Parameters
        ----------
        link :
            Currently, the mock link object to wrap.
        """
        self._lhs_id = lhs_id
        self._rhs = rhs

    def __str__(self) -> str:
        """Convert this object to a string."""
        return "{LHS: " + self._lhs_id + ", RHS: " + self._rhs + "}"

    def suspend_link(self) -> None:
        """Causes the link to be suspended."""
        raise NotImplementedError

    def resume_link(self) -> None:
        """Resumes the link if it was suspended."""
        raise NotImplementedError

    def break_link(self) -> None:
        """
        Break the link.

        Breaking the link removes the dependencies between the left-hand and right-hand side of the
        link. This object becomes invalid and cannot be used after calling this method.
        """
        raise NotImplementedError

    @property
    def lhs(self) -> str:
        """
        The left-hand side of the link.

        The left-hand side receives a value from the right-hand
        side (analogous to a variable assignment in most languages). This will always be
        a simple variable name.
        """
        return self._lhs_id

    @property
    def rhs(self) -> str:
        """
        The right-hand side of the link equation.

        You can change the link by changing this value.
        """
        return self._rhs

    # @rhs.setter
    # def rhs(self, rhs: str) -> None:
    #     """
    #     The right-hand side of the link equation.
    #
    #     You can change the link by changing this value.
    #
    #     Parameters
    #     ----------
    #     rhs: str
    #         the new value for the link's right-hand side.
    #     """
    #     self._rhs = rhs
    # TODO: not on grpc api, may want to just remove
