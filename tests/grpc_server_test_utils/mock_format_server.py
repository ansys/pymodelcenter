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

import ansys.api.modelcenter.v0.format_messages_pb2 as format_messages
import ansys.api.modelcenter.v0.grpc_modelcenter_format_pb2_grpc as format_grpc

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
