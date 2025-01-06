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
"""Contains a gRPC-backed implementation of the IDriverComponent."""
from typing import TYPE_CHECKING

from .abstract_control_statement import AbstractControlStatement
from .component import Component

if TYPE_CHECKING:
    from .engine import Engine

from ansys.api.modelcenter.v0.element_messages_pb2 import ElementId

import ansys.modelcenter.workflow.api as mc_api


class DriverComponent(
    Component,
    AbstractControlStatement,
    mc_api.IDriverComponent,
):
    """Defines a driver component in the workflow.

    In process-mode workflows, driver components can contain children.
    In data-mode workflows, driver components should still be instantiated with an instance
    of this class, but the method to get child elements simply returns an empty collection.

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
            ID of the component.
        engine : Engine
            Engine to use to create the component.
        """
        super(DriverComponent, self).__init__(element_id=element_id, engine=engine)
