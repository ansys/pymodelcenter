"""Module containing methods to query the MCD GRPC server."""


from enum import Enum

import grpc

import ansys.modelcenter.workflow.grpc_modelcenter.proto.modelcenter_pb2 as mcd
import ansys.modelcenter.workflow.grpc_modelcenter.proto.modelcenter_pb2_grpc as mcd_grpc


class WorkflowType(Enum):
    """Type of workflow."""

    DATA = 0
    PROCESS = 1


def get_engine_info(target: str = "localhost:50051") -> mcd.EngineInfoResponse:
    """
    GRPC query to GetEngineInfo().

    Parameters
    ----------
    target : str
        Target for the query; string of the form HOST_ADDRESS:PORT.
        Defaults to "localhost:50051".

    Returns
    -------
    EngineInfoResponse
        Result of the query.
    """
    with grpc.insecure_channel(target) as channel:
        stub = mcd_grpc.EngineStub(channel)
        return stub.GetEngineInfo()


def shutdown(target: str = "localhost:50051") -> None:
    """
    GRPC query to Shutdown().

    Parameters
    ----------
    target : str
        Target for the query; string of the form HOST_ADDRESS:PORT.
        Defaults to "localhost:50051".
    """
    with grpc.insecure_channel(target) as channel:
        stub = mcd_grpc.EngineStub(channel)
        stub.Shutdown()


def load_workflow(path: str, target: str = "localhost:50051") -> None:
    """
    GRPC query to LoadWorkflow().

    Parameters
    ----------
    path : str
        Path to the workflow to be opened.

    target : str
        Target for the query; string of the form HOST_ADDRESS:PORT.
        Defaults to "localhost:50051".
    """
    request = mcd.LoadWorkflowRequest()
    request.path = path

    with grpc.insecure_channel(target) as channel:
        stub = mcd_grpc.EngineStub(channel)
        stub.LoadWorkflow(request)


def new_workflow(name: str, type_: WorkflowType, target: str = "localhost:50051") -> None:
    """
    GRPC query to NewWorkflow().

    Parameters
    ----------
    name : str
        Name of new workflow to create.

    type_ : WorkflowType
        Type of workflow to create.

    target : str
        Target for the query; string of the form HOST_ADDRESS:PORT.
        Defaults to "localhost:50051".
    """
    request = mcd.NewWorkflowRequest()
    request.name = name
    request.type = type_

    with grpc.insecure_channel(target) as channel:
        stub = mcd_grpc.EngineStub(channel)
        stub.NewWorkflow(request)
