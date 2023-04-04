"""Implementation of Assembly."""

from typing import Collection, Optional, Sequence, Union
from xml.etree.ElementTree import Element as XMLElement

import ansys.common.variableinterop as acvi
from grpc import Channel
from overrides import overrides

import ansys.modelcenter.workflow.api as mc_api

from .abstract_renamable import AbstractRenamableElement
from .component import Component
from .create_variable import create_variable
from .group import Group
from .proto.element_messages_pb2 import (
    AddAssemblyRequest,
    AddAssemblyVariableRequest,
    ElementId,
    ElementName,
)
from .var_value_convert import interop_type_to_mc_type_string
from .variable_container import AbstractGRPCVariableContainer


class Assembly(AbstractGRPCVariableContainer, AbstractRenamableElement, mc_api.IAssembly):
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
    def control_type(self) -> str:
        result = self._client.RegistryGetControlType(self._element_id)
        return result.type

    @property  # type: ignore
    @overrides
    def parent_assembly(self) -> Optional[mc_api.IAssembly]:
        result = self._client.ElementGetParentElement(self._element_id)
        if result.id_string is None or result.id_string == "":
            return None
        else:
            return Assembly(result, self._channel)

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
        return [Component(one_element_id) for one_element_id in result.ids]

    @overrides
    def _create_group(self, element_id: ElementId) -> mc_api.IGroup:
        return Group(element_id, self._channel)

    @overrides
    def add_variable(self, name: str, mc_type: Union[acvi.VariableType, str]) -> mc_api.IVariable:
        type_in_request: str = (
            mc_type if isinstance(mc_type, str) else interop_type_to_mc_type_string(mc_type)
        )
        result = self._client.AssemblyAddVariable(
            AddAssemblyVariableRequest(
                name=ElementName(name=name),
                target_assembly=self._element_id,
                variable_type=type_in_request,
            )
        )
        return create_variable(acvi.VariableType.UNKNOWN, result.id, self._channel)

    @property  # type: ignore
    @overrides
    def index_in_parent(self) -> int:
        response = self._client.ElementGetIndexInParent(self._element_id)
        return response.index

    @overrides
    def delete_variable(self, name: str) -> bool:
        assembly_name = self.name
        var_name = f"{assembly_name}.{name}"
        target_var = self._client.WorkflowGetVariableByName(ElementName(name=var_name))
        # TODO: fix gRPC API here to optionally just take the name in the first place
        return self._client.AssemblyDeleteVariable(target_var).existed

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

    @overrides
    def set_custom_metadata(
        self,
        name: str,
        value: Union[str, int, float, bool, XMLElement],
        access: mc_api.ComponentMetadataAccess,
        archive: bool,
    ) -> None:
        # TODO: skipping implementation for now, debating collapsing into AEW property methods.
        return None

    @overrides
    def get_custom_metadata(self, name: str) -> Union[str, int, float, bool, XMLElement]:
        # TODO: skipping implementation for now, debating collapsing into AEW property methods.
        return ""
