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
"""Defines the engine."""
from os import PathLike
from string import Template
from threading import Condition, Thread
from typing import Collection, Dict, List, Mapping, Optional, Union

import ansys.api.modelcenter.v0.engine_messages_pb2 as eng_msg
from ansys.api.modelcenter.v0.grpc_modelcenter_pb2_grpc import GRPCModelCenterServiceStub
from ansys.engineeringworkflow.api import WorkflowEngineInfo
import ansys.platform.instancemanagement as pypim
from ansys.tools.common import cyberchannel
import grpc
import numpy
from overrides import overrides

from ansys.modelcenter.workflow.api import IEngine, WorkflowType

from .format import Format
from .grpc_error_interpretation import WRAP_INVALID_ARG, interpret_rpc_error
from .mcd_process import MCDProcess
from .workflow import Workflow


def _heartbeat_loop(condition: Condition, address: str, engine, interval: numpy.uint) -> None:
    """Runs a loop that sends heartbeat messages to the server at regular
    intervals."""
    # should use Condition to perform timing AND decide whether or not to bail,
    # allows immediate leaving while still joining the thread
    # should keep going if HeartbeatRequest fails for a reason besides UNAVAILABLE
    channel = grpc.insecure_channel(address)
    stub = engine._create_client(channel)
    should_continue_heartbeating: bool = not engine.is_closed
    while should_continue_heartbeating:
        request = eng_msg.HeartbeatRequest()
        stub.Heartbeat(request)
        # sleep for a little less than the heartbeat interval
        with condition:
            condition.wait(max(0, (interval * 0.95) / 1000))
        should_continue_heartbeating = not engine.is_closed


class WorkflowAlreadyLoadedError(Exception):
    """Raised to indicate that a workflow is already loaded.

    This error may be raised if the underlying ModelCenter engine only
    supports a single workflow loaded at a time.
    """

    ...


