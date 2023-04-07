"""Provides an object-oriented way to interact with ModelCenter variables via gRPC."""
from abc import ABC
from typing import Collection, Optional, Sequence

import ansys.common.variableinterop as acvi
from grpc import Channel
from overrides import overrides

import ansys.modelcenter.workflow.api as mc_api

from .abstract_workflow_element import AbstractWorkflowElement
from .proto.element_messages_pb2 import ElementId
from .var_value_convert import convert_grpc_value_to_acvi, grpc_type_enum_to_interop_type


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
        # TODO/REDUCE: Skipping implementation, will drop for Phase II.
        raise NotImplementedError()

    @property
    @overrides
    def interop_type(self) -> acvi.VariableType:
        response = self._client.VariableGetType(self._element_id)
        return grpc_type_enum_to_interop_type(response.var_type)

    @property
    @overrides
    def get_modelcenter_type(self) -> str:
        response = self._client.VariableGetType(self._element_id)
        return response.mc_type

    # TODO/REDUCE: Consider dropping invalidate, predecent / dependent methods for Phase II

    @overrides
    def invalidate(self) -> None:
        # TODO: Currently missing a call on gRPC API.
        pass

    @overrides
    def direct_precedents(self, follow_suspended: bool = False) -> Collection[mc_api.IVariable]:
        # TODO: Currently missing a call on gRPC API
        return []

    @overrides
    def direct_dependents(self, follow_suspended: bool = False) -> Collection[mc_api.IVariable]:
        # TODO: Currently missing a call on gRPC API
        return []

    @overrides
    def precedent_links(self) -> Collection[mc_api.IVariableLink]:
        # TODO: Currently missing a call on gRPC API
        return []

    @overrides
    def dependent_links(self) -> Collection[mc_api.IVariableLink]:
        # TODO: Currently missing a call on gRPC API
        return []

    @overrides
    def precedents(self, follow_suspended: bool = False) -> Sequence[mc_api.IVariable]:
        # TODO: Currently missing a call on gRPC API
        return []

    @overrides
    def dependents(self, follow_suspended: bool = False) -> Sequence[mc_api.IVariable]:
        # TODO: Currently missing a gRPC endpoint
        return []

    @property
    @overrides
    def is_input_to_component(self) -> bool:
        response = self._client.VariableGetIsInput(self._element_id)
        return response.is_input_in_component

    @property
    @overrides
    def is_input_to_model(self) -> bool:
        response = self._client.VariableGetIsInput(self._element_id)
        return response.is_input_in_workflow

    @overrides
    def get_value(self, hid: Optional[str]) -> acvi.VariableState:
        response = self._client.VariableGetState(self._element_id)
        interop_value: acvi.IVariableValue
        try:
            interop_value = convert_grpc_value_to_acvi(response.value)
        except ValueError as convert_failure:
            # TODO/ERRORS: Need a specific error type here.
            raise Exception(
                "Unexpected failure converting gRPC value response"
            ) from convert_failure
        return acvi.VariableState(value=interop_value, is_valid=response.is_valid)


class BaseArray(BaseVariable, mc_api.IArray, ABC):
    """Base class for gRPC-based ModelCenter array variables."""

    @property
    @overrides
    def auto_size(self) -> bool:
        # TODO: currently missing a gRPC endpoint
        return True

    @auto_size.setter
    @overrides
    def auto_size(self, value: bool) -> None:
        # TODO: currently missing a gRPC endpoint
        pass
