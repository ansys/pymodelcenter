"""Implementation of Assembly."""

from grpc import Channel
from overrides import overrides

import ansys.modelcenter.workflow.api as api

from .proto.element_messages_pb2 import ElementId
from .proto.grpc_modelcenter_workflow_pb2_grpc import ModelCenterWorkflowServiceStub


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
