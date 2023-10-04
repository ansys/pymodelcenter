"""Defines a function that creates a wrapper from a gRPC element info."""
from typing import TYPE_CHECKING

import ansys.engineeringworkflow.api as aew_api

if TYPE_CHECKING:
    from .engine import Engine
from ansys.api.modelcenter.v0.element_messages_pb2 import ElementType
from ansys.api.modelcenter.v0.workflow_messages_pb2 import ElementInfo


def create_element(info: ElementInfo, engine: "Engine") -> aew_api.IElement:
    """Create an appropriately-typed wrapper given a gRPC element info."""
    import ansys.modelcenter.workflow.grpc_modelcenter.abstract_workflow_element as abstract_elem
    import ansys.modelcenter.workflow.grpc_modelcenter.assembly as assembly_impl
    import ansys.modelcenter.workflow.grpc_modelcenter.component as component_impl
    import ansys.modelcenter.workflow.grpc_modelcenter.create_datapin as create_variable
    import ansys.modelcenter.workflow.grpc_modelcenter.group as group_impl

    if (
        info.type == ElementType.ELEMENT_TYPE_ASSEMBLY
        or info.type == ElementType.ELEMENT_TYPE_DRIVERCOMPONENT
    ):
        return assembly_impl.Assembly(info.id, engine)
    elif info.type == ElementType.ELEMENT_TYPE_COMPONENT:
        return component_impl.Component(info.id, engine)
    elif info.type == ElementType.ELEMENT_TYPE_GROUP:
        return group_impl.Group(info.id, engine)
    elif info.type == ElementType.ELEMENT_TYPE_VARIABLE:
        return create_variable.create_datapin(info.var_type, info.id, engine)
    else:
        # (including ELEMENT_TYPE_UNSPECIFIED)
        return abstract_elem.UnsupportedWorkflowElement(info.id, engine)
