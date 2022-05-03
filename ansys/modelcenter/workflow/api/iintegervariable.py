from abc import ABC, abstractmethod

from ansys.modelcenter.workflow.api.ivariable import IVariable


class IIntegerVariable(IVariable, ABC):
    """
    COM instance.

    Implements IVariable.
    """

    @property
    def value(self) -> int:
        """
        Value of the variable.
        """
        raise NotImplementedError

    @property
    def value_absolute(self) -> int:
        """
        The value of the variable (Fetched without attempting to validate).
        """
        raise NotImplementedError

    @property
    def lower_bound(self) -> int:
        """
        Lower bound of the variable.
        """
        raise NotImplementedError

    @property
    def upper_bound(self) -> int:
        """
        Upper bound of the variable.
        """
        raise NotImplementedError

    @property
    def units(self) -> str:
        """
        Units of the variable.
        """
        raise NotImplementedError

    @property
    def description(self) -> str:
        """
        Description of the variable.
        """
        raise NotImplementedError

    @property
    def enum_values(self) -> str:
        """
        Enumerated values of the variable.
        """
        raise NotImplementedError

    @property
    def enum_aliases(self) -> str:
        """
        Enumerated aliases of the variable.
        """
        raise NotImplementedError

    @property
    def format(self) -> str:
        """
        Format of the variable.
        """
        raise NotImplementedError

    @abstractmethod
    def set_initial_value(self, value: int) -> None:
        """
        Sets the initial value of the variable.

        Parameters
        ----------
        value
            Initial value.
        """
        raise NotImplementedError

    @abstractmethod
    def has_lower_bound(self) -> bool:
        """
        Whether or not the variable has an lower bound.

        Returns
        -------
        bool
            yes(TRUE) or no(FALSE).
        """
        raise NotImplementedError

    @abstractmethod
    def has_upper_bound(self) -> bool:
        """
        Whether or not the variable has an upper bound.

        Returns
        -------
        bool
            yes(TRUE) or no(FALSE).
        """
        raise NotImplementedError

    @abstractmethod
    def to_formatted_string(self) -> str:
        """
        Converts the value to a formatted string.

        Returns
        -------
        str
            The formatted value.
        """
        raise NotImplementedError

    @abstractmethod
    def from_formatted_string(self, value: str) -> None:
        """
        Sets the value from a formatted string.

        Parameters
        ----------
        value
            Formatted value to load.
        """
        raise NotImplementedError

    @abstractmethod
    def to_formatted_string_absolute(self) -> str:
        """
        Converts the value to a formatted string without validating.

        Returns
        -------
        str
            The formatted value.
        """
        raise NotImplementedError

    @abstractmethod
    def clear_upper_bound(self) -> None:
        """
        Clears the lower bound property of the variable if it has previously been set.
        """
        raise NotImplementedError

    @abstractmethod
    def clear_lower_bound(self) -> None:
        """
        Clears the upper bound property of the variable if it has previously been set.
        """
        raise NotImplementedError
