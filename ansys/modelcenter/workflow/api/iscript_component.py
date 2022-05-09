"""Definition of ScriptComponent."""
import clr

from .ivariable import IVariable
from .icomponent import IComponent

clr.AddReference("phoenix-mocks/Phoenix.Mock.v45")
from Phoenix.Mock import MockScriptComponent


class IScriptComponent(IComponent):
    """A Script Component in a Workflow."""

    def __init__(self, instance: MockScriptComponent):
        """Initialize."""
        super().__init__(instance)

    @property
    def language(self) -> str:
        """The script language."""
        return self._instance.language

    @language.setter
    def language(self, value: str) -> None:
        """The script language.

        Must be set prior to setting the source.

        Parameters
        ----------
        value : str
            The new value of the script language.
        """
        self._instance.language = value

    @property
    def timeout(self) -> float:
        """The script timeout in seconds."""
        return self._instance.timeout

    @timeout.setter
    def timeout(self, value: float) -> None:
        """The script timeout in seconds.

        Use -1 to set no timeout.

        Parameters
        ----------
        value : float
            The new value of the script timeout in seconds.
        """
        self._instance.timeout = value

    @property
    def forward_schedule(self) -> bool:
        """True to run the component in forward scheduling mode."""
        return self._instance.forwardSchedule

    @forward_schedule.setter
    def forward_schedule(self, value: bool) -> None:
        """True to run the component in forward scheduling mode.

        Parameters
        ----------
        value : bool
            The new value of the forward_schedule.
        """
        self._instance.forwardSchedule = value

    @property
    def pre_validate(self) -> bool:
        """True to pre-validate the component."""
        return self._instance.prevalidate

    @pre_validate.setter
    def pre_validate(self, value: bool) -> None:
        """True to pre-validate the component.

        Parameters
        ----------
        value : bool
            The new value of the pre_validate.
        """
        self._instance.prevalidate = value

    @property
    def source_script(self) -> str:
        """
        The source script code of the script component.

        Returns
        -------
        str :
            The source script
        """
        return self._instance.getSourceScript()

    @source_script.setter
    def source_script(self, value: str) -> None:
        """
        Set the source script code of the script component to the \
        given string.

        The source code is parsed based on the current language setting.
        The script language should be set before calling this function.

        Parameters
        ----------
        value : str
            String value to use as the script code.
        """
        self._instance.setSourceFromString(value)

    # TODO: Seems redundant to source_script property.
    def set_source_from_file(self, file: str) -> None:
        """
        Set the source script code of the script component to the \
        contents of the file.

        The source code is parsed based on the current language
        setting.  The script language should be set before calling this
        function.

        Parameters
        ----------
        file : str
            The full path of the file.
        """
        self._instance.setSourceFromString(file)

    def add_variable(self, name: str, type_: str, state: str) -> IVariable:
        """
        Add the variable to the component.

        Parameters
        ----------
        name : str
            The name of the variable.
        type_ : str
            The type of the variable e.x. "double", "string[]",
            "object", etc.
        state : str
            The state of the variable e.x. "input", "output".

        Returns
        -------
        The IVariable object of the newly created variable."
        """
        mcapi_variable = self._instance.addVariable(name, type_, state)
        # TODO: Uncomment when implemented (merged with `feat/icomponent-2`).
        return mcapi_variable  # IVariableConverter.from_dot_net(mcapi_variable)

    def remove_variable(self, name: str) -> None:
        """
        Removes the variable from the component.

        Parameters
        ----------
        name : str
            The name of the variable to remove.
        """
        self._instance.removeVariable(name)

    def set_variables(self, inputs: str, outputs: str) -> None:
        """
        Set the variables of the component.

        Previous variables of this component are removed.

        Parameters
        ----------
        inputs : str
            Comma separated list of input variables e.g.
            "long n, double[] p, ..."
        outputs : str
            Comma separated list of output variables e.g.
            "double x, string y, ..."
        """
        self._instance.setVariables(inputs, outputs)
