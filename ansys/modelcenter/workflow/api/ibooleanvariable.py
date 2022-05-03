from abc import ABC, abstractmethod

from ansys.modelcenter.workflow.api.ivariable import IVariable


class IBooleanVariable(IVariable, ABC):
    """
    COM instance.

    Implements IVariable.
    """

    @abstractmethod
    def set_initial_value(self, value: bool) -> None:
        """
        Sets the initial value of the variable.

        Parameters
        ----------
        value
            The initial value.
        """
        raise NotImplementedError
