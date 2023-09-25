"""Contains an abstract base for control statement implementations."""

from abc import ABC
from typing import TYPE_CHECKING, Mapping

from ansys.api.modelcenter.v0.element_messages_pb2 import ElementId
from ansys.api.modelcenter.v0.workflow_messages_pb2 import ElementInfo
import ansys.engineeringworkflow.api as aew_api
from overrides import overrides

import ansys.modelcenter.workflow.api as mc_api
import ansys.modelcenter.workflow.grpc_modelcenter.abstract_assembly_child as aachild

from .abstract_datapin_container import AbstractGRPCDatapinContainer
from .abstract_renamable import AbstractRenamableElement
from .element_wrapper import create_element
from .group import Group
from .grpc_error_interpretation import WRAP_TARGET_NOT_FOUND, interpret_rpc_error

if TYPE_CHECKING:
    from .engine import Engine


class AbstractControlStatement(
    AbstractRenamableElement,
    AbstractGRPCDatapinContainer,
    aachild.AbstractAssemblyChild,
    aew_api.IControlStatement,
    ABC,
):
    """
    An abstract base for control statements (driver components and assemblies).

    .. note::
        This class should not be directly instantiated by clients. Get a Workflow object
        from an instantiated engine, and use it to get valid instances of Assembly,
        Component or DriverComponent.
    """

    def __init__(self, element_id: ElementId, engine: "Engine"):
        """
        Initialize a new instance.

        Parameters
        ----------
        element_id : ElementId
            The id of the .
        engine: Engine
            The engine that created this assembly.
        """
        super(AbstractControlStatement, self).__init__(element_id=element_id, engine=engine)

    @interpret_rpc_error(WRAP_TARGET_NOT_FOUND)
    @overrides
    def get_elements(self) -> Mapping[str, aew_api.IElement]:
        result = self._client.AssemblyGetAssembliesAndComponents(self._element_id)
        one_child_element_info: ElementInfo
        child_elements = [
            create_element(one_child_element_info, self._engine)
            for one_child_element_info in result.elements
        ]
        one_child_element: aew_api.IElement
        return {element.name: element for element in child_elements}

    @overrides
    def _create_group(self, element_id: ElementId) -> mc_api.IGroup:
        return Group(element_id, self._engine)
