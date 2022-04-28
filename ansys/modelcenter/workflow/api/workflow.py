from typing import Any, Tuple

from ansys.common.variableinterop import (
    BooleanArrayValue,
    BooleanValue,
    IntegerArrayValue,
    IntegerValue,
    IVariableValue,
    RealArrayValue,
    RealValue,
    StringArrayValue,
    StringValue,
)
from ansys.modelcenter.workflow.api.IAssembly import IAssembly


class Workflow:
    """Represents a Workflow or Model in  ModelCenter."""

    def __init__(self, modelcenter: Any):
        """
        Initialize a new Workflow instance.

        Parameters
        ----------
        modelcenter : object
            The row interface object to use to make direct calls to
            ModelCenter.
        """
        self.__modelcenter = modelcenter

    @staticmethod
    def value_to_variable_value(value: Any) -> IVariableValue:
        """
        Convert the given python value to the appropriate \
        IVariableValue type.

        Supported types: bool, int, float, str, and list of the same.

        Parameters
        ----------
        value : Any
            The python type to convert.
        Returns
        -------
        An IVariableValue type appropriate for the value given.
        """
        if isinstance(value, bool):
            return BooleanValue(value)
        elif isinstance(value, int):
            return IntegerValue(value)
        elif isinstance(value, float):
            return RealValue(value)
        elif isinstance(value, str):
            return StringValue(value)
        elif isinstance(value, list):
            first = value[0]
            if isinstance(first, bool):
                return BooleanArrayValue(values=value)
            elif isinstance(first, int):
                return IntegerArrayValue(values=value)
            elif isinstance(first, float):
                return RealArrayValue(values=value)
            elif isinstance(first, str):
                return StringArrayValue(values=value)
        raise TypeError

    @property
    def workflow_directory(self) -> str:
        """
        Directory of the current Workflow.

        If no workflow is open it will raise an error. If the model has
        not yet been saved, it will return an empty string.
        """
        return self.__modelcenter.modelDirectory

    @property
    def workflow_file_name(self) -> str:
        """Full path of the current Workflow."""
        return self.__modelcenter.modelFileName

    def set_value(self, var_name: str, value: str) -> None:
        """
        Set the value of a variable.

        Parameters
        ----------
        var_name : str
            Full ModelCenter path of the variable.
        value : str
            The New serialized value to set variable to.
        """
        if isinstance(value, IVariableValue):
            api_value = value.to_api_string()
        else:
            api_value = str(value)
        self.__modelcenter.setValue(var_name, api_value)

    def get_value(self, var_name: str) -> object:
        """
        Get the value of a variable.

        Parameters
        ----------
        var_name :  str
            Full ModelCenter path of the variable.

        Returns
        -------
        The value as one of the IVariableValue types.
        """
        value = self.__modelcenter.getValue(var_name)
        return Workflow.value_to_variable_value(value)

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
        pass

    # IDispatch* getVariable(BSTR name);
    #   IDoubleVariable IDoubleArray IBooleanVariable IIntegerVariable IReferenceVariable
    #   IObjectVariable IFileVariable IStringVariable IBooleanArray IIntegerArray IReferenceArray
    #   IFileArray IStringArray IGeometryVariable:
    def get_variable(self, name: str) -> object:
        pass

    # IDispatch* getComponent(BSTR name);
    def get_component(self, name: str) -> object:   # IComponenet, IIfComponenet, IScriptComponent
        pass

    # void tradeStudyEnd();
    def trade_study_end(self) -> None:
        pass

    # Skip IDispatch* createJobManager([optional]VARIANT showProgressDialog);

    # void tradeStudyStart();
    def trade_study_start(self) -> None:
        pass

    def get_halt_status(self) -> bool:
        """
        Finds out if the user has pressed the halt button.

        A wrapper around the IModelCenter.getHaltStatus() method.

        Returns
        -------
        Boolean True for yes or False for no.
        """
        return self.__modelcenter.getHaltStatus()

    def get_value_absolute(self, var_name: str) -> IVariableValue:
        """
        Gets the value of a variable without validating it.

        A wrapper around the IModelCenter.getValueAbolute(BSTR varName)
        method.

        Parameters
        ----------
        var_name : str
            Full ModelCenter Path of the variable.

        Returns
        -------
        The value as a variant.
        """
        value = self.__modelcenter.getValueAbsolute(var_name)
        return Workflow.value_to_variable_value(value)

    def set_scheduler(self, schedular: str) -> None:
        """
        Sets the current active scheduler for the Model.

        A wrapper around the IModelCenter.setScheduler(BSTR varName)
        method.

        Parameters
        ----------
        schedular : str
            The scheduler type. Possible types are:
                * forward
                * backward
                * mixed
                * script
            Note: all scheduler types are case-sensitive.
        """
        self.__modelcenter.setScheduler(schedular)

    def remove_component(self, name: str) -> None:
        """
        Removes the specified component from the Model.

        A wrapper around the IModelCenter.removeComponent(BSTR name)
        method.

        Parameters
        ----------
        name :
            Full ModelCenter path of the component to remove.
        """
        self.__modelcenter.removeComponent(name)

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

    def get_assembly(self, name: str = None) -> object:    # IAssembly
        """Gets the named assembly or the top level assembly."""
        if name is None or name == "":
            assembly = self.__modelcenter.getModel()
        else:
            assembly = self.__modelcenter.getAssembly(name)
        if assembly is None:
            return None
        return IAssembly(assembly)

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
