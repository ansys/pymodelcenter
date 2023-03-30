"""Defines an abstract base class for gRPC-backed workflow elements."""

from abc import ABC
from typing import Collection

import ansys.common.variableinterop as acvi
import ansys.engineeringworkflow.api as aew_api
import grpc
from overrides import overrides

from .proto.custom_metadata_messages_pb2 import MetadataGetValueRequest, MetadataSetValueRequest
from .proto.element_messages_pb2 import ElementId
from .proto.grpc_modelcenter_workflow_pb2_grpc import ModelCenterWorkflowServiceStub
from .var_value_convert import convert_grpc_value_to_acvi, convert_interop_value_to_grpc


class AbstractWorkflowElement(aew_api.IElement, ABC):
    """An abstract base class for gRPC-backed workflow elements."""

    def _create_client(self, channel: grpc.Channel) -> ModelCenterWorkflowServiceStub:
        return ModelCenterWorkflowServiceStub(channel)

    def __init__(self, element_id: ElementId, channel: grpc.Channel):
        """
        Initialize a new instance.

        Parameters
        ----------
        element_id: the element ID of the group this object represents in ModelCenter.
        channel: the gRPC channel on which to communicate.
        """
        self._channel: grpc.Channel = channel
        self._client: ModelCenterWorkflowServiceStub = self._create_client(channel)
        self._element_id: ElementId = element_id

    @property
    @overrides
    def element_id(self) -> str:
        return self._element_id.id_string

    @property
    @overrides
    def parent_element_id(self) -> str:
        result = self._client.ElementGetParentElement(self._element_id)
        return result.id_string

    @property
    @overrides
    def name(self) -> str:
        result = self._client.ElementGetFullName(self._element_id)
        return result.name

    @overrides
    def get_property(self, property_name: str) -> aew_api.Property:
        grpc_value = self._client.PropertyOwnerGetPropertyValue(
            MetadataGetValueRequest(id=self._element_id, property_name=property_name)
        )
        acvi_value = convert_grpc_value_to_acvi(grpc_value)
        return aew_api.Property(
            parent_element_id=self._element_id.id_string,
            property_name=property_name,
            property_value=acvi_value,
        )

    @overrides
    def get_properties(self) -> Collection[aew_api.Property]:
        names = self._client.PropertyOwnerGetProperties()
        name: str
        return [self.get_property(property_name=name) for name in names]

    @overrides
    def set_property(self, property_name: str, property_value: acvi.IVariableValue) -> None:
        grpc_value = convert_interop_value_to_grpc(property_value)
        self._client.PropertyOwnerSetPropertyValue(
            MetadataSetValueRequest(
                id=self._element_id, property_name=property_name, value=grpc_value
            )
        )
