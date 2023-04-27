"""Provides an object-oriented way to interact with ModelCenter variables via gRPC."""
from abc import ABC
from typing import Optional

import ansys.common.variableinterop as acvi
import ansys.engineeringworkflow.api as aew_api
from grpc import Channel
from overrides import overrides

import ansys.modelcenter.workflow.api as mc_api

from .abstract_workflow_element import AbstractWorkflowElement
from .grpc_error_interpretation import WRAP_TARGET_NOT_FOUND, interpret_rpc_error
from .proto.element_messages_pb2 import ElementId
from .proto.workflow_messages_pb2 import ElementIdOrName
from .var_value_convert import convert_grpc_value_to_acvi, grpc_type_enum_to_interop_type


class BaseDatapin(AbstractWorkflowElement, mc_api.IDatapin, ABC):
    """Represents a datapin in the workflow."""

    def __init__(self, element_id: ElementId, channel: Channel):
        """
        Initialize a new instance.

        Parameters
        ----------
        element_id : ElementId
            The id of the element.
        """
        super(BaseDatapin, self).__init__(element_id=element_id, channel=channel)

    @property
    @interpret_rpc_error(WRAP_TARGET_NOT_FOUND)
    @overrides
    def value_type(self) -> acvi.VariableType:
        response = self._client.VariableGetType(self._element_id)
        return grpc_type_enum_to_interop_type(response.var_type)

    @property
    @interpret_rpc_error(WRAP_TARGET_NOT_FOUND)
    @overrides
    def is_input_to_component(self) -> bool:
        response = self._client.VariableGetIsInput(self._element_id)
        return response.is_input_in_component

    @property
    @interpret_rpc_error(WRAP_TARGET_NOT_FOUND)
    @overrides
    def is_input_to_workflow(self) -> bool:
        response = self._client.VariableGetIsInput(self._element_id)
        return response.is_input_in_workflow

    @interpret_rpc_error(WRAP_TARGET_NOT_FOUND)
    @overrides
    def get_value(self, hid: Optional[str] = None) -> acvi.VariableState:
        if hid is not None:
            raise ValueError("This engine implementation does not yet support HIDs.")
        response = self._client.VariableGetState(ElementIdOrName(target_id=self._element_id))
        interop_value: acvi.IVariableValue
        try:
            interop_value = convert_grpc_value_to_acvi(response.value)
        except ValueError as convert_failure:
            raise aew_api.EngineInternalError(
                "Unexpected failure converting gRPC value response"
            ) from convert_failure
        return acvi.VariableState(value=interop_value, is_valid=response.is_valid)
