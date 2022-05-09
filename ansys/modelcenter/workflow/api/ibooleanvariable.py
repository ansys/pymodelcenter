from ansys.modelcenter.workflow.api.ivariable import IVariable


class IBooleanVariable(IVariable):
    """
    COM instance.

    Implements IVariable.
    """

    def set_initial_value(self, value: bool) -> None:
        """
        Sets the initial value of the variable.

        Parameters
        ----------
        value
            The initial value.
        """
        raise NotImplementedError
