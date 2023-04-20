"""Defines an abstract base class for elements that return child variables and groups."""

from abc import ABC, abstractmethod
from typing import Mapping

import grpc
from overrides import overrides

import ansys.modelcenter.workflow.api as mc_api

from .abstract_workflow_element import AbstractWorkflowElement
from .create_datapin import create_datapin
from .grpc_error_interpretation import WRAP_TARGET_NOT_FOUND, interpret_rpc_error
from .proto.element_messages_pb2 import ElementId
from .proto.variable_value_messages_pb2 import VariableInfo
from .var_value_convert import grpc_type_enum_to_interop_type


class AbstractGRPCDatapinContainer(AbstractWorkflowElement, mc_api.IGroupOwner, ABC):
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

    def __init__(self, element_id: ElementId, channel: grpc.Channel):
        """
        Initialize a new instance.

        Parameters
        ----------
        element_id: the element ID of the group this object represents in ModelCenter.
        channel: the gRPC channel on which to communicate.
        """
        super(AbstractGRPCDatapinContainer, self).__init__(element_id=element_id, channel=channel)

    @property
    @interpret_rpc_error(WRAP_TARGET_NOT_FOUND)
    @overrides
    def groups(self) -> Mapping[str, mc_api.IGroup]:
        # LTTODO: alter gRPC response so that short names are included in the first place.
        """Get the child groups of this element."""
        result = self._client.RegistryGetGroups(self._element_id)
        one_element_id: ElementId
        groups = [self._create_group(one_element_id) for one_element_id in result.ids]
        one_group: mc_api.IGroup
        return {one_group.name: one_group for one_group in groups}

    @interpret_rpc_error(WRAP_TARGET_NOT_FOUND)
    @overrides
    def get_datapins(self) -> Mapping[str, mc_api.IDatapin]:
        # LTTODO: alter gRPC response so that short names are included in the first place.
        result = self._client.RegistryGetVariables(self._element_id)
        one_var_info: VariableInfo
        variables = [
            create_datapin(
                grpc_type_enum_to_interop_type(one_var_info.value_type),
                one_var_info.id,
                self._channel,
            )
            for one_var_info in result.variables
        ]
        one_variable: mc_api.IDatapin
        return {one_variable.name: one_variable for one_variable in variables}
