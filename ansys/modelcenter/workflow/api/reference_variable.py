from ansys.modelcenter.workflow.api import IRefProp


# TODO: inherit from IVariable when available.
class IReferenceVariable:   # (IVariable):
    """COM Instance.
    @implements IVariable"""

    @property
    def value(self) -> float:
        """Value of the variable."""
        # double value;
        raise NotImplementedError

    @property
    def reference(self) -> str:
        """Reference of the variable."""
        # BSTR reference;
        raise NotImplementedError

    @property
    def referenced_variables(self) -> object:
        """Gets the referenced variables."""
        # VARIANT referencedVariables;
        raise NotImplementedError

    @property
    def referenced_variable(self) -> object:
        """
        Gets the referenced variable.

        Convenience method for if there is only one reference.

        Returns
        -------

        """
        # VARIANT referencedVariable;
        raise NotImplementedError

    def create_ref_prop(self,  name: str, type_: str) -> IRefProp:
        """
        Creates a reference property for the variable.

        Parameters
        ----------
        name :
            Name of the reference property.
        type_ :
            Type of reference property to create. Allowed types are:
            double, long, boolean, and string.

        Returns
        -------
        IRefProp object.
        """
        # IDispatch* createRefProp( BSTR name, BSTR type );
        raise NotImplementedError

    def get_ref_prop_value(self, name: str) -> object:
        """
        Gets the value of a specified reference property for the \
        variable.

        Parameters
        ----------
        name :
            Name of the reference property.

        Returns
        -------
        The value as a variant.
        """
        # VARIANT getRefPropValue( BSTR name );
        raise NotImplementedError

    def set_ref_prop_value(self, name: str, value: str) -> None:
        """
        Sets the value of a specified reference property for the variable.

        Parameters
        ----------
        name :
            Name of the reference property.
        value :
            New value.
        """
        # void setRefPropValue( BSTR name, BSTR value );
        raise NotImplementedError

    def get_ref_prop_value_absolute(self, name: str) -> object:
        """
        Gets the value of a specified reference property for the \
        variable, without validating first.

        Parameters
        ----------
        name :
            Name of the reference property.

        Returns
        -------
        The value as a variant.
        """
        # VARIANT getRefPropValueAbsolute( BSTR name );
        raise NotImplementedError
