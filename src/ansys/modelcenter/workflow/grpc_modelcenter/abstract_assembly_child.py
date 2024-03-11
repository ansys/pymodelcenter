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
"""Defines the abstract base class for children of assemblies.

Assemblies themselves are also included.
"""
from abc import ABC
from typing import TYPE_CHECKING, Optional, Tuple

import ansys.engineeringworkflow.api as aew_api
from overrides import overrides

import ansys.modelcenter.workflow.api as mc_api
import ansys.modelcenter.workflow.grpc_modelcenter.abstract_workflow_element as abstract_wfe

if TYPE_CHECKING:
    from .engine import Engine

from ansys.api.modelcenter.v0.element_messages_pb2 import ElementId

from .grpc_error_interpretation import WRAP_TARGET_NOT_FOUND, interpret_rpc_error


class AbstractAssemblyChild(abstract_wfe.AbstractWorkflowElement, mc_api.IAssemblyChild, ABC):
    """Defines an abstract base class for children of assemblies."""

    def __init__(self, element_id: ElementId, engine: "Engine"):
        """Initialize an instance."""
        super(AbstractAssemblyChild, self).__init__(element_id=element_id, engine=engine)

    @property
    @interpret_rpc_error(WRAP_TARGET_NOT_FOUND)
    @overrides
    def index_in_parent(self) -> int:
        response = self._client.ElementGetIndexInParent(self._element_id)
        return response.index

    @property
    @interpret_rpc_error(WRAP_TARGET_NOT_FOUND)
    @overrides
    def parent_assembly(self) -> Optional[mc_api.IAssembly]:
        result = self.get_parent_element()
        if not (result is None or isinstance(result, mc_api.IAssembly)):
            raise aew_api.EngineInternalError(
                f"The parent of an assembly or component should only ever be an assembly, "
                f"but a {result.__class__} was found instead."
            )
        else:
            return result

    @property
    @interpret_rpc_error(WRAP_TARGET_NOT_FOUND)
    def control_type(self) -> str:
        """Control type of the item.

        Returns
        -------
        str
            Control type of the item.
        """
        result = self._client.RegistryGetControlType(self._element_id)
        return result.type

    @interpret_rpc_error(WRAP_TARGET_NOT_FOUND)
    @overrides
    def get_analysis_view_position(self) -> Tuple[int, int]:
        response = self._client.AssemblyGetAnalysisViewPosition(self._element_id)
        return response.x_pos, response.y_pos
