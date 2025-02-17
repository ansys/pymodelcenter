# Copyright (C) 2022 - 2025 ANSYS, Inc. and/or its affiliates.
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
"""Provides for interacting with ModelCenter variables with gRPC.

This interaction is handled in an object-oriented way.
"""
from abc import ABC
from typing import TYPE_CHECKING, Collection, Optional

import ansys.engineeringworkflow.api as aew_api
import ansys.tools.variableinterop as atvi
from overrides import overrides

import ansys.modelcenter.workflow.api as mc_api

from . import create_datapin
from .abstract_workflow_element import AbstractWorkflowElement

if TYPE_CHECKING:
    from .engine import Engine

from ansys.api.modelcenter.v0.element_messages_pb2 import ElementId
from ansys.api.modelcenter.v0.variable_value_messages_pb2 import GetVariableDependenciesRequest
from ansys.api.modelcenter.v0.workflow_messages_pb2 import ElementIdOrName

from .grpc_error_interpretation import WRAP_TARGET_NOT_FOUND, interpret_rpc_error
from .var_value_convert import convert_grpc_value_to_atvi, grpc_type_enum_to_interop_type


class BaseDatapin(AbstractWorkflowElement, mc_api.IDatapin, ABC):
    """Represents a datapin on the workflow."""

    def __init__(self, element_id: ElementId, engine: "Engine"):
        """Initialize an instance.

        Parameters
        ----------
        element_id : ElementId
            ID of the element.
        engine : Engine
            Engine to use to create the datapin.
        """
        super(BaseDatapin, self).__init__(element_id=element_id, engine=engine)

    @property
    @interpret_rpc_error(WRAP_TARGET_NOT_FOUND)
    @overrides
    def value_type(self) -> atvi.VariableType:
        response = self._client.VariableGetType(self._element_id)
        return grpc_type_enum_to_interop_type(response.var_type)

    @property
    @interpret_rpc_error(WRAP_TARGET_NOT_FOUND)
    @overrides
    def is_input_to_component(self) -> bool:
        response = self._client.VariableGetIsInput(self._element_id)
        return response.is_input_component

    @property
    @interpret_rpc_error(WRAP_TARGET_NOT_FOUND)
    @overrides
    def is_input_to_workflow(self) -> bool:
        response = self._client.VariableGetIsInput(self._element_id)
        return response.is_input_workflow

    @interpret_rpc_error(WRAP_TARGET_NOT_FOUND)
    @overrides
    def get_state(self, hid: Optional[str] = None) -> atvi.VariableState:
        if hid is not None:
            raise ValueError("This engine implementation does not yet support HIDs.")
        response = self._client.VariableGetState(ElementIdOrName(target_id=self._element_id))
        interop_value: atvi.IVariableValue
        try:
            interop_value = convert_grpc_value_to_atvi(response.value, self._engine.is_local)
        except ValueError as convert_failure:
            raise aew_api.EngineInternalError(
                "Unexpected failure occurred converting gRPC value response."
            ) from convert_failure
        return atvi.VariableState(value=interop_value, is_valid=response.is_valid)

    @interpret_rpc_error(WRAP_TARGET_NOT_FOUND)
    @overrides
    def get_dependents(
        self, only_fetch_direct_dependents: bool, follow_suspended_links: bool
    ) -> Collection[mc_api.IDatapin]:
        request = GetVariableDependenciesRequest(
            id=self._element_id,
            only_fetch_direct_dependencies=only_fetch_direct_dependents,
            follow_suspended=follow_suspended_links,
        )

        response = self._client.VariableGetDependents(request)
        variables = [
            create_datapin.create_datapin(one_var_info.value_type, one_var_info.id, self._engine)
            for one_var_info in response.variables
        ]
        return variables

    @interpret_rpc_error(WRAP_TARGET_NOT_FOUND)
    @overrides
    def get_precedents(
        self, only_fetch_direct_precedents: bool, follow_suspended_links: bool
    ) -> Collection[mc_api.IDatapin]:
        request = GetVariableDependenciesRequest(
            id=self._element_id,
            only_fetch_direct_dependencies=only_fetch_direct_precedents,
            follow_suspended=follow_suspended_links,
        )

        response = self._client.VariableGetPrecedents(request)
        variables = [
            create_datapin.create_datapin(one_var_info.value_type, one_var_info.id, self._engine)
            for one_var_info in response.variables
        ]

        return variables
