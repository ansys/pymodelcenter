import clr
clr.AddReference(r"phoenix-mocks\Phoenix.Mock.v45")
import Phoenix.Mock as phxmock

from typing import List, TYPE_CHECKING, Union
from overrides import overrides

from .icomponent import IComponent
if TYPE_CHECKING:
    from .engine import Engine
from .i18n import i18n


class Workflow:
    def __init__(self, instance: phxmock.MockModelCenter, engine: 'Engine'):
        """
        Create a new instance.

        Parameters
        ----------
        self._instance = instance
        engine: Engine the engine that created this instance
        """
        self._instance = instance
        self._engine = engine

    # BSTR modelDirectory;
    @property
    def workflow_directory(self) -> str:
        pass

    # BSTR modelFileName;
    @property
    def workflow_file_name(self) -> str:
        pass

    # void setValue(BSTR varName, BSTR value);
    def set_value(self, var_name: str, value: str) -> None:
        pass

    # VARIANT getValue(BSTR varName);
    def get_value(self, var_name: str) -> object:
        pass

    # void createComponent(
    #   BSTR serverPath, BSTR name, BSTR parent, [optional]VARIANT xPos, [optional]VARIANT yPos);
    def create_component(
            self,
            server_path: str,
            parent: str,
            x_pos: object = None,
            y_pos: object = None) -> None:
        pass

    # void createLink(BSTR variable, BSTR equation);
    def create_link(self, variable: str, equation: str) -> None:
        pass

    # void saveModel();
    def save_workflow(self) -> None:
        pass

    # void saveModelAs(BSTR fileName);
    def save_workflow_as(self, file_name: str) -> None:
        pass

    # void closeModel();
    def close_workflow(self) -> None:
        self._engine._instance.closeModel()
        self._engine._notify_close_workflow(self)

    # IDispatch* getVariable(BSTR name);
    #   IDoubleVariable IDoubleArray IBooleanVariable IIntegerVariable IReferenceVariable
    #   IObjectVariable IFileVariable IStringVariable IBooleanArray IIntegerArray IReferenceArray
    #   IFileArray IStringArray IGeometryVariable:
    def get_variable(self, name: str) -> object:
        pass

    def get_component(self, name: str) -> object:   # IComponent, IIfComponent, IScriptComponent
        """
        Get a component from the workflow.

        Parameters
        ----------
        name: str
            The full path to the component.

        Returns
        -------
        The component.
        """

        class MockComponentWrapper(IComponent):
            @property  # type: ignore
            @overrides
            def variables(self) -> object:
                pass

            @property  # type: ignore
            @overrides
            def groups(self) -> object:
                pass

            @property  # type: ignore
            @overrides
            def user_data(self) -> object:
                pass

            @property  # type: ignore
            @overrides
            def associated_files(self) -> Union[str, List[str]]:
                pass

            @property  # type: ignore
            @overrides
            def index_in_parent(self) -> int:
                pass

            @property  # type: ignore
            @overrides
            def parent_assembly(self) -> object:
                pass

            @overrides
            def get_name(self) -> str:
                return self._instance.getName()

            @overrides
            def get_full_name(self) -> str:
                pass

            @overrides
            def get_source(self) -> str:
                pass

            @overrides
            def get_variable(self, name: str) -> object:
                pass

            @overrides
            def get_type(self) -> str:
                pass

            @overrides
            def get_metadata(self, name: str) -> object:
                pass

            @overrides
            def set_metadata(self, name: str, type_: object, value: object, access: object,
                             archive: bool) -> None:
                pass

            @overrides
            def run(self) -> None:
                pass

            @overrides
            def invoke_method(self, method: str) -> None:
                pass

            @overrides
            def invalidate(self) -> None:
                pass

            @overrides
            def reconnect(self) -> None:
                pass

            @overrides
            def download_values(self) -> None:
                pass

            @overrides
            def rename(self, name: str) -> None:
                pass

            @overrides
            def show(self) -> None:
                pass

            def __init__(self, instance: phxmock.MockComponent):
                self._instance = instance

        mock: phxmock.MockComponent = self._instance.getComponent(name)
        if mock is None:
            msg: str = i18n("Exceptions", "ERROR_COMPONENT_NOT_FOUND")
            raise Exception(msg)
        comp: IComponent = MockComponentWrapper(mock)
        return comp

    def trade_study_end(self) -> None:
        self._instance.tradeStudyEnd()

    # Skip IDispatch* createJobManager([optional]VARIANT showProgressDialog);

    def trade_study_start(self) -> None:
        self._instance.tradeStudyStart()

    # boolean getHaltStatus();
    def get_halt_status(self) -> bool:
        pass

    # VARIANT getValueAbsolute(BSTR varName);
    def get_value_absolute(self, var_name: str) -> object:    # IVariableValue:
        pass

    # void setScheduler(BSTR scheduler);
    def set_scheduler(self, schedular: str) -> None:
        pass

    # void removeComponent(BSTR name);
    def remove_component(self, name: str) -> None:
        pass

    # void breakLink(BSTR variable);
    def break_link(self, variable: str) -> None:
        pass

    # VARIANT runMacro(BSTR macro, [optional]VARIANT useMCObject);
    def run_macro(self, macro: str, use_mc_object: object = None) -> object:
        pass

    # IDispatch* createAssembly(BSTR name, BSTR parent, [optional]VARIANT assemblyType);
    def create_assembly(self, name: str, parent: str, assembly_type: object = None):
        pass

    # IDispatch* createAssemblyVariable(BSTR name, BSTR type, BSTR parent);
    def create_assembly_variable(self, name: str, type_: str, parent: str) -> object:    # IVariable
        pass

    # void autoLink(BSTR srcComp, BSTR destComp);
    def auto_link(self, src_comp: str, dest_comp: str) -> None:
        pass

    # LPDISPATCH getLinks([optional]VARIANT reserved);
    def get_links(self, reserved: object = None):
        pass

    # BSTR getModelUUID();
    def get_workflow_uuid(self) -> str:
        pass

    # void halt();
    def halt(self) -> None:
        pass

    # void run(BSTR variableArray);
    def run(self, variable_array: str) -> None:
        pass

    # IDispatch* getDataMonitor(BSTR component, VARIANT index);
    def get_data_monitor(self, componenet: str, index: object) -> object:   # IDataMonitor
        pass

    # IDispatch* createDataMonitor(BSTR component, BSTR name, int x, int y);
    def create_data_monitor(
            self, component: str, name: str, x: int, y: int) -> object:     # IDataMonitor
        pass

    # boolean removeDataMonitor(BSTR component, VARIANT index);
    def remove_data_monitor(self, component: str, index: object) -> bool:
        pass

    # IDispatch* getDataExplorer(int index);
    def get_data_explorer(self, index: int) -> object:  # PHXDataExplorer
        pass

    # void moveComponent(BSTR component, BSTR parent, [optional]VARIANT index);
    def move_component(self, component: str, parent: str, index: object) -> None:
        pass

    # void setXMLExtension(BSTR xml);
    def set_xml_extension(self, xml: str) -> None:
        pass

    # IDispatch* getModel();
    # IDispatch* getAssembly(BSTR name);
    def get_assembly(self, name: str = None) -> object:    # IAssembly
        """Gets the named assembly or the top level assembly."""
        pass

    # IDispatch* createAndInitComponent(
    #   BSTR serverPath, BSTR name, BSTR parent, BSTR initString,
    #   [optional]VARIANT xPos, [optional]VARIANT yPos);
    def create_and_init_component(
            self,
            server_path: str,
            name: str,
            parent: str,
            init_string: str,
            x_pos: object = None,
            y_pos: object = None):
        pass

    # BSTR getMacroScript(BSTR macroName);
    def get_macro_script(self, macro_name: str) -> str:
        pass

    # void setMacroScript(BSTR macroName, BSTR script);
    def set_macro_script(self, macro_name: str, script: str) -> None:
        pass

    # BSTR getMacroScriptLanguage(BSTR macroName);
    def get_macro_script_language(self, macro_name: str) -> str:
        pass

    # void setMacroScriptLanguage(BSTR macroName, BSTR language);
    def set_macro_script_langauge(self, macro_name: str, language: str) -> None:
        pass

    # void addNewMacro(BSTR macroName, boolean isAppMacro);
    def add_new_macro(self, macro_name: str, is_app_macro: bool) -> None:
        pass

    # LPDISPATCH getVariableMetaData(BSTR name);
    def get_variable_meta_data(self, name: str) -> object:  # PHXDATAHISTORYLib.IDHVariable
        pass

    # IDispatch* createDataExplorer(BSTR tradeStudyType, BSTR setup);
    def create_data_explorer(self, trade_study_type: str, setup: str) -> object:    # IDataExplorer
        pass

    # double getMacroTimeout(BSTR macroName);
    def get_macro_timeout(self, macro_name: str) -> float:
        pass

    # void setMacroTimeout(BSTR macroName, double timeout);
    def set_macro_timeout(self, macro_name: str, timeout: float) -> None:
        pass
