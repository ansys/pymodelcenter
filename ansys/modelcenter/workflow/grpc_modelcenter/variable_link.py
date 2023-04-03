"""Implementation of VariableLink."""
from overrides import overrides

import ansys.modelcenter.workflow.api as wfapi
import ansys.modelcenter.workflow.grpc_modelcenter.proto.grpc_modelcenter_workflow_pb2_grpc as grpc_mcd_workflow  # noqa: E501
import ansys.modelcenter.workflow.grpc_modelcenter.proto.workflow_messages_pb2 as workflow_msg


class VariableLink(wfapi.IVariableLink):
    """GRPC implementation of IVariableLink."""

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
    def __str__(self):
        return "{LHS: " + self._lhs_id + ", RHS: " + self._rhs + "}"

    @overrides
    def suspend_link(self) -> None:
        raise NotImplementedError()

    @overrides
    def resume_link(self) -> None:
        raise NotImplementedError()

    @overrides
    def break_link(self) -> None:
        request = workflow_msg.WorkflowBreakLinkRequest()
        request.target_var.id_string = self._lhs_id
        response: workflow_msg.WorkflowBreakLinkResponse = self._stub.WorkflowBreakLink(request)
        if not response.existed:
            raise ValueError("Target id does not exist.")

    @property  # type: ignore
    @overrides
    def lhs(self) -> str:
        return self._lhs_id

    @property  # type: ignore
    @overrides
    def rhs(self) -> str:
        return self._rhs
