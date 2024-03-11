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
"""Defines the function for creating a datapin object.

Creation requres a given datapin type and gRPC information.
"""
from typing import TYPE_CHECKING

from ansys.api.modelcenter.v0.variable_value_messages_pb2 import VariableType
import ansys.tools.variableinterop as atvi

import ansys.modelcenter.workflow.api as mc_api
import ansys.modelcenter.workflow.grpc_modelcenter.boolean_datapin as bool_pin_impl
import ansys.modelcenter.workflow.grpc_modelcenter.file_datapin as file_pin_impl
import ansys.modelcenter.workflow.grpc_modelcenter.integer_datapin as int_pin_impl
import ansys.modelcenter.workflow.grpc_modelcenter.real_datapin as double_pin_impl
import ansys.modelcenter.workflow.grpc_modelcenter.reference_datapin as ref_pin_impl
import ansys.modelcenter.workflow.grpc_modelcenter.string_datapin as string_pin_impl
import ansys.modelcenter.workflow.grpc_modelcenter.unsupported_type_datapin as unsupported_pin_impl

from .var_value_convert import grpc_type_enum_to_interop_type

if TYPE_CHECKING:
    from .engine import Engine

from ansys.api.modelcenter.v0.element_messages_pb2 import ElementId


class _DatapinCreationVisitor(atvi.IVariableTypePseudoVisitor[mc_api.IDatapin]):
    def __init__(self, element_id: ElementId, engine: "Engine"):
        self._element_id = element_id
        self._engine = engine

    def visit_unknown(self) -> mc_api.IDatapin:
        return unsupported_pin_impl.UnsupportedTypeDatapin(
            element_id=self._element_id, engine=self._engine
        )

    def visit_int(self) -> mc_api.IDatapin:
        return int_pin_impl.IntegerDatapin(element_id=self._element_id, engine=self._engine)

    def visit_real(self) -> mc_api.IDatapin:
        return double_pin_impl.RealDatapin(element_id=self._element_id, engine=self._engine)

    def visit_boolean(self) -> mc_api.IDatapin:
        return bool_pin_impl.BooleanDatapin(element_id=self._element_id, engine=self._engine)

    def visit_string(self) -> mc_api.IDatapin:
        return string_pin_impl.StringDatapin(element_id=self._element_id, engine=self._engine)

    def visit_file(self) -> mc_api.IDatapin:
        return file_pin_impl.FileDatapin(element_id=self._element_id, engine=self._engine)

    def visit_int_array(self) -> mc_api.IDatapin:
        return int_pin_impl.IntegerArrayDatapin(element_id=self._element_id, engine=self._engine)

    def visit_real_array(self) -> mc_api.IDatapin:
        return double_pin_impl.RealArrayDatapin(element_id=self._element_id, engine=self._engine)

    def visit_bool_array(self) -> mc_api.IDatapin:
        return bool_pin_impl.BooleanArrayDatapin(element_id=self._element_id, engine=self._engine)

    def visit_string_array(self) -> mc_api.IDatapin:
        return string_pin_impl.StringArrayDatapin(element_id=self._element_id, engine=self._engine)

    def visit_file_array(self) -> mc_api.IDatapin:
        return file_pin_impl.FileArrayDatapin(element_id=self._element_id, engine=self._engine)


def create_datapin(
    var_value_type: VariableType, element_id: ElementId, engine: "Engine"
) -> mc_api.IDatapin:
    """Create a ``mc_api.IDatapin`` object using the given parameters.

    Parameters
    ----------
    var_value_type : VariableType
        Variable type for the datapin.
    element_id : ElementId
        ID of the particular datapin.
    engine : Engine
        Engine that created the datapin
    """
    if var_value_type == VariableType.VARIABLE_TYPE_REFERENCE:
        return ref_pin_impl.ReferenceDatapin(element_id=element_id, engine=engine)
    elif var_value_type == VariableType.VARIABLE_TYPE_REFERENCE_ARRAY:
        return ref_pin_impl.ReferenceArrayDatapin(element_id=element_id, engine=engine)
    else:
        atvi_type: atvi.VariableType = grpc_type_enum_to_interop_type(var_value_type)
        return atvi.vartype_accept(_DatapinCreationVisitor(element_id, engine), atvi_type)
