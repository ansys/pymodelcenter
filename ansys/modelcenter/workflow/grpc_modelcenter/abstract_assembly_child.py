"""Defines an abstract base class for children of assemblies (including assemblies themselves)."""
from abc import ABC
from typing import Optional

from grpc import Channel
from overrides import overrides

import ansys.modelcenter.workflow.api as mc_api
import ansys.modelcenter.workflow.grpc_modelcenter.abstract_workflow_element as abstract_wfe

from .grpc_error_interpretation import (
    WRAP_TARGET_NOT_FOUND,
    EngineInternalError,
    interpret_rpc_error,
)
from .proto.element_messages_pb2 import ElementId


class AbstractAssemblyChild(abstract_wfe.AbstractWorkflowElement, mc_api.IAssemblyChild, ABC):
    """An abstract base class for children of assemblies."""

    def __init__(self, element_id: ElementId, channel: Channel):
        """Initialize a new instance."""
        super(AbstractAssemblyChild, self).__init__(element_id=element_id, channel=channel)

    @property
    @interpret_rpc_error(WRAP_TARGET_NOT_FOUND)
    @overrides
    def index_in_parent(self) -> int:
        response = self._client.ElementGetIndexInParent(self._element_id)
        return response.index

    @property
    @interpret_rpc_error(WRAP_TARGET_NOT_FOUND)
    @overrides
    def parent_assembly(self) -> Optional[mc_api.IAssembly]:
        result = self.get_parent_element()
        if not (result is None or isinstance(result, mc_api.IAssembly)):
            raise EngineInternalError(
                f"The parent of an assembly or component should only ever be an assembly, "
                f"but found a {result.__class__} instead"
            )
        else:
            return result

    @property
    @interpret_rpc_error(WRAP_TARGET_NOT_FOUND)
    def control_type(self) -> str:
        """Get the control type of this item."""
        result = self._client.RegistryGetControlType(self._element_id)
        return result.type
