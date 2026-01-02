# Copyright (C) 2022 - 2026 ANSYS, Inc. and/or its affiliates.
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
"""Provides a reusable way to patch client creation on gRPC-based PyModelCenter
classes."""


def monkeypatch_client_creation(
    mpatch_or_context, target_class, mock_client, client_creation_func="_create_client"
):
    """Monkeypatch a test implementation type.

    :param mpatch_or_context: either the monkeypatch object provided by
        pytest, or a monkeypatch context object during the lifespan of
        which the patch will apply.
    :param target_class: the class to monkeypatch. This should be the
        implementation class from grpc_modelcenter that is under test.
        The class should have a method it uses to create a client from a
        gRPC channel that can be replaced.
    :param mock_client: the mock client to return
    :param client_creation_func: the name of the method to patch.
    """
    # Create a lambda that returns the mock client.
    mock_client_create = lambda obj, channel, mock_client=mock_client: mock_client

    # Monkeypatch the target type.
    mpatch_or_context.setattr(target_class, client_creation_func, mock_client_create)
