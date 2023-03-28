"""Defines an abstract base class for elements that return child variables and groups."""

from abc import ABC, abstractmethod
from typing import Collection, Sequence

import ansys.engineeringworkflow.api as eng_wkfl_api
import grpc
from overrides import overrides

import ansys.modelcenter.workflow.api as mc_api

from .abstract_workflow_element import AbstractWorkflowElement
from .proto.element_messages_pb2 import ElementId
from .variable import Variable


class AbstractGRPCVariableContainer(AbstractWorkflowElement, eng_wkfl_api.IVariableContainer, ABC):
    """An abstract base class for elements that return child variables and groups."""

    @abstractmethod
    def _create_group(self, element_id: ElementId) -> mc_api.IGroup:
        """
        Create an object to represent a child group.

        Concrete implementations should implement this with a concrete IGroup implementation.

        Parameters
        ----------
        element_id: the element ID of the child group.
        """
        raise NotImplementedError()

    def __init__(self, element_id: ElementId, channel: grpc.Channel):
        """
        Initialize a new instance.

        Parameters
        ----------
        element_id: the element ID of the group this object represents in ModelCenter.
        channel: the gRPC channel on which to communicate.
        """
        super(AbstractGRPCVariableContainer, self).__init__(element_id=element_id, channel=channel)

    @property  # type: ignore
    def groups(self) -> Sequence[mc_api.IGroup]:
        """Get the child groups of this element."""
        result = self._client.RegistryGetGroups(self._element_id)
        one_element_id: ElementId
        return [self._create_group(one_element_id) for one_element_id in result.ids]

    @overrides
    def get_variables(self) -> Collection[mc_api.IVariable]:
        result = self._client.RegistryGetVariables(self._element_id)
        one_element_id: ElementId
        return [Variable(one_element_id, self._channel) for one_element_id in result.ids]