"""Defines a function that's used to create a variable object given a type and gRPC info."""
from typing import TYPE_CHECKING

import ansys.tools.variableinterop as atvi

import ansys.modelcenter.workflow.api as mc_api
import ansys.modelcenter.workflow.grpc_modelcenter.boolean_datapin as bool_pin_impl
import ansys.modelcenter.workflow.grpc_modelcenter.integer_datapin as int_pin_impl
import ansys.modelcenter.workflow.grpc_modelcenter.real_datapin as double_pin_impl
import ansys.modelcenter.workflow.grpc_modelcenter.string_datapin as string_pin_impl
import ansys.modelcenter.workflow.grpc_modelcenter.unsupported_type_datapin as unsupported_pin_impl

if TYPE_CHECKING:
    from .engine import Engine
from .proto.element_messages_pb2 import ElementId


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
        return unsupported_pin_impl.UnsupportedTypeDatapin(
            element_id=self._element_id, engine=self._engine
        )

    def visit_int_array(self) -> mc_api.IDatapin:
        return int_pin_impl.IntegerArrayDatapin(element_id=self._element_id, engine=self._engine)

    def visit_real_array(self) -> mc_api.IDatapin:
        return double_pin_impl.RealArrayDatapin(element_id=self._element_id, engine=self._engine)

    def visit_bool_array(self) -> mc_api.IDatapin:
        return bool_pin_impl.BooleanArrayDatapin(element_id=self._element_id, engine=self._engine)

    def visit_string_array(self) -> mc_api.IDatapin:
        return string_pin_impl.StringArrayDatapin(element_id=self._element_id, engine=self._engine)

    def visit_file_array(self) -> mc_api.IDatapin:
        return unsupported_pin_impl.UnsupportedTypeDatapin(
            element_id=self._element_id, engine=self._engine
        )


def create_datapin(
    var_value_type: atvi.VariableType, element_id: ElementId, engine: "Engine"
) -> mc_api.IDatapin:
    """
    Given a datapin type from ATVI and an element ID and Engine, create a datapin wrapper object.

    Parameters
    ----------
    var_value_type : atvi.VariableType
        The variable type that the variable should be.
    element_id : ElementId
        The element ID of the particular variable.
    engine : Engine
        The Engine that created this datapin.
    """
    return atvi.vartype_accept(_DatapinCreationVisitor(element_id, engine), var_value_type)
