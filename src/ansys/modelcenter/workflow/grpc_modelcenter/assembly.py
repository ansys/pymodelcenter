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
"""Defines the assembly."""

from typing import TYPE_CHECKING, Optional, Tuple

import ansys.tools.variableinterop as atvi
from overrides import overrides

import ansys.modelcenter.workflow.api as mc_api
import ansys.modelcenter.workflow.grpc_modelcenter.abstract_control_statement as abstractcs

from .create_datapin import create_datapin

if TYPE_CHECKING:
    from .engine import Engine

from ansys.api.modelcenter.v0.element_messages_pb2 import (
    AddAssemblyRequest,
    AddAssemblyVariableRequest,
    AddAssemblyVariableResponse,
    ElementId,
    ElementName,
)
from ansys.api.modelcenter.v0.workflow_messages_pb2 import (
    DeleteAssemblyVariableRequest,
    ElementIdOrName,
    NamedElementWorkflow,
)

from .grpc_error_interpretation import (
    WRAP_INVALID_ARG,
    WRAP_NAME_COLLISION,
    WRAP_TARGET_NOT_FOUND,
    InvalidInstanceError,
    interpret_rpc_error,
)
from .var_value_convert import interop_type_to_grpc_type_enum, interop_type_to_mc_type_string


class Assembly(
    abstractcs.AbstractControlStatement,
    mc_api.IAssembly,
):
    """Represents an assembly in ModelCenter.

    .. note::
        This class should not be directly instantiated by clients. Get a ``Workflow`` object from
        an instantiated ``Engine`` instance and use it to get a valid instance of this object.
    """

    def __init__(self, element_id: ElementId, engine: "Engine"):
        """Initialize an instance.

        Parameters
        ----------
        element_id : ElementId
            ID of the assembly.
        engine: Engine
            Engine to use to create the assembly.
        """
        super(Assembly, self).__init__(element_id=element_id, engine=engine)

    @overrides
    def __eq__(self, other):
        return isinstance(other, Assembly) and self.element_id == other.element_id

    @property
    @overrides
    def parent_element_id(self) -> str:
        result: str
        try:
            result = super().parent_element_id
        except InvalidInstanceError:
            # return empty string instead of an error if this is the root
            if self.full_name.find(".") == -1:
                result = ""
            else:
                raise
        return result

    @interpret_rpc_error({**WRAP_TARGET_NOT_FOUND, **WRAP_NAME_COLLISION, **WRAP_INVALID_ARG})
    @overrides
    def add_datapin(self, name: str, mc_type: atvi.VariableType) -> mc_api.IDatapin:
        type_in_request: str = interop_type_to_mc_type_string(mc_type)
        result: AddAssemblyVariableResponse = self._client.AssemblyAddVariable(
            AddAssemblyVariableRequest(
                name=ElementName(name=name),
                target_assembly=self._element_id,
                variable_type=type_in_request,
            )
        )
        return create_datapin(interop_type_to_grpc_type_enum(mc_type), result.id, self._engine)

    @interpret_rpc_error(WRAP_TARGET_NOT_FOUND)
    @overrides
    def delete_datapin(self, name: str) -> bool:
        assembly_name = self.name
        var_name = f"{assembly_name}.{name}"
        request = DeleteAssemblyVariableRequest(
            target=ElementIdOrName(
                target_name=NamedElementWorkflow(element_full_name=ElementName(name=var_name))
            )
        )
        return self._client.AssemblyDeleteVariable(request).existed

    @interpret_rpc_error({**WRAP_TARGET_NOT_FOUND, **WRAP_NAME_COLLISION, **WRAP_INVALID_ARG})
    @overrides
    def add_assembly(
        self,
        name: str,
        av_pos: Optional[Tuple[int, int]] = None,
        assembly_type: Optional[mc_api.AssemblyType] = None,
    ) -> mc_api.IAssembly:
        request = AddAssemblyRequest(
            name=ElementName(name=name),
            parent=self._element_id,
            assembly_type=assembly_type.value
            if assembly_type is not None
            else mc_api.AssemblyType.ASSEMBLY.value,
        )
        if av_pos is not None:
            (x_pos, y_pos) = av_pos
            request.av_pos.x_pos = x_pos
            request.av_pos.y_pos = y_pos
        response = self._client.AssemblyAddAssembly(request)
        return Assembly(response.id, self._engine)
