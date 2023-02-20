"""
Module containing methods to query the MCD GRPC server.
"""


import grpc
from ansys.modelcenter.workflow.grpc_modelcenter.proto.modelcenter_pb2_grpc import *  # type: ignore
from ansys.modelcenter.workflow.grpc_modelcenter.proto.modelcenter_pb2 import *  # type: ignore


def get_engine_info(target: str = "localhost:50051") -> EngineInfoResponse:
    """
    GRPC query to GetEngineInfo().

    Parameters
    ----------
    target : str
        Target for the query; string of the form HOST_ADDRESS:PORT

    Returns
    -------
    EngineInfoResponse
        Result of the query.
    """
    channel = grpc.insecure_channel(target)
    stub = EngineStub(channel)
    return stub.GetEngineInfo()
