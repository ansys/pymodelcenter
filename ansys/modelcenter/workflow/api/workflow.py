from typing import (
    TYPE_CHECKING,
    AbstractSet,
    Any,
    Collection,
    Iterable,
    List,
    Mapping,
    Optional,
    Tuple,
    Union,
)

import ansys.common.variableinterop as acvi
from ansys.common.variableinterop import IVariableValue
from ansys.engineeringworkflow.api import (
    IControlStatement,
    IElement,
    IVariable,
    IWorkflowInstance,
    Property,
    WorkflowInstanceState,
)
import clr
from overrides import overrides

from . import DataExplorer
from .datamonitor import DataMonitor
from .i18n import i18n
from .icomponent import IComponent
from .variable_links import VariableLink, dotnet_links_to_iterable

if TYPE_CHECKING:
    from .engine import Engine
clr.AddReference(r"phoenix-mocks\Phoenix.Mock.v45")
import Phoenix.Mock as phxmock

from ansys.modelcenter.workflow.api.assembly import Assembly


class MockDataMonitorWrapper(DataMonitor):
    """Maps a COM MockDataMonitor to the IDataMonitor interface."""

    def __init__(self, monitor: phxmock.MockDataMonitor):
        """
        Initialize.
        """


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


class Workflow(IWorkflowInstance):
    """Represents a Workflow or Model in ModelCenter."""

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
        self._state = WorkflowInstanceState.UNKNOWN

# IWorkflowInstance

    @overrides
    def get_state(self) -> WorkflowInstanceState:
        if self._instance.getHaltStatus():
            return WorkflowInstanceState.PAUSED
        return self._state

    @overrides
    def run(self, inputs: Mapping[str, acvi.VariableState], reset: bool,
            validation_ids: AbstractSet[str]) -> Mapping[str, acvi.VariableState]:
        raise NotImplementedError

    @overrides
    def start_run(self, inputs: Mapping[str, acvi.VariableState], reset: bool,
                  validation_ids: AbstractSet[str]) -> str:
        raise NotImplementedError

    @overrides
    def get_root(self) -> IControlStatement:
        assembly = self._instance.getModel()
        if assembly is None:
            return None
        return Assembly(assembly)

    @overrides
    def get_element_by_id(self, element_id: str) -> IElement:
        raise NotImplementedError

