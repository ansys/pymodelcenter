from typing import Collection, List, Optional, Sequence, Union

from ansys.common.variableinterop import IVariableValue
from ansys.engineeringworkflow.api import IControlStatement, IElement, Property
from overrides import overrides

from .component_metadata import ComponentMetadataAccess, ComponentMetadataType
from .i18n import i18n
from .igroup import IGroup
from .igroups import IGroups
from .ivariable import IVariable


class Assembly(IControlStatement):
    """COM Instance of an Assembly."""

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

# IControlStatement

    @property  # type: ignore
    @overrides
    def control_type(self) -> str:
        """Gets the type of the Assembly (Sequence, Assembly, etc)."""
        return self._assembly.AssemblyType

    @overrides
    def get_components(self) -> Collection[IElement]:
        # VARIANT Components;
        raise NotImplementedError

# IVariableContainer

    @overrides
    def get_variables(self) -> Collection[IVariable]:
        """Returns a collection of variables in the Assembly."""
        # VARIANT Variables;
        raise NotImplementedError

# IElement

    @property  # type: ignore
    @overrides
    def element_id(self) -> str:
        # TODO: Should return UUID of the element probably. Not available via COM.
        raise NotImplementedError

    @property  # type: ignore
    @overrides
    def parent_element_id(self) -> str:
        # TODO: Should return UUID of the element probably. Not available via COM.
        raise NotImplementedError

    @property  # type: ignore
    @overrides
    def name(self):
        return self._assembly.getName()

    @overrides
    def get_property(self, property_name: str) -> Property:
        # TODO: Is property a metadata?
        raise NotImplementedError

    @overrides
    def get_properties(self) -> Collection[Property]:
        # TODO: Is property a metadata?
        raise NotImplementedError

    @overrides
    def set_property(self, property_name: str, property_value: IVariableValue) -> None:
        # TODO: Is property a metadata?
        raise NotImplementedError

# ModelCenter specific

    @property
    def groups(self) -> Sequence[IGroup]:
        """
        Get a list of variable groups in the Assembly.

        Returns
        -------
        A list of variable groups in the assembly.
        """
        return IGroups(self._assembly.Groups)

    @property
    def assemblies(self) -> Sequence['Assembly']:
        """
        Pointer to the Assemblies in the Assembly.

        Returns
        -------
        IAssemblies object.
        """
        # VARIANT Assemblies;
        dotnet_mock_mc_assemblies = self._assembly.Assemblies
        return [Assembly(dotnet_mock_mc_assemblies.Item(mock_index))
                for mock_index in range(0, dotnet_mock_mc_assemblies.Count)]

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

    def get_full_name(self) -> str:
        """Get the Full ModelCenter path of the Assembly."""
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

    def set_metadata(self,
                     name: str,
                     value: Union[str, int, float, bool],
                     access: ComponentMetadataAccess,
                     archive: bool,
                     value_is_xml: bool = False) -> None:
        """
        Sets the meta data value of the given meta data key name.

        Parameters
        ----------
        name :
            Metadata specifier used to store the data.
        value :
            The value of the metadata item.
        access :
            The level of access allowed to the metadata.
        archive :
            Whether or not the metadata should be considered archived.
        value_is_xml :
            Whether the metadata value is XML. This should be used
            only when passing a string containing XML that should be interpreted as such.
        """
        meta_type: ComponentMetadataType = ComponentMetadataType.STRING
        if isinstance(value, str):
            meta_type = ComponentMetadataType.STRING
            if value_is_xml:
                meta_type = ComponentMetadataType.XML
        elif isinstance(value, float):
            meta_type = ComponentMetadataType.DOUBLE
        elif isinstance(value, bool):
            # It's important that this comes before int, as python bool is a subclass of int.
            meta_type = ComponentMetadataType.BOOLEAN
        elif isinstance(value, int):
            meta_type = ComponentMetadataType.LONG
        else:
            raise TypeError(i18n('Exceptions', 'ERROR_METADATA_TYPE_NOT_ALLOWED'))

        return self._assembly.setMetadata(name, meta_type.value, value, access.value, archive)

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
        return self._assembly.getMetadata(name)
