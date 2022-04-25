from string import Template
import clr
clr.AddReference("Phoenix.Mock.v45")
from Phoenix.Mock import MockModelCenter


class ModelCenter:
    """Manages the main ModelCenter Desktop application.

    Creating an instance of this object will start an instance of ModelCenter Desktop in batch mode.
    LTTODO: add more notes on usage as the api is filled out. See the COM api documentation for
    LTTODO: some of the examples we probably want.
    """

    def __init__(self):
        self._instance = MockModelCenter()

    @property
    def version(self) -> str:
        """
        The version of the ModelCenter Desktop application being used.
        ModelCenter versions are in the form ``1.2.3`` where

        * -1 is the major version,
        * -2 is the minor version, and
        * -3 is the patch version
        """
        version = {
            "major": self._instance.get_version(0),
            "minor": self._instance.get_version(1),
            "patch": self._instance.get_version(2)
        }
        return Template("${major}.${minor}.${patch}").safe_substitute(version)
