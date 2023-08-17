"""Demonstrates the use of monkeypatch_client_creation."""
import ansys.api.modelcenter.v0.engine_messages_pb2 as engine_messages
import ansys.api.modelcenter.v0.grpc_modelcenter_pb2_grpc as engine_grpc
import grpc

from .client_creation_monkeypatch import monkeypatch_client_creation
from .mock_engine_server import MockEngineServer


class ExamplePyModelCenterImplementationObject:
    """A stand-in for an actual implementation type from grpc_modelcenter."""

    def _create_client(self, grpc_channel) -> engine_grpc.GRPCModelCenterServiceStub:
        """
        Create a client from a grpc channel.

        If this test approach is to be used, each implementation class will need a method
        like this that can be patched out. As a suggested convention, it should be an instance
        method that takes a channel and returns a client.
        """
        return engine_grpc.GRPCModelCenterServiceStub(grpc_channel)

    def __init__(self, object_id, grpc_channel):
        """
        The stand-in's constructor.
        """

        # Typical implementation objects will store an ID to what ModelCenter object
        # they're referencing.
        self._id = object_id

        # This is the call that the monkeypatch will impact.
        self._client = self._create_client(grpc_channel)

    def get_version_major(self):
        """
        A stand-in for some API method that this hypothetical class is implementing.
        """

        # Note that under this testing approach, the actual business logic methods are untouched.
        result = self._client.GetEngineInfo(engine_messages.GetServerInfoRequest())
        return result.version.major


class ExampleMockEngineStub:
    """
    A stand-in for a mock gRPC client.

    Under this testing approach, when writing tests for a class, you could create a mock
    class like this to replace the gRPC client in the tested class.
    """

    def __init__(self, mock_info_response):
        self._mock_info_response = mock_info_response

    def GetEngineInfo(self, request):
        """
        A replacement for the actual client's GetEngineInfo method.
        """
        return self._mock_info_response


def test_example_impl_object_real():
    """
    Show that the example object can be tested using a real gRPC server with a mock servicer.

    The test will run slowly, but this requires absolutely no modification to the tested type.
    """
    with MockEngineServer() as server:
        with server.get_channel() as channel:
            example_sut = ExamplePyModelCenterImplementationObject("some_id", channel)
            assert example_sut.get_version_major() == 23


def test_example_impl_object_fake(monkeypatch):
    """
    Demonstrate that the example object can be tested quickly by monkeypatching client creation.
    """
    # Set up the mock client object:
    mock_response = engine_messages.GetServerInfoResponse()
    mock_response.version.major = 47
    mock_client = ExampleMockEngineStub(mock_response)

    # Monkeypatch the tested type (NOT the tested object) so that client creation is replaced.
    monkeypatch_client_creation(monkeypatch, ExamplePyModelCenterImplementationObject, mock_client)
    # Note that the patch only affects this test.
    with grpc.insecure_channel("localhost:5001") as channel_not_actually_used:
        example_sut = ExamplePyModelCenterImplementationObject("some_id", channel_not_actually_used)
        assert example_sut.get_version_major() == 47


def test_zzz_example_impl_object_real():
    """
    A test with a name to cause pytest to run it AFTER the monkeypatch version.

    This shows that the monkeypatch version is not impacted.
    """
    with MockEngineServer() as server:
        with server.get_channel() as channel:
            example_sut = ExamplePyModelCenterImplementationObject("some_id", channel)
            assert example_sut.get_version_major() == 23
