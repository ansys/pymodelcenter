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
"""Contains the common base class for all variables."""
from abc import ABC, abstractmethod
from typing import Collection

import ansys.engineeringworkflow.api as aew_api
import ansys.tools.variableinterop as atvi


class IDatapin(aew_api.IDatapin, ABC):
    """Represents a datapin on the workflow."""

    @abstractmethod
    def set_metadata(self, new_metadata: atvi.CommonVariableMetadata) -> None:
        """Set the standard metadata for the datapin."""

    @abstractmethod
    def get_dependents(
        self, only_fetch_direct_dependents: bool = False, follow_suspended_links: bool = False
    ) -> Collection[aew_api.IDatapin]:
        """Get the dependent (output) datapins for the datapin.

        Parameters
        ----------
        only_fetch_direct_dependents : bool, optional
            Whether to return only the direct dependents. The default is
            ``False``, in which case all dependents are returned recursively.
        follow_suspended_links : bool, optional
            Whether to follow suspended links between datapins. The default
            is ``False``.

        Returns
        -------
        Collection[aew_api.IDatapin]
            Collection of dependent datapins.
        """

    @abstractmethod
    def get_precedents(
        self, only_fetch_direct_precedents: bool = False, follow_suspended_links: bool = False
    ) -> Collection[aew_api.IDatapin]:
        """Get the precedent (input) datapins for the datapin.

        Parameters
        ----------
        only_fetch_direct_dependents : bool, optional
            Whether to return only the direct dependents. The default is
            ``False``, in which case all dependents are returned recursively.
        follow_suspended_links : bool, optional
            Whether to follow suspended links between datapins. The default
            is ``False``.

        Returns
        -------
        Collection[aew_api.IDatapin]
            Collection of precedent datapins.
        """
