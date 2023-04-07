"""Implementation of Assembly."""

from typing import Collection, Optional, Sequence, Union

import ansys.common.variableinterop as acvi
from grpc import Channel
from overrides import overrides

import ansys.modelcenter.workflow.api as mc_api
import ansys.modelcenter.workflow.grpc_modelcenter.abstract_assembly_child as aachild
import ansys.modelcenter.workflow.grpc_modelcenter.component as component

from .abstract_renamable import AbstractRenamableElement
from .create_variable import create_variable
from .group import Group
from .proto.element_messages_pb2 import (
    AddAssemblyRequest,
    AddAssemblyVariableRequest,
    AddAssemblyVariableResponse,
    DeleteAssemblyVariableRequest,
    ElementId,
    ElementIdOrName,
    ElementName,
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

    @property  # type: ignore
    @overrides
    def assemblies(self) -> Sequence[mc_api.IAssembly]:
        result = self._client.RegistryGetAssemblies(self._element_id)
        return [Assembly(one_element_id, self._channel) for one_element_id in result.ids]

    @overrides
    def get_components(self) -> Collection[mc_api.IComponent]:
        result = self._client.AssemblyGetComponents(self._element_id)
        one_element_id: ElementId
        # TODO: test when component wrapper is actually ready
        return [component.Component(one_element_id, self._channel) for one_element_id in result.ids]

    @overrides
    def _create_group(self, element_id: ElementId) -> mc_api.IGroup:
        return Group(element_id, self._channel)

    @overrides
    def add_variable(self, name: str, mc_type: Union[acvi.VariableType, str]) -> mc_api.IVariable:
        type_in_request: str = (
            mc_type if isinstance(mc_type, str) else interop_type_to_mc_type_string(mc_type)
        )
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

    @overrides
    def delete_variable(self, name: str) -> bool:
        assembly_name = self.name
        var_name = f"{assembly_name}.{name}"
        request = DeleteAssemblyVariableRequest(
            target=ElementIdOrName(target_name=ElementName(name=var_name))
        )
        return self._client.AssemblyDeleteVariable(request).existed

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
