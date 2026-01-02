# Copyright (C) 2022 - 2026 ANSYS, Inc. and/or its affiliates.
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
"""Defines the abstract base class for the datapin container."""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Mapping

from overrides import overrides

import ansys.modelcenter.workflow.api as mc_api

from .abstract_workflow_element import AbstractWorkflowElement
from .create_datapin import create_datapin

if TYPE_CHECKING:
    from .engine import Engine
    from .group import Group

from ansys.api.modelcenter.v0.element_messages_pb2 import ElementId
from ansys.api.modelcenter.v0.variable_value_messages_pb2 import VariableInfo

from .grpc_error_interpretation import WRAP_TARGET_NOT_FOUND, interpret_rpc_error


class AbstractGRPCDatapinContainer(AbstractWorkflowElement, mc_api.IGroupOwner, ABC):
    """Defines the abstract base class for the datapin container.

    A datapin container returns child variables and groups.
    """

    @abstractmethod
    def _create_group(self, element_id: ElementId) -> mc_api.IGroup:
        """Create an object to represent a child group.

        Concrete implementations should implement this with a concrete
        ``mc_api.IGroup`` implementation.

        Parameters
        ----------
        element_id : ElementId
            ID of the child group.

        Returns
        -------
        mc_api.IGroup
            Created child group.
        """

    def __init__(self, element_id: ElementId, engine: "Engine"):
        """Initialize an instance.

        Parameters
        ----------
        element_id : ElementId
            ID of the group that the object represents in ModelCenter.
        engine : Engine
            Engine that created the datapin
        """
        super(AbstractGRPCDatapinContainer, self).__init__(element_id=element_id, engine=engine)

    @interpret_rpc_error(WRAP_TARGET_NOT_FOUND)
    @overrides
    def get_groups(self) -> Mapping[str, mc_api.IGroup]:
        # LTTODO: alter gRPC response so that short names are included in the first place.
        """Get the child groups of the element."""
        result = self._client.RegistryGetGroups(self._element_id)
        one_element_id: ElementId
        groups = [self._create_group(one_element_id) for one_element_id in result.ids]
        one_group: "Group"
        return {one_group.name: one_group for one_group in groups}

    @interpret_rpc_error(WRAP_TARGET_NOT_FOUND)
    @overrides
    def get_datapins(self) -> Mapping[str, mc_api.IDatapin]:
        # LTTODO: alter gRPC response so that short names are included in the first place.
        result = self._client.RegistryGetVariables(self._element_id)
        one_var_info: VariableInfo
        variables = [
            create_datapin(one_var_info.value_type, one_var_info.id, self._engine)
            for one_var_info in result.variables
        ]
        one_variable: mc_api.IDatapin
        return {one_variable.name: one_variable for one_variable in variables}
