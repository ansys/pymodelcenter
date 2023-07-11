"""Contains implementations of reference property related classes."""
from abc import abstractmethod
from typing import TYPE_CHECKING, Mapping

import grpc

from . import var_value_convert
from ..api.ireferenceproperty import IReferencePropertyBase
from .grpc_error_interpretation import (
    WRAP_OUT_OF_BOUNDS,
    WRAP_TARGET_NOT_FOUND,
    interpret_rpc_error,
)
from .proto.grpc_modelcenter_workflow_pb2_grpc import ModelCenterWorkflowServiceStub
from .var_metadata_convert import convert_grpc_metadata
from .var_value_convert import convert_grpc_value_to_atvi, grpc_type_enum_to_interop_type

if TYPE_CHECKING:
    from .engine import Engine

import ansys.engineeringworkflow.api as aew_api
from ansys.tools import variableinterop as atvi
from overrides import overrides

from ansys.modelcenter.workflow.api import (
    IReferenceArrayProperty,
    IReferenceProperty,
    IReferencePropertyManager,
)
import ansys.modelcenter.workflow.grpc_modelcenter.proto.variable_value_messages_pb2 as var_msgs

from .proto.element_messages_pb2 import ElementId
from .proto.variable_value_messages_pb2 import (
    ReferencePropertyGetIsInputResponse,
    ReferencePropertyIdentifier,
    ReferencePropertySetIsInputRequest,
)


class ReferencePropertyBase(IReferencePropertyBase):
    """
    A base class for reference properties that defines common methods.

    .. note::
        This base class should not be used directly. Instead, use ReferenceProperty or
        ReferenceArrayProperty as required.
    """

    @abstractmethod
    def __init__(self, element_id: ElementId, name: str, engine: "Engine") -> None:
        """
        Initialize a new instance.

        Parameters
        ----------
        element_id: ElementId
            The id of the reference that owns this property.
        name: str
            The name of the property.
        engine: Engine
            The Engine that created this property.
        """
        self._element_id: ElementId = element_id
        self._name = name
        self._engine = engine
        self._client: ModelCenterWorkflowServiceStub = self._create_client(engine.channel)

    @staticmethod
    def _create_client(channel: grpc.Channel) -> ModelCenterWorkflowServiceStub:
        return ModelCenterWorkflowServiceStub(channel)  # pragma: no cover

    @overrides
    def get_value_type(self) -> atvi.VariableType:
        request = var_msgs.ReferencePropertyIdentifier(
            reference_var=self._element_id, prop_name=self._name
        )
        response: var_msgs.ReferencePropertyGetTypeResponse = self._client.ReferencePropertyGetType(
            request
        )
        return grpc_type_enum_to_interop_type(response)

    @interpret_rpc_error(WRAP_TARGET_NOT_FOUND)
    @overrides
    def get_metadata(self) -> atvi.CommonVariableMetadata:
        request = var_msgs.ReferencePropertyIdentifier(
            reference_var=self._element_id, prop_name=self._name
        )
        response: var_msgs.VariableMetadata = self._client.ReferencePropertyGetMetadata(request)
        metadata_value = getattr(response, response.WhichOneof("value"))
        return convert_grpc_metadata(metadata_value)

    @overrides
    def set_metadata(self, new_value: atvi.CommonVariableMetadata):
        pass

    @property
    @interpret_rpc_error(WRAP_TARGET_NOT_FOUND)
    @overrides
    def is_input(self) -> bool:
        request = ReferencePropertyIdentifier(reference_var=self._element_id, prop_name=self._name)
        response: ReferencePropertyGetIsInputResponse = self._client.ReferencePropertyGetIsInput(
            request
        )
        return response.is_input

    @is_input.setter
    @interpret_rpc_error(WRAP_TARGET_NOT_FOUND)
    def is_input(self, is_input: bool):
        """Setter for is_input property."""
        target = ReferencePropertyIdentifier(reference_var=self._element_id, prop_name=self._name)
        request = ReferencePropertySetIsInputRequest(target=target, new_value=is_input)
        self._client.ReferencePropertySetIsInput(request)

    @property
    @overrides
    def name(self) -> str:
        return self._name


