from typing import Optional
from overrides import overrides

from .iarray import IArray
from .irefprop import IRefArrayProp
from .ivariable import VarType
import clr
clr.AddReference('phoenix-mocks/Phoenix.Mock.v45')
import Phoenix.Mock as Mocks


class IReferenceArray(IArray):
    """
    Hold a reference to an array.

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
        self._instance = Mocks.MockReferenceArray(name, state)

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

####################################################################################################
# region Inherited from IArray

    @property
    @overrides
    def size(self) -> int:
        return self._instance.size

    @size.setter
    def size(self, value):
        self._instance.size = value

    @property
    @overrides
    def auto_size(self) -> bool:
        return self._instance.autoSize

    @auto_size.setter
    def auto_size(self, value):
        self._instance.autoSize = value

    @property
    @overrides
    def num_dimensions(self) -> int:
        return self._instance.numDimensions

    @num_dimensions.setter
    def num_dimensions(self, value):
        self._instance.numDimensions = value

    @property
    @overrides
    def length(self) -> int:
        return self._instance.length

    @length.setter
    def length(self, value):
        self._instance.length = value

    @overrides
    def to_string_ex(self, index: int) -> str:
        return self._instance.toStringEx(index)

    @overrides
    def from_string_ex(self, value: str, index: int) -> None:
        self._instance.fromStringEx(value, index)

    @overrides
    def to_string_absolute_ex(self, index: int) -> str:
        pass

    @overrides
    def get_length(self, dim: Optional[object]) -> int:
        pass

    @overrides
    def set_length(self, length: int, dim: Optional[object]) -> None:
        pass

    @overrides
    def set_dimensions(self, d1: int, d2: Optional[object], d3: Optional[object],
                       d4: Optional[object], d5: Optional[object], d6: Optional[object],
                       d7: Optional[object], d8: Optional[object], d9: Optional[object],
                       d10: Optional[object]) -> None:
        # 'args' needs to be the first method local variable declared for the wrapped call to work
        args = locals().values()
        self._instance.setDimensions(*args)

    @overrides
    def get_size(self, dim: Optional[object]) -> int:
        return self._instance.getSize(dim)

    @overrides
    def set_size(self, length: int, dim: Optional[object]) -> None:
        self._instance.setSize(length, dim)

    @overrides
    def get_dimensions(self) -> object:
        return self._instance.getDimensions()

# endregion
####################################################################################################

    @property
    def auto_grow(self) -> bool:
        """
        Whether or not the reference array is set to automatically \
        grow.
        """
        return self._instance.autoGrow

    @auto_grow.setter
    def auto_grow(self, value):
        self._instance.autoGrow = value

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
        return self._instance.getValue(index)

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
        return self._instance.setValue(value, index)

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
        return IRefArrayProp('', '', self._instance.createRefProp(name, type_))

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
        return self._instance.getRefPropValue(name, index)

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
        self._instance.setRefPropValue(name, index, value)

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
        return self._instance.getRefPropValueAbsolute(name, index)

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
        return self._instance.get_referencedVariables(index)

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
        return self._instance.get_referencedVariable(index)

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
        return self._instance.getValueAbsolute(index)
