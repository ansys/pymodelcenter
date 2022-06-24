from typing import Collection, Optional, Sequence

from ansys.common.variableinterop import IVariableValue
from ansys.engineeringworkflow.api import IControlStatement, IElement, IVariable, Property
import clr
from overrides import overrides

from .arrayish import Arrayish
from .custom_metadata_owner import CustomMetadataOwner

clr.AddReference("phoenix-mocks/Interop.ModelCenter")
from ModelCenter import IAssembly as mcapiIAssembly  # type: ignore

import ansys.modelcenter.workflow.api.dot_net_utils as utils
import ansys.modelcenter.workflow.api.igroup as igroup


class Assembly(CustomMetadataOwner, IControlStatement):
    """COM Instance."""

    def __init__(self, assembly: mcapiIAssembly):
        """
        Initialize a new instance.

        Parameters
        ----------
        assembly : object
            The raw IAssembly interface object to use to make direct
            call to ModelCenter.
        """
        super().__init__(assembly)

    # IElement

    @property  # type: ignore
    @overrides
    def name(self):
        return self._wrapped.getName()

    @property  # type: ignore
    @overrides
    def element_id(self) -> str:
        # TODO: Should return UUID of the element probably. Not available via COM.
        return None  # type: ignore

    @property  # type: ignore
    @overrides
    def parent_element_id(self) -> str:
        # TODO: Should return UUID of the element probably. Not available via COM.
        return None  # type: ignore

    @overrides
    def get_property(self, property_name: str) -> Property:
        value = super().get_custom_metadata_value(property_name)
        if value is not None:
            return Property(self.element_id, property_name, value)
        raise ValueError("Property not found.")

    @overrides
    def get_properties(self) -> Collection[Property]:
        # TODO: Getting collection of metadata is not provided by ModelCenter objects.
        raise NotImplementedError

    @overrides
    def set_property(self, property_name: str, property_value: IVariableValue) -> None:
        super().set_custom_metadata_value(property_name, property_value)

    # IVariableContainer

    @overrides
    def get_variables(self) -> Collection[IVariable]:
        return Arrayish(self._wrapped.Variables, utils.from_dot_net_to_ivariable)

    # IControlStatement

    @property  # type: ignore
    @overrides
    def control_type(self) -> str:
        """Gets the type of the Assembly (Sequence, Assembly, etc)."""
        return self._wrapped.AssemblyType

    @overrides
    def get_components(self) -> Collection[IElement]:
        dotnet_mock_mc_components = self._wrapped.Components
        from .icomponent import IComponent
        return [IComponent(dotnet_mock_mc_components.Item(mock_index))
                for mock_index in range(0, dotnet_mock_mc_components.Count)]

    # ModelCenter specific

    @property
    def groups(self) -> Sequence['igroup.IGroup']:
        """
        Get a list of variable groups in the Assembly.

        Returns
        -------
        A list of variable groups in the assembly.
        """
        return Arrayish(self._wrapped.Groups, igroup.IGroup)

    @property
    def assemblies(self) -> Sequence['Assembly']:
        """
        Pointer to the Assemblies in the Assembly.

        Returns
        -------
        IAssemblies object.
        """
        # VARIANT Assemblies;
        dotnet_mock_mc_assemblies = self._wrapped.Assemblies
        return [Assembly(dotnet_mock_mc_assemblies.Item(mock_index))
                for mock_index in range(0, dotnet_mock_mc_assemblies.Count)]

    @property
    def icon_id(self) -> int:
        """The ID number of the icon to use for the Assembly."""
        return self._wrapped.iconID

    @icon_id.setter
    def icon_id(self, value: int) -> None:
        """
        Set the ID number of the icon to use for the Assembly.

        Parameters
        ----------
        value: int
            The new value.
        """
        self._wrapped.iconID = value

    @property
    def index_in_parent(self) -> int:
        """Gets the position of the Assembly within the parent."""
        return self._wrapped.IndexInParent

    @property
    def parent_assembly(self) -> Optional['Assembly']:    # IAssembly:
        """
        Gets the parent of assembly of this assembly.

        Returns
        -------
        IAssembly object.

        """
        to_wrap = self._wrapped.ParentAssembly
        return None if to_wrap is None else Assembly(to_wrap)

    @property
    def user_data(self) -> object:
        """
        An arbitrary Variant which is not used internally by \
        ModelCenter but can store data for programmatic purposes.

        Value is not stored across file save/load.
        """
        return self._wrapped.userData

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
        self._wrapped.userData = value

    def get_full_name(self) -> str:
        """Get the Full ModelCenter path of the Assembly."""
        # BSTR getFullName();
        return self._wrapped.getFullName()

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
            return Assembly(self._wrapped.addAssembly2(name, x_pos, y_pos, assembly_type))
        else:
            return Assembly(self._wrapped.addAssembly(name, assembly_type))

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
        self._wrapped.addVariable(name, type_)

    def rename(self, name: str) -> None:
        """
        Renames the current Assembly.

        Parameters
        ----------
        name :
            New name of the Assembly.
        """
        # void rename(BSTR name);
        self._wrapped.rename(name)

    def delete_variable(self, name: str) -> None:
        self._wrapped.deleteVariable(name)
