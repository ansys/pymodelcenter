from typing import Optional


class Assembly:
    """COM Instance."""

    def __init__(self, assembly: object):
        """
        Initialize a new instance.

        Parameters
        ----------
        assembly : object
            The raw IAssembly interface object to use to make direct
            call to ModelCenter.
        """
        self._assembly = assembly

    @property
    def variables(self) -> object:  # IVariables:
        """
        Pointer to the variables in the Assembly.

        Returns
        -------
        IVariables object.
        """
        # VARIANT Variables;
        raise NotImplementedError

    @property
    def groups(self) -> object:     # IGroups
        """
        Pointer to the Groups in the Assembly.

        Returns
        -------
        IGroups object.
        """
        # VARIANT Groups;
        raise NotImplementedError

    @property
    def assemblies(self) -> object:     # IAssemblies
        """
        Pointer to the Assemblies in the Assembly.

        Returns
        -------
        IAssemblies object.
        """
        # VARIANT Assemblies;
        raise NotImplementedError

    @property
    def components(self) -> object:     # IComponent
        """
        Pointer to the Components in the Assembly.

        Returns
        -------
        IComponents object.
        """
        # VARIANT Components;
        raise NotImplementedError

    @property
    def icon_id(self) -> int:
        """The ID number of the icon to use for the Assembly."""
        return self._assembly.iconID

    @icon_id.setter
    def icon_id(self, value: int) -> None:
        """
        Set the ID number of the icon to use for the Assembly.

        Parameters
        ----------
        value: int
            The new value.
        """
        self._assembly.iconID = value

    @property
    def index_in_parent(self) -> int:
        """Gets the position of the Assembly within the parent."""
        return self._assembly.IndexInParent

    @property
    def parent_assembly(self) -> Optional['Assembly']:    # IAssembly:
        """
        Gets the parent of assembly of this assembly.

        Returns
        -------
        IAssembly object.

        """
        to_wrap = self._assembly.ParentAssembly
        return None if to_wrap is None else Assembly(to_wrap)

    @property
    def assembly_type(self) -> str:
        """Gets the type of the Assembly (Sequence, Assembly, etc)."""
        return self._assembly.AssemblyType

    @property
    def user_data(self) -> object:
        """
        An arbitrary Variant which is not used internally by \
        ModelCenter but can store data for programmatic purposes.

        Value is not stored across file save/load.
        """
        return self._assembly.userData

    @user_data.setter
    def user_data(self, value: any) -> object:
        """
        An arbitrary Variant which is not used internally by \
        ModelCenter but can store data for programmatic purposes.

        Value is not stored across file save/load.
        """
        # LTTODO: It's difficult to know exactly what to do here, since
        # the user_data type is defined as a VARIANT on the MC API, and MC itself allows any
        # VARIANT to be set.
        # The documentation suggests that the restriction to VARIANT is not actually important
        # but is probably a consequence of the restrictions of the COM API; that is, there's nothing
        # wrong with allowing this to be any data type, since the receiving application (MCD) is
        # not actually supposed to do anything with this data but store it (allowing the client
        # script to "tag" assemblies, etc, with arbitrary data).
        # It's likely that we'll need to do some input validation here
        # to conform to the particulars of the actual API "transport" winds up being used
        # (i.e. GRPC as opposed to COM) and then also allow whatever is on the receiving
        # end to decide whether it has other restrictions.
        # For now, we do nothing and just pass the unmodified value in, and let pythonnet
        # decide whether it can set it into the user data field.
        self._assembly.userData = value

    def get_name(self) -> str:
        """Get the name of the Assembly."""
        return self._assembly.getName()

    def get_full_name(self) -> str:
        """Get the Full ModelCenter path of the Assembly."""
        # BSTR getFullName();
        return self._assembly.getFullName()

    def add_assembly(self,
                     name: str,
                     x_pos: Optional[int],
                     y_pos: Optional[int],
                     assembly_type: Optional[str] = None) -> 'Assembly':     # IAssembly
        """
        This method creates a sub-Assembly in the current Assembly \
        with a specific type and position.

        Parameters
        ----------
        name : str
            the name of the subassembly
        x_pos : Optional[int]
            the position of the sub-assembly on the x axis. Ignored if y_pos is not also specified.
        y_pos : Optional[int]
            the position of the sub-assembly on the y axis. Ignored if x_pos is not also specified.
        assembly_type :

        Returns
        -------
        IAssembly object.
        """

        if x_pos is not None and y_pos is not None:
            return Assembly(self._assembly.addAssembly2(name, x_pos, y_pos, assembly_type))
        else:
            return Assembly(self._assembly.addAssembly(name, assembly_type))

    def add_variable(self, name: str, type_: str) -> object:    # IVariable
        # IDispatch* addVariable(BSTR name, BSTR type);
        """
        Creates a variable for the current Assembly.

        Parameters
        ----------
        name : str
            Name of the new variable to create.
        type_ : str
            Type of the new variable. Possible types are:
                           - double
                           - int
                           - boolean
                           - string
                           - file
                           - double[]
                           - int[]
                           - boolean[]
                           - string[]
                           - quadfacet
                           - surfaceofrevolution
                           - nurbs
                           - bspline
                           - ruled
                           - skinned
                           - vrml
                           - node

        Returns
        -------
        IVariable object.
        """
        # TODO: Wrap and return when variable wrappers are available
        self._assembly.addVariable(name, type_)

    def rename(self, name: str) -> None:
        """
        Renames the current Assembly.

        Parameters
        ----------
        name :
            New name of the Assembly.
        """
        # void rename(BSTR name);
        self._assembly.rename(name)

    def delete_variable(self, name: str) -> None:
        self._assembly.deleteVariable(name)

    def set_metadata(self, name: str, type_, value, access, archive) -> None:
        """
        Sets the meta data value of the given meta data key name.

        Parameters
        ----------
        name :
            Metadata specifier used to store the data.
        type_ :
        value :
        access :
        archive :
        """
        # void setMetadata(
        #       BSTR name, MetadataType type, VARIANT value,
        #       MetadataAccess access, boolean archive);
        raise NotImplementedError

    def get_metadata(self, name: str) -> object:    # Metadata
        """
        Gets the meta data value of the given meta data key name.

        Parameters
        ----------
        name :
            Metadata key name.

        Returns
        -------
        Metadata value.
        """
        # VARIANT getMetadata(BSTR name);
        raise NotImplementedError
