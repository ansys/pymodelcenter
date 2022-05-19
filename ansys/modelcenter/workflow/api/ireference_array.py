import ansys.common.variableinterop as acvi
import clr
from overrides import overrides

from .data_type import VarType
from .iarray import IArray
from .irefprop import IRefArrayProp

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
        self._wrapped: mocks.MockReferenceArray = wrapped
        self._standard_metadata: acvi.RealArrayMetadata = acvi.RealArrayMetadata()

####################################################################################################
# region Inherited from IVariable

    @property
    @overrides
    def value(self) -> acvi.RealArrayValue:
        return acvi.RealArrayValue.from_api_string(self._wrapped.toString())

    @value.setter
    @overrides
    def value(self, new_value: acvi.RealArrayValue):
        self._wrapped.set_value(new_value)

    @property
    @overrides
    def value_absolute(self) -> acvi.RealArrayValue:
        return self.value

    @property
    @overrides
    def standard_metadata(self) -> acvi.CommonVariableMetadata:
        return self._standard_metadata

    @standard_metadata.setter
    @overrides
    def standard_metadata(self, value: acvi.CommonVariableMetadata):
        self._standard_metadata = value

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
        Gets the value of a specified reference property for an \
        element in the array.

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
        Gets the value of a specified reference property for an \
        element in the array without running to validate.

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
