# Do not let isort move this somewhere else. It must be imported before attempting to import
# the Mocks assembly.
import clr
clr.AddReference('phoenix-mocks/Phoenix.Mock.v45')

from ansys.modelcenter.workflow.api.workflow import Workflow
from typing import Any


class Engine:
    def __init__(self, modelcenter: Any):
        """
        Create a new instance of the Engine API.
        """

        # TODO: Can we get mypy to check our calls to the MC object somehow?
        self.__modelcenter: Any = modelcenter

    # BOOL IsInteractive;
    @property
    def is_interactive(self) -> bool:
        # IsInteractive is an int property on the interface for COM reasons.
        return bool(self.__modelcenter.IsInteractive)

    # unsigned long ProcessID;
    @property
    def process_id(self) -> int:
        return int(self.__modelcenter.ProcessID)

    # void newModel([optional]VARIANT modelType);
    def new_workflow(self, workflow_type: object = None) -> Workflow:
        pass

    # void loadModel(BSTR fileName, [optional]VARIANT onConnectError);
    def load_workflow(self, file_name: str, on_connect_error: object) -> Workflow:
        pass

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
