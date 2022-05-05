"""Definition of IComponent."""
from typing import Any, List, Union

from System import Object as DotNetObject
from System import String as DotNetString
import clr

from .assembly import Assembly
from .dot_net_utils import from_dot_net_to_ivariable, to_dot_net_list
from .igroups import IGroups
from .ivariable import IVariable
from .ivariables import IVariables
from .metadata_owner import MetadataOwner

clr.AddReference("phoenix-mocks/Interop.ModelCenter")
from ModelCenter import IComponent as mcapiIComponent
from ModelCenter import MetadataAccess, MetadataType


class IComponent(MetadataOwner):
    """A component in a Workflow."""

    def __init__(self, instance: mcapiIComponent):
        """
        Initialize component object.

        Parameters
        ----------
        instance : mcapiIComponent
            Raw ModelCenter API object to wrap.
        """
        super().__init__(instance)

    @property
    def variables(self) -> IVariables:
        """Variables in the component."""
        variables = self._instance.Variables
        return IVariables(variables)

    @property
    def groups(self) -> IGroups:
        """All groups in the component."""
        return IGroups(self._instance.Groups)

    @property
    def user_data(self) -> Any:
        """Arbitrary object which is not used internally, but can \
        store data for programmatic purposes.

        The value is not stored across save/load operations.
        """
        return self._instance.userData

    @user_data.setter
    def user_data(self, source: Any) -> None:
        """Arbitrary object which is not used internally, but can \
        store data for programmatic purposes.

        The value is not stored across save/load operations.
        """
        if isinstance(source, list):
            dot_net_source = to_dot_net_list(source, DotNetObject)
        else:
            dot_net_source = source
        self._instance.userData = dot_net_source

    @property
    def associated_files(self) -> Union[str, List[str]]:
        """Set of files associated with the component."""
        ret = self._instance.AssociatedFiles
        return ret

    @associated_files.setter
    def associated_files(self, source: Union[str, List[str]]):
        """Set of files associated with the component."""
        if isinstance(source, str):
            dot_net_value = source
        else:
            dot_net_value = to_dot_net_list(source, DotNetString)

        self._instance.AssociatedFiles = dot_net_value

    @property
    def index_in_parent(self) -> int:
        """Position of this component in its parent assembly."""
        return self._instance.IndexInParent

    @property
    def parent_assembly(self) -> Assembly:
        """Parent assembly of this component."""
        assembly = self._instance.ParentAssembly
        return Assembly(assembly)

    def get_name(self) -> str:
        """
        Get the name of the component.

        Returns
        -------
        The name of the component.
        """
        return self._instance.getName()

    def get_full_name(self) -> str:
        """
        Get the full path of the component.

        Returns
        -------
        The full path of the component.
        """
        return self._instance.getFullName()

    def get_source(self) -> str:
        """
        Get the source of the component.

        Returns
        -------
        The source of the component.
        """
        return self._instance.getSource()

    def get_variable(self, name: str) -> IVariable:
        """
        Get a variable in this component by name.

        Parameters
        ----------
        name: str
            The name of the variable, in dotted notation relative to
            the component.

        Returns
        -------
        The variable object.
        """
        mcapi_variable = self._instance.getVariable(name)
        return from_dot_net_to_ivariable(mcapi_variable)

    def get_type(self) -> str:
        """
        Get the type of the component.

        Valid values include:
        * Component
        * Assembly
        * Sequence
        * If
        * Parallel
        * Empty
        * ForEach

        Returns
        -------
        The type of the component.
        """
        return self._instance.getType()

    def get_metadata(self, name: str) -> IVariable:
        """
        Get the metadata value of the given metadata key name.

        Parameters
        ----------
        name: str
            The key name of the metadata to retrieve.

        Returns
        -------
        The value of the metadata key.
        """
        return IVariableConverter.from_dot_net(self._instance.getMetadata(name))

    def set_metadata(
            self, name: str, type_: MetadataType, value: Any,
            access: MetadataAccess, archive: bool
    ) -> None:  # MetadataType, VARIANT, MetadataAccess
        """
        Set the metadata value of a given key.

        Parameters
        ----------
        name: str
            The key name of the metadata to set.
        type_: object
            The type of metadata to set.
        value: object
            The metadata value to set.
        access: object
            The access permissions of the metadata.
        archive: bool
            Whether this property should be archived.
        """
        if isinstance(value, list):
            dot_net_value = DotNetListConverter.to_dot_net(value, DotNetObject)
        else:
            dot_net_value = value
        self._instance.setMetadata(name, type_, dot_net_value, access)

    def run(self) -> None:
        """Run the component."""
        self._instance.Run()

    def invoke_method(self, method: str) -> None:
        """
        Invoke one of the component's methods.

        Parameters
        ----------
        method: str
            The name of the method to invoke.
        """
        self._instance.InvokeMethod(method)

    def invalidate(self) -> None:
        """Invalidate the component and all of its variables."""
        raise NotImplementedError

    def reconnect(self) -> None:
        """Reload this component from its source."""
        self._instance.Reconnect()

    def download_values(self) -> None:
        """Download the component's variable values from the server if\
        it is a ModelCenter Remote Execution component."""
        self._instance.DownloadValues()

    def rename(self, name: str) -> None:
        """
        Rename the current component.

        Parameters
        ----------
        name: str
            The new name of the component.
        """
        self._instance.Rename(name)

    def get_position_x(self) -> int:
        """
        Get the X position of the component in the Analysis View.

        Returns
        -------
        The X position.
        """
        # int getPositionX();
        return self._instance.getPositionX()

    def get_position_y(self) -> int:
        """
        Get the Y position of the component in the Analysis View.

        Returns
        -------
        The Y position.
        """
        # int getPositionY();
        return self._instance.getPositionY()

    def show(self) -> None:
        """Show the component's GUI, if it has one."""
        self._instance.Show()
