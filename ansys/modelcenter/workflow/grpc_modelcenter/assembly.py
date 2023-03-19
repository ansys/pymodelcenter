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
    AddAssemblyVariableRequest,
    ElementId,
    ElementName,
    RenameRequest,
)
from .proto.grpc_modelcenter_workflow_pb2_grpc import ModelCenterWorkflowServiceStub
from .var_value_convert import convert_grpc_value_to_acvi, convert_interop_value_to_grpc
from .variable import Variable


class Assembly(api.Assembly):
    """Represents an assembly in ModelCenter."""

    def _create_client(self, channel: Channel) -> ModelCenterWorkflowServiceStub:
        return ModelCenterWorkflowServiceStub(channel)

    def __init__(self, element_id: ElementId, channel: Channel):
        """
        Initialize a new instance.

        Parameters
        ----------
        element_id : ElementId
            The id of the .
        """
        self._element_id = element_id
        self._channel = channel
        self._client = self._create_client(channel)

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
        result = self._client.ElementGetName(self._element_id)
        return result.name

    @overrides
    def get_full_name(self) -> str:
        result = self._client.ElementGetFullName(self._element_id)
        return result.name

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

    @overrides
    def get_variables(self) -> Sequence[api.IVariable]:
        result = self._client.RegistryGetVariables(self._element_id)
        return [Variable(one_element_id, self._channel) for one_element_id in result.ids]

    @property  # type: ignore
    @overrides
    def assemblies(self) -> Sequence[api.Assembly]:
        result = self._client.RegistryGetAssemblies(self._element_id)
        return [Assembly(one_element_id, self._channel) for one_element_id in result.ids]

    @property  # type: ignore
    @overrides
    def groups(self) -> Sequence[api.IGroup]:
        result = self._client.RegistryGetGroups(self._element_id)
        return [Group(one_element_id, self._channel) for one_element_id in result.ids]

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
