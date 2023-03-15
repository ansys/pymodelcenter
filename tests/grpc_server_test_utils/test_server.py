import concurrent.futures
from typing import Optional

import grpc


class TestGRPCServer:
    """
    A base class for test GRPC servers.

    When the server is used in a with block, it will start serving on a randomly assigned
    available port. Call get_channel to get a channel that can be used to communicate with
    the server.
    """

    def __init__(self, max_workers: int = 1):
        """
        Construct a new instance.
        """
        self._max_workers = max_workers
        self._server: Optional[grpc.server] = None
        self._port: int = 0

    def _add_servicers(self):
        """
        Add servicers to the server.

        Derivative classes should add their servicers and then call the superclass
        method. Combined with Python multiple inheritance, this allows
        creation of mock server types which can handle requests on multiple servers
        simply by inheriting from several mock server types.
        """
        pass

    def __enter__(self):
        self._server = grpc.server(
            concurrent.futures.ThreadPoolExecutor(max_workers=self._max_workers)
        )
        self._port = self._server.add_insecure_port("127.0.0.1:0")
        self._add_servicers()
        self._server.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._server is not None:
            self._server.stop(grace=0)
            self._server.wait_for_termination()
            self._server = None

    def get_channel(self) -> grpc.Channel:
        """
        Get a channel that can be used to communicate with the server.

        The caller is responsible for opening / closing the returned channel object.
        """
        if self._port == 0:
            raise ValueError(
                "You must enter a with block using this object to get a prebuilt channel."
            )
        else:
            return grpc.insecure_channel(f"localhost:{self._port}")
