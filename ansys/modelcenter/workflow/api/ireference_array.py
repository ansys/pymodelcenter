class IReferenceArray:
    """
    COM Instance.
    @implements IArray
    """

    # boolean hasChanged;

    # boolean hide;

    # LPDISPATCH OwningComponent;

    # long size;

    # long numDimensions;

    @property
    def auto_grow(self) -> bool:
        """Whether or not the reference array is set to automatically \
         grow."""
        # boolean autoGrow;
        raise NotImplementedError

    # boolean isValid();

    # void validate();

    # BSTR getName();

    # BSTR getFullName();

    # BSTR getType();

    # boolean isInput();

    # BSTR toString();

    # void fromString(BSTR value);

    # BSTR toStringAbsolute();

    # void invalidate();

    # LPDISPATCH directPrecedents( [optional]VARIANT followSuspended, [optional]VARIANT reserved);

    # LPDISPATCH directDependents( [optional]VARIANT followSuspended, [optional]VARIANT reserved);

    # LPDISPATCH precedentLinks( [optional]VARIANT reserved);

    # LPDISPATCH dependentLinks( [optional]VARIANT reserved);

    # LPDISPATCH precedents( [optional]VARIANT followSuspended, [optional]VARIANT reserved);

    # LPDISPATCH dependents( [optional]VARIANT followSuspended, [optional]VARIANT reserved);

    # boolean isInputToComponent();

    # boolean isInputToModel();

    # void setMetadata(
    #   BSTR name, MetadataType type, VARIANT value, MetadataAccess access, boolean archive);

    # VARIANT getMetadata(BSTR name);

    # BSTR toStringEx(long index);

    # void fromStringEx(BSTR value, long index);

    # BSTR toStringAbsoluteEx(long index);

    # long getLength( [optional] VARIANT dim);

    # void setLength(long length, [optional] VARIANT dim);

    # void setDimensions(
    #   long d1,
    #   [optional] VARIANT d2, [optional] VARIANT d3, [optional] VARIANT d4,
    #   [optional] VARIANT d5, [optional] VARIANT d6, [optional] VARIANT d7,
    #   [optional] VARIANT d8, [optional] VARIANT d9, [optional] VARIANT d10);

    def get_value(self, index: int) -> float:   # RealValue:
        """
        Value of an array element.

        Parameters
        ----------
        index : int
            Index of the array element (0-based index).

        Returns
        -------

        """
        # double value(long index);

#    # void value(long index, double newValue);
#    Value of an array element.
#
#    @param index      Index of the array element (0-based index).
#    @param newValue
#
#    # BSTR reference(long index);
#    Reference of an array element.
#
#    @param index   Index of the array element (0-based index).
#
#    @return
#
#    # void reference(long index, BSTR newValue);
#    Reference of an array element.
#
#    @param index      Index of the array element (0-based index).
#
#    @param newValue
#
#    def get_value(self):
#    # double getValue(int index);
#    Gets the value of an array element.
#
#    @param index   Index of the array element (0-based index).
#
#    @return       The value.
#
#    # double setValue(double value, int index);
#    Sets the value of an array element.
#
#    @param value   New value.
#    @param index   Index of the array element (0-based index).
#
#    @return
#
#    # IDispatch* createRefProp(BSTR name, BSTR type);
#    Creates a reference property for the array.
#
#    @param name    Name of the reference property.
#    @param type    Type of reference property to create.
#                    Allowed types are: double, long, boolean, and string.
#
#    @return       IDispatch* to an IRefArrayProp object.
#
#    # VARIANT getRefPropValue( BSTR name, int index );
#    Gets the value of a specified reference property for an element in the array.
#
#    @param name    Name of the reference property.
#    @param index   Index of the array element (0-based index).
#
#    @return       The value as a variant.
#
#    # void setRefPropValue( BSTR name, int index, BSTR value );
#    Sets the value of a specified reference property for an element in the array.
#
#    @param name    Name of the reference property.
#    @param index   Index of the array element (0-based index).
#    @param value   New value.
#
#    # VARIANT getRefPropValueAbsolute( BSTR name, int index );
#    Gets the value of a specified reference property for an element in
#    the array without runningto validate.
#
#    @param name    Name of the reference property.
#    @param index   Index of the array element (0-based index).
#
#    @return       The value as a variant.
#
#    # VARIANT referencedVariables(long index);
#    Gets the reference variables of the index element of the array.
#
#    @param index   Index of the array element (0-based index).
#
#    @return       The references variables of the element.
#
#    # VARIANT referencedVariable(long index);
#    Gets the reference variable of the index element of the array.
#
#    Convenience method for if the indexed variable only has one reference.
#
#    @param index   Index of the array element (0-based index).
#
#    @return       The reference variable of the index element.
#
#    # double getValueAbsolute(int index);
#    gets the value of the variable at a specific location without validating.
#
#    @param index    The array element index (0-based index).
#
#    @return        The reference value.
