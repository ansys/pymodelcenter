from ansys.modelcenter.workflow.api.ivariable import IVariable


class IStringVariable(IVariable):
    """
    COM instance.

    Implements IVariable.
    """

    @property
    def value(self) -> str:
        """
        Value of the variable.
        """
        raise NotImplementedError

    @property
    def value_absolute(self) -> str:
        """
        The value of the variable. (Fetched without attempting to validate)
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

    def set_initial_value(self, value: str) -> None:
        """
        Sets the initial value of the variable.

        Parameters
        ----------
        value
            Initial value.
        """
        raise NotImplementedError
