"""Implementation of Format."""
from typing import TYPE_CHECKING

from numpy import float64, int64
from overrides import overrides

from ansys.modelcenter.workflow.api import IFormat

if TYPE_CHECKING:
    from .engine import Engine

from ansys.api.modelcenter.v0.format_messages_pb2 import (
    FormatDoubleRequest,
    FormatDoubleResponse,
    FormatIntegerRequest,
    FormatIntegerResponse,
    FormatStringRequest,
    FormatStringResponse,
)
from ansys.api.modelcenter.v0.grpc_modelcenter_format_pb2_grpc import ModelCenterFormatServiceStub

from .grpc_error_interpretation import WRAP_INVALID_ARG, interpret_rpc_error


class Format(IFormat):
    """
    Formatter for converting between strings and values.

    .. note::
        This class should not be directly instantiated by clients. Create an ``Engine``, and use it
        to get a valid instance of this object.
    """

    def __init__(self, fmt: str, engine: "Engine"):
        """
        Initialize a new instance.

        Parameters
        ----------
        fmt : str
            Format string this formatter will use.
        engine : Engine
            ``Engine`` creating this formatter.
        """
        self._format: str = fmt
        if self._format == "":
            self._format = "General"
        self._stub = self._create_client(engine.channel)

    @staticmethod
    def _create_client(grpc_channel) -> ModelCenterFormatServiceStub:
        """Create a client from a gRPC channel."""
        return ModelCenterFormatServiceStub(grpc_channel)

    @property  # type: ignore
    @overrides
    def format(self) -> str:
        return self._format

    @format.setter  # type: ignore
    @overrides
    def format(self, fmt: str) -> None:
        self._format = fmt

    @interpret_rpc_error(WRAP_INVALID_ARG)
    @overrides
    def string_to_integer(self, string: str) -> int64:
        request = FormatStringRequest(format=self._format, original=string)
        response: FormatIntegerResponse = self._stub.FormatStringToInteger(request)
        return response.result

    @interpret_rpc_error(WRAP_INVALID_ARG)
    @overrides
    def string_to_real(self, string: str) -> float64:
        request = FormatStringRequest()
        request.format = self._format
        request.original = string
        response: FormatDoubleResponse = self._stub.FormatStringToDouble(request)
        return float64(response.result)

    @interpret_rpc_error(WRAP_INVALID_ARG)
    @overrides
    def integer_to_string(self, integer: int64) -> str:
        request = FormatIntegerRequest()
        request.format = self._format
        request.original = integer
        response: FormatStringResponse = self._stub.FormatIntegerToString(request)
        return response.result

    @interpret_rpc_error(WRAP_INVALID_ARG)
    @overrides
    def real_to_string(self, real: float64) -> str:
        request = FormatDoubleRequest()
        request.format = self._format
        request.original = real
        response: FormatStringResponse = self._stub.FormatDoubleToString(request)
        return response.result

    @interpret_rpc_error(WRAP_INVALID_ARG)
    @overrides
    def string_to_string(self, string: str) -> str:
        request = FormatStringRequest()
        request.format = self._format
        request.original = string
        response: FormatStringResponse = self._stub.FormatStringToString(request)
        return response.result

    @interpret_rpc_error(WRAP_INVALID_ARG)
    @overrides
    def integer_to_editable_string(self, integer: int64) -> str:
        request = FormatIntegerRequest()
        request.format = self._format
        request.original = integer
        response: FormatStringResponse = self._stub.FormatIntegerToEditString(request)
        return response.result

    @interpret_rpc_error(WRAP_INVALID_ARG)
    @overrides
    def real_to_editable_string(self, real: float64) -> str:
        request = FormatDoubleRequest()
        request.format = self._format
        request.original = real
        response: FormatStringResponse = self._stub.FormatDoubleToEditString(request)
        return response.result
