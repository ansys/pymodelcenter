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
"""Defines a function that creates a wrapper from a gRPC element info."""
from typing import TYPE_CHECKING

import ansys.engineeringworkflow.api as aew_api

if TYPE_CHECKING:
    from .engine import Engine
from ansys.api.modelcenter.v0.element_messages_pb2 import ElementType
from ansys.api.modelcenter.v0.workflow_messages_pb2 import ElementInfo


def create_element(info: ElementInfo, engine: "Engine") -> aew_api.IElement:
    """Create an appropriately-typed wrapper given a gRPC element info.

    Parameters
    ----------
    info : ElementInfo
        Element information from gRPC.
    engine : Engine
        ``Engine`` used to create the element.

    Returns
    -------
    aew_api.IElement
        Created element.
    """
    import ansys.modelcenter.workflow.grpc_modelcenter.abstract_workflow_element as abstract_elem
    import ansys.modelcenter.workflow.grpc_modelcenter.assembly as assembly_impl
    import ansys.modelcenter.workflow.grpc_modelcenter.component as component_impl
    import ansys.modelcenter.workflow.grpc_modelcenter.create_datapin as create_variable
    import ansys.modelcenter.workflow.grpc_modelcenter.driver_component as driver_comp_impl
    import ansys.modelcenter.workflow.grpc_modelcenter.group as group_impl

    if info.type == ElementType.ELEMENT_TYPE_ASSEMBLY:
        return assembly_impl.Assembly(info.id, engine)
    elif info.type == ElementType.ELEMENT_TYPE_DRIVERCOMPONENT:
        return driver_comp_impl.DriverComponent(info.id, engine)
    elif info.type == ElementType.ELEMENT_TYPE_COMPONENT:
        return component_impl.Component(info.id, engine)
    elif info.type == ElementType.ELEMENT_TYPE_GROUP:
        return group_impl.Group(info.id, engine)
    elif info.type == ElementType.ELEMENT_TYPE_VARIABLE:
        return create_variable.create_datapin(info.var_type, info.id, engine)
    else:
        # (including ELEMENT_TYPE_UNSPECIFIED)
        return abstract_elem.UnsupportedWorkflowElement(info.id, engine)
