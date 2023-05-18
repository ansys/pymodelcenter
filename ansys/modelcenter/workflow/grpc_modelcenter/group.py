"""Provides an object-oriented way to interact with ModelCenter variable groups via gRPC."""
from typing import TYPE_CHECKING

from overrides import overrides

import ansys.modelcenter.workflow.api as api

from .. import api as mc_api
from .abstract_datapin_container import AbstractGRPCDatapinContainer

if TYPE_CHECKING:
    from .engine import Engine
from .proto.element_messages_pb2 import ElementId


class Group(AbstractGRPCDatapinContainer, api.IGroup):
    """
    Represents a group in the workflow.

    .. note::
        This class should not be directly instantiated by clients. Get a Workflow object from
        an instantiated Engine, and use it to get a valid instance of this object.
    """

    def _create_group(self, element_id: ElementId) -> mc_api.IGroup:
        return Group(element_id, self._engine)

    def __init__(self, element_id: ElementId, engine: "Engine"):
        """
        Initialize a new instance.

        Parameters
        ----------
        element_id : ElementId
            The id of the element.
        engine: Engine
            The engine that created this group.
        """
        super(Group, self).__init__(element_id=element_id, engine=engine)

    @overrides
    def __eq__(self, other):
        return isinstance(other, Group) and self.element_id == other.element_id
