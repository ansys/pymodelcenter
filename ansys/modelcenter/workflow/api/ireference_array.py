from typing import Optional, Sequence

import ansys.common.variableinterop as acvi
import clr
from overrides import overrides

from .dot_net_utils import from_dot_net_list, from_dot_net_to_ivariable
from .iarray import IArray
from .idoublearray import IDoubleArray
from .irefprop import IRefArrayProp

clr.AddReference('phoenix-mocks/Phoenix.Mock.v45')
import Phoenix.Mock as mocks  # type: ignore


class IReferenceArray(IArray[mocks.MockReferenceArray]):
    """
    Hold a reference to an array.

    Currently, only valid for real (double) arrays.

    Implements IVariable.
    """

    def __init__(self, wrapped: mocks.MockReferenceArray):
        """
        Initialize.

        Parameters
        ----------
        wrapped : mocks.MockReferenceArray
            The MockReferenceArray to be wrapped.
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
        self._wrapped.fromString(new_value.to_api_string())

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
    def standard_metadata(self, new_metadata: acvi.RealArrayMetadata) -> None:
        if not isinstance(new_metadata, acvi.RealArrayMetadata):
            raise acvi.exceptions.IncompatibleTypesException(
                new_metadata.variable_type.name,
                self._standard_metadata.variable_type.name)
        else:
            self._standard_metadata = new_metadata

# endregion
####################################################################################################

    @property
    def auto_grow(self) -> bool:
        """
        Whether or not the reference array is set to automatically grow.
        """
        return self._wrapped.autoGrow

    @auto_grow.setter
    def auto_grow(self, value: bool) -> None:
        self._wrapped.autoGrow = value

    def get_element_value(self, index: int) -> acvi.RealValue:
        """
        Gets the value of an array element.

        Parameters
        ----------
        index
            Index of the array element (0-based index).

        Returns
        -------
        acvi.RealValue
            The value.
        """
        return acvi.RealValue(self._wrapped.get_value(index))

    def set_element_value(self, value: float, index: int) -> acvi.RealValue:
        """
        Sets the value of an array element.

        Parameters
        ----------
        value
            New value.
        index
            Index of the array element (0-based index).
        """
        return acvi.RealValue(self._wrapped.setValue(value, index))

    def create_real_ref_prop(self, name: str, type_: str) -> IRefArrayProp:
        """
        Creates a reference property for the array.

        Parameters
        ----------
        name :
            Name of the reference property.
        type_ :
            Type of reference property to create. Allowed types are:
            double, long, boolean, and string.

        Returns
        -------
        IRefArrayProp
        """
        return IRefArrayProp(self._wrapped.createRefProp(name, type_))

    def get_real_ref_prop_value(self, name: str, index: int) -> IDoubleArray:
        """
        Gets the value of a specified reference property for the \
        variable.

        Parameters
        ----------
        name :
            Name of the reference property.
        index :
            Index of the array element (0-based index).

        Returns
        -------
        IRefArrayProp
        """
        return from_dot_net_to_ivariable(self._wrapped.getRefPropValue(name, index))

    def set_real_ref_prop_value(self, name: str, index: int, value: IDoubleArray) -> None:
        """
        Sets the value of a specified reference property for an \
        element in the array.

        Parameters
        ----------
        name
            Name of the reference property.
        index
            Index of the array element (0-based index).
        value
            New value.
        """
        self._wrapped.setRefPropValue(name, index, value.value.to_api_string())

    def get_real_ref_prop_value_absolute(self, name: str, index: int) -> IDoubleArray:
        """
        Gets the value of a specified reference property for an \
        element in the array without running to validate.

        Parameters
        ----------
        name
            Name of the reference property.
        index
            Index of the array element (0-based index).

        Returns
        -------
        object
            The value as a variant.
        """
        return from_dot_net_to_ivariable(self._wrapped.getRefPropValueAbsolute(name, index))

    def referenced_variables(self, index: int) -> Sequence[IDoubleArray]:
        """
        Gets the reference variables of the index element of the array.

        Parameters
        ----------
        index
            Index of the array element (0-based index).

        Returns
        -------
        object
            The references variables of the element.
        """
        return from_dot_net_list(self._wrapped.get_referencedVariables(index), IDoubleArray)

    def referenced_variable(self, index: int) -> IDoubleArray:
        """
        Gets the reference variable of the index element of the array.

        Convenience method for if the indexed variable only has one reference.

        Parameters
        ----------
        index
            Index of the array element (0-based index).

        Returns
        -------
        IDoubleArray
            The reference variable of the index element.
        """
        return from_dot_net_to_ivariable(self._wrapped.get_referencedVariable(index))

    def get_value_absolute(self, index: int) -> acvi.RealValue:
        """
        gets the value of the variable at a specific location without \
        validating.

        Parameters
        ----------
        index
            The array element index (0-based index).

        Returns
        -------
        float
            The reference value.
        """
        return acvi.RealValue(self._wrapped.getValueAbsolute(index))
