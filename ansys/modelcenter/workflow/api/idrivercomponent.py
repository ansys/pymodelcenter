"""Contains a definition for an interface for driver components."""
import ansys.engineeringworkflow.api as aew_api
import ansys.modelcenter.workflow.api.icomponent as component


class IDriverComponent(
    component.IComponent,
    aew_api.IControlStatement,
):
    """
    Represents a driver component within a workflow.

    For process-mode workflows, driver components will have children.
    Driver components will still be represented by instances of this interface
    even if the workflow is a data-dependency workflow and the component in question
    has no children (get_elements will return an empty collection).
    """
