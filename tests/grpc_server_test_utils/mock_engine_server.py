# Copyright (C) 2022 - 2025 ANSYS, Inc. and/or its affiliates.
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

import ansys.api.modelcenter.v0.engine_messages_pb2 as engine_messages
import ansys.api.modelcenter.v0.grpc_modelcenter_pb2_grpc as engine_grpc

from .test_server import TestGRPCServer


class MockEngineServicer(engine_grpc.GRPCModelCenterServiceServicer):
    """A mock servicer for the MCD engine service."""

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
    """A mock server for servicing engine requests."""

    def __init__(self, max_workers: int = 1):
        super(MockEngineServer, self).__init__(max_workers=max_workers)
        self._engine_servicer = MockEngineServicer()

    def get_engine_servicer(self) -> MockEngineServicer:
        """Access the mock servicer handling engine requests."""
        return self._engine_servicer

    def _add_servicers(self):
        """Add the engine servicer."""
        engine_grpc.add_GRPCModelCenterServiceServicer_to_server(
            servicer=self._engine_servicer, server=self._server
        )
        super(MockEngineServer, self)._add_servicers()
