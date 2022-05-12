"""Definition of IComponent."""
from typing import Any, List, Sequence, Union

from System import Object as DotNetObject
from System import String as DotNetString
import clr

from ansys.modelcenter.workflow.api.arrayish import Arrayish
import ansys.modelcenter.workflow.api.assembly as assembly
from ansys.modelcenter.workflow.api.dot_net_utils import from_dot_net_to_ivariable, to_dot_net_list
import ansys.modelcenter.workflow.api.igroup as igroup
import ansys.modelcenter.workflow.api.ivariable as ivariable

from .custom_metadata_owner import CustomMetadataOwner

clr.AddReference("phoenix-mocks/Interop.ModelCenter")
from ModelCenter import IComponent as mcapiIComponent


class IComponent(CustomMetadataOwner):
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
    def variables(self) -> 'Sequence[ivariable.IVariable]':
        """Variables in the component."""
        variables = self._instance.Variables
        return Arrayish(variables, from_dot_net_to_ivariable)

    @property
    def groups(self) -> 'Sequence[igroup.IGroup]':
        """All groups in the component."""
        return Arrayish(self._instance.Groups, igroup.IGroup)

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
        dot_net_value: Union[str, List[str]]
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
    def parent_assembly(self) -> 'assembly.Assembly':
        """Parent assembly of this component."""
        parent_assembly = self._instance.ParentAssembly
        return assembly.Assembly(parent_assembly)

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

    def get_variable(self, name: str) -> 'IVariable':
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

    def run(self) -> None:
        """Run the component."""
        self._instance.run()

    def invoke_method(self, method: str) -> None:
        """
        Invoke one of the component's methods.

        Parameters
        ----------
        method: str
            The name of the method to invoke.
        """
        self._instance.invokeMethod(method)

    def invalidate(self) -> None:
        """Invalidate the component and all of its variables."""
        self._instance.invalidate()

    def reconnect(self) -> None:
        """Reload this component from its source."""
        self._instance.reconnect()

    def download_values(self) -> None:
        """Download the component's variable values from the server if\
        it is a ModelCenter Remote Execution component."""
        self._instance.downloadValues()

    def rename(self, name: str) -> None:
        """
        Rename the current component.

        Parameters
        ----------
        name: str
            The new name of the component.
        """
        self._instance.rename(name)

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
        self._instance.show()
