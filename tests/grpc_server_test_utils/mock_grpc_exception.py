import grpc


class MockGrpcError(grpc.RpcError):
    def __init__(self, code: grpc.StatusCode, details: str):
        self._code: grpc.StatusCode = code
        self._details: str = details

    def code(self) -> grpc.StatusCode:
        return self._code

    def details(self) -> str:
        return self._details
