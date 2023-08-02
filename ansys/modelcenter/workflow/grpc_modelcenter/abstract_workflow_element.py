"""Defines an abstract base class for gRPC-backed workflow elements."""

from abc import ABC
from typing import TYPE_CHECKING, AbstractSet, Mapping, Optional

import ansys.engineeringworkflow.api as aew_api
from ansys.engineeringworkflow.api import Property
import ansys.modelcenter.workflow.grpc_modelcenter.element_wrapper as elem_wrapper
import ansys.tools.variableinterop as atvi
import grpc
from overrides import overrides

if TYPE_CHECKING:
    from .engine import Engine

from .grpc_error_interpretation import WRAP_INVALID_ARG, WRAP_TARGET_NOT_FOUND, interpret_rpc_error
from .proto.custom_metadata_messages_pb2 import MetadataGetValueRequest, MetadataSetValueRequest
from .proto.element_messages_pb2 import ElementId
from .proto.grpc_modelcenter_workflow_pb2_grpc import ModelCenterWorkflowServiceStub
from .proto.variable_value_messages_pb2 import VariableValue
from .var_value_convert import convert_grpc_value_to_atvi, convert_interop_value_to_grpc


class AbstractWorkflowElement(aew_api.IElement, ABC):
    """An abstract base class for gRPC-backed workflow elements."""

    def _create_client(self, channel: grpc.Channel) -> ModelCenterWorkflowServiceStub:
        return ModelCenterWorkflowServiceStub(channel)  # pragma: no cover

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
        self._engine = engine
        self._client: ModelCenterWorkflowServiceStub = self._create_client(engine.channel)
        self._element_id: ElementId = element_id

    @property
    @overrides
    def element_id(self) -> str:
        return self._element_id.id_string

    @property
    @interpret_rpc_error(WRAP_TARGET_NOT_FOUND)
    @overrides
    def parent_element_id(self) -> str:
        result = self._client.ElementGetParentElement(self._element_id)
        return result.id.id_string

    @property
    @interpret_rpc_error(WRAP_TARGET_NOT_FOUND)
    @overrides
    def name(self) -> str:
        result = self._client.ElementGetName(self._element_id)
        return result.name

    @property
    @interpret_rpc_error(WRAP_TARGET_NOT_FOUND)
    @overrides
    def full_name(self) -> str:
        result = self._client.ElementGetFullName(self._element_id)
        return result.name

    @interpret_rpc_error({**WRAP_INVALID_ARG, **WRAP_TARGET_NOT_FOUND})
    @overrides
    def get_property(self, property_name: str) -> aew_api.Property:
        grpc_value: VariableValue = self._client.PropertyOwnerGetPropertyValue(
            MetadataGetValueRequest(id=self._element_id, property_name=property_name)
        )
        atvi_value = convert_grpc_value_to_atvi(grpc_value, self._engine.is_local)
        return aew_api.Property(
            parent_element_id=self._element_id.id_string,
            property_name=property_name,
            property_value=atvi_value,
        )

    @interpret_rpc_error({**WRAP_INVALID_ARG, **WRAP_TARGET_NOT_FOUND})
    @overrides
    def get_property_names(self) -> AbstractSet[str]:
        response = self._client.PropertyOwnerGetProperties(self._element_id)
        return set([name for name in response.names])

    @interpret_rpc_error(WRAP_TARGET_NOT_FOUND)
    @overrides
    def get_properties(self) -> Mapping[str, Property]:
        response = self._client.PropertyOwnerGetProperties(self._element_id)
        return {name: self.get_property(property_name=name) for name in response.names}

    @interpret_rpc_error({**WRAP_INVALID_ARG, **WRAP_TARGET_NOT_FOUND})
    @overrides
    def set_property(self, property_name: str, property_value: atvi.IVariableValue) -> None:
        grpc_value = convert_interop_value_to_grpc(
            property_value, engine_is_local=self._engine.is_local
        )
        self._client.PropertyOwnerSetPropertyValue(
            MetadataSetValueRequest(
                id=self._element_id, property_name=property_name, value=grpc_value
            )
        )

    @interpret_rpc_error(WRAP_TARGET_NOT_FOUND)
    @overrides
    def get_parent_element(self) -> Optional[aew_api.IElement]:
        result = self._client.ElementGetParentElement(self._element_id)
        if not result.id.id_string:
            return None
        else:
            return elem_wrapper.create_element(result, self._engine)


class UnsupportedWorkflowElement(AbstractWorkflowElement):
    """Represents a workflow element that is known to exists but whose type is not supported."""

    def __init__(self, element_id: ElementId, engine: "Engine"):
        """
        Initialize a new instance.

        Parameters
        ----------
        element_id: ElementId
            The element ID of the element this object represents in ModelCenter.
        engine: Engine
            The Engine that created this element.
        """
        super(UnsupportedWorkflowElement, self).__init__(element_id=element_id, engine=engine)
