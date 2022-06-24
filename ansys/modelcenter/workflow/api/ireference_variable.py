from typing import Sequence, Union

from ansys.common import variableinterop as acvi
import clr
from overrides import overrides

from .dot_net_utils import from_dot_net_list, from_dot_net_to_ivariable, to_dot_net_list
from .idoublevariable import IDoubleVariable
from .irefprop import IRefProp
from .ivariable import IVariable

clr.AddReference("phoenix-mocks/Phoenix.Mock.v45")
from Phoenix.Mock import MockDoubleVariable, MockReferenceVariable


class IReferenceVariable(IVariable):
    """
    Hold a reference to a variable.

    Currently, only valid for real (double) variables.

    Implements IVariable.
    """

    def __init__(self, wrapped: MockReferenceVariable):
        """
        Initialize.

        Parameters
        ----------
        wrapped : MockReferenceVariable
            The .NET MockReferenceVariable to wrap.
        """
        self._wrapped = wrapped
        self._std_metadata: acvi.CommonVariableMetadata = acvi.RealMetadata()

    ####################################################################################################
    # region Inherited from IVariable

    @property
    @overrides
    def value(self) -> acvi.RealValue:
        return acvi.RealValue(self._wrapped.value)

    @value.setter
    @overrides
    def value(self, val: Union[float, acvi.RealValue]):
        self._wrapped.value = val if isinstance(val, acvi.RealValue) else acvi.RealValue(val)

    @property
    @overrides
    def value_absolute(self) -> acvi.RealValue:
        return self.value

    @property
    @overrides
    def standard_metadata(self) -> acvi.CommonVariableMetadata:
        return self._std_metadata

    @standard_metadata.setter
    @overrides
    def standard_metadata(self, value: acvi.CommonVariableMetadata):
        self._std_metadata = value

    # endregion
    ####################################################################################################

    @property
    def reference(self) -> str:
        """Reference of the variable."""
        return self._wrapped.reference

    @reference.setter
    def reference(self, value: str):
        self._wrapped.reference = value

    @property
    def referenced_variables(self) -> Sequence[IDoubleVariable]:
        """Gets the referenced variables."""
        return from_dot_net_list(self._wrapped.referencedVariables, IDoubleVariable)

    @referenced_variables.setter
    def referenced_variables(self, values: Sequence[IDoubleVariable]):
        mock_list = [var._wrapped for var in values]
        self._wrapped.referencedVariables = to_dot_net_list(mock_list, MockDoubleVariable)

    @property
    def referenced_variable(self) -> IVariable:
        """
        Gets the referenced variable.

        Convenience method for if there is only one reference.

        Returns
        -------
        IVariable
            The referenced variable.
        """
        return from_dot_net_to_ivariable(self._wrapped.referencedVariable)

    @referenced_variable.setter
    def referenced_variable(self, value: IVariable):
        self._wrapped.referencedVariable = value._wrapped

    def create_real_ref_prop(self, name: str, type_: str) -> IRefProp:
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
        IRefProp
        """
        return IRefProp(self._wrapped.createRefProp(name, type_))

    def get_real_ref_prop_value(self, name: str) -> acvi.RealValue:
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
        return acvi.RealValue(self._wrapped.getRefPropValue(name))

    def set_real_ref_prop_value(self, name: str, value: str) -> None:
        """
        Sets the value of a specified reference property for the \
        variable.

        Parameters
        ----------
        name : str
            Name of the reference property.
        value : str
            New value.
        """
        self._wrapped.setRefPropValue(name, value)

    def get_real_ref_prop_value_absolute(self, name: str) -> acvi.RealValue:
        """
        Gets the value of a specified reference property for the \
        variable, without validating first.

        Parameters
        ----------
        name : str
            Name of the reference property.

        Returns
        -------
        The value as a variant.
        """
        return acvi.RealValue(self._wrapped.getRefPropValueAbsolute(name))
