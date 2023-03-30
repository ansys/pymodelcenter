"""Defines a function that's used to create a variable object given a type and gRPC info."""

import ansys.common.variableinterop as acvi
import grpc

import ansys.modelcenter.workflow.api as mc_api

from .proto.element_messages_pb2 import ElementId
from .unsupported_var import UnsupportedTypeVariable


def create_variable(
    var_value_type: acvi.VariableType, element_id=ElementId, channel=grpc.Channel
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
    return UnsupportedTypeVariable(element_id, channel)
