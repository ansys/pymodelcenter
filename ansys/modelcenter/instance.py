class Instance:
    def __init__(self):
        pass

    # BSTR modelDirectory;
    @property
    def model_directory(self) -> str:
        pass

    # BSTR modelFileName;
    @property
    def model_file_name(self) -> str:
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
    def save_model(self) -> None:
        pass

    # void saveModelAs(BSTR fileName);
    def save_model_as(self, file_name: str) -> None:
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

    # boolean getHaltStatus();
    def get_halt_status(self) -> bool:
        pass

    # IDispatch* getModel();
    def get_model(self) -> object:  # IAssembly
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

    # IDispatch* getAssembly(BSTR name);
    def get_assembly(self, name: str) -> object:    # IAsempty
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
    def get_variable_mata_data(self, name: str) -> object:  # PHXDATAHISTORYLib.IDHVariable
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
