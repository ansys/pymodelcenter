"""Utilities for finding and starting a ModelCenter Desktop process."""
from io import TextIOWrapper
from pathlib import Path
import subprocess
import time
from typing import Optional
import winreg


def _find_exe_location() -> str:  # pragma: no cover
    """Attempts to find ModelCenter.exe."""
    key: winreg.HKEYType = winreg.OpenKey(
        winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Phoenix Integration\ModelCenter"
    )

    install_dir: str = winreg.QueryValueEx(key, "CurrentInstallLocation")[0]
    path: Path = Path(f"{install_dir}\\ModelCenterD.exe")
    if path.exists():
        return str(path)
    else:
        return f"{install_dir}\\ModelCenter.exe"


class MCDProcess:
    """Responsible for launching and keeping track of MCD process."""

    def __init__(self) -> None:
        """Initialize a new MCDProcess instance."""
        self._exe_path: str = _find_exe_location()
        self._process: Optional[subprocess.Popen] = None
        self._debug: bool = True if self._exe_path.endswith("ModelCenterD.exe") else False
        self._timeout: float = 60 if self._debug else 30

    def start(self, run_only: bool = False) -> int:
        """Start the MCD process."""
        args = [self._exe_path, "/Grpc", "/Automation"]
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
                colon_index = line.find(":")+1  # MCD returns string like: 0.0.0.0:50051
                return int(line[colon_index:].strip())
            else:
                time.sleep(0.1)
        raise Exception("Timed out waiting for ModelCenter to start.")

    def get_process_id(self) -> int:
        """Get the process id of the MCD process."""
        if self._process is None:
            return -1
        return self._process.pid
