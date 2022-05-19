from typing import Optional, Sequence
from overrides import overrides

import ansys.common.variableinterop as acvi
from .variable_links import VariableLink
from .iarray import IArray
from .irefprop import IRefArrayProp
from .ivariable import VarType
import clr
clr.AddReference('phoenix-mocks/Phoenix.Mock.v45')
import Phoenix.Mock as mocks


class IReferenceArray(IArray[mocks.MockReferenceArray]):
    """
    Hold a reference to an array.

    Implements IVariable.
    """

    def __init__(self, wrapped: mocks.MockReferenceArray):
        """
        Initialize.

        Parameters
        ----------
        name : str
            The name of the variable.
        state : VarType
            The state of the variable.
        """
        self._wrapped = wrapped
        self._standard_metadata = acvi.RealArrayMetadata()

####################################################################################################
# region Inherited from IVariable

    @property
    @overrides
    def value(self) -> acvi.IVariableValue:
        return acvi.RealArrayValue.from_api_string(self._wrapped.toString())

    @value.setter
    @overrides
    def value(self, new_value: acvi.IVariableValue):
        self._wrapped.set_value(new_value)

    @property
    @overrides
    def value_absolute(self) -> acvi.IVariableValue:
        pass

    @property
    @overrides
    def standard_metadata(self) -> acvi.CommonVariableMetadata:
        return self._standard_metadata

    @standard_metadata.setter
    @overrides
    def standard_metadata(self, value: acvi.CommonVariableMetadata):
        self._standard_metadata = value

    @property
    @overrides
    def has_changed(self) -> bool:
        return self._wrapped.hasChanged

    @property
    @overrides
    def hide(self) -> bool:
        return self._wrapped.hide

    @hide.setter
    def hide(self, value: bool):
        self._wrapped.hide = value

    @property
    @overrides
    def owning_component(self) -> object:
        return self._wrapped.OwningComponent

    @overrides
    def is_valid(self) -> bool:
        return self._wrapped.isValid()

    @overrides
    def validate(self) -> None:
        self._wrapped.validate()

    @overrides
    def get_name(self) -> str:
        return self._wrapped.getName()

    @overrides
    def get_full_name(self) -> str:
        return self._wrapped.getFullName()

    @overrides
    def get_type(self) -> str:
        return self._wrapped.getType()

    def is_input(self) -> bool:
        return self._wrapped.isInput()

    def to_string(self) -> str:
        return self._wrapped.toString()

    def from_string(self, value: str) -> None:
        self._wrapped.fromString(value)

    def to_string_absolute(self) -> str:
        return self._wrapped.toStringAbsolute()

    def invalidate(self) -> None:
        self._wrapped.invalidate()

    @overrides
    def direct_precedents(self, follow_suspended: bool = False,
                          reserved: Optional[object] = False) -> Sequence['IVariable']:
        return self._wrapped.directPrecedents(follow_suspended, reserved)

    @overrides
    def direct_dependents(self, follow_suspended: bool = False,
                          reserved: Optional[object] = None) -> Sequence['IVariable']:
        return self._wrapped.directDependents(follow_suspended, reserved)

    @overrides
    def precedent_links(self, reserved: Optional[object] = None) -> Sequence[VariableLink]:
        return self._wrapped.precedentLinks(reserved)

    @overrides
    def dependent_links(self, reserved: Optional[object] = None) -> Sequence[VariableLink]:
        return self._wrapped.dependentLinks(reserved)

    @overrides
    def precedents(self, follow_suspended: bool = False,
                   reserved: Optional[object] = None) -> Sequence['IVariable']:
        return self._wrapped.precedents(follow_suspended, reserved)

    @overrides
    def dependents(self, follow_suspended: bool = False,
                   reserved: Optional[object] = None) -> Sequence['IVariable']:
        return self._wrapped.dependents(follow_suspended, reserved)

    @overrides
    def is_input_to_component(self) -> bool:
        return self._wrapped.isInputToComponent()

    @overrides
    def is_input_to_model(self) -> bool:
        return self._wrapped.isInputToModel()

    def set_metadata(self, name: str, type_: object, value: object, access: object,
                     archive: bool) -> None:
        self._wrapped.setMetadata(name, type_, value, access, archive)

    def get_metadata(self, name: str) -> object:
        return self._wrapped.getMetadata(name)

# endregion
####################################################################################################

