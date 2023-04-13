"""Defines a function that creates a wrapper from a gRPC element info."""
import ansys.engineeringworkflow.api as aew_api
import grpc

from .proto.element_messages_pb2 import ElementType
from .proto.workflow_messages_pb2 import ElementInfo


def create_element(info: ElementInfo, channel: grpc.Channel) -> aew_api.IElement:
    """Create an appropriately-typed wrapper given a gRPC element info."""
    import ansys.modelcenter.workflow.grpc_modelcenter.abstract_workflow_element as abstract_elem
    import ansys.modelcenter.workflow.grpc_modelcenter.assembly as assembly_impl
    import ansys.modelcenter.workflow.grpc_modelcenter.component as component_impl
    import ansys.modelcenter.workflow.grpc_modelcenter.create_variable as create_variable
    import ansys.modelcenter.workflow.grpc_modelcenter.group as group_impl
    import ansys.modelcenter.workflow.grpc_modelcenter.var_value_convert as var_value_convert

    if info.type == ElementType.ELEMTYPE_ASSEMBLY or info.type == ElementType.ELEMTYPE_IFCOMPONENT:
        return assembly_impl.Assembly(info.id, channel)
    elif info.type == ElementType.ELEMTYPE_COMPONENT:
        return component_impl.Component(info.id, channel)
    elif info.type == ElementType.ELEMTYPE_GROUP:
        return group_impl.Group(info.id, channel)
    elif info.type == ElementType.ELEMTYPE_VARIABLE:
        return create_variable.create_variable(
            var_value_convert.grpc_type_enum_to_interop_type(info.var_type), info.id, channel
        )
    else:
        # (including ELEMTYPE_UNKNOWN)
        return abstract_elem.UnsupportedWorkflowElement(info.id, channel)
