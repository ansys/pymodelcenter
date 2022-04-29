import clr

clr.AddReference(r"phoenix-mocks\Phoenix.Mock.v45")

from typing import TYPE_CHECKING, Any, Iterable, List, Optional, Tuple, Union

import Phoenix.Mock as phxmock
import ansys.common.variableinterop as acvi
from overrides import overrides

from . import DataExplorer
from .icomponent import IComponent

if TYPE_CHECKING:
    from .engine import Engine

from .i18n import i18n
from .variable_links import VariableLink, dotnet_links_to_iterable


class WorkflowVariable:
    # LTTODO: Fleshing this out is part of another PBI.

    def __init__(self, variable: Any):
        """
        Create a new instance
        Parameters
        ----------
        variable: Any
            the actual ModelCenter variable to wrap.
        """
        self._variable = variable


class Workflow:
    def __init__(self, instance: phxmock.MockModelCenter, engine: 'Engine'):
        """
        Initialize a new Workflow instance.

        Parameters
        ----------
        instance : object
            The raw interface object to use to make direct calls to
            ModelCenter.
        engine : Engine
            The engine that created this instance.
        """
        self._instance = instance
        self._engine = engine

    @property
    def workflow_directory(self) -> str:
        """
        Directory of the current Workflow.

        If no workflow is open it will raise an error. If the model has
        not yet been saved, it will return an empty string.
        """
        return self._instance.modelDirectory

    @property
    def workflow_file_name(self) -> str:
        """Full path of the current Workflow."""
        return self._instance.modelFileName

    def set_value(self, var_name: str, value: str) -> None:
        pass
        """
        Set the value of a variable.

        A wrapper around the
        IModelCenter.setValue(BSTR varName, BSTR value) method.

        Parameters
        ----------
        var_name : str
            Full ModelCenter path of the variable.
        value : str
            The New serialized value to set variable to.
        """
        if isinstance(value, acvi.IVariableValue):
            api_value = value.to_api_string()
        else:
            api_value = str(value)
        self._instance.setValue(var_name, api_value)

    def get_value(self, var_name: str) -> object:
        """
        Get the value of a variable.

        A wrapper around the IModelCenter.getValue(BSTR varName) method.

        Parameters
        ----------
        var_name :  str
            Full ModelCenter path of the variable.

        Returns
        -------
        The value as one of the acvi.IVariableValue types.
        """
        raw = self._instance.getValue(var_name)
        if isinstance(raw, bool):
            return acvi.BooleanValue(raw)
        elif isinstance(raw, int):
            return acvi.IntegerValue(raw)
        elif isinstance(raw, float):
            return acvi.RealValue(raw)
        elif isinstance(raw, str):
            return acvi.StringValue(raw)
        elif isinstance(raw, list):
            first = raw[0]
            if isinstance(first, bool):
                return acvi.BooleanArrayValue(values=raw)
            elif isinstance(first, int):
                return acvi.IntegerArrayValue(values=raw)
            elif isinstance(first, float):
                return acvi.RealArrayValue(values=raw)
            elif isinstance(first, str):
                return acvi.StringArrayValue(values=raw)
        raise TypeError

    # void createComponent(
    #   BSTR serverPath, BSTR name, BSTR parent, [optional]VARIANT xPos, [optional]VARIANT yPos);
    def create_component(
            self,
            server_path: str,
            name: str,
            parent: str,
            x_pos: Optional[object] = None,
            y_pos: Optional[object] = None) -> None:
        pass

        # LTTODO: The mock expects System.Reflection.Missing.Value for x_pos and y_pos to indicate
        # that no value was passed, but it's not feasible to actually pass that, since pythonnet
        # seems to get tripped up while it's using reflection to find a method to actually call
        # (Missing.Value has a special meaning there, it seems.)
        # This is something the actual GRPC API will probably have to solve.

        self._instance.createComponent(
            server_path,
            name,
            parent,
            x_pos,
            y_pos
        )

    # void createLink(BSTR variable, BSTR equation);
    def create_link(self, variable: str, equation: str) -> None:
        self._instance.createLink(variable, equation)

    # void saveModel();
    def save_workflow(self) -> None:
        self._instance.saveModel()

    # void saveModelAs(BSTR fileName);
    def save_workflow_as(self, file_name: str) -> None:
        self._instance.saveModelAs(file_name)

    # void closeModel();
    def close_workflow(self) -> None:
        self._instance.closeModel()
        self._engine._notify_close_workflow(self)

    # IDispatch* getVariable(BSTR name);
    #   IDoubleVariable IDoubleArray IBooleanVariable IIntegerVariable IReferenceVariable
    #   IObjectVariable IFileVariable IStringVariable IBooleanArray IIntegerArray IReferenceArray
    #   IFileArray IStringArray IGeometryVariable:
    def get_variable(self, name: str) -> object:
        return WorkflowVariable(self._instance.getVariable(name))

    def get_component(self, name: str) -> IComponent:   # IComponent, IIfComponent, IScriptComponent
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
        self._instance.breakLink(variable)

    # VARIANT runMacro(BSTR macro, [optional]VARIANT useMCObject);
    def run_macro(self, macro_name: str, use_mc_object: bool = False) -> object:
        """
        Run the specified macro.

        Parameters
        ----------
        macro_name : str
            The name of the macro.
        use_mc_object : bool
            Whether to use the ModelCenter object.

        Returns
        -------
        object :
            The script text.
        """
        return self._instance.runMacro(macro_name, use_mc_object)

    # IDispatch* createAssembly(BSTR name, BSTR parent, [optional]VARIANT assemblyType);
    def create_assembly(self, name: str, parent: str, assembly_type: object = None):
        pass

    # IDispatch* createAssemblyVariable(BSTR name, BSTR type, BSTR parent);
    def create_assembly_variable(self, name: str, type_: str, parent: str) -> object:    # IVariable
        pass

    # void autoLink(BSTR srcComp, BSTR destComp);
    def auto_link(self, src_comp: str, dest_comp: str) -> None:
        self._instance.autoLink(src_comp, dest_comp)

    # LPDISPATCH getLinks([optional]VARIANT reserved);
    def get_links(self, reserved: object = None) -> Iterable[VariableLink]:
        return dotnet_links_to_iterable(self._instance.getLinks(reserved))

    # BSTR getModelUUID();
    def get_workflow_uuid(self) -> str:
        return self._instance.getModelUUID()

    # void halt();
    def halt(self) -> None:
        self._instance.halt()

    # void run(BSTR variableArray);
    def run(self, variable_array: str) -> None:
        pass

    # IDispatch* getDataMonitor(BSTR component, VARIANT index);
    def get_data_monitor(self, component: str, index: object) -> object:   # IDataMonitor
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

    # void setAssemblyStyle(
    #   BSTR assemblyName, AssemblyStyle style, [optional]VARIANT width, [optional]VARIANT height);
    def set_assembly_style(
            self,
            assembly_name: str,
            style: object,
            width: object = None,
            height: object = None) -> None:
        pass

    # AssemblyStyle getAssemblyStyle(BSTR assemblyName, int *width, int *height);
    def get_assembly_style(self, assembly_name: str) -> Tuple[int, int]:
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
        """
        Get a macro script.

        This method is not safe for use from a component in parallel
        mode and will throw an exception if used in such a manner.

        Parameters
        ----------
        macro_name : str
            The name of the macro.

        Returns
        -------
        str :
            The script text.
        """
        return self._instance.getMacroScript(macro_name)

    # void setMacroScript(BSTR macroName, BSTR script);
    def set_macro_script(self, macro_name: str, script: str) -> None:
        """
        Set a macro script.

        This method is not safe for use from a component in parallel
        mode and will throw an exception if used in such a manner.

        Parameters
        ----------
        macro_name : str
            The name of the macro.
        script : str
            The script text.
        """
        self._instance.setMacroScript(macro_name, script)

    # BSTR getMacroScriptLanguage(BSTR macroName);
    def get_macro_script_language(self, macro_name: str) -> str:
        """
        Get a macro script language.

        This method is not safe for use from a component in parallel
        mode and will throw an exception if used in such a manner.

        Parameters
        ----------
        macro_name : str
            The name of the macro.

        Returns
        -------
        str :
            A string representing the macro script language.
        """
        return self._instance.getMacroScriptLanguage(macro_name)

    # void setMacroScriptLanguage(BSTR macroName, BSTR language);
    def set_macro_script_language(self, macro_name: str, language: str) -> None:
        """
        Set a macro script language.

        This method is not safe for use from a component in parallel
        mode and will throw an exception if used in such a manner.

        Parameters
        ----------
        macro_name : str
            The name of the macro.
        language : str
            A string representing the macro script language.
        """
        self._instance.setMacroScriptLanguage(macro_name, language)

    # void addNewMacro(BSTR macroName, boolean isAppMacro);
    def add_new_macro(self, macro_name: str, is_app_macro: bool) -> None:
        """
        Add a new macro.

        Parameters
        ----------
        macro_name : str
            The name of the macro to show in the editor.
        is_app_macro : bool
            If true, the new macro will be an application macro.
            Otherwise, the new macro will be a workflow macro.
        """
        self._instance.addNewMacro(macro_name, is_app_macro)

    # LPDISPATCH getVariableMetaData(BSTR name);
    def get_variable_meta_data(self, name: str) -> object:  # PHXDATAHISTORYLib.IDHVariable
        pass

    # IDispatch* createDataExplorer(BSTR tradeStudyType, BSTR setup);
    def create_data_explorer(self, trade_study_type: str, setup: str) -> DataExplorer:
        """
        Creates a new Data Explorer.

        This documentation assumes you're creating it for a trade study.
        If you're not you can pass almost anything in for
        trade_study_type or setup.

        Parameters
        ----------
        trade_study_type : str
            Registry ID of the Plug-In.
        setup : str
            A string that is generated from the Plug-In's ``toString``
            method that can be restored later by the Plug-In's
            ``fromString`` method.

        Returns
        -------
        object :
            IDataExplorer object.
        """
        de_object: object = self._instance.createDataExplorer(trade_study_type, setup)
        return DataExplorer(de_object)

    # double getMacroTimeout(BSTR macroName);
    def get_macro_timeout(self, macro_name: str) -> float:
        """
        Get a macro's timeout.

        This method is not safe for use from a component in parallel
        mode and will throw an exception if used in such a manner.

        Parameters
        ----------
        macro_name : str
            The name of the macro.

        Returns
        -------
        float :
            Number of seconds to allow a script to run before canceling
            it; -1 indicates no timeout.
        """
        return self._instance.getMacroTimeout(macro_name)

    # void setMacroTimeout(BSTR macroName, double timeout);
    def set_macro_timeout(self, macro_name: str, timeout: float) -> None:
        """
        Set a macro's timeout.

        This method is not safe for use from a component in parallel
        mode and will throw an exception if used in such a manner.

        Parameters
        ----------
        macro_name : str
            The name of the macro.
        timeout : float
            The number of seconds to allow a script to run before canceling it;
             -1 indicates no timeout.
        """
        self._instance.setMacroTimeout(macro_name, timeout)