####################################################################################################
# region Inherited from IArray

    @property
    def size(self) -> int:
        return self._wrapped.size

    @size.setter
    def size(self, value):
        self._wrapped.size = value

    @property
    @overrides
    def auto_size(self) -> bool:
        return self._wrapped.autoSize

    @auto_size.setter
    def auto_size(self, value):
        self._wrapped.autoSize = value

    @property
    def num_dimensions(self) -> int:
        return self._wrapped.numDimensions

    @num_dimensions.setter
    def num_dimensions(self, value):
        self._wrapped.numDimensions = value

    @property
    def length(self) -> int:
        return self._wrapped.length

    @length.setter
    def length(self, value):
        self._wrapped.length = value

    def to_string_ex(self, index: int) -> str:
        return self._wrapped.toStringEx(index)

    def from_string_ex(self, value: str, index: int) -> None:
        self._wrapped.fromStringEx(value, index)

    def to_string_absolute_ex(self, index: int) -> str:
        pass

    def get_length(self, dim: Optional[object]) -> int:
        pass

    def set_length(self, length: int, dim: Optional[object]) -> None:
        pass

    def set_dimensions(self, d1: int, d2: Optional[object], d3: Optional[object],
                       d4: Optional[object], d5: Optional[object], d6: Optional[object],
                       d7: Optional[object], d8: Optional[object], d9: Optional[object],
                       d10: Optional[object]) -> None:
        # 'args' needs to be the first method local variable declared for the wrapped call to work
        args = locals().values()
        self._wrapped.setDimensions(*args)

    def get_size(self, dim: Optional[object]) -> int:
        return self._wrapped.getSize(dim)

    def set_size(self, length: int, dim: Optional[object]) -> None:
        self._wrapped.setSize(length, dim)

    def get_dimensions(self) -> object:
        return self._wrapped.getDimensions()

# endregion
####################################################################################################

    @property
    def auto_grow(self) -> bool:
        """
        Whether or not the reference array is set to automatically \
        grow.
        """
        return self._wrapped.autoGrow

    @auto_grow.setter
    def auto_grow(self, value):
        self._wrapped.autoGrow = value

    def get_value(self, index: int) -> float:
        """
        Gets the value of an array element.

        Parameters
        ----------
        index : int
            Index of the array element (0-based index).

        Returns
        -------
        The value.
        """
        return self._wrapped.getValue(index)

    def set_value(self, value: float, index: int) -> float:
        """
        Sets the value of an array element.

        Parameters
        ----------
        value : float
            New value.
        index : int
            Index of the array element (0-based index).

        Returns
        -------

        """
        return self._wrapped.setValue(value, index)

    def create_ref_prop(self, name: str, type_: str) -> IRefArrayProp:
        """
        Creates a reference property for the array.

        Parameters
        ----------
        name : str
            Name of the reference property.
        type_ : str
            Type of reference property to create. Allowed types are:
            double, long, boolean, and string.

        Returns
        -------
        IRefArrayProp object.
        """
        return IRefArrayProp('', '', self._wrapped.createRefProp(name, type_))

    def get_ref_prop_value(self, name: str, index: int) -> object:
        """
        Gets the value of a specified reference property for an element \
        in the array.

        Parameters
        ----------
        name : str
            Name of the reference property.
        index : int
            Index of the array element (0-based index).

        Returns
        -------
        The value as a variant.
        """
        return self._wrapped.getRefPropValue(name, index)

    def set_ref_prop_value(self, name: str, index: int, value: str) -> None:
        """
        Sets the value of a specified reference property for an \
        element in the array.

        Parameters
        ----------
        name : str
            Name of the reference property.
        index : int
            Index of the array element (0-based index).
        value : str
            New value.
        """
        self._wrapped.setRefPropValue(name, index, value)

    def get_ref_prop_value_absolute(self, name: str, index: int) -> object:
        """
        Gets the value of a specified reference property for an element \
        in the array without running to validate.

        Parameters
        ----------
        name : str
            Name of the reference property.
        index : int
            Index of the array element (0-based index).

        Returns
        -------
        The value as a variant.
        """
        return self._wrapped.getRefPropValueAbsolute(name, index)

    def referenced_variables(self, index: int) -> object:
        """
        Gets the reference variables of the index element of the array.

        Parameters
        ----------
        index : int
            Index of the array element (0-based index).

        Returns
        -------
        The references variables of the element.

        """
        return self._wrapped.get_referencedVariables(index)

    def referenced_variable(self, index: int) -> object:
        """
        Gets the reference variable of the index element of the array.

        Convenience method for if the indexed variable only has one
        reference.

        Parameters
        ----------
        index : int
            Index of the array element (0-based index).

        Returns
        -------
        The reference variable of the index element.
        """
        return self._wrapped.get_referencedVariable(index)

    def get_value_absolute(self, index: int) -> float:
        """
        Gets the value of the variable at a specific location without \
        validating.

        Parameters
        ----------
        index : int
            The array element index (0-based index).

        Returns
        -------
        The reference value.
        """
        return self._wrapped.getValueAbsolute(index)
