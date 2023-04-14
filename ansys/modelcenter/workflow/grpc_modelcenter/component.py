"""Definition of Component."""
from typing import Optional, Tuple

from grpc import Channel, StatusCode
from overrides import overrides

import ansys.modelcenter.workflow.api as mc_api
import ansys.modelcenter.workflow.grpc_modelcenter.abstract_assembly_child as aachild
import ansys.modelcenter.workflow.grpc_modelcenter.abstract_renamable as abstract_renamable
import ansys.modelcenter.workflow.grpc_modelcenter.group as group

from .abstract_datapin_container import AbstractGRPCDatapinContainer
from .grpc_error_interpretation import WRAP_INVALID_ARG, WRAP_TARGET_NOT_FOUND, interpret_rpc_error
from .proto.element_messages_pb2 import ComponentInvokeMethodRequest, ElementId


class ComponentReconnectionFailedError(Exception):
    """Raised when a component reconnection failed."""

    ...


class ComponentDownloadValuesFailedError(Exception):
    """Raised when downloading a component's values failed."""

    ...


class Component(
    AbstractGRPCDatapinContainer,
    abstract_renamable.AbstractRenamableElement,
    aachild.AbstractAssemblyChild,
    mc_api.IComponent,
):
    """A component in a Workflow."""

    def __init__(self, element_id: ElementId, channel: Channel):
        """
        Initialize a new instance.

        Parameters
        ----------
        element_id : ElementId
            The id of the component.
        channel : Channel
        """
        super(Component, self).__init__(element_id=element_id, channel=channel)

    @overrides
    def _create_group(self, element_id: ElementId) -> mc_api.IGroup:
        return group.Group(element_id, self._channel)

    @interpret_rpc_error(WRAP_TARGET_NOT_FOUND)
    @overrides
    def get_source(self) -> str:
        response = self._client.ComponentGetSource(self._element_id)
        return response.source

    @interpret_rpc_error({**WRAP_TARGET_NOT_FOUND, **WRAP_INVALID_ARG})
    @overrides
    def invoke_method(self, method: str) -> None:
        self._client.ComponentInvokeMethod(
            ComponentInvokeMethodRequest(target=self._element_id, method_name=method)
        )

    @interpret_rpc_error(WRAP_TARGET_NOT_FOUND)
    @overrides
    def invalidate(self) -> None:
        self._client.ComponentInvalidate(self._element_id)

    @property
    @interpret_rpc_error(WRAP_TARGET_NOT_FOUND)
    @overrides
    def is_connected(self) -> bool:
        response = self._client.ComponentIsConnected(self._element_id)
        return response.is_connected

    @interpret_rpc_error(
        {**WRAP_TARGET_NOT_FOUND, StatusCode.FAILED_PRECONDITION: ComponentReconnectionFailedError}
    )
    @overrides
    def reconnect(self) -> None:
        self._client.ComponentReconnect(self._element_id)

    @interpret_rpc_error(
        {
            **WRAP_TARGET_NOT_FOUND,
            StatusCode.FAILED_PRECONDITION: ComponentDownloadValuesFailedError,
        }
    )
    @overrides
    def download_values(self) -> None:
        self._client.ComponentDownloadValues(self._element_id)

    @interpret_rpc_error(WRAP_TARGET_NOT_FOUND)
    @overrides
    def get_analysis_view_position(self) -> Tuple[int, int]:
        response = self._client.AssemblyGetAnalysisViewPosition(self._element_id)
        return response.x_pos, response.y_pos

    @property
    @interpret_rpc_error(WRAP_TARGET_NOT_FOUND)
    @overrides
    def pacz_url(self) -> Optional[str]:
        response = self._client.ComponentGetPaczUrl(self._element_id)
        return response.pacz_url if response.HasField("pacz_url") else None
