"""Defines a reusable implementation of renaming an element with a gRPC client."""
from abc import ABC
from typing import TYPE_CHECKING

from overrides import overrides

import ansys.modelcenter.workflow.api as mc_api
import ansys.modelcenter.workflow.grpc_modelcenter.abstract_workflow_element as abstract_wfe

if TYPE_CHECKING:
    from .engine import Engine
from .grpc_error_interpretation import (
    WRAP_INVALID_ARG,
    WRAP_NAME_COLLISION,
    WRAP_TARGET_NOT_FOUND,
    interpret_rpc_error,
)
from .proto.element_messages_pb2 import ElementId, ElementName, RenameRequest


class AbstractRenamableElement(abstract_wfe.AbstractWorkflowElement, mc_api.IRenamableElement, ABC):
    """Inheritable implementation of renaming with a gRPC client."""

    def __init__(self, element_id: ElementId, engine: "Engine"):
        """
        Initialize a new instance.

        Parameters
        ----------
        element_id: ElementId
            The element ID of the group this object represents in ModelCenter.
        engine: Engine
            The Engine that created this element.
        """
        super(AbstractRenamableElement, self).__init__(element_id=element_id, engine=engine)

    @interpret_rpc_error({**WRAP_INVALID_ARG, **WRAP_NAME_COLLISION, **WRAP_TARGET_NOT_FOUND})
    @overrides
    def rename(self, new_name: str) -> None:
        self._client.AssemblyRename(
            RenameRequest(target_assembly=self._element_id, new_name=ElementName(name=new_name))
        )
