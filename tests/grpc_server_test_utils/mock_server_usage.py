"""
A dummy test file showing how the mock servers might be used.

Unfortunately, as you will see if you use this method, this approach results in very slow tests.
We would either have to reuse the server between tests and reset the servicers,
or have to accept each test taking more than two full seconds apiece.
I'll leave this here for now so that we can reference this approach if we want to test with an
actual server w/ mock implementation for some reason in the future.
"""
import ansys.api.modelcenter.v0.engine_messages_pb2 as engine_messages
import ansys.api.modelcenter.v0.format_messages_pb2 as format_messages
import ansys.api.modelcenter.v0.grpc_modelcenter_format_pb2_grpc as format_grpc
import ansys.api.modelcenter.v0.grpc_modelcenter_pb2_grpc as engine_grpc

from .mock_engine_server import MockEngineServer
from .mock_format_server import MockFormatServer


class MockComboServer(MockFormatServer, MockEngineServer):
    """
    A class showing that it is possible to simply aggregate multiple mock server types.
    """


def test_mock_format_server():
    """
    Show using one of the mock server types directly.
    """
    with MockFormatServer() as server:
        with server.get_channel() as channel:
            stub = format_grpc.ModelCenterFormatServiceStub(channel)
            response = stub.FormatStringToDouble(
                format_messages.FormatStringRequest(format="", original="")
            )
            assert response.result == 1


def test_combo_server():
    """
    Show using an aggregate combo server.
    """
    with MockComboServer() as server:
        with server.get_channel() as channel:
            format_stub = format_grpc.ModelCenterFormatServiceStub(channel)
            engine_stub = engine_grpc.GRPCModelCenterServiceStub(channel)
            format_response = format_stub.FormatStringToDouble(
                format_messages.FormatStringRequest(format="", original="")
            )
            engine_response = engine_stub.GetEngineInfo(engine_messages.GetServerInfoRequest())
            assert format_response.result == 1
            assert engine_response.version.major == 23