class Engine(IEngine):
    """Provides the gRPC implementation of IEngine."""

    def __init__(
        self,
        is_run_only: bool = False,
        force_local: bool = False,
        heartbeat_interval: numpy.uint = 30000,
        allowed_heartbeat_misses: numpy.uint = 3,
    ):
        """Initialize an instance.

        Parameters
        ----------
        is_run_only : bool
            Whether to start ModelCenter in run-only mode. The default is ``False``.
        force_local : bool
            Whether to force ModelCenter to start on the local machine, even if
            `PyPIM <https://github.com/ansys/pypim>`_ is configured. The default
            is ``False``.
        heartbeat_interval : numpy.uint
            Number of milliseconds within which a heartbeat call must be made before the server
            considers a heartbeat signal to have been missed.
        allowed_heartbeat_misses : numpy.uint
            Number of heartbeat misses allowed before the server terminates.
        """
        self._is_closed = False
        self._is_run_only: bool = is_run_only
        self._heartbeat_interval: numpy.uint = heartbeat_interval
        self._allowed_heartbeat_misses: numpy.uint = allowed_heartbeat_misses
        self._heartbeat_thread: Optional[Thread] = None
        self._heartbeat_condition: Optional[Condition] = None
        self._instance: Optional[pypim.Instance] = None
        self._process: Optional[MCDProcess] = None
        self._channel: Optional[grpc.Channel] = None
        self._launch_modelcenter(force_local)
        self._stub = self._create_client(self._channel)
        self._workflow_id: Optional[str] = None

    def __enter__(self):
        """Initialization when created in a 'with' statement."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Clean up when leaving a 'with' block."""
        self.close()

    def _launch_modelcenter(self, force_local: bool = False) -> None:
        """Launch ModelCenter, using PyPIM if it is configured.

        Parameters
        ----------
        force_local : bool
            Whether to force ModelCenter to start on the local machine, even if
            `PyPIM <https://github.com/ansys/pypim>`_ is configured. The default
            is ``False``.
        """
        if pypim.is_configured() and not force_local:
            if self._is_run_only:
                raise Exception("PyPim does not support running ModelCenter in run-only mode.")
            else:
                pim = pypim.connect()
                self._instance = pim.create_instance(product_name="modelcenter")
                self._instance.wait_for_ready()
                # LTTODO: Pypi support not required for this release; this has not been verified to work
                self._channel = self._instance.build_grpc_channel()
        else:
            self._process = MCDProcess()
            port: int = self._process.start(
                self._is_run_only, self._heartbeat_interval, self._allowed_heartbeat_misses
            )
            self._channel = cyberchannel.create_channel("wnua", "localhost", str(port))

        # run a background task to send heartbeat messages to the server
        self._heartbeat_condition = Condition()
        self._heartbeat_thread = Thread(
            target=_heartbeat_loop,
            args=(
                self._heartbeat_condition,
                self._channel._channel.target(),
                self,
                self._heartbeat_interval,
            ),
            daemon=True,
        )
        self._heartbeat_thread.start()

    @property
    def is_closed(self) -> bool:
        """Flag indicating if this instance has been closed."""
        return self._is_closed

    @interpret_rpc_error()
    def close(self):
        """Shut down the gRPC server and clear out all objects."""
        self._is_closed = True

        if self._heartbeat_condition is not None:
            with self._heartbeat_condition:
                self._heartbeat_condition.notify_all()
            self._heartbeat_condition = None

        if self._heartbeat_thread is not None and self._heartbeat_thread.is_alive():
            self._heartbeat_thread.join(self._heartbeat_interval * 1.1)
            self._heartbeat_thread = None

        if self._instance is not None:
            self._instance.delete()
        else:
            request = eng_msg.ShutdownRequest()
            self._stub.Shutdown(request)
        self._stub = None

        self._channel.close()
        self._channel = None

        self._process = None

    @staticmethod
    def _create_client(grpc_channel) -> GRPCModelCenterServiceStub:
        """Create a client from a gRPC channel."""
        return GRPCModelCenterServiceStub(grpc_channel)

    @property
    def is_local(self) -> bool:
        """Flag indicating if ModelCenter Desktop was started locally or
        remotely.

        Returns
        -------
        bool
            ``True`` if ModelCenter Desktop was started locally, ``False`` otherwise.
        """
        return self._process is not None

    @property
    def channel(self) -> Optional[grpc.Channel]:
        """Get the gRPC channel used to communicate with ModelCenter Desktop.

        Returns
        -------
        grpc.Channel
            ``grpc.Channel`` object or ``None`` if it has not been created.
        """
        return self._channel

    @property
    def process_id(self) -> int:
        """ID of the connected process, which is useful for debugging.

        Returns
        -------
        int
            Process ID of the connected ModelCenter Desktop.
        """
        if self._process is not None:
            return self._process.get_process_id()  # pragma: no cover
        else:
            # Can get this with gRPC; just useful for debugging, so leaving out for now.
            return -1

    @interpret_rpc_error(
        {grpc.StatusCode.RESOURCE_EXHAUSTED: WorkflowAlreadyLoadedError, **WRAP_INVALID_ARG}
    )
    @overrides
    def new_workflow(self, name: str, workflow_type: WorkflowType = WorkflowType.DATA) -> Workflow:
        request = eng_msg.NewWorkflowRequest(
            path=name,
            workflow_type=(
                eng_msg.WORKFLOW_TYPE_DATA_DEPENDENCY
                if workflow_type is WorkflowType.DATA
                else eng_msg.WORKFLOW_TYPE_PROCESS
            ),
        )
        response: eng_msg.NewWorkflowResponse = self._stub.EngineCreateWorkflow(request)
        return Workflow(response.workflow_id, name, self)

    @interpret_rpc_error(
        {
            grpc.StatusCode.NOT_FOUND: FileNotFoundError,
            grpc.StatusCode.RESOURCE_EXHAUSTED: WorkflowAlreadyLoadedError,
            **WRAP_INVALID_ARG,
        }
    )
    @overrides
    def load_workflow(
        self, file_name: Union[PathLike, str], ignore_connection_errors: Optional[bool] = None
    ) -> Workflow:
        request = eng_msg.LoadWorkflowRequest(
            path=str(file_name),
            connect_err_mode=(
                eng_msg.OnConnectionErrorMode.ON_CONNECTION_ERROR_MODE_IGNORE
                if ignore_connection_errors
                else eng_msg.ON_CONNECTION_ERROR_MODE_RAISE_ERROR
            ),
        )
        response: eng_msg.LoadWorkflowResponse = self._stub.EngineLoadWorkflow(request)
        return Workflow(response.workflow_id, request.path, self)

    @overrides
    def get_formatter(self, fmt: str) -> Format:
        formatter: Format = Format(fmt, self)
        return formatter

    @interpret_rpc_error(WRAP_INVALID_ARG)
    @overrides
    def get_preference(self, pref: str) -> Union[bool, int, float, str]:
        request = eng_msg.GetPreferenceRequest(preference_name=pref)
        response: eng_msg.GetPreferenceResponse = self._stub.EngineGetPreference(request)
        attr: Optional[str] = response.WhichOneof("value")
        if attr is not None:
            return getattr(response, attr)
        else:
            raise Exception("Server did not return a value.")

    @interpret_rpc_error(WRAP_INVALID_ARG)
    @overrides
    def set_preference(self, pref: str, value: Union[bool, int, float, str]) -> None:
        request = eng_msg.SetPreferenceRequest(preference_name=pref)
        if isinstance(value, bool):
            request.bool_value = value
        elif isinstance(value, int):
            request.int_value = value
        elif isinstance(value, float):
            request.double_value = value
        else:
            request.str_value = value
        self._stub.EngineSetPreference(request)

    @interpret_rpc_error()
    @overrides
    def get_units(self) -> Mapping[str, Collection[str]]:
        result: Dict[str, List[str]] = {}
        category_request = eng_msg.GetUnitCategoriesRequest()
        category_response: eng_msg.GetUnitCategoriesResponse = self._stub.EngineGetUnitCategories(
            category_request
        )
        for category in category_response.names:
            result[category] = []
            request = eng_msg.GetUnitNamesRequest()
            request.category = category
            response: eng_msg.GetUnitNamesResponse = self._stub.EngineGetUnitNames(request)
            for unit in response.names:
                result[category].append(unit)
        return result

    @overrides
    def get_run_only_mode(self) -> bool:
        return self._is_run_only

    @interpret_rpc_error()
    @overrides
    def get_server_info(self) -> WorkflowEngineInfo:
        request = eng_msg.GetServerInfoRequest()
        response: eng_msg.GetServerInfoResponse = self._stub.GetEngineInfo(request)

        version = {
            "major": response.version.major,
            "minor": response.version.minor,
            "patch": response.version.patch,
        }
        version_str: str = Template("${major}.${minor}.${patch}").safe_substitute(version)

        info = WorkflowEngineInfo(
            release_year=version["major"],
            release_id=version["minor"],
            build=version["patch"],
            is_release_build=response.is_release,
            build_type=response.build_type,
            version_as_string=version_str,
            server_type=response.server_type,
            install_location=response.directory_path,
            base_url=None,
        )
        return info