# ModelCenter specific

    @staticmethod
    def value_to_variable_value(value: Any) -> acvi.IVariableValue:
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
            return acvi.BooleanValue(value)
        elif isinstance(value, int):
            return acvi.IntegerValue(value)
        elif isinstance(value, float):
            return acvi.RealValue(value)
        elif isinstance(value, str):
            return acvi.StringValue(value)
        elif isinstance(value, list):
            first = value[0]
            if isinstance(first, bool):
                return acvi.BooleanArrayValue(values=value)
            elif isinstance(first, int):
                return acvi.IntegerArrayValue(values=value)
            elif isinstance(first, float):
                return acvi.RealArrayValue(values=value)
            elif isinstance(first, str):
                return acvi.StringArrayValue(values=value)
        raise TypeError

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

        Parameters
        ----------
        var_name :  str
            Full ModelCenter path of the variable.

        Returns
        -------
        The value as one of the IVariableValue types.
        """
        value = self._instance.getValue(var_name)
        return Workflow.value_to_variable_value(value)

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
            def get_position_x(self) -> int:
                pass

            def get_position_y(self) -> int:
                pass

            @property
            def pacz_url(self):
                pass

            @property
            def element_id(self) -> str:
                pass

            @property
            def parent_element_id(self) -> str:
                pass

            def get_property(self, property_name: str) -> Property:
                pass

            def get_properties(self) -> Collection[Property]:
                pass

            def set_property(self, property_name: str, property_value: IVariableValue) -> None:
                pass

            @overrides
            def get_variables(self) -> Collection[IVariable]:
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

            @property  # type: ignore
            @overrides
            def name(self) -> str:
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
        self._state = WorkflowInstanceState.SUCCESS

    # Skip IDispatch* createJobManager([optional]VARIANT showProgressDialog);

    def trade_study_start(self) -> None:
        self._instance.tradeStudyStart()
        self._state = WorkflowInstanceState.RUNNING

    def get_halt_status(self) -> bool:
        """
        Finds out if the user has pressed the halt button.

        Returns
        -------
        Boolean True for yes or False for no.
        """
        return self._instance.getHaltStatus()

    def get_value_absolute(self, var_name: str) -> acvi.IVariableValue:
        """
        Gets the value of a variable without validating it.

        Parameters
        ----------
        var_name : str
            Full ModelCenter Path of the variable.

        Returns
        -------
        The value as a variant.
        """
        value = self._instance.getValueAbsolute(var_name)
        return Workflow.value_to_variable_value(value)

    def set_scheduler(self, schedular: str) -> None:
        """
        Sets the current active scheduler for the Model.

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
        self._instance.setScheduler(schedular)

    def remove_component(self, name: str) -> None:
        """
        Removes the specified component from the Model.

        Parameters
        ----------
        name :
            Full ModelCenter path of the component to remove.
        """
        self._instance.removeComponent(name)

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
    def create_assembly(self, name: str, parent: str, assembly_type: Optional[str] = None):
        return self._instance.createAssembly(name, parent, assembly_type)

    # IDispatch* createAssemblyVariable(BSTR name, BSTR type, BSTR parent);
    def create_assembly_variable(self, name: str, type_: str, parent: str) ->\
            acvi.CommonVariableMetadata:
        """
        Create a new variable in an Assembly.

        Possible variable types are:
          - double
          - int
          - boolean
          - string
          - file
          - double[]
          - int[]
          - boolean[]
          - string[]
          - quadfacet
          - surfaceofrevolution
          - nurbs
          - bspline
          - ruled
          - skinned
          - vrml
          - node

        Parameters
        ----------
        name : str
            Desired name of the new variable.
        type_ : str
            Type of the new variable.
        parent : str
            Full path of the parent Assembly.

        Returns
        -------
        CommonVariableMetadata :
            Created variable metadata.
        """
        return self._convert_variable(self._instance.createAssemblyVariable(name, type_, parent))

    @staticmethod
    def _convert_variable(variable: object) -> acvi.CommonVariableMetadata:
        """
        Convert IVariable object into appropriate CommonVariableMetadata implementation.

        Parameters
        ----------
        variable : object
            IVariable object containing variable data.
        """
        metadata: acvi.CommonVariableMetadata = None
        type_: str = variable.getType()
        is_array: bool = False
        if type_.endswith('[]'):
            is_array = True
            type_ = type_[:-2]

        if type_ == 'boolean':
            if is_array:
                metadata = acvi.BooleanArrayMetadata()
            else:
                metadata = acvi.BooleanMetadata()
            metadata.description = variable.description
        elif type_ == 'double':
            if is_array:
                metadata = acvi.RealArrayMetadata()
            else:
                metadata = acvi.RealMetadata()
            metadata.description = variable.description
            metadata.units = variable.units
            metadata.display_format = variable.format
            metadata.lower_bound = variable.lowerBound
            metadata.upper_bound = variable.upperBound
            metadata.enumerated_values = acvi.RealArrayValue.from_api_string(variable.enumValues)
            metadata.enumerated_aliases =\
                acvi.StringArrayValue.from_api_string(variable.enumAliases)
        elif type_ == 'integer':
            if is_array:
                metadata = acvi.IntegerArrayMetadata()
            else:
                metadata = acvi.IntegerMetadata()
            metadata.description = variable.description
            metadata.lower_bound = variable.lowerBound
            metadata.upper_bound = variable.upperBound
            metadata.enumerated_values = acvi.IntegerArrayValue.from_api_string(variable.enumValues)
            metadata.enumerated_aliases =\
                acvi.StringArrayValue.from_api_string(variable.enumAliases)
        elif type_ == 'string':
            if is_array:
                metadata = acvi.StringArrayMetadata()
            else:
                metadata = acvi.StringMetadata()
            metadata.description = variable.description
            metadata.enumerated_values = acvi.StringArrayValue.from_api_string(variable.enumValues)
            metadata.enumerated_aliases =\
                acvi.StringArrayValue.from_api_string(variable.enumAliases)
        else:
            raise NotImplementedError

        # TODO: Add remaining types.
        # TODO: Copying custom metadata is not possible due to lack of getMetaDataKeys.

        return metadata

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

    def run(self, variable_array: Optional[str]) -> None:
        """
        Runs a specified set of variables in the workflow.

        Parameters
        ----------
        variable_array: Optional[str]
            A comma-separated list of variables to validate.
            If no variables are specified, then the entire workflow
            will be run.
        """
        self._instance.run(variable_array or "")

    def get_data_monitor(self, component: str, index: int) -> DataMonitor:
        """
        Get the DataMonitor at the given index for the given component.

        Parameters
        ----------
        component: str
            The name of the component.
        index: int
            The index of the DataMonitor in the component.

        Returns
        -------
        The component's DataMonitor at the given index.
        """

        dm_object: phxmock.MockDataMonitor = self._instance.getDataMonitor(component, index)
        return DataMonitor(dm_object)

    def create_data_monitor(self, component: str, name: str, x: int, y: int) -> object:
        """
        Create a DataMonitor associated with the specified component.

        Parameters
        ----------
        component: str
            The name of the component to associate the DataMonitor with.
        name: str
            The name of the DataMonitor.
        x: int
            The x-position of the DataMonitor.
        y: int
            The y-position of the DataMonitor.

        Returns
        -------
        The created DataMonitor.
        """

        dm_object: phxmock.MockDataMonitor = self._instance.createDataMonitor(component, name, x, y)
        return DataMonitor(dm_object)

    def remove_data_monitor(self, component: str, index: int) -> bool:
        """
        Remove the DataMonitor at the given index for the given component.

        Parameters
        ----------
        component: str
            The name of the component.
        index: int
            The index of the DataMonitor in the component.

        Returns
        -------
        True if the component had a DataMonitor at the given index.
        """
        return self._instance.removeDataMonitor(component, index)

    def get_data_explorer(self, index: int) -> Optional[DataExplorer]:
        """
        Get the specified DataExplorer.

        Parameters
        ----------
        index: int
            The index of the DataExplorer.

        Returns
        -------
        The DataExplorer at the given index.
        """
        de_object: object = self._instance.getDataExplorer(index)
        if de_object is None:
            return None
        else:
            return DataExplorer(de_object)

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
            assembly = self._instance.getModel()
        else:
            assembly = self._instance.getAssembly(name)
        if assembly is None:
            return None
        return Assembly(assembly)

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
    def get_variable_meta_data(self, name: str) -> acvi.CommonVariableMetadata:
        """
        Get metadata from a variable.

        Throws an exception if the variable is not found.

        Parameters
        ----------
        name : str
            The full name of the variable.

        Returns
        -------
        CommonVariableMetadata :
            The metadata, in the form of a CommonVariableMetadata
            implementation.
        """
        metadata: acvi.CommonVariableMetadata = None
        variable = self._instance.getVariableMetaData(name)  # PHXDATAHISTORYLib.IDHVariable
        is_array: bool = variable.type.endswith('[]')
        type_: str = variable.type[:-2] if is_array else variable.type

        if type_ == 'double':
            if is_array:
                metadata = acvi.RealArrayMetadata()
            else:
                metadata = acvi.RealMetadata()
            # TODO: Where do other metadata come from? variable.getMetaData?
            # metadata.description =
            # metadata.units =
            # metadata.display_format =
            metadata.lower_bound = variable.lowerBound
            metadata.upper_bound = variable.upperBound
            metadata.enumerated_values = acvi.RealArrayValue.from_api_string(variable.enumValues)
            metadata.enumerated_aliases =\
                acvi.StringArrayValue.from_api_string(variable.enumAliases)

        elif type_ == 'integer':
            if is_array:
                metadata = acvi.IntegerArrayMetadata()
            else:
                metadata = acvi.IntegerMetadata()
            metadata.lower_bound = variable.lowerBound
            metadata.upper_bound = variable.upperBound
            metadata.enumerated_values = acvi.IntegerArrayValue.from_api_string(variable.enumValues)
            metadata.enumerated_aliases =\
                acvi.StringArrayValue.from_api_string(variable.enumAliases)

        elif type_ == 'boolean':
            if is_array:
                metadata = acvi.BooleanArrayMetadata()
            else:
                metadata = acvi.BooleanMetadata()

        elif type_ == 'string':
            if is_array:
                metadata = acvi.StringArrayMetadata()
            else:
                metadata = acvi.StringMetadata()
            metadata.enumerated_values = acvi.StringArrayValue.from_api_string(variable.enumValues)
            metadata.enumerated_aliases =\
                acvi.StringArrayValue.from_api_string(variable.enumAliases)
        else:
            raise NotImplementedError

        # TODO: Add remaining types.
        if metadata is not None:
            # Copy custom metadata.
            keys = variable.getMetaDataKeys()
            for key in keys:
                metadata.custom_metadata[key] = variable.getMetaData(key)
        return metadata

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
