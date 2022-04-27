"""Definition of Engine and associated classes."""
from enum import Enum
from typing import Union

import clr
from numpy import float64, int64
from overrides import overrides

from .i18n import i18n
from .iformat import IFormat
from .workflow import Workflow

clr.AddReference(r"phoenix-mocks\Phoenix.Mock.v45")
from Phoenix.Mock import MockFormatter, MockModelCenter


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


class Engine:
    def __init__(self):
        """Initialize a new Engine instance."""
        self._instance = MockModelCenter()
        self._workflow: Union[Workflow, None] = None

    # BOOL IsInteractive;
    @property
    def is_interactive(self) -> bool:
        pass

    # unsigned long ProcessID;
    @property
    def process_id(self) -> int:
        pass

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
        if self._workflow is not None:
            msg: str = i18n("Exceptions", "ERROR_WORKFLOW_ALREADY_OPEN")
            raise Exception(msg)
        else:
            self._instance.newModel(workflow_type.value)
            self._workflow = Workflow()
            return self._workflow

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
        if self._workflow is not None:
            msg: str = i18n("Exceptions", "ERROR_WORKFLOW_ALREADY_OPEN")
            raise Exception(msg)
        else:
            self._instance.loadModel(file_name, on_connect_error.value)
            self._workflow = Workflow()
            return self._workflow

    def get_formatter(self, fmt: str) -> IFormat:
        """
        Create an instance of a formatter that can be used to format \
        numbers to and from a particular string style.

        See documentation on IFormat.set_format for more information on
        available styles.

        Parameters
        ----------
        fmt: str
            Specified string format for the IFormat object.

        Returns
        -------
        An IFormat object that formats in the given style.
        """

        class MockFormatWrapper(IFormat):

            def __init__(self, instance: MockFormatter):
                """Initialize."""
                self._instance = instance

            @overrides
            def get_format(self) -> str:
                return self._instance.getFormat()

            @overrides
            def set_format(self, fmt: str) -> None:
                raise NotImplementedError

            @overrides
            def string_to_integer(self, string: str) -> int64:
                raise NotImplementedError

            @overrides
            def string_to_real(self, string: str) -> float64:
                raise NotImplementedError

            @overrides
            def integer_to_string(self, integer: int64) -> str:
                raise NotImplementedError

            @overrides
            def real_to_string(self, real: float64) -> str:
                raise NotImplementedError

            @overrides
            def string_to_string(self, string: str) -> str:
                raise NotImplementedError

            @overrides
            def integer_to_editable_string(self, integer: int64) -> str:
                raise NotImplementedError

            @overrides
            def real_to_editable_string(self, real: float64) -> str:
                raise NotImplementedError

        formatter: IFormat = MockFormatWrapper(self._instance.getFormatter(fmt))
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
        pass

    # BSTR getUnitCategoryName(long index);
    def get_unit_category_name(self, index: int) -> str:
        pass

    # long getNumUnits(BSTR category);
    def get_num_units(self, category: str) -> int:
        pass

    # BSTR getUnitName(BSTR category, long index);
    def get_unit_name(self, category: str, index: int) -> str:
        pass

    # boolean getRunOnlyMode();
    def get_run_only_mode(self) -> bool:
        pass

    # void setRunOnlyMode(boolean shouldBeInRunOnly);
    def set_run_only_mode(self, should_be_in_run_only: bool) -> None:
        pass

    # void saveTradeStudy(BSTR uri, int format, LPDISPATCH dataExplorer);
    def save_trade_study(self, uri: str, format_: int, data_explorer: object) -> None:
        pass
