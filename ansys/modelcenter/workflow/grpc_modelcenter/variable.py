"""Provides an object-oriented way to interact with ModelCenter variables via gRPC."""
from abc import ABC
from typing import Collection, Optional, Sequence, Union
from xml.etree.ElementTree import Element as XMLElement

import ansys.common.variableinterop as acvi
from grpc import Channel
from overrides import overrides

import ansys.modelcenter.workflow.api as mc_api

from .abstract_workflow_element import AbstractWorkflowElement
from .proto.element_messages_pb2 import ElementId


class BaseVariable(AbstractWorkflowElement, mc_api.IVariable, ABC):
    """Represents a variable in the workflow."""

    def __init__(self, element_id: ElementId, channel: Channel):
        """
        Initialize a new instance.

        Parameters
        ----------
        element_id : ElementId
            The id of the element.
        """
        super(BaseVariable, self).__init__(element_id=element_id, channel=channel)

    @property
    @overrides
    def owning_component(self) -> mc_api.IComponent:
        # TODO: implement this method for all MC variables here.
        raise NotImplementedError()

    @property
    @overrides
    def interop_type(self) -> acvi.VariableType:
        # TODO: implement this method for all MC variables here.
        raise NotImplementedError()

    @property
    @overrides
    def get_modelcenter_type(self) -> str:
        # TODO: implement this method for all MC variables here.
        raise NotImplementedError()

    @overrides
    def invalidate(self) -> None:
        # TODO: implement this method for all MC variables here.
        raise NotImplementedError()

    @overrides
    def direct_precedents(self, follow_suspended: bool = False) -> Collection[mc_api.IVariable]:
        # TODO: implement this method for all MC variables here.
        raise NotImplementedError()

    @overrides
    def direct_dependents(self, follow_suspended: bool = False) -> Collection[mc_api.IVariable]:
        # TODO: implement this method for all MC variables here.
        raise NotImplementedError()

    @overrides
    def precedent_links(self) -> Collection[mc_api.IVariableLink]:
        # TODO: implement this method for all MC variables here.
        raise NotImplementedError()

    @overrides
    def dependent_links(self) -> Collection[mc_api.IVariableLink]:
        # TODO: implement this method for all MC variables here.
        raise NotImplementedError()

    @overrides
    def precedents(self, follow_suspended: bool = False) -> Sequence[mc_api.IVariable]:
        # TODO: implement this method for all MC variables here.
        raise NotImplementedError()

    @overrides
    def dependents(self, follow_suspended: bool = False) -> Sequence[mc_api.IVariable]:
        # TODO: implement this method for all MC variables here.
        raise NotImplementedError()

    @property
    @overrides
    def is_input_to_component(self) -> bool:
        # TODO: implement this method for all MC variables here.
        raise NotImplementedError()

    @overrides
    def get_value(self, hid: Optional[str]) -> acvi.VariableState:
        # TODO: implement this method for all MC variables here.
        raise NotImplementedError()

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
