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
"""Defines the abstract base class for control statement implementations."""

from abc import ABC
from typing import TYPE_CHECKING, Mapping

from ansys.api.modelcenter.v0.element_messages_pb2 import ElementId
from ansys.api.modelcenter.v0.workflow_messages_pb2 import ElementInfo
import ansys.engineeringworkflow.api as aew_api
from overrides import overrides

import ansys.modelcenter.workflow.api as mc_api
import ansys.modelcenter.workflow.grpc_modelcenter.abstract_assembly_child as aachild

from .abstract_datapin_container import AbstractGRPCDatapinContainer
from .abstract_renamable import AbstractRenamableElement
from .element_wrapper import create_element
from .group import Group
from .grpc_error_interpretation import WRAP_TARGET_NOT_FOUND, interpret_rpc_error

if TYPE_CHECKING:
    from .engine import Engine


class AbstractControlStatement(
    AbstractRenamableElement,
    AbstractGRPCDatapinContainer,
    aachild.AbstractAssemblyChild,
    aew_api.IControlStatement,
    ABC,
):
    """Defines an abstract base class for control statements.

    Control statements include driver components and assemblies.

    .. note::
        This class should not be directly instantiated by clients. Get a ``Workflow`` object
        from an instantiated ``Engine`` instance and use it to get valid ``Assembly``,
        ``Component``, or ``DriverComponent`` instances.
    """

    def __init__(self, element_id: ElementId, engine: "Engine"):
        """Initialize an instance.

        Parameters
        ----------
        element_id : ElementId
            ID of the control statement.
        engine : Engine
            Engine to create the control statement.
        """
        super(AbstractControlStatement, self).__init__(element_id=element_id, engine=engine)

    @interpret_rpc_error(WRAP_TARGET_NOT_FOUND)
    @overrides
    def get_elements(self) -> Mapping[str, aew_api.IElement]:
        result = self._client.AssemblyGetAssembliesAndComponents(self._element_id)
        one_child_element_info: ElementInfo
        child_elements = [
            create_element(one_child_element_info, self._engine)
            for one_child_element_info in result.elements
        ]
        one_child_element: aew_api.IElement
        return {element.name: element for element in child_elements}

    @overrides
    def _create_group(self, element_id: ElementId) -> mc_api.IGroup:
        return Group(element_id, self._engine)
