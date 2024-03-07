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
"""This package provides a gRPC-based implementation of the ModelCenter Python
API.

This implementation finds a local installation of ModelCenter, launches
it, and attempts to communicate with it via gRPC.
"""

from .abstract_workflow_element import UnsupportedWorkflowElement
from .assembly import Assembly
from .boolean_datapin import BooleanArrayDatapin, BooleanDatapin
from .component import (
    Component,
    ComponentDownloadValuesFailedError,
    ComponentReconnectionFailedError,
)
from .datapin_link import DatapinLink
from .driver_component import DriverComponent
from .engine import Engine, WorkflowAlreadyLoadedError
from .file_datapin import FileArrayDatapin, FileDatapin
from .format import Format
from .group import Group
from .grpc_error_interpretation import (
    EngineDisconnectedError,
    InvalidInstanceError,
    UnexpectedEngineError,
)
from .integer_datapin import IntegerArrayDatapin, IntegerDatapin
from .mcd_process import EngineLicensingFailedException, MCDProcess
from .real_datapin import RealArrayDatapin, RealDatapin
from .reference_datapin import ReferenceArrayDatapin, ReferenceDatapin
from .reference_datapin_metadata import ReferenceDatapinMetadata
from .reference_property import ReferenceArrayProperty, ReferenceProperty
from .string_datapin import StringArrayDatapin, StringDatapin
from .unsupported_type_datapin import DatapinWithUnsupportedTypeException, UnsupportedTypeDatapin
from .var_value_convert import ValueTypeNotSupportedError
from .workflow import Workflow
