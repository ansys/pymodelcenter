from typing import Optional
from overrides import overrides

from .iref_prop import IRefProp
from .ivariable import IVariable, VarType
import clr
clr.AddReference('phoenix-mocks/Phoenix.Mock.v45')
import Phoenix.Mock as Mocks


class IReferenceVariable(IVariable):
    """
    Hold a reference to a variable.

    Implements IVariable.
    """

    def __init__(self, name: str, state: VarType):
        """
        Initialize.

        Parameters
        ----------
        name : str
            The name of the variable.
        state : VarType
            The state of the variable.
        """
        self._instance = Mocks.MockReferenceVariable(name, state)

####################################################################################################
# region Inherited from IVariable
    @property
    @overrides
    def has_changed(self) -> bool:
        return self._instance.hasChanged

    @property
    @overrides
    def hide(self) -> bool:
        return self._instance.hide

    @hide.setter
    def hide(self, value: bool):
        self._instance.hide = value

    @property
    @overrides
    def owning_component(self) -> object:
        return self._instance.OwningComponent

    @owning_component.setter
    def owning_component(self, value: object):
        self._instance.OwningComponent = value

    @overrides
    def is_valid(self) -> bool:
        return self._instance.isValid()

    @overrides
    def validate(self) -> None:
        self._instance.validate()

    @overrides
    def get_name(self) -> str:
        return self._instance.getName()

    @overrides
    def get_full_name(self) -> str:
        return self._instance.getFullName()

    @overrides
    def get_type(self) -> str:
        return self._instance.getType()

    @overrides
    def is_input(self) -> bool:
        return self._instance.isInput()

    @overrides
    def to_string(self) -> str:
        return self._instance.toString()

    @overrides
    def from_string(self, value: str) -> None:
        self._instance.fromString(value)

    @overrides
    def to_string_absolute(self) -> str:
        return self._instance.toStringAbsolute()

    @overrides
    def invalidate(self) -> None:
        self._instance.invalidate()

    @overrides
    def direct_precedents(self, follow_suspended: Optional[object],
                          reserved: Optional[object]) -> object:
        return self._instance.directPrecedents(follow_suspended, reserved)

    @overrides
    def direct_dependents(self, follow_suspended: Optional[object],
                          reserved: Optional[object]) -> object:
        return self._instance.directDependents(follow_suspended, reserved)

    @overrides
    def precedent_links(self, reserved: Optional[object]) -> object:
        return self._instance.precedentLinks(reserved)

    @overrides
    def dependent_links(self, reserved: Optional[object]) -> object:
        return self._instance.dependentLinks(reserved)

    @overrides
    def precedents(self, follow_suspended: Optional[object], reserved: Optional[object]) -> object:
        return self._instance.precedents(follow_suspended, reserved)

    @overrides
    def dependents(self, follow_suspended: Optional[object], reserved: Optional[object]) -> object:
        return self._instance.dependents(follow_suspended, reserved)

    @overrides
    def is_input_to_component(self) -> bool:
        return self._instance.isInputToComponent()

    @overrides
    def is_input_to_model(self) -> bool:
        return self._instance.isInputToModel()

    @overrides
    def set_metadata(self, name: str, type_: object, value: object, access: object,
                     archive: bool) -> None:
        self._instance.setMetadata(name, type_, value, access, archive)

    @overrides
    def get_metadata(self, name: str) -> object:
        return self._instance.getMetadata(name)

# endregion
####################################################################################################

    @property
    def value(self) -> float:
        """Value of the variable."""
        return self._instance.value

    @value.setter
    def value(self, val: float):
        self._instance.value = val

    @property
    def reference(self) -> str:
        """Reference of the variable."""
        return self._instance.reference

    @reference.setter
    def reference(self, value: str):
        self._instance.reference = value

    @property
    def referenced_variables(self) -> object:
        """Gets the referenced variables."""
        return self._instance.referencedVariables

    @referenced_variables.setter
    def referenced_variables(self, value):
        self._instance.referencedVariables = value

    @property
    def referenced_variable(self) -> object:
        """
        Gets the referenced variable.

        Convenience method for if there is only one reference.

        Returns
        -------

        """
        return self._instance.referencedVariable

    @referenced_variable.setter
    def referenced_variable(self, value):
        self._instance.referencedVariable = value

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
        # TODO: replace when possible (mock is not implemented)
        #  return IRefProp(self._instance.createRefProp(name, type_))
        return IRefProp()

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
        return self._instance.getRefPropValue(name)

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
        self._instance.setRefPropValue(name, value)

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
        return self._instance.getRefPropValueAbsolute(name)
