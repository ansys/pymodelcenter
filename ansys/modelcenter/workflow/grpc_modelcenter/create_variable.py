"""Defines a function that's used to create a variable object given a type and gRPC info."""

import ansys.common.variableinterop as acvi
from ansys.common.variableinterop.ivariable_type_pseudovisitor import T
import grpc

import ansys.modelcenter.workflow.api as mc_api

from .boolean_variable import BooleanArray, BooleanVariable
from .double_variable import DoubleArray, DoubleVariable
from .integer_variable import IntegerArray, IntegerVariable
from .proto.element_messages_pb2 import ElementId
from .string_variable import StringArray, StringVariable
from .unsupported_var import UnsupportedTypeVariable


class _VariableCreationVisitor(acvi.IVariableTypePseudoVisitor[mc_api.IVariable]):
    def __init__(self, element_id: ElementId, channel: grpc.Channel):
        self._element_id = element_id
        self._channel = channel

    def visit_unknown(self) -> T:
        return UnsupportedTypeVariable(element_id=self._element_id, channel=self._channel)

    def visit_int(self) -> T:
        return IntegerVariable(element_id=self._element_id, channel=self._channel)

    def visit_real(self) -> T:
        return DoubleVariable(element_id=self._element_id, channel=self._channel)

    def visit_boolean(self) -> T:
        return BooleanVariable(element_id=self._element_id, channel=self._channel)

    def visit_string(self) -> T:
        return StringVariable(element_id=self._element_id, channel=self._channel)

    def visit_file(self) -> T:
        return UnsupportedTypeVariable(element_id=self._element_id, channel=self._channel)

    def visit_int_array(self) -> T:
        return IntegerArray(element_id=self._element_id, channel=self._channel)

    def visit_real_array(self) -> T:
        return DoubleArray(element_id=self._element_id, channel=self._channel)

    def visit_bool_array(self) -> T:
        return BooleanArray(element_id=self._element_id, channel=self._channel)

    def visit_string_array(self) -> T:
        return StringArray(element_id=self._element_id, channel=self._channel)

    def visit_file_array(self) -> T:
        return UnsupportedTypeVariable(element_id=self._element_id, channel=self._channel)


def create_variable(
    var_value_type: acvi.VariableType, element_id: ElementId, channel: grpc.Channel
) -> mc_api.IVariable:
    """
    Given a variable type from ACVI and an element ID and channel, make an appropriate variable.

    Parameters
    ----------
    var_value_type : acvi.VariableType
        The variable type that the variable should be.
    element_id : the element ID of the particular variable.
    channel : the gRPC channel
    """
    return acvi.vartype_accept(_VariableCreationVisitor(element_id, channel), var_value_type)
