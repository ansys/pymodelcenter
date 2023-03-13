"""Implementation of Format."""
import grpc
from numpy import float64, int64
from overrides import overrides

from ansys.modelcenter.workflow.api.format import Format as IFormat

from .proto.format_messages_pb2 import (
    FormatFromDoubleRequest,
    FormatFromIntegerRequest,
    FormatFromStringRequest,
    FormatToDoubleResponse,
    FormatToIntegerResponse,
    FormatToStringResponse,
)
from .proto.grpc_modelcenter_format_pb2_grpc import ModelCenterFormatServiceStub


class Format(IFormat):
    """GRPC implementation of IFormat."""

    def __init__(self, fmt: str):
        """Initialize."""
        self._format: str = fmt
        # (MPP): Unsure if we should pass this in from Engine
        self._channel = grpc.insecure_channel("localhost:50051")
        self._stub = ModelCenterFormatServiceStub(self._channel)

    @property  # type: ignore
    @overrides
    def format(self) -> str:
        return self._format

    @format.setter  # type: ignore
    @overrides
    def format(self, fmt: str) -> None:
        self._format = fmt

    @overrides
    def string_to_integer(self, string: str) -> int64:
        request = FormatFromStringRequest(format=self._format, original=string)
        response: FormatToIntegerResponse = self._stub.FormatStringToInteger(request)
        return response.result

    @overrides
    def string_to_real(self, string: str) -> float64:
        request = FormatFromStringRequest()
        request.format = self._format
        request.original = string
        response: FormatToDoubleResponse = self._stub.FormatStringToDouble(request)
        return response.result

    @overrides
    def integer_to_string(self, integer: int64) -> str:
        request = FormatFromIntegerRequest()
        request.format = self._format
        request.original = integer
        response: FormatToStringResponse = self._stub.FormatIntegerToString(request)
        return response.result

    @overrides
    def real_to_string(self, real: float64) -> str:
        request = FormatFromDoubleRequest()
        request.format = self._format
        request.original = real
        response: FormatToStringResponse = self._stub.FormatDoubleToString(request)
        return response.result

    @overrides
    def string_to_string(self, string: str) -> str:
        request = FormatFromStringRequest()
        request.format = self._format
        request.original = string
        response: FormatToStringResponse = self._stub.FormatStringToString(request)
        return response.result

    @overrides
    def integer_to_editable_string(self, integer: int64) -> str:
        request = FormatFromIntegerRequest()
        request.format = self._format
        request.original = integer
        response: FormatToStringResponse = self._stub.FormatIntegerToEditString(request)
        return response.result

    @overrides
    def real_to_editable_string(self, real: float64) -> str:
        request = FormatFromDoubleRequest()
        request.format = self._format
        request.original = real
        response: FormatToStringResponse = self._stub.FormatDoubleToEditString(request)
        return response.result
