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
"""Defines the component."""
from abc import ABC, abstractmethod

import ansys.engineeringworkflow.api as aew_api

import ansys.modelcenter.workflow.api.iassembly as assembly
import ansys.modelcenter.workflow.api.igroup as igroup
import ansys.modelcenter.workflow.api.irenamable_elements as renamable_element


class IComponent(
    renamable_element.IRenamableElement,
    aew_api.IComponent,
    igroup.IGroupOwner,
    assembly.IAssemblyChild,
    ABC,
):
    """Represents a component in the workflow."""

    # ModelCenter

    @abstractmethod
    def get_source(self) -> str:
        """Get the source of the component.

        Returns
        -------
        str
            Source of the component.
        """

    @property
    @abstractmethod
    def control_type(self) -> str:
        """Type of the component.

        Options include:

        * Assembly
        * Component
        * Empty
        * ForEach
        * If
        * Parallel
        * Sequence

        Returns
        -------
        str
            Type of the component.
        """

    @abstractmethod
    def invoke_method(self, method: str) -> None:
        """Invoke one of the component's methods.

        Parameters
        ----------
        method : str
            Name of the method.
        """

    @abstractmethod
    def invalidate(self) -> None:
        """Invalidate the component and all of its datapins."""

    @property
    @abstractmethod
    def is_connected(self) -> bool:
        """Flag indicating if the component is connected to its source."""

    @abstractmethod
    def reconnect(self) -> None:
        """Reload the component from its source."""

    @abstractmethod
    def download_values(self) -> None:
        """Download the component's datapin values from the server if it is a
        ModelCenter Remote Execution component."""
