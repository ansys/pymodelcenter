"""Definition of Engine and associated classes."""
from enum import Enum
from string import Template
from typing import Union

import clr

from .data_explorer import DataExplorer
from .format import Format
from .i18n import i18n
from .workflow import Workflow

clr.AddReference(r"phoenix-mocks\Phoenix.Mock.v45")
from Phoenix.Mock import MockModelCenter


class WorkflowType(Enum):
    """Enumeration of the types of workflows that can be created."""

    DATA = "dataModel",
    """Legacy style workflow where execution flow is determined from
    links between components and an execution strategy."""
    PROCESS = "processModel"
    """Modern style workflow where execution flow is explicitly designed
    by the user using flow components."""


class OnConnectionErrorMode(Enum):
    """Enumeration of actions to take on connection error."""

    ERROR = 3,
    """Abort loading and throw the error back to the caller."""
    IGNORE = 1,
    """Ignore the error and continue loading."""
    DIALOG = -1
    """(UI mode only) Show an error dialog."""


class EngineInfo:
    """Information about the engine."""

    def __init__(self, exec_path: str, version: str, dir_path: str):
        """
        Initialize.

        Parameters
        ----------
        exec_path: str
            Path to the engine executable.
        version: str
            Version of the engine.
        dir_path: str
            Path to the directory the engine executable is in.
        """
        self._engine_directory_path: str = dir_path
        self._engine_executable_path: str = exec_path
        self._version: str = version

    @property
    def directory_path(self) -> str:
        """Path to the directory the engine executable is in."""
        return self._engine_directory_path

    @property
    def executable_path(self) -> str:
        """Path to the engine executable."""
        return self._engine_executable_path

    @property
    def version(self) -> str:
        """Version of the engine."""
        return self._version


class Engine:
    def __init__(self):
        """Initialize a new Engine instance."""
        self._instance = MockModelCenter()

    # BOOL IsInteractive;
    @property
    def is_interactive(self) -> bool:
        # IsInteractive is an int property on the interface for COM reasons.
        return bool(self._instance.IsInteractive)

    # unsigned long ProcessID;
    @property
    def process_id(self) -> int:
        return int(self._instance.ProcessID)

    def new_workflow(self, workflow_type: WorkflowType = WorkflowType.DATA) -> Workflow:
        """
        Create a new workflow.

        Parameters
        ----------
        workflow_type: WorkflowType
            The type of workflow to create. Defaults to a data workflow.

        Returns
        -------
        A new Workflow instance.
        """
        if self._instance.getModel() is not None:
            msg: str = i18n("Exceptions", "ERROR_WORKFLOW_ALREADY_OPEN")
            raise Exception(msg)
        else:
            self._instance.newModel(workflow_type.value)
            return Workflow(self._instance)

    def load_workflow(self, file_name: str,
                      on_connect_error: OnConnectionErrorMode = OnConnectionErrorMode.ERROR) \
            -> Workflow:
        """
        Load a saved workflow from a file.

        Parameters
        ----------
        file_name: str
            The path to the file to load.
        on_connect_error: OnConnectionErrorMode
            What to do in the event of an error.

        Returns
        -------
        A new Workflow instance.
        """
        if self._instance.getModel() is not None:
            msg: str = i18n("Exceptions", "ERROR_WORKFLOW_ALREADY_OPEN")
            raise Exception(msg)
        else:
            self._instance.loadModel(file_name, on_connect_error.value)
            return Workflow(self._instance)

    def get_formatter(self, fmt: str) -> Format:
        """
        Create an instance of a formatter that can be used to format \
        numbers to and from a particular string style.

        See documentation on Format.format for more information on
        available styles.

        Parameters
        ----------
        fmt: str
            Specified string format for the IFormat object.

        Returns
        -------
        A Format object that formats in the given style.
        """
        formatter: Format = Format(self._instance.getFormatter(fmt))
        return formatter

    def set_user_name(self, user_name: str) -> None:
        """
        Set the username used for authentication.

        Parameters
        ----------
        user_name: str
            The username.
        """
        self._instance.setUserName(user_name)

    def set_password(self, password: str) -> None:
        """
        Set the password used for authentication.

        Parameters
        ----------
        password: str
            The password.
        """
        self._instance.setPassword(password)

    def get_preference(self, pref: str) -> Union[bool, int, float, str]:
        """
        Get the value of a preference.

        Preferences control how the engine behaves in various ways.
        The value returned may be boolean, integer, real, or string
        typed.

        Parameters
        ----------
        pref: str
            The name of the preference for which to return the value.

        Returns
        -------
        The value of the given preference.
        """
        return self._instance.getPreference(pref)

    # long getNumUnitCategories();
    def get_num_unit_categories(self) -> int:
        return self._instance.getNumUnitCategories()

    # BSTR getUnitCategoryName(long index);
    def get_unit_category_name(self, index: int) -> str:
        return self._instance.getUnitCategoryName(index)

    # long getNumUnits(BSTR category);
    def get_num_units(self, category: str) -> int:
        return self._instance.getNumUnits(category)

    # BSTR getUnitName(BSTR category, long index);
    def get_unit_name(self, category: str, index: int) -> str:
        return self._instance.getUnitName(category, index)

    def get_run_only_mode(self) -> bool:
        """
        Get whether the engine is in Run-Only mode.

        Run-Only mode has lower licensing requirements, but does not
        allow for the workflow to be edited.

        Returns
        -------
        True if in Run-Only mode; otherwise, False.
        """
        return self._instance.getRunOnlyMode()

    def set_run_only_mode(self, should_be_in_run_only: bool) -> None:
        """
        Set whether the engine is in Run-Only mode.

        Note that this method call only be called immediately after
        creation of the Engine, and will throw otherwise.

        Parameters
        ----------
        should_be_in_run_only: bool
            True if Run-Only mode should be enabled; otherwise, False.
        """
        self._instance.setRunOnlyMode(should_be_in_run_only)

    def save_trade_study(self, uri: str, data_explorer: DataExplorer) -> None:
        """
        Save the trade study currently loaded in the DataExplorer to \
        the given URI.

        The file will be overwritten if it exists.

        Parameters
        ----------
        uri: str
            The uri to which to write the trade study.
        data_explorer: DataExplorer
            The data explorer whose plots and data should be saved.
        """
        self._instance.saveTradeStudy(uri, 3, data_explorer)

    def get_engine_info(self) -> EngineInfo:
        """
        Get information about the engine.

        Returns
        -------
        A EngineInfo object with information about the Engine.
        """
        full_path: str = self._instance.appFullPath
        version = {
            "major": self._instance.get_version(0),
            "minor": self._instance.get_version(1),
            "patch": self._instance.get_version(2)
        }
        version_str: str = Template("${major}.${minor}.${patch}").safe_substitute(version)
        mc_path: str = self._instance.getModelCenterPath()
        info: EngineInfo = EngineInfo(full_path, version_str, mc_path)
        return info
