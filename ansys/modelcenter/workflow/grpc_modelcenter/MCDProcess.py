import subprocess
import winreg


def _find_exe_location() -> str:
    """Attempts to find ModelCenter.exe"""

    key: winreg.HKEYType = winreg.OpenKey(
        winreg.HKEY_LOCAL_MACHINE,
        r"SOFTWARE\Phoenix Integration\ModelCenter")

    install_dir: str = winreg.QueryValueEx(key, "CurrentInstallLocation")[0]
    return f"{install_dir}\\ModelCenter.exe"


class MCDProcess:
    """
    Responsible for launching and keeping track of a ModelCenter Desktop
    process.

    TODO: Error handling, finish class implementation (what else is
          needed?)
    """

    def __init__(self):
        self._exe_path: str = _find_exe_location()
        self._process = None

    def start(self):
        """Start the MCD process."""

        # May want to use some additional parameters for capturing stdout, etc.
        self._process = subprocess.Popen(self._exe_path)

