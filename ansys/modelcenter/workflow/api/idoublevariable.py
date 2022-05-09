import ansys.common.variableinterop as acvi

from ansys.modelcenter.workflow.api.ivariable import IVariable


class IDoubleVariable(IVariable):
    """
    COM instance.

    Implements IVariable.
    """

    @property
    def value(self) -> acvi.RealValue:
        """
        Value of the variable.
        """
        return acvi.RealValue(self._instance.value)

    @value.setter
    def value(self, value: float):
        self._instance.value = value

    @property
    def value_absolute(self) -> float:
        """
        The value of the variable. (Fetched without attempting to validate)
        """
        raise NotImplementedError

    @property
    def lower_bound(self) -> float:
        """
        Lower bound of the variable.
        """
        raise NotImplementedError

    @property
    def upper_bound(self) -> float:
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

    def set_initial_value(self, value: float) -> None:
        """
        Sets the initial value of the variable.

        Parameters
        ----------
        value
            The initial value.
        """
        raise NotImplementedError

    def has_lower_bound(self) -> bool:
        """
        Finds out whether or not the variable has an lower bound.

        Returns
        -------
        bool
            yes(TRUE) or no(FALSE).
        """
        raise NotImplementedError

    def has_upper_bound(self) -> bool:
        """
        Finds out whether or not the variable has an upper bound.

        Returns
        -------
        bool
            yes(TRUE) or no(FALSE).
        """
        raise NotImplementedError

    def to_formatted_string(self) -> str:
        """
        Converts the value to a formatted string, validating the variable if necessary.

        Returns
        -------
        str
            A formatted string.
        """
        raise NotImplementedError

    def from_formatted_string(self, value: str) -> None:
        """
        Sets the value from a formatted string.

        Parameters
        ----------
        value
            Formatted value to load.
        """
        raise NotImplementedError

    def to_formatted_string_absolute(self) -> str:
        """
        Converts the value to an absolute formatted string.

        Returns
        -------
        str
            An absolute formatted string.
        """
        raise NotImplementedError

    def clear_upper_bound(self) -> None:
        """
        Clears the upper bound property of the variable if it has previously been set.
        """
        raise NotImplementedError

    def clear_lower_bound(self) -> None:
        """
        Clears the lower bound property of the variable if it has previously been set.
        """
        raise NotImplementedError