class ReferenceProperty(ReferencePropertyBase, IReferenceProperty):
    """Represents a reference property."""

    @overrides
    def __init__(self, element_id: ElementId, name: str, engine: "Engine") -> None:
        super().__init__(element_id=element_id, name=name, engine=engine)

    @interpret_rpc_error(WRAP_TARGET_NOT_FOUND)
    @overrides
    def get_state(self) -> atvi.VariableState:
        target_prop = var_msgs.ReferencePropertyIdentifier(
            reference_var=self._element_id, prop_name=self._name
        )
        request = var_msgs.IndexedReferencePropertyIdentifier(target_prop=target_prop)
        response = self._client.ReferencePropertyGetValue(request)
        interop_value: atvi.IVariableValue
        try:
            interop_value = convert_grpc_value_to_atvi(response.value, self._engine.is_local)
        except ValueError as convert_failure:
            raise aew_api.EngineInternalError(
                "Unexpected failure converting gRPC value response"
            ) from convert_failure
        return atvi.VariableState(value=interop_value, is_valid=response.is_valid)

    @interpret_rpc_error(WRAP_TARGET_NOT_FOUND)
    @overrides
    def set_value(self, new_value: atvi.VariableState) -> None:
        grpc_value = var_value_convert.convert_interop_value_to_grpc(new_value.value)
        target_prop = var_msgs.IndexedReferencePropertyIdentifier(
            target_prop=var_msgs.ReferencePropertyIdentifier(
                reference_var=self._element_id, prop_name=self._name
            )
        )
        request = var_msgs.ReferencePropertySetValueRequest(
            target_prop=target_prop, new_value=grpc_value
        )
        self._client.ReferencePropertySetValue(request)


class ReferenceArrayProperty(ReferencePropertyBase, IReferenceArrayProperty):
    """Represents a reference array property."""

    @overrides
    def __init__(self, element_id: ElementId, name: str, engine: "Engine") -> None:
        super().__init__(element_id=element_id, name=name, engine=engine)

    @overrides
    def set_value_at(self, index: int, new_value: atvi.VariableState) -> None:
        grpc_value = var_value_convert.convert_interop_value_to_grpc(new_value.value)
        target_prop = var_msgs.IndexedReferencePropertyIdentifier(
            target_prop=var_msgs.ReferencePropertyIdentifier(
                reference_var=self._element_id, prop_name=self._name
            ),
            index=index,
        )
        request = var_msgs.ReferencePropertySetValueRequest(
            target_prop=target_prop, new_value=grpc_value
        )
        self._client.ReferencePropertySetValue(request)

    @interpret_rpc_error({**WRAP_TARGET_NOT_FOUND, **WRAP_OUT_OF_BOUNDS})
    @overrides
    def get_state_at(self, index: int) -> atvi.VariableState:
        target_prop = var_msgs.ReferencePropertyIdentifier(
            reference_var=self._element_id, prop_name=self._name
        )
        request = var_msgs.IndexedReferencePropertyIdentifier(target_prop=target_prop, index=index)
        response: var_msgs.VariableState = self._client.ReferencePropertyGetValue(request)
        interop_value: atvi.IVariableValue
        try:
            interop_value = convert_grpc_value_to_atvi(response.value, self._engine.is_local)
        except ValueError as convert_failure:
            raise aew_api.EngineInternalError(
                "Unexpected failure converting gRPC value response"
            ) from convert_failure
        return atvi.VariableState(value=interop_value, is_valid=response.is_valid)


class ReferencePropertyManager(IReferencePropertyManager):
    """Provides utility methods for getting reference properties from reference datapins."""

    @overrides
    def get_reference_properties(self) -> Mapping[str, IReferenceProperty]:
        return {}