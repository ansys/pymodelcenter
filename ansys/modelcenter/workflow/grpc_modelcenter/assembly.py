"""Implementation of Assembly."""

from typing import Optional

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
