"""Defines a function that creates a wrapper from a gRPC element info."""
from typing import TYPE_CHECKING

import ansys.engineeringworkflow.api as aew_api

if TYPE_CHECKING:
    from .engine import Engine
from .proto.element_messages_pb2 import ElementType
from .proto.workflow_messages_pb2 import ElementInfo


def create_element(info: ElementInfo, engine: "Engine") -> aew_api.IElement:
    """Create an appropriately-typed wrapper given a gRPC element info."""
    import ansys.modelcenter.workflow.grpc_modelcenter.abstract_workflow_element as abstract_elem
    import ansys.modelcenter.workflow.grpc_modelcenter.assembly as assembly_impl
    import ansys.modelcenter.workflow.grpc_modelcenter.component as component_impl
    import ansys.modelcenter.workflow.grpc_modelcenter.create_datapin as create_variable
    import ansys.modelcenter.workflow.grpc_modelcenter.group as group_impl

    if info.type == ElementType.ELEMTYPE_ASSEMBLY or info.type == ElementType.ELEMTYPE_IFCOMPONENT:
        return assembly_impl.Assembly(info.id, engine)
    elif info.type == ElementType.ELEMTYPE_COMPONENT:
        return component_impl.Component(info.id, engine)
    elif info.type == ElementType.ELEMTYPE_GROUP:
        return group_impl.Group(info.id, engine)
    elif info.type == ElementType.ELEMTYPE_VARIABLE:
        return create_variable.create_datapin(info.var_type, info.id, engine)
    else:
        # (including ELEMTYPE_UNKNOWN)
        return abstract_elem.UnsupportedWorkflowElement(info.id, engine)
