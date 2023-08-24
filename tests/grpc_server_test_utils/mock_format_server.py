import ansys.api.modelcenter.v0.format_messages_pb2 as format_messages  # noqa: 501
import ansys.api.modelcenter.v0.grpc_modelcenter_format_pb2_grpc as format_grpc  # noqa: 501

from .test_server import TestGRPCServer


class MockFormatServicer(format_grpc.ModelCenterFormatServiceServicer):
    def FormatStringToInteger(self, request, context):
        return format_messages.FormatIntegerResponse(result=1)

    def FormatStringToDouble(self, request, context):
        return format_messages.FormatDoubleResponse(result=1.0)


class MockFormatServer(TestGRPCServer):
    def __init__(self, max_workers: int = 1):
        super(MockFormatServer, self).__init__(max_workers=max_workers)
        self._format_servicer = MockFormatServicer()

    def get_format_servicer(self) -> MockFormatServicer:
        return self._format_servicer

    def _add_servicers(self):
        format_grpc.add_ModelCenterFormatServiceServicer_to_server(
            servicer=self._format_servicer, server=self._server
        )
        super(MockFormatServer, self)._add_servicers()
