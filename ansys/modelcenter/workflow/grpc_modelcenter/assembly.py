"""Implementation of Assembly."""

from typing import Optional, Sequence

import ansys.common.variableinterop as acvi
import ansys.engineeringworkflow.api as base_api
from grpc import Channel
from overrides import overrides

import ansys.modelcenter.workflow.api as api

from .group import Group
from .proto.custom_metadata_messages_pb2 import MetadataGetValueRequest, MetadataSetValueRequest
from .proto.element_messages_pb2 import (
    AddAssemblyRequest,
    AddAssemblyVariableRequest,
    AssemblyIconSetRequest,
    ElementId,
    ElementName,
    RenameRequest,
)
from .var_value_convert import convert_grpc_value_to_acvi, convert_interop_value_to_grpc
from .variable import Variable
from .variable_container import AbstractGRPCVariableContainer


class Assembly(AbstractGRPCVariableContainer, api.IAssembly):
    """Represents an assembly in ModelCenter."""

    def __init__(self, element_id: ElementId, channel: Channel):
        """
        Initialize a new instance.

        Parameters
        ----------
        element_id : ElementId
            The id of the .
        """
        super(Assembly, self).__init__(element_id=element_id, channel=channel)

    @property  # type: ignore
    @overrides
    def element_id(self) -> str:
        """
        TODO.

        Returns
        -------
        TODO.
        """
        # TODO: readonly?
        return self._element_id.id_string

    @property  # type: ignore
    @overrides
    def name(self):
        return self.get_name()

    @property  # type: ignore
    @overrides
    def control_type(self) -> str:
        result = self._client.RegistryGetControlType(self._element_id)
        return result.type

    @property  # type: ignore
    @overrides
    def parent_assembly(self) -> Optional[api.Assembly]:
        result = self._client.ElementGetParentElement(self._element_id)
        if result.id_string is None or result.id_string == "":
            return None
        else:
            return Assembly(result, self._channel)

    @property  # type: ignore
    @overrides
    def assemblies(self) -> Sequence[api.Assembly]:
        result = self._client.RegistryGetAssemblies(self._element_id)
        return [Assembly(one_element_id, self._channel) for one_element_id in result.ids]

    @overrides
    def _create_group(self, element_id: ElementId) -> api.IGroup:
        return Group(element_id, self._channel)

    @overrides
    def add_variable(self, name: str, type_: str) -> api.IVariable:
        result = self._client.AssemblyAddVariable(
            AddAssemblyVariableRequest(
                name=ElementName(name=name), target_assembly=self._element_id, variable_type=type_
            )
        )
        return Variable(result.id, self._channel)

    @overrides
    def rename(self, name: str) -> None:
        self._client.AssemblyRename(
            RenameRequest(target_assembly=self._element_id, new_name=ElementName(name=name))
        )

    @overrides
    def get_property(self, property_name: str) -> base_api.Property:
        grpc_value = self._client.PropertyOwnerGetPropertyValue(
            MetadataGetValueRequest(id=self._element_id, property_name=property_name)
        )
        acvi_value = convert_grpc_value_to_acvi(grpc_value)
        return base_api.Property(
            parent_element_id=self._element_id.id_string,
            property_name=property_name,
            property_value=acvi_value,
        )

    @overrides
    def set_property(self, property_name: str, property_value: acvi.IVariableValue) -> None:
        grpc_value = convert_interop_value_to_grpc(property_value)
        self._client.PropertyOwnerSetPropertyValue(
            MetadataSetValueRequest(
                id=self._element_id, property_name=property_name, value=grpc_value
            )
        )

    @property  # type: ignore
    @overrides
    def icon_id(self) -> int:
        response = self._client.AssemblyGetIcon(self._element_id)
        return response.id

    @icon_id.setter  # type: ignore
    @overrides
    def icon_id(self, value: int) -> None:
        self._client.AssemblySetIcon(
            AssemblyIconSetRequest(target=self._element_id, new_icon_id=value)
        )

    @property  # type: ignore
    @overrides
    def index_in_parent(self) -> int:
        response = self._client.ElementGetIndexInParent(self._element_id)
        return response.index

    @overrides
    def delete_variable(self, name: str) -> None:
        assembly_name = self.get_full_name()
        var_name = f"{assembly_name}.{name}"
        target_var = self._client.WorkflowGetVariableByName(ElementName(name=var_name))
        self._client.AssemblyDeleteVariable(target_var)

    @overrides
    def add_assembly(
        self,
        name: str,
        x_pos: Optional[int],
        y_pos: Optional[int],
        assembly_type: Optional[str] = None,
    ) -> api.IAssembly:
        request = AddAssemblyRequest(
            name=ElementName(name=name), parent=self._element_id, assembly_type=assembly_type
        )
        if x_pos is not None and y_pos is not None:
            request.av_pos.x_pos = x_pos
            request.av_pos.y_pos = y_pos
        response = self._client.AssemblyAddAssembly(request)
        return Assembly(response.id, self._channel)
