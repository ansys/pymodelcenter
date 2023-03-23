"""Definition of Component."""
from typing import Any, Collection, List, Sequence, Union

from ansys.common.variableinterop import IVariableValue
from ansys.engineeringworkflow.api import IVariable, Property
from overrides import overrides

from ansys.modelcenter.workflow.api import IComponent, assembly, igroup


class Component(IComponent):
    """A component in a Workflow."""

    def __init__(self, elem_id: str):
        """
        Initialize component object.

        Parameters
        ----------
        elem_id: str
        The id string of the component.
        """
        self._id = elem_id

    @property  # type: ignore
    @overrides
    def name(self):
        # return self._wrapped.getName()
        raise NotImplementedError

    @property  # type: ignore
    @overrides
    def element_id(self) -> str:
        return self._id

    @property  # type: ignore
    @overrides
    def parent_element_id(self) -> str:
        raise NotImplementedError

    @overrides
    def get_property(self, property_name: str) -> Property:
        # value = super().get_custom_metadata_value(property_name)
        # if value is not None:
        #     return Property(self.element_id, property_name, value)
        # raise ValueError("Property not found.")
        raise NotImplementedError

    @overrides
    def get_properties(self) -> Collection[Property]:
        raise NotImplementedError

    @overrides
    def set_property(self, property_name: str, property_value: IVariableValue) -> None:
        super().set_custom_metadata_value(property_name, property_value)

    @overrides
    def get_variables(self) -> Collection[IVariable]:
        # variables = self._wrapped.Variables
        # return Arrayish(variables, from_dot_net_to_ivariable)
        raise NotImplementedError

    @property  # type: ignore
    @overrides
    def pacz_url(self):
        raise NotImplementedError

    # ModelCenter

    @property  # type: ignore
    @overrides
    def groups(self) -> "Sequence[igroup.IGroup]":
        # return Arrayish(self._wrapped.Groups, igroup.IGroup)
        raise NotImplementedError

    @property  # type: ignore
    @overrides
    def user_data(self) -> Any:
        # return self._wrapped.userData
        raise NotImplementedError

    @user_data.setter  # type: ignore
    @overrides
    def user_data(self, source: Any) -> None:
        # if isinstance(source, list):
        #     dot_net_source = to_dot_net_list(source, DotNetObject)
        # else:
        #     dot_net_source = source
        # self._wrapped.userData = dot_net_source
        raise NotImplementedError

    @property  # type: ignore
    @overrides
    def associated_files(self) -> Union[str, List[str]]:
        # ret = self._wrapped.AssociatedFiles
        # return ret
        raise NotImplementedError

    @associated_files.setter  # type: ignore
    @overrides
    def associated_files(self, source: Union[str, List[str]]):
        # dot_net_value: Union[str, List[str]]
        # if isinstance(source, str):
        #     dot_net_value = source
        # else:
        #     dot_net_value = to_dot_net_list(source, DotNetString)
        #
        # self._wrapped.AssociatedFiles = dot_net_value
        raise NotImplementedError

    @property  # type: ignore
    @overrides
    def index_in_parent(self) -> int:
        # return self._wrapped.IndexInParent
        raise NotImplementedError

    @property  # type: ignore
    @overrides
    def parent_assembly(self) -> "assembly.Assembly":
        # parent_assembly = self._wrapped.ParentAssembly
        # return assembly.Assembly(parent_assembly)
        raise NotImplementedError

    @overrides
    def get_full_name(self) -> str:
        # return self._wrapped.getFullName()
        raise NotImplementedError

    @overrides
    def get_source(self) -> str:
        # return self._wrapped.getSource()
        raise NotImplementedError

    @overrides
    def get_variable(self, name: str) -> "IVariable":
        # mcapi_variable = self._wrapped.getVariable(name)
        # return from_dot_net_to_ivariable(mcapi_variable)
        raise NotImplementedError

    @overrides
    def get_type(self) -> str:
        # return self._wrapped.getType()
        raise NotImplementedError

    @overrides
    def run(self) -> None:
        # self._wrapped.run()
        raise NotImplementedError

    @overrides
    def invoke_method(self, method: str) -> None:
        # self._wrapped.invokeMethod(method)
        raise NotImplementedError

    @overrides
    def invalidate(self) -> None:
        # self._wrapped.invalidate()
        raise NotImplementedError

    @overrides
    def reconnect(self) -> None:
        # self._wrapped.reconnect()
        raise NotImplementedError

    @overrides
    def download_values(self) -> None:
        # self._wrapped.downloadValues()
        raise NotImplementedError

    @overrides
    def rename(self, name: str) -> None:
        # self._wrapped.rename(name)
        raise NotImplementedError

    @overrides
    def get_position_x(self) -> int:
        # return self._wrapped.getPositionX()
        raise NotImplementedError

    @overrides
    def get_position_y(self) -> int:
        # return self._wrapped.getPositionY()
        raise NotImplementedError

    @overrides
    def show(self) -> None:
        # self._wrapped.show()
        raise NotImplementedError
