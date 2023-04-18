"""Provides an object-oriented way to interact with ModelCenter variable groups via gRPC."""
from grpc import Channel
from overrides import overrides

import ansys.modelcenter.workflow.api as api

from .. import api as mc_api
from .proto.element_messages_pb2 import ElementId
from .variable_container import AbstractGRPCVariableContainer


class Group(AbstractGRPCVariableContainer, api.IGroup):
    """Represents a group in the workflow."""

    def _create_group(self, element_id: ElementId) -> mc_api.IGroup:
        return Group(element_id, self._channel)

    def __init__(self, element_id: ElementId, channel: Channel):
        """
        Initialize a new instance.

        Parameters
        ----------
        element_id : ElementId
            The id of the element.
        """
        super(Group, self).__init__(element_id=element_id, channel=channel)

    @overrides
    def __eq__(self, other):
        return isinstance(other, Group) and self.element_id == other.element_id
