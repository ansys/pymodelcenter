"""Defines an abstract base class for gRPC-backed workflow elements."""

from abc import ABC

import grpc

from .proto.element_messages_pb2 import ElementId
from .proto.grpc_modelcenter_workflow_pb2_grpc import ModelCenterWorkflowServiceStub


class AbstractWorkflowElement(ABC):
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

    def get_name(self) -> str:
        """Get the short name of the element (relative to its parent)."""
        return self._client.ElementGetName(self._element_id).name

    def get_full_name(self) -> str:
        """Get the full name of the element (relative to its parent)."""
        return self._client.ElementGetFullName(self._element_id).name
