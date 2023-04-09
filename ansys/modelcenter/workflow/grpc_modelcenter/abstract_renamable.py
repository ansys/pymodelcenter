"""Defines a reusable implementation of renaming an element with a gRPC client."""
from abc import ABC

import grpc
from overrides import overrides

import ansys.modelcenter.workflow.api as mc_api
import ansys.modelcenter.workflow.grpc_modelcenter.abstract_workflow_element as abstract_wfe

from .proto.element_messages_pb2 import ElementId, ElementName, RenameRequest


class AbstractRenamableElement(abstract_wfe.AbstractWorkflowElement, mc_api.IRenamableElement, ABC):
    """Inheritable implementation of renaming with a gRPC client."""

    def __init__(self, element_id: ElementId, channel: grpc.Channel):
        """
        Initialize a new instance.

        Parameters
        ----------
        element_id: the element ID of the group this object represents in ModelCenter.
        channel: the gRPC channel on which to communicate.
        """
        super(AbstractRenamableElement, self).__init__(element_id=element_id, channel=channel)

    @overrides
    def rename(self, new_name: str) -> None:
        self._client.AssemblyRename(
            RenameRequest(target_assembly=self._element_id, new_name=ElementName(name=new_name))
        )
