"""Implementation of Assembly."""

from typing import Optional, Sequence

import ansys.common.variableinterop as acvi
import ansys.engineeringworkflow.api as aew_api
from grpc import Channel
from overrides import overrides

import ansys.modelcenter.workflow.api as mc_api
import ansys.modelcenter.workflow.grpc_modelcenter.abstract_assembly_child as aachild

from .abstract_renamable import AbstractRenamableElement
from .create_variable import create_variable
from .element_wrapper import create_element
from .group import Group
from .grpc_error_interpretation import (
    WRAP_INVALID_ARG,
    WRAP_NAME_COLLISION,
    WRAP_TARGET_NOT_FOUND,
    InvalidInstanceError,
    interpret_rpc_error,
)
from .proto.element_messages_pb2 import (
    AddAssemblyRequest,
    AddAssemblyVariableRequest,
    AddAssemblyVariableResponse,
    ElementId,
    ElementName,
)
from .proto.workflow_messages_pb2 import (
    DeleteAssemblyVariableRequest,
    ElementIdOrName,
    ElementInfo,
    NamedElementInWorkflow,
)
from .var_value_convert import interop_type_to_mc_type_string, mc_type_string_to_interop_type
from .variable_container import AbstractGRPCVariableContainer


class Assembly(
    AbstractRenamableElement,
    AbstractGRPCVariableContainer,
    aachild.AbstractAssemblyChild,
    mc_api.IAssembly,
):
    """Represents an assembly in ModelCenter."""

    def __init__(self, element_id: ElementId, channel: Channel):
        """
        Initialize a new instance.

        Parameters
        ----------
        element_id : ElementId
            The id of the .
        """
        super(Assembly, self).__init__(element_id=element_id, channel=channel)

    @overrides
    def __eq__(self, other):
        return isinstance(other, Assembly) and self.element_id == other.element_id

    @property
    @overrides
    def parent_element_id(self) -> str:
        result: str
        try:
            result = super().parent_element_id
        except InvalidInstanceError:
            # return empty string instead of an error if this is the root
            if self.full_name.find(".") == -1:
                result = ""
            else:
                raise
        return result

    @interpret_rpc_error(WRAP_TARGET_NOT_FOUND)
    @overrides
    def get_elements(self) -> Sequence[aew_api.IElement]:
        result = self._client.AssemblyGetAssembliesAndComponents(self._element_id)
        one_child_element: ElementInfo
        return [
            create_element(one_child_element, self._channel)
            for one_child_element in result.elements
        ]

    @overrides
    def _create_group(self, element_id: ElementId) -> mc_api.IGroup:
        return Group(element_id, self._channel)

    @interpret_rpc_error({**WRAP_TARGET_NOT_FOUND, **WRAP_NAME_COLLISION})
    @overrides
    def add_variable(self, name: str, mc_type: acvi.VariableType) -> mc_api.IVariable:
        type_in_request: str = interop_type_to_mc_type_string(mc_type)
        result: AddAssemblyVariableResponse = self._client.AssemblyAddVariable(
            AddAssemblyVariableRequest(
                name=ElementName(name=name),
                target_assembly=self._element_id,
                variable_type=type_in_request,
            )
        )
        return create_variable(
            mc_type_string_to_interop_type(type_in_request), result.id, self._channel
        )

    @interpret_rpc_error(WRAP_TARGET_NOT_FOUND)
    @overrides
    def delete_variable(self, name: str) -> bool:
        assembly_name = self.name
        var_name = f"{assembly_name}.{name}"
        request = DeleteAssemblyVariableRequest(
            target=ElementIdOrName(
                target_name=NamedElementInWorkflow(element_full_name=ElementName(name=var_name))
            )
        )
        return self._client.AssemblyDeleteVariable(request).existed

    @interpret_rpc_error({**WRAP_TARGET_NOT_FOUND, **WRAP_NAME_COLLISION, **WRAP_INVALID_ARG})
    @overrides
    def add_assembly(
        self,
        name: str,
        x_pos: Optional[int],
        y_pos: Optional[int],
        assembly_type: Optional[str] = None,
    ) -> mc_api.IAssembly:
        request = AddAssemblyRequest(
            name=ElementName(name=name), parent=self._element_id, assembly_type=assembly_type
        )
        if x_pos is not None and y_pos is not None:
            request.av_pos.x_pos = x_pos
            request.av_pos.y_pos = y_pos
        response = self._client.AssemblyAddAssembly(request)
        return Assembly(response.id, self._channel)
