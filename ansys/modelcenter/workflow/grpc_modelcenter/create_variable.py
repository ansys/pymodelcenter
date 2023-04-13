"""Defines a function that's used to create a variable object given a type and gRPC info."""

import ansys.common.variableinterop as acvi
from ansys.common.variableinterop.ivariable_type_pseudovisitor import T
import grpc

import ansys.modelcenter.workflow.api as mc_api
import ansys.modelcenter.workflow.grpc_modelcenter.boolean_variable as bool_var_impl
import ansys.modelcenter.workflow.grpc_modelcenter.double_variable as double_var_impl
import ansys.modelcenter.workflow.grpc_modelcenter.integer_variable as int_var_impl
import ansys.modelcenter.workflow.grpc_modelcenter.string_variable as string_var_impl
import ansys.modelcenter.workflow.grpc_modelcenter.unsupported_var as unsupported_var_impl

from .proto.element_messages_pb2 import ElementId


class _VariableCreationVisitor(acvi.IVariableTypePseudoVisitor[mc_api.IVariable]):
    def __init__(self, element_id: ElementId, channel: grpc.Channel):
        self._element_id = element_id
        self._channel = channel

    def visit_unknown(self) -> T:
        return unsupported_var_impl.UnsupportedTypeVariable(
            element_id=self._element_id, channel=self._channel
        )

    def visit_int(self) -> T:
        return int_var_impl.IntegerVariable(element_id=self._element_id, channel=self._channel)

    def visit_real(self) -> T:
        return double_var_impl.RealVariable(element_id=self._element_id, channel=self._channel)

    def visit_boolean(self) -> T:
        return bool_var_impl.BooleanVariable(element_id=self._element_id, channel=self._channel)

    def visit_string(self) -> T:
        return string_var_impl.StringVariable(element_id=self._element_id, channel=self._channel)

    def visit_file(self) -> T:
        return unsupported_var_impl.UnsupportedTypeVariable(
            element_id=self._element_id, channel=self._channel
        )

    def visit_int_array(self) -> T:
        return int_var_impl.IntegerArray(element_id=self._element_id, channel=self._channel)

    def visit_real_array(self) -> T:
        return double_var_impl.RealArrayVariable(element_id=self._element_id, channel=self._channel)

    def visit_bool_array(self) -> T:
        return bool_var_impl.BooleanArrayVariable(
            element_id=self._element_id, channel=self._channel
        )

    def visit_string_array(self) -> T:
        return string_var_impl.StringArrayVariable(
            element_id=self._element_id, channel=self._channel
        )

    def visit_file_array(self) -> T:
        return unsupported_var_impl.UnsupportedTypeVariable(
            element_id=self._element_id, channel=self._channel
        )


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
