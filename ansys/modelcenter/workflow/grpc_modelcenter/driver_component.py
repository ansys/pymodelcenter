"""Contains a gRPC-backed implementation of IDriverComponent."""
from typing import TYPE_CHECKING

from .abstract_control_statement import AbstractControlStatement
from .component import Component

if TYPE_CHECKING:
    from .engine import Engine

from ansys.api.modelcenter.v0.element_messages_pb2 import ElementId
import ansys.modelcenter.workflow.api as mc_api


class DriverComponent(
    Component,
    AbstractControlStatement,
    mc_api.IDriverComponent,
):
    """
    Defines a driver component in a workflow.

    In process-mode workflows, driver components can contain children.
    In data-mode workflows, driver components should still be instantiated with an instance
    of this class, but the method to get child elements will simply return an empty collection.

    .. note::
    This class should not be directly instantiated by clients. Get a ``Workflow`` object
    from an instantiated engine, and use it to get valid instances of Assembly,
    Component or DriverComponent.
    """

    def __init__(self, element_id: ElementId, engine: "Engine"):
        """
        Initialize a new instance.

        Parameters
        ----------
        element_id : ElementId
            ID of the component.
        engine : Engine
            ``Engine`` that created this component.
        """
        super(DriverComponent, self).__init__(element_id=element_id, engine=engine)
