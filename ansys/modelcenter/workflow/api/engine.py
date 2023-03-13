"""Definition of Engine and associated classes."""
from enum import Enum
from os import PathLike
from string import Template
from typing import Union

from ansys.engineeringworkflow.api import (
    IFileBasedWorkflowEngine,
    IWorkflowInstance,
    WorkflowEngineInfo,
)
import clr
from overrides import overrides

from .data_explorer import DataExplorer
from .format import Format
from .i18n import i18n
from .workflow import Workflow

clr.AddReference(r"phoenix-mocks\Phoenix.Mock.v45")
from Phoenix.Mock import MockModelCenter  # type: ignore


class WorkflowType(Enum):
    """Enumeration of the types of workflows that can be created."""

    DATA = ("dataModel",)
    """Legacy style workflow where execution flow is determined from
    links between components and an execution strategy."""
    PROCESS = "processModel"
    """Modern style workflow where execution flow is explicitly designed
    by the user using flow components."""


class OnConnectionErrorMode(Enum):
    """Enumeration of actions to take on connection error."""

    ERROR = (3,)
    """Abort loading and throw the error back to the caller."""
    IGNORE = (1,)
    """Ignore the error and continue loading."""
    DIALOG = -1
    """(UI mode only) Show an error dialog."""


class Engine(IFileBasedWorkflowEngine):
    """Engine class used to wrap around MockModelCenter class."""

    def __init__(self):
        """Initialize a new Engine instance."""
        self._instance = MockModelCenter()

    @property
    def process_id(self) -> int:
        """
        The process identifier of the ModelCenter process.

        Useful for cases where ModelCenter is running in COM server mode and a client process
        needs to grant it permission to do something (like move a window to the foreground).

        Returns
        -------
        int
            The process identifier.
        """
        return int(self._instance.ProcessID)

    def new_workflow(self, name: str, workflow_type: WorkflowType = WorkflowType.DATA) -> Workflow:
        """
        Create a new workflow.

        Parameters
        ----------
        name: str
            A filename or path where the new workflow will be made.
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
            self._instance.saveModelAs(name)
            return Workflow(self._instance)

    @overrides
    def load_workflow(self, file_name: Union[PathLike, str]) -> IWorkflowInstance:
        return self.load_workflow_ex(str(file_name))

    def load_workflow_ex(
        self, file_name: str, on_connect_error: OnConnectionErrorMode = OnConnectionErrorMode.ERROR
    ) -> Workflow:
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

    def get_num_unit_categories(self) -> int:
        """
        Get the number of unit categories in the IModelCenter object.

        Returns
        -------
        int
            The number for unit categories, or -1 if there is an error.
        """
        return self._instance.getNumUnitCategories()

    def get_unit_category_name(self, index: int) -> str:
        """
        Get the name of the category of a unit.

        Parameters
        ----------
        index : int
            Index of the unit.

        Returns
        -------
        str
            The name of the category, or empty string if there is an error.
        """
        return self._instance.getUnitCategoryName(index)

    def get_num_units(self, category: str) -> int:
        """
        Get the number of units inside a specified category.

        Parameters
        ----------
        category : str
            Specified category of units.

        Returns
        -------
        int
            The number of units, or -1 if there is an error.
        """
        return self._instance.getNumUnits(category)

    def get_unit_name(self, category: str, index: int) -> str:
        """
        Get the name of the unit.

        Parameters
        ----------
        category : str
            Category to retrieve the unit.
        index : int
            Index of the element in the category.

        Returns
        -------
        str
            The name of the unit, or empty string if there is an error.
        """
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

    # TODO: Rename to get_engine_info?
    @overrides
    def get_server_info(self) -> WorkflowEngineInfo:
        """
        Get information about the engine.

        Returns
        -------
        A `WorkflowEngineInfo` object with information about the Engine.
        """
        version = {
            "major": self._instance.get_version(0),
            "minor": self._instance.get_version(1),
            "patch": self._instance.get_version(2),
        }
        version_str: str = Template("${major}.${minor}.${patch}").safe_substitute(version)
        install_location: str = self._instance.getModelCenterPath()  # or self._instance.appFullPath
        info = WorkflowEngineInfo(
            release_year=version["major"],
            release_id=version["minor"],
            build=version["patch"],
            is_release_build=False,
            build_type="dev",
            version_as_string=version_str,
            server_type="MockModelCenter",
            install_location=install_location,
            base_url=None,
        )
        return info
