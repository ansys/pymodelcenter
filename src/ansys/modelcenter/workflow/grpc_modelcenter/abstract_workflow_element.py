# Copyright (C) 2022 - 2024 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
"""Defines the abstract base class for gRPC-backed workflow elements."""

from abc import ABC
from typing import TYPE_CHECKING, AbstractSet, Mapping, Optional

import ansys.engineeringworkflow.api as aew_api
from ansys.engineeringworkflow.api import Property
import ansys.tools.variableinterop as atvi
import grpc
from overrides import overrides

import ansys.modelcenter.workflow.grpc_modelcenter.element_wrapper as elem_wrapper

if TYPE_CHECKING:
    from .engine import Engine

from ansys.api.modelcenter.v0.custom_metadata_messages_pb2 import (
    MetadataGetValueRequest,
    MetadataSetValueRequest,
)
from ansys.api.modelcenter.v0.element_messages_pb2 import ElementId
from ansys.api.modelcenter.v0.grpc_modelcenter_workflow_pb2_grpc import (
    ModelCenterWorkflowServiceStub,
)
from ansys.api.modelcenter.v0.variable_value_messages_pb2 import VariableValue

from .grpc_error_interpretation import WRAP_INVALID_ARG, WRAP_TARGET_NOT_FOUND, interpret_rpc_error
from .var_value_convert import convert_grpc_value_to_atvi, convert_interop_value_to_grpc


class AbstractWorkflowElement(aew_api.IElement, ABC):
    """Defines the abstract base class for gRPC-backed workflow elements."""

    def _create_client(self, channel: grpc.Channel) -> ModelCenterWorkflowServiceStub:
        return ModelCenterWorkflowServiceStub(channel)  # pragma: no cover

    def __init__(self, element_id: ElementId, engine: "Engine"):
        """Initialize an instance.

        Parameters
        ----------
        element_id : ElementId
            ID of the group that the object represents in ModelCenter.
        engine : Engine
            Engine that created the element.
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
    """Represents a known workflow element whose type is not supported."""

    def __init__(self, element_id: ElementId, engine: "Engine"):
        """Initialize an instance.

        Parameters
        ----------
        element_id : ElementId
            ID of the element that the object represents in ModelCenter.
        engine : Engine
            Engine that created the element.
        """
        super(UnsupportedWorkflowElement, self).__init__(element_id=element_id, engine=engine)
