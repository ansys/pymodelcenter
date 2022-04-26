from enum import Enum

from .workflow import Workflow
import clr
clr.AddReference("Phoenix.Mock.v45")
from Phoenix.Mock import MockModelCenter


class WorkflowType(Enum):
    """Enumeration of the types of workflows that can be created."""
    DATA = "dataModel",
    PROCESS = "processModel"


class OnConnectionErrorMode(Enum):
    ERROR = 3,
    IGNORE = 1,
    DIALOG = -1


class Engine:
    def __init__(self):
        self._instance = MockModelCenter()

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
        workflow_type The type of workflow to create. Defaults to a data
        workflow.

        Returns
        -------
        A new Workflow instance.
        """
        self._instance.newModel(workflow_type.value)
        return Workflow()

    def load_workflow(self, file_name: str,
                      on_connect_error: OnConnectionErrorMode = OnConnectionErrorMode.ERROR) \
            -> Workflow:
        """
        Load a saved workflow from a file.

        Parameters
        ----------
        file_name The path to the file to load.
        on_connect_error What to do in the event of an error.

        Returns
        -------
        A new Workflow instance.
        """
        self._instance.loadModel(file_name, on_connect_error.value)
        return Workflow()

    # IDispatch* getFormatter(BSTR format);
    def get_formatter(self, format_: str) -> object:     # IPHXFormat
        pass

    # void setUserName(BSTR userName);
    def set_user_name(self, user_name: str) -> None:
        pass

    # void setPassword(BSTR password);
    def set_password(self, password: str) -> None:
        pass

    # VARIANT getPreference(BSTR pref);
    def get_preference(self, pref: str) -> object:
        pass

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
