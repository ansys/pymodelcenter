from typing import MutableSequence

from .iarray import IArray
from .iref_array_prop import IRefArrayProp
from .irefprop import IRefArrayProp


# TODO: inherit from IArray when available.
class IReferenceArray(IArray):
    """
    COM Instance.
    @implements IArray
    """

    @property
    def auto_grow(self) -> bool:
        """Whether or not the reference array is set to automatically \
         grow."""
        # boolean autoGrow;
        raise NotImplementedError

    @property
    def value(self) -> MutableSequence[float]:
        """
        An access wrapper to the values, assuming the array of values \
        is a single dimensional array.
        """
        # double value(long index);
        # void value(long index, double newValue);
        raise NotImplementedError

    @property
    def reference(self) -> MutableSequence[str]:
        """
        An access wrapper to the references, assuming the array of
        references is a single dimensional array.
        """
        # BSTR reference(long index);
        # void reference(long index, BSTR newValue);
        raise NotImplementedError

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
        # double getValue(int index);
        raise NotImplementedError

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
        # double setValue(double value, int index);
        raise NotImplementedError

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
        # IDispatch* createRefProp(BSTR name, BSTR type);
        raise NotImplementedError

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
        # VARIANT getRefPropValue( BSTR name, int index );
        raise NotImplementedError

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
        # void setRefPropValue( BSTR name, int index, BSTR value );
        raise NotImplementedError

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
        # VARIANT getRefPropValueAbsolute( BSTR name, int index );
        raise NotImplementedError

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
        # VARIANT referencedVariables(long index);
        raise NotImplementedError

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
        # VARIANT referencedVariable(long index);
        raise NotImplementedError

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
        # double getValueAbsolute(int index);
        raise NotImplementedError
