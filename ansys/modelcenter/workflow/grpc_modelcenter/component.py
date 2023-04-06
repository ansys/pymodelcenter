"""Definition of Component."""
from typing import Collection, Tuple, Union
from xml.etree.ElementTree import Element as XMLElement

from grpc import Channel
from overrides import overrides

import ansys.modelcenter.workflow.api as mc_api
import ansys.modelcenter.workflow.grpc_modelcenter.abstract_assembly_child as aachild

from .abstract_renamable import AbstractRenamableElement
from .group import Group
from .proto.element_messages_pb2 import ComponentInvokeMethodRequest, ElementId
from .variable_container import AbstractGRPCVariableContainer


class Component(
    AbstractGRPCVariableContainer,
    AbstractRenamableElement,
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
        return Group(element_id, self._channel)

    @property
    @overrides
    def associated_files(self) -> Collection[str]:
        # TODO/REDUCE: skipping impl for now, will be dropped for Phase II.
        return []

    @associated_files.setter
    @overrides
    def associated_files(self) -> Collection[str]:
        # TODO/REDUCE: skipping impl for now, will be dropped for Phase II.
        return [""]

    @overrides
    def get_source(self) -> str:
        response = self._client.ComponentGetSource(self._element_id)
        return response.source

    @overrides
    def get_variable(self, name: str) -> mc_api.IVariable:
        # TODO: skipping for now as the need for it will be removed by an upstream AEW update.
        raise NotImplementedError()

    @overrides
    def invoke_method(self, method: str) -> None:
        self._client.ComponentInvokeMethod(
            ComponentInvokeMethodRequest(target=self._element_id, method_name=method)
        )

    @overrides
    def invalidate(self) -> None:
        self._client.ComponentInvalidate(self._element_id)

    @property
    @overrides
    def is_connected(self) -> bool:
        response = self._client.ComponentIsConnected(self._element_id)
        return response.is_connected

    @overrides
    def reconnect(self) -> None:
        self._client.ComponentReconnect(self._element_id)

    @overrides
    def download_values(self) -> None:
        self._client.ComponentDownloadValues(self._element_id)

    @overrides
    def get_analysis_view_position(self) -> Tuple[int, int]:
        response = self._client.AssemblyGetAnalysisViewPosition(self._element_id)
        return response.x_pos, response.y_pos

    @property
    @overrides
    def pacz_url(self):
        # TODO: Need a more reliable gRPC call than just trying to parse source string
        # TODO: Upstream merge will include actual return type
        pass

    @overrides
    def set_custom_metadata(
        self,
        name: str,
        value: Union[str, int, float, bool, XMLElement],
        access: mc_api.ComponentMetadataAccess,
        archive: bool,
    ) -> None:
        # TODO: skipping implementation for now, will be dropped soon.
        pass

    @overrides
    def get_custom_metadata(self, name: str) -> Union[str, int, float, bool, XMLElement]:
        # TODO: skipping implementation for now, will be dropped soon.
        return ""
