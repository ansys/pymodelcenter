import ansys.modelcenter.workflow.grpc_modelcenter.proto.engine_messages_pb2 as engine_messages  # noqa: 501
import ansys.modelcenter.workflow.grpc_modelcenter.proto.grpc_modelcenter_pb2_grpc as engine_grpc  # noqa: 501

from .test_server import TestGRPCServer


class MockEngineServicer(engine_grpc.GRPCModelCenterServiceServicer):
    """
    A mock servicer for the MCD engine service.
    """

    def GetEngineInfo(self, request, context):
        response = engine_messages.GetServerInfoResponse(
            is_release=False,
            build_type="test",
            server_type="mock",
            directory_path="/this/is/a/fake/path",
            executable_path="nonexistent.exe",
        )
        response.version.major = 23
        response.version.minor = 2
        response.version.patch = 0
        response.version.revision = 1
        return response


class MockEngineServer(TestGRPCServer):
    """
    A mock server for servicing engine requests.
    """

    def __init__(self, max_workers: int = 1):
        super(MockEngineServer, self).__init__(max_workers=max_workers)
        self._engine_servicer = MockEngineServicer()

    def get_engine_servicer(self) -> MockEngineServicer:
        """
        Access the mock servicer handling engine requests.
        """
        return self._engine_servicer

    def _add_servicers(self):
        """
        Add the engine servicer.
        """
        engine_grpc.add_GRPCModelCenterServiceServicer_to_server(
            servicer=self._engine_servicer, server=self._server
        )
        super(MockEngineServer, self)._add_servicers()
