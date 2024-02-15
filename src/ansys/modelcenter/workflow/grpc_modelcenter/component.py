"""Definition of Component."""
from typing import TYPE_CHECKING, Optional

from grpc import StatusCode
from overrides import overrides

import ansys.modelcenter.workflow.api as mc_api
import ansys.modelcenter.workflow.grpc_modelcenter.abstract_assembly_child as aachild
import ansys.modelcenter.workflow.grpc_modelcenter.abstract_renamable as abstract_renamable
import ansys.modelcenter.workflow.grpc_modelcenter.group as group

from .abstract_datapin_container import AbstractGRPCDatapinContainer

if TYPE_CHECKING:
    from .engine import Engine

from ansys.api.modelcenter.v0.element_messages_pb2 import ComponentInvokeMethodRequest, ElementId

from .grpc_error_interpretation import WRAP_INVALID_ARG, WRAP_TARGET_NOT_FOUND, interpret_rpc_error


class ComponentReconnectionFailedError(Exception):
    """Raised when a component reconnection failed."""

    ...


class ComponentDownloadValuesFailedError(Exception):
    """Raised when downloading a component's values failed."""

    ...


class Component(
    abstract_renamable.AbstractRenamableElement,
    AbstractGRPCDatapinContainer,
    aachild.AbstractAssemblyChild,
    mc_api.IComponent,
):
    """
    Defines a component in a workflow.

    .. note::
        This class should not be directly instantiated by clients. Get a ``Workflow`` object from
        an instantiated ``Engine``, and use it to get a valid instance of this object.
    """

    def __init__(self, element_id: ElementId, engine: "Engine"):
        """
        Initialize a new instance.

        Parameters
        ----------
        element_id : ElementId
            ID of the component.
        engine : Engine
            ``Engine`` that created this component.
        """
        super(Component, self).__init__(element_id=element_id, engine=engine)

    @overrides
    def __eq__(self, other):
        return isinstance(other, Component) and self.element_id == other.element_id

    @overrides
    def _create_group(self, element_id: ElementId) -> mc_api.IGroup:
        return group.Group(element_id, self._engine)

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

    @property
    @interpret_rpc_error(WRAP_TARGET_NOT_FOUND)
    @overrides
    def pacz_url(self) -> Optional[str]:
        response = self._client.ComponentGetPaczUrl(self._element_id)
        return response.pacz_url if response.HasField("pacz_url") else None
