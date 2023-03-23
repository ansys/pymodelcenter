"""Provides an object-oriented way to interact with ModelCenter variable groups via gRPC."""
from grpc import Channel

import ansys.modelcenter.workflow.api as api

from .proto.element_messages_pb2 import ElementId


class Group(api.IGroup):
    """Represents a group in the workflow."""

    def __init__(self, element_id: ElementId, channel: Channel):
        """
        Initialize a new instance.

        Parameters
        ----------
        element_id : ElementId
            The id of the element.
        """
        self._element_id = element_id

    @property  # type: ignore
    def element_id(self) -> str:
        """Get the ID of the element."""
        return self._element_id.id_string
