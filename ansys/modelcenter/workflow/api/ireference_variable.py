class IReferenceVariable:
    """COM Instance.
    @implements IVariable"""

#    # boolean hasChanged;
#
#    # boolean hide;
#
#    # LPDISPATCH OwningComponent;
#
#    # double value;
#    Value of the variable.
#    # BSTR reference;
#    Reference of the variable.
#    # VARIANT referencedVariables;
#    Gets the referenced variables.
#    # VARIANT referencedVariable;
#    Gets the referenced variable.
#
#    Convenience method for if there is only one reference.
#    # boolean isValid();
#
#    # void validate();
#
#    # BSTR getName();
#
#    # BSTR getFullName();
#
#    # BSTR getType();
#
#    # boolean isInput();
#
#    # BSTR toString();
#
#    # void fromString(BSTR value);
#
#    # BSTR toStringAbsolute();
#
#    # void invalidate();
#
#    # LPDISPATCH directPrecedents( [optional]VARIANT followSuspended, [optional]VARIANT reserved);
#
#    # LPDISPATCH directDependents( [optional]VARIANT followSuspended, [optional]VARIANT reserved);
#
#    # LPDISPATCH precedentLinks( [optional]VARIANT reserved);
#
#    # LPDISPATCH dependentLinks( [optional]VARIANT reserved);
#
#    # LPDISPATCH precedents( [optional]VARIANT followSuspended, [optional]VARIANT reserved);
#
#    # LPDISPATCH dependents( [optional]VARIANT followSuspended, [optional]VARIANT reserved);
#
#    # boolean isInputToComponent();
#
#    # boolean isInputToModel();
#
#    # void setMetadata(
#    #      BSTR name, MetadataType type, VARIANT value, MetadataAccess access, boolean archive);
#
#    # VARIANT getMetadata(BSTR name);
#
#    # IDispatch* createRefProp( BSTR name, BSTR type );
#    Creates a reference property for the variable.
#
#    @param name    Name of the reference property.
#    @param type    Type of reference property to create.
#                    Allowed types are: double, long, boolean, and string.
#
#    @return       IDispatch* to an IRefProp object.
#    # VARIANT getRefPropValue( BSTR name );
#    Gets the value of a specified reference property for the variable.
#
#    @param name    Name of the reference property.
#
#    @return       The value as a variant.
#    # void setRefPropValue( BSTR name, BSTR value );
#    Sets the value of a specified reference property for the variable.
#
#    @param name    Name of the reference property.
#    @param value   New value.
#    # VARIANT getRefPropValueAbsolute( BSTR name );
#    Gets the value of a specified reference property for the variable,
#    without validating first.
#
#    @param name    Name of the reference property.
#
#    @return       The value as a variant.
