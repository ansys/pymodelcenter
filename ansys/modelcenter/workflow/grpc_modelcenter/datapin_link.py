"""Implementation of DatapinLink."""
import ansys.api.modelcenter.v0.element_messages_pb2 as elem_msg
import ansys.api.modelcenter.v0.grpc_modelcenter_workflow_pb2_grpc as grpc_mcd_workflow
import ansys.api.modelcenter.v0.workflow_messages_pb2 as workflow_msg
from overrides import overrides

import ansys.modelcenter.workflow.api as wfapi

from .grpc_error_interpretation import WRAP_TARGET_NOT_FOUND, interpret_rpc_error


class DatapinLink(wfapi.IDatapinLink):
    """
    A link between datapins in a workflow.

    .. note::
        This class should not be directly instantiated by clients. Get a Workflow object from
        an instantiated Engine, and use it to get a valid instance of this object.
    """

    def __init__(
        self, stub: grpc_mcd_workflow.ModelCenterWorkflowServiceStub, lhs_id: str, rhs: str
    ):
        """
        Construct a new instance.

        Parameters
        ----------
        lhs_id: The left hand side of the link equation.
        rhs: The right hand side of the link equation.
        """
        self._stub = stub
        self._lhs_id = lhs_id
        self._rhs = rhs

    @overrides
    def __eq__(self, other):
        return isinstance(other, DatapinLink) and self.lhs == other.lhs and self.rhs == other.rhs

    @overrides
    def __str__(self):
        return "{LHS: " + self._lhs_id + ", RHS: " + self._rhs + "}"  # pragma: no cover

    @interpret_rpc_error()
    @overrides
    def break_link(self) -> None:
        request = workflow_msg.WorkflowBreakLinkRequest()
        request.target_var.id_string = self._lhs_id
        response: workflow_msg.WorkflowBreakLinkResponse = self._stub.WorkflowBreakLink(request)
        if not response.existed:
            raise ValueError("Target id does not exist.")

    @interpret_rpc_error()
    def _do_suspend_or_resume(self, suspend: bool) -> None:
        request = workflow_msg.WorkflowSuspendOrResumeLinkRequest(
            target_link_lhs=elem_msg.ElementId(id_string=self._lhs_id), suspend=suspend
        )
        self._stub.WorkflowSuspendOrResumeLink(request)

    @overrides
    def suspend(self) -> None:
        self._do_suspend_or_resume(True)

    @overrides
    def resume(self) -> None:
        self._do_suspend_or_resume(False)

    @interpret_rpc_error(WRAP_TARGET_NOT_FOUND)
    @overrides
    def is_suspended(self) -> bool:
        response: workflow_msg.WorkflowLinkSuspension = self._stub.WorkflowGetLinkSuspensionState(
            workflow_msg.WorkflowBreakLinkRequest(
                target_var=elem_msg.ElementId(id_string=self._lhs_id)
            )
        )
        return response.is_suspended

    @property  # type: ignore
    @overrides
    def lhs(self) -> str:
        return self._lhs_id

    @property  # type: ignore
    @overrides
    def rhs(self) -> str:
        return self._rhs
