"""Defines a function that's used to create a variable object given a type and gRPC info."""

import ansys.common.variableinterop as acvi
from ansys.common.variableinterop.ivariable_type_pseudovisitor import T
import grpc

import ansys.modelcenter.workflow.api as mc_api
import ansys.modelcenter.workflow.grpc_modelcenter.boolean_datapin as bool_pin_impl
import ansys.modelcenter.workflow.grpc_modelcenter.integer_datapin as int_pin_impl
import ansys.modelcenter.workflow.grpc_modelcenter.real_datapin as double_pin_impl
import ansys.modelcenter.workflow.grpc_modelcenter.string_datapin as string_pin_impl
import ansys.modelcenter.workflow.grpc_modelcenter.unsupported_type_datapin as unsupported_pin_impl

from .proto.element_messages_pb2 import ElementId


class _DatapinCreationVisitor(acvi.IVariableTypePseudoVisitor[mc_api.IDatapin]):
    def __init__(self, element_id: ElementId, channel: grpc.Channel):
        self._element_id = element_id
        self._channel = channel

    def visit_unknown(self) -> T:
        return unsupported_pin_impl.UnsupportedTypeDatapin(
            element_id=self._element_id, channel=self._channel
        )

    def visit_int(self) -> T:
        return int_pin_impl.IntegerDatapin(element_id=self._element_id, channel=self._channel)

    def visit_real(self) -> T:
        return double_pin_impl.RealDatapin(element_id=self._element_id, channel=self._channel)

    def visit_boolean(self) -> T:
        return bool_pin_impl.BooleanDatapin(element_id=self._element_id, channel=self._channel)

    def visit_string(self) -> T:
        return string_pin_impl.StringDatapin(element_id=self._element_id, channel=self._channel)

    def visit_file(self) -> T:
        return unsupported_pin_impl.UnsupportedTypeDatapin(
            element_id=self._element_id, channel=self._channel
        )

    def visit_int_array(self) -> T:
        return int_pin_impl.IntegerArray(element_id=self._element_id, channel=self._channel)

    def visit_real_array(self) -> T:
        return double_pin_impl.RealArrayDatapin(element_id=self._element_id, channel=self._channel)

    def visit_bool_array(self) -> T:
        return bool_pin_impl.BooleanArrayDatapin(element_id=self._element_id, channel=self._channel)

    def visit_string_array(self) -> T:
        return string_pin_impl.StringArrayDatapin(
            element_id=self._element_id, channel=self._channel
        )

    def visit_file_array(self) -> T:
        return unsupported_pin_impl.UnsupportedTypeDatapin(
            element_id=self._element_id, channel=self._channel
        )


def create_datapin(
    var_value_type: acvi.VariableType, element_id: ElementId, channel: grpc.Channel
) -> mc_api.IDatapin:
    """
    Given a datapin type from ACVI and an element ID and channel, create a datapin wrapper object.

    Parameters
    ----------
    var_value_type : acvi.VariableType
        The variable type that the variable should be.
    element_id : the element ID of the particular variable.
    channel : the gRPC channel
    """
    return acvi.vartype_accept(_DatapinCreationVisitor(element_id, channel), var_value_type)
