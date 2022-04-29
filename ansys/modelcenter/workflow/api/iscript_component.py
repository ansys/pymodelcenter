from .icomponent import IComponent


class IScriptComponent(IComponent):
    """COM Instance.

    @implements IComponent"""

    @property
    def language(self) -> str:
        """The script language.  Must be set prior to setting the \
        source."""
        # BSTR language;
        raise NotImplementedError

    @property
    def timeout(self) -> float:
        """The script timeout in seconds.  Use -1 to set no timeout."""
        # double timeout;
        raise NotImplementedError

    @property
    def forward_schedule(self) -> bool:
        """True to run the component in forward scheduling mode."""
        # boolean forwardSchedule;
        raise NotImplementedError

    @property
    def pre_validate(self) -> bool:
        """True to pre-validate the component."""
        # boolean prevalidate;
        raise NotImplementedError

    def set_source_from_string(self, script: str) -> None:
        """
        Sets the source script code of the script component to the \
        given string.

        The source code is parsed baesd on the current language setting.
        The script language should be set before calling this function.

        Parameters
        ----------
        script :
        @param script string value to use as the script code"
        """
        # void setSourceFromString(BSTR script);
        raise NotImplementedError

    def set_source_from_file(self, file: str) -> None:
        """
        Sets the source script code of the script component to the \
        contents of the file.

        The source code is parsed based on the current language
        setting.  The script language should be set before calling this
        function.

        Parameters
        ----------
        file :
            The full path of the file
        """
        # void setSourceFromFile(BSTR file);
        raise NotImplementedError

    def add_variable(self, name: str, type_: str, state: str) -> object:    # IVariable
        """
        Adds the variable to the component.

        Parameters
        ----------
        name :
            The name of the variable
        type_ :
            The type of the variable e.x. "double", "string[]",
            "object", etc.
        state :
            The state of the variable e.x. "input", "output".

        Returns
        -------
        The IVariable object of the newly created variable"
        """
        # LPDISPATCH addVariable(BSTR name, BSTR type, BSTR state);
        raise NotImplementedError

    def remove_variable(self, name: str) -> None:
        """
        Removes the variable from the component.

        Parameters
        ----------
        name : str
            The name of the variable to remove"
        """
        # void removeVariable(BSTR name);
        raise NotImplementedError

    def set_variables(self, inputs, outputs: str) -> None:
        """
        Sets the variables of the component.

        Previous variables of this component are removed.

        Parameters
        ----------
        inputs :
            Comma separated list of input variables e.g.
            "long n, double[] p, ..."
        outputs :
            Comma separated list of output variables e.g.
            "double x, string y, ..."
        """
        # void setVariables(VARIANT inputs, BSTR outputs);
        raise NotImplementedError

    def get_source_script(self) -> str:
        """
        Gets the source script code of the script component.

        Returns
        -------
        The source script
        """
        # BSTR getSourceScript();
        raise NotImplementedError
