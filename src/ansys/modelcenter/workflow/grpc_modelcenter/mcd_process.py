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
"""Utilities for finding and starting a ModelCenter Desktop process."""
from io import TextIOWrapper
from pathlib import Path
import subprocess
import time
from typing import Optional
import winreg

import numpy


def _find_exe_location() -> str:  # pragma: no cover
    """Attempts to find the ModelCenter EXE file."""
    key: winreg.HKEYType = winreg.OpenKey(
        winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Phoenix Integration\ModelCenter"
    )

    install_dir: str = winreg.QueryValueEx(key, "CurrentInstallLocation")[0]
    path: Path = Path(f"{install_dir}\\ModelCenterD.exe")
    if path.exists():
        return str(path)
    else:
        return f"{install_dir}\\ModelCenter.exe"


class EngineLicensingFailedException(Exception):
    """Indicates that engine licensing has failed."""

    ...


class MCDProcess:
    """Launches and keeps track of a ModelCenter Desktop process."""

    def __init__(self) -> None:
        """Initialize an instance."""
        self._exe_path: str = _find_exe_location()
        self._process: Optional[subprocess.Popen] = None
        self._debug: bool = True if self._exe_path.endswith("ModelCenterD.exe") else False
        self._timeout: float = 60 if self._debug else 30

    def start(
        self,
        run_only: bool = False,
        heartbeat_interval: numpy.uint = 30000,
        allowed_heartbeat_misses: numpy.uint = 3,
    ) -> int:
        """Start the ModelCenter Desktop process.

        Parameters
        ----------
        run_only : bool, optional
            Whether to start ModelCenter in run-only mode. The default
            is ``False``.
        heartbeat_interval : numpy.uint, optional
            Interval between heartbeat messages. The default is ``30000``.
        allowed_heartbeat_misses : numpy.uint, optional
            Number of allowed missed heartbeats before the server terminates.
            The default is ``3``.

        Returns
        -------
        Port number that the gRPC server was started on.
        """
        args = [
            self._exe_path,
            "/Grpc",
            "/Automation",
            f"/Heartbeat:{heartbeat_interval}:{allowed_heartbeat_misses}",
        ]
        if run_only:
            args.append("/runonly")
        self._process = subprocess.Popen(args, stdout=subprocess.PIPE)

        # Wait until we read the grpc server start message from stdout.
        start: float = time.time()
        assert self._process.stdout is not None
        for line in TextIOWrapper(self._process.stdout, encoding="utf-8"):
            # if self._debug:
            #     print(line)
            # But bail if too much time passes before that happens.
            if time.time() - start > self._timeout:
                break
            elif line.startswith("grpc server listening on "):
                colon_index = line.find(":") + 1  # MCD returns string like: 0.0.0.0:50051
                return int(line[colon_index:].strip())
            elif line.startswith("grpcmc: licensing failed"):
                raise EngineLicensingFailedException(
                    "The engine reported that licensing has failed."
                )
            else:
                time.sleep(0.1)
        raise Exception("Timed out waiting for ModelCenter to start.")

    def get_process_id(self) -> int:
        """Get the process ID of the ModelCenter Desktop process."""
        if self._process is None:
            return -1
        return self._process.pid
