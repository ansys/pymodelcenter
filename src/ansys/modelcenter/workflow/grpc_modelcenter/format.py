# Copyright (C) 2022 - 2024 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
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
    """Formatter for converting between strings and values.

    .. note::
        This class should not be directly instantiated by clients. Create
        an ``Engine`` instance, and use it to get a valid instance of this object.
    """

    def __init__(self, fmt: str, engine: "Engine"):
        """Initialize a new instance.

        Parameters
        ----------
        fmt : str
            Format string that the formatter is to use.
        engine : Engine
            Engine to use to create the formatter.
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
