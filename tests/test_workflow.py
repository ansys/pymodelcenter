"""Tests for Workflow."""
from typing import Any, Iterable, List, Optional, Type

import clr

clr.AddReference('phoenix-mocks/Phoenix.Mock.v45')
from Phoenix.Mock import (
    MockBooleanArray,
    MockBooleanVariable,
    MockDoubleArray,
    MockDoubleVariable,
    MockIntegerArray,
    MockIntegerVariable,
    MockModelCenter,
    MockStringArray,
    MockStringVariable,
)
from System import Boolean as DotNetBoolean
from System import Double as DotNetDouble
from System import Int64 as DotNetInt64
from System import Object as DotNetObject
from System import String as DotNetString
from System.Collections.Generic import List as DotNetList
import ansys.common.variableinterop as acvi
import pytest

import ansys.modelcenter.workflow.api as mcapi

mock_mc: Optional[Any] = None
"""
Mock ModelCenter object.

Used to simulate ModelCenter's response to different API calls.
"""

workflow: Optional[mcapi.Workflow] = None
"""
Workflow object under test.
"""


def setup_function(_):
    """
    Setup called before each test function in this module.

    Parameters
    ----------
    _ :
        The function about to test.
    """
    global mock_mc, workflow
    # To use when Engine supports injection of ModelCenter:
    # mock_mc = MockModelCenter()
    # engine = mcapi.Engine(mock_mc)
    engine = mcapi.Engine()
    mock_mc = engine._instance
    workflow = engine.new_workflow("workflow.pxcz")


def py_list_to_net_list(src: List) -> DotNetList:
    """
    Convert the given Python-list to a DotNet-Object-List.

    Parameters
    ----------
    src : List
        Python list to convert, each entry will become an entry in the
        resulting dot net list.

    Returns
    -------
    A DotNetList of objects. i.e. in DotNet terminology: List<Object>
    """
    result = DotNetList[DotNetObject]()
    for item in src:
        if isinstance(item, list):
            item_list = py_list_to_net_typed_list(item)
            result.Add(item_list)
        else:
            result.Add(item)
    return result


def py_list_to_net_typed_list(src: List) -> DotNetList:
    """
    Convert the given Python-list to a DotNet-List of the appropriate \
    primitive type.

    Types are one of four different primitive types.  For Python the
    types are: bool, int, float or str.  For Dot Net the type are:
    Boolean, Int64, Double and String.

    Parameters
    ----------
    src : List
        Python list to convert, each entry will become an entry in the
        resulting dot net list.  The first item in the list is used
        to determine the type of list.

    Returns
    -------
    A DotNet list of one of the DotNet primitive types.  i.e.
    List<Boolean>, List<Int64>, List<Double> or List<String>.
    """
    first = src[0]
    if isinstance(first, bool):
        result = DotNetList[DotNetBoolean]()
    elif isinstance(first, int):
        result = DotNetList[DotNetInt64]()
    elif isinstance(first, float):
        result = DotNetList[DotNetDouble]()
    elif isinstance(first, str):
        result = DotNetList[DotNetString]()
    else:
        raise TypeError
    for item in src:
        result.Add(item)
    return result


def test_get_component():
    # Setup
    global workflow, mock_mc
    mock_mc.createComponent("a", "word", "a", 0, 0)

    # SUT
    result: mcapi.IComponent = workflow.get_component("a.word")

    # Verification
    assert result.get_name() == "word"


def test_get_component_missing():
    # Setup
    global workflow, mock_mc

    # SUT
    with pytest.raises(Exception) as except_info:
        workflow.get_component("a.word")

    # Verification
    assert except_info.value.args[0] == "Error: A component with the given name was not found."


def test_trade_study_start():
    # Setup
    global workflow, mock_mc

    # SUT
    workflow.trade_study_start()

    # Verification
    assert mock_mc.getCallCount("tradeStudyStart") == 1


def test_trade_study_end():
    # Setup
    global workflow, mock_mc

    # SUT
    workflow.trade_study_end()

    # Verification
    assert mock_mc.getCallCount("tradeStudyEnd") == 1


def test_workflow_close():
    # Setup
    sut_engine = mcapi.Engine()
    sut_workflow: mcapi.Workflow = sut_engine.new_workflow("workflow.pxcz")

    # Check pre-reqs.
    with pytest.raises(Exception) as except_info:
        sut_engine.new_workflow("workflow2.pxcz")

    # Execute
    sut_workflow.close_workflow()

    # Verify
    assert except_info.value.args[0] == "Error: Only one Workflow can be open at a time. "\
        "Close the current Workflow before loading or creating a new one."
    next_workflow = sut_engine.new_workflow("workflow.pxcz")
    assert isinstance(next_workflow, mcapi.Workflow)
    assert sut_engine._instance.getCallCount("closeModel") == 1


def test_save_workflow():
    # Setup
    sut_engine = mcapi.Engine()
    sut_workflow: mcapi.Workflow = sut_engine.new_workflow("workflow.pxcz")
    assert sut_workflow._instance.getCallCount("saveModel") == 0

    # Execute
    sut_workflow.save_workflow()

    # Verify
    assert sut_workflow._instance.getCallCount("saveModel") == 1


def test_save_workflow_as():
    # Setup
    sut_engine = mcapi.Engine()
    sut_workflow: mcapi.Workflow = sut_engine.new_workflow("workflow.pxcz")
    assert sut_workflow._instance.getCallCount("saveModelAs") == 0

    # Execute
    sut_workflow.save_workflow_as(r"C:\Temp\workflow.pxcz")

    # Verify
    assert sut_workflow._instance.getCallCount("saveModelAs") == 1
    argument = sut_workflow._instance.getArgumentRecord("saveModelAs", 0)[0]
    assert argument == r"C:\Temp\workflow.pxcz"


@pytest.mark.parametrize(
    'server_path,parent,name,x_pos,y_pos,expected_passed_x_pos,expected_passed_y_pos',
    [
        pytest.param('saserv://tests/add42', 'Adder', 'Workflow.model.workflow.model', 47, 42,
                     47, 42, id="fully specified position"),
        # It's difficult to test these cases, because the mock expects Missing.Value,
        # and that really screws with the reflection-based method matching in pythonnet,
        # since it seems Missing.Value has special meaning in that case.
        # Passing None doesn't work and neither does leaving the method off.
        # This is probably something that the real GRPC api will have to solve.
        # pytest.param('saserv://tests/add42', 'Adder', 'Workflow.model.workflow.model', None, 42,
        #             Missing.Value, 42, id="missing x value"),
        # pytest.param('saserv://tests/add42', 'Adder', 'Workflow.model.workflow.model', 47, None,
        #             47, Missing.Value, id="missing y value")
    ]
)
def test_create_component(
        server_path: str,
        name: str,
        parent: str,
        x_pos: Optional[object],
        y_pos: Optional[object],
        expected_passed_x_pos,
        expected_passed_y_pos
) -> None:
    # Setup
    sut_engine = mcapi.Engine()
    sut_workflow: mcapi.Workflow = sut_engine.new_workflow("workflow.pxcz")
    assert sut_workflow._instance.getCallCount("createComponent") == 0

    # Execute
    sut_workflow.create_component(server_path, name, parent, x_pos, y_pos)

    # Verify
    assert sut_workflow._instance.getCallCount("createComponent") == 1
    assert sut_workflow._instance.getArgumentRecord("createComponent", 0) == [
        server_path, name, parent, expected_passed_x_pos, expected_passed_y_pos]


def test_create_link() -> None:
    # Setup
    sut_engine = mcapi.Engine()
    sut_workflow: mcapi.Workflow = sut_engine.new_workflow("workflow.pxcz")
    assert sut_workflow._instance.getCallCount("createLink") == 0
    test_var_name = "inputs.var1"
    test_eqn = "Workflow.comp.output4"

    # Execute
    sut_workflow.create_link(test_var_name, test_eqn)

    # Verify
    assert sut_workflow._instance.getCallCount("createLink") == 1
    assert sut_workflow._instance.getArgumentRecord("createLink", 0) == [
        test_var_name, test_eqn
    ]


def test_get_variable() -> None:
    # Setup
    sut_engine = mcapi.Engine()
    sut_workflow: mcapi.Workflow = sut_engine.new_workflow("workflow.pxcz")
    test_var_name = "test_assembly_var"
    sut_workflow._instance.createAssemblyVariable(test_var_name, "Input", "Model")
    assert sut_workflow._instance.getCallCount("getVariable") == 0

    # Execute
    result = sut_workflow.get_variable("Model.test_assembly_var")

    # Verify
    assert sut_workflow._instance.getCallCount("getVariable") == 1
    assert sut_workflow._instance.getArgumentRecord("getVariable", 0) == ["Model.test_assembly_var"]
    assert result._variable.getFullName() == "Model.test_assembly_var"


def test_workflow_directory() -> None:
    """
    Testing of workflow_directory method.
    """
    global mock_mc, workflow
    mock_mc.modelDirectory = "D:\\Some\\Path\\model.ext"
    mock_mc.clearCallCounts()

    # SUT
    result = workflow.workflow_directory

    # Verify
    assert isinstance(result, str)
    assert result == "D:\\Some\\Path\\model.ext"
    # assert mock_mc.getCallCount("modelDirectory") == 1
    assert mock_mc.getTotalCallCount() == 1


def test_workflow_file_name():
    """
    Testing of workflow_file_name method.
    """
    global mock_mc, workflow
    mock_mc.modelFileName = "model.ext"
    mock_mc.clearCallCounts()

    # SUT
    result = workflow.workflow_file_name

    # Verify
    assert isinstance(result, str)
    assert result == "model.ext"
    # assert mock_mc.getCallCount("modelFileName") == 1
    assert mock_mc.getTotalCallCount() == 1


set_value_tests = [
    pytest.param(acvi.BooleanValue(True), "True", id="bool"),
    pytest.param(acvi.IntegerValue(42), "42", id="int"),
    pytest.param(acvi.RealValue(3.14), "3.14", id="read"),
    pytest.param(acvi.StringValue("strVal"), "strVal", id="str"),
    pytest.param(acvi.BooleanArrayValue(values=[True, False]), "True,False", id="bool[]"),
    pytest.param(acvi.IntegerArrayValue(values=[86, 42]), "86,42", id="int[]"),
    pytest.param(acvi.RealArrayValue(values=[0.717, 1.414]), "0.717,1.414", id="real[]"),
    pytest.param(acvi.StringArrayValue(values=["one", "two"]), '"one","two"', id="str[]"),
    pytest.param("Some String", "Some String", id="raw str"),
    pytest.param(14.44, "14.44", id="raw float"),
]


@pytest.mark.parametrize("src,expected", set_value_tests)
def test_set_value(src: Any, expected: str):
    """
    Testing of set_value method.
    """
    global mock_mc, workflow

    # SUT
    workflow.set_value("var.name", src)

    # Verify
    assert mock_mc.getCallCount("setValue") == 1
    args = mock_mc.getLastArgumentRecord("setValue")
    assert args[0] == "var.name"
    result = args[1]
    assert type(result) == str
    assert result == expected


get_value_tests = [
    pytest.param("root.b", acvi.BooleanValue(False), id="bool"),
    pytest.param("root.i", acvi.IntegerValue(42), id="int"),
    pytest.param("root.r", acvi.RealValue(3.14), id="real"),
    pytest.param("root.s", acvi.StringValue("sVal"), id="str"),
    pytest.param("root.ba", acvi.BooleanArrayValue(values=[True, False, True]), id="bool array"),
    pytest.param("root.ia", acvi.IntegerArrayValue(values=[86, 42, 1]), id="int array"),
    pytest.param("root.ra", acvi.RealArrayValue(values=[1.414, 0.717, 3.14]), id="real array"),
    pytest.param("root.sa", acvi.StringArrayValue(values=["one", "two", "three"]), id="str array"),
]
"""Collection of tests for get_value, used in test_get_value."""


def setup_test_values():
    """
    Setup some values usable of testing get_value and \
    get_value_absolute.
    """
    global mock_mc
    mock_mc.createAssemblyVariable('b', "Input", "root")
    mock_mc.createAssemblyVariable('i', "Input", "root")
    mock_mc.createAssemblyVariable('r', "Input", "root")
    mock_mc.createAssemblyVariable('s', "Input", "root")
    mock_mc.createAssemblyVariable('ba', "Input", "root")
    mock_mc.createAssemblyVariable('ia', "Input", "root")
    mock_mc.createAssemblyVariable('ra', "Input", "root")
    mock_mc.createAssemblyVariable('sa', "Input", "root")
    vars_ = py_list_to_net_typed_list([
        'root.b', 'root.i', 'root.r', 'root.s',
        'root.ba', 'root.ia', 'root.ra', 'root.sa'
    ])
    vals = py_list_to_net_list([
        False, 42, 3.14, "sVal",
        [True, False, True],
        [86, 42, 1],
        [1.414, 0.717, 3.14],
        ["one", "two", "three"]
    ])
    mock_mc.SetMockValues(vars_, vals)


@pytest.mark.parametrize("var_name,expected", get_value_tests)
def test_get_value(var_name: str, expected: acvi.IVariableValue):
    """
    Testing of get_value_tests method pulling each of the different
    variable types.
    """
    global mock_mc, workflow
    setup_test_values()

    # SUT
    result = workflow.get_value(var_name)

    # Verify
    assert result == expected
    assert type(result) == type(expected)
    assert mock_mc.getCallCount("getValue")


@pytest.mark.parametrize(
    "halted", [pytest.param(False, id="running"), pytest.param(True, id="halted")]
 )
def test_get_halt_status(halted: bool):
    """Testing of get_halt_status method."""
    global mock_mc, workflow
    if halted:
        mock_mc.halt()

    # SUT
    result = workflow.get_halt_status()

    # Verify
    assert result == halted
    assert type(result) == bool
    assert mock_mc.getCallCount("getHaltStatus")


value_absolute_tests = get_value_tests.copy()
"""Collection of test for get_value_absolute.

Reusing the tests for get_values, but then adding some additional tests
below."""

value_absolute_tests.extend([
    pytest.param("root.ba[1]", acvi.BooleanValue(False), id="bool array indexed"),
    pytest.param("root.ia[2]", acvi.IntegerValue(1), id="int array indexed"),
    pytest.param("root.ra[0]", acvi.RealValue(1.414), id="real array indexed"),
    pytest.param("root.sa[1]", acvi.StringValue("two"), id="str array indexed"),
])


@pytest.mark.parametrize(
    "var_name,expected", value_absolute_tests
)
def test_get_value_absolute(var_name: str, expected: acvi.IVariableValue):
    """
    Testing of get_value_tests method pulling each of the different \
    variable types.
    """
    global mock_mc, workflow
    setup_test_values()

    # SUT
    result = workflow.get_value_absolute(var_name)

    # Verify
    assert result == expected
    assert type(result) == type(expected)
    assert mock_mc.getCallCount("getValueAbsolute")


@pytest.mark.parametrize("schedular", ["forward", "backward", "mixed", "script"])
def test_set_scheduler(schedular: str) -> None:
    """
    Testing of set_scheduler method with different schedular values
    Parameters
    ----------
    schedular :  str
        schedular value to test
    """
    global mock_mc, workflow

    # SUT
    workflow.set_scheduler(schedular)

    # Verify
    assert mock_mc.getCallCount("setScheduler") == 1
    args: list = mock_mc.getLastArgumentRecord("setScheduler")
    assert len(args) == 1
    assert args[0] == schedular


def test_remove_component():
    """ Testing of remove_component method."""
    global mock_mc, workflow

    # SUT
    workflow.remove_component("componentName")

    # Verify
    assert mock_mc.getCallCount("removeComponent")
    args: list = mock_mc.getLastArgumentRecord("removeComponent")
    assert len(args) == 1
    assert args[0] == "componentName"


@pytest.mark.parametrize(
    "name,get_model_call_count,get_assembly_call_count,result_type",
    [
        pytest.param(None,           2, 0, mcapi.Assembly,  id="root"),
        pytest.param("root.aName",   1, 1, mcapi.Assembly,  id="named"),
        pytest.param("root.noExist", 1, 1, None,       id="missing")
    ]
)
def test_get_assembly(
        name: str, get_model_call_count: int, get_assembly_call_count: int, result_type: Type):
    """
    Testing of get_assembly.

    Parameters
    ----------
    name : str
        name of assembly to request.
    get_model_call_count : int
        expected call count of IModelCenter.getModel
    get_assembly_call_count : int
        expected call count of IModelCenter.getAssembly
    result_type : Type or None
        expected type of result, or None is expected to return None
    """
    global mock_mc, workflow
    mock_mc.createAssembly("aName", "root", "aType")

    # SUT
    result = workflow.get_assembly(name)

    # Verify
    if result_type is None:
        assert result is None
    else:
        assert type(result) == result_type
    # MockModelCenter.getAssembly doesn't have call tracking enabled
    # assert mock_mc.getCallCount("getAssembly") == get_assembly_call_count
    assert mock_mc.getCallCount("getModel") == get_model_call_count


def test_create_data_explorer():
    """
    Verify that create_data_explorer works as expected.
    """
    # Setup
    global mock_mc, workflow

    # SUT
    de: mcapi.DataExplorer = workflow.create_data_explorer("MockTradeStudyType", "Mock Setup")

    # Verification
    assert mock_mc.getCallCount("createDataExplorer") == 1
    assert de is not None


def _setup_variables(mc: MockModelCenter) -> None:
    """
    Setup various mock variables along with values.

    Parameters
    ----------
    mc : MockModelCenter
        MockModelCenter to be set up with variables.
    """
    variables = DotNetList[DotNetObject]()
    values = DotNetList[DotNetObject]()

    # Boolean
    var = MockBooleanVariable("model.boolean", 0)
    var.description = "Boolean value in Model."
    variables.Add(var)
    values.Add(True)

    # Integer
    var = MockIntegerVariable("model.integer", 0)
    var.lowerBound = 0
    var.upperBound = 5
    var.units = "persons"
    var.description = "Integer value in Model."
    var.format = "a format"
    var.enumValues = "1, 2, 3"
    var.enumAliases = "one, two, three"
    variables.Add(var)
    values.Add(3)

    # Double
    var = MockDoubleVariable("model.double", 0)
    var.lowerBound = -10
    var.upperBound = 15
    var.units = "m/s"
    var.description = "Double value in Model."
    var.format = "mock format"
    var.enumValues = "1.0, 2.1, 3.0"
    var.enumAliases = "one, more_than_two, three"
    variables.Add(var)
    values.Add(3.75)

    # String
    var = MockStringVariable("model.string", 0)
    var.description = "String value in Model."
    var.enumValues = "\"one\" \"two\" \"three\""
    var.enumAliases = "One Two Three"
    variables.Add(var)
    values.Add("Capsule 1")

    # Boolean[]
    var = MockBooleanArray("model.booleans", 0)
    var.description = "Boolean array in Model."
    variables.Add(var)
    values.Add(True)  # ?

    # Integer[]
    var = MockIntegerArray("model.integers", 0)
    var.lowerBound = 0
    var.upperBound = 5
    var.units = "persons"
    var.description = "Integer array in Model."
    var.format = "a format"
    var.enumValues = "1, 2, 3"
    var.enumAliases = "one, two, three"
    variables.Add(var)
    values.Add(3)

    # Double[]
    var = MockDoubleArray("model.doubles", 0)
    var.lowerBound = -10
    var.upperBound = 15
    var.units = "m/s"
    var.description = "Double array in Model."
    var.format = "mock format"
    var.enumValues = "1.0, 2.1, 3.0"
    var.enumAliases = "one, more_than_two, three"
    variables.Add(var)
    values.Add(3.75)

    # String[]
    var = MockStringArray("model.strings", 0)
    var.description = "String array in Model."
    var.enumValues = "\"one\" \"two\" \"three\""
    var.enumAliases = "One Two Three"
    variables.Add(var)
    values.Add("Capsule 1")

    mc.SetMockVariables(variables, values)


def test_get_variable_meta_data() -> None:
    # Setup
    _setup_variables(mock_mc)

    # SUT
    boolean_metadata = workflow.get_variable_meta_data("model.boolean")
    integer_metadata = workflow.get_variable_meta_data("model.integer")
    double_metadata = workflow.get_variable_meta_data("model.double")
    string_metadata = workflow.get_variable_meta_data("model.string")
    boolean_array_metadata = workflow.get_variable_meta_data("model.booleans")
    integer_array_metadata = workflow.get_variable_meta_data("model.integers")
    double_array_metadata = workflow.get_variable_meta_data("model.doubles")
    string_array_metadata = workflow.get_variable_meta_data("model.strings")

    # Verification
    assert mock_mc.getCallCount("getVariableMetaData") == 8

    assert boolean_metadata.variable_type == acvi.VariableType.BOOLEAN
    assert integer_metadata.variable_type == acvi.VariableType.INTEGER
    assert double_metadata.variable_type == acvi.VariableType.REAL
    assert string_metadata.variable_type == acvi.VariableType.STRING
    assert boolean_array_metadata.variable_type == acvi.VariableType.BOOLEAN_ARRAY
    assert integer_array_metadata.variable_type == acvi.VariableType.INTEGER_ARRAY
    assert double_array_metadata.variable_type == acvi.VariableType.REAL_ARRAY
    assert string_array_metadata.variable_type == acvi.VariableType.STRING_ARRAY


@pytest.mark.parametrize(
    'mc_type,acvi_type',
    [
        # TODO: Other types require support from MockModelCenter.
        pytest.param('boolean', acvi.VariableType.BOOLEAN),
        pytest.param('integer', acvi.VariableType.INTEGER),
        pytest.param('double', acvi.VariableType.REAL),
        pytest.param('string', acvi.VariableType.STRING),
        # arrays
        pytest.param('boolean[]', acvi.VariableType.BOOLEAN_ARRAY),
        pytest.param('integer[]', acvi.VariableType.INTEGER_ARRAY),
        pytest.param('double[]', acvi.VariableType.REAL_ARRAY),
        pytest.param('string[]', acvi.VariableType.STRING_ARRAY),
    ]
)
def test_create_assembly_variable(mc_type: str, acvi_type: acvi.VariableType) -> None:
    # SUT
    metadata: acvi.CommonVariableMetadata =\
        workflow.create_assembly_variable("variable_name", mc_type, "container")

    # Verification
    assert metadata.variable_type == acvi_type


def test_run_macro() -> None:
    """
    Verify that run_macro works as expected.
    """

    # Setup
    global mock_mc, workflow

    # SUT
    result: object = workflow.run_macro("macro", False)

    # Verification
    assert mock_mc.getCallCount("runMacro") == 1
    assert result is None  # arbitrary value from MockModelCenter


def test_add_new_macro() -> None:
    """
    Verify that add_new_macro works as expected.
    """

    # Setup
    global mock_mc, workflow

    # SUT
    workflow.add_new_macro("macro", False)

    # Verification
    assert mock_mc.getCallCount("addNewMacro") == 1


def test_set_macro_script() -> None:
    """
    Verify that set_macro_script works as expected.
    """

    # Setup
    global mock_mc, workflow

    # SUT
    workflow.set_macro_script("macro", "a script to run")

    # Verification
    assert mock_mc.getCallCount("setMacroScript") == 1


def test_get_macro_script() -> None:
    """
    Verify that get_macro_script works as expected.
    """

    # Setup
    global mock_mc, workflow

    # SUT
    script: str = workflow.get_macro_script("macro")

    # Verification
    assert mock_mc.getCallCount("getMacroScript") == 1
    assert script == "ここには何もない！目を逸らしてください！"  # arbitrary value from MockModelCenter


def test_set_macro_script_language() -> None:
    """
    Verify that set_macro_script_language works as expected.
    """

    # Setup
    global mock_mc, workflow

    # SUT
    workflow.set_macro_script_language("macro", "JavaScript")

    # Verification
    assert mock_mc.getCallCount("setMacroScriptLanguage") == 1


def test_get_macro_script_language() -> None:
    """
    Verify that get_macro_script_language works as expected.
    """

    # Setup
    global mock_mc, workflow

    # SUT
    script: str = workflow.get_macro_script_language("macro")

    # Verification
    assert mock_mc.getCallCount("getMacroScriptLanguage") == 1
    assert script == "いろいろなブランドの美味しさが楽しめます"  # arbitrary value from MockModelCenter


def test_set_macro_timeout() -> None:
    """
    Verify that set_macro_timeout works as expected.
    """

    # Setup
    global mock_mc, workflow

    # SUT
    workflow.set_macro_timeout("macro", 3.5)

    # Verification
    assert mock_mc.getCallCount("setMacroTimeout") == 1


def test_get_macro_timeout() -> None:
    """
    Verify that get_macro_timeout works as expected.
    """

    # Setup
    global mock_mc, workflow

    # SUT
    timeout: float = workflow.get_macro_timeout("macro")

    # Verification
    assert mock_mc.getCallCount("getMacroTimeout") == 1
    assert timeout == 25.0  # arbitrary value from MockModelCenter


def test_break_link() -> None:
    """
    Verify that breaking a link works correctly.
    """

    # Setup
    sut_engine = mcapi.Engine()
    sut_workflow: mcapi.Workflow = sut_engine.new_workflow()
    link_var_name: str = "Component.dont.link.me"
    assert sut_workflow._instance.getCallCount("breakLink") == 0

    # Execute
    sut_workflow.break_link(link_var_name)

    # Verify
    assert sut_workflow._instance.getCallCount("breakLink") == 1
    assert sut_workflow._instance.getArgumentRecord("breakLink", 0) == [link_var_name]


@pytest.mark.parametrize(
    "link_lhs_values",
    [
        pytest.param([], id="empty"),
        pytest.param(['linkTarget1', 'linkTarget2', 'linkTarget3'], id="some links")
    ]
)
def test_get_links(link_lhs_values: Iterable[str]) -> None:
    """
    Verify that get_links works when there are no links.
    """

    # Setup
    sut_engine = mcapi.Engine()
    sut_workflow = sut_engine.new_workflow()
    for link_lhs in link_lhs_values:
        sut_workflow.create_link(link_lhs, "LINKSOURCE")

    # Execute
    links: Iterable[mcapi.VariableLink] = sut_workflow.get_links()

    # Verify
    assert [link.lhs for link in links] == link_lhs_values


def test_halt() -> None:
    # Setup
    sut_engine = mcapi.Engine()
    sut_workflow = sut_engine.new_workflow()
    assert sut_workflow._instance.getCallCount("halt") == 0

    # Execute
    sut_workflow.halt()

    # Verify
    assert sut_workflow._instance.getCallCount("halt") == 1


def test_get_uuid() -> None:
    # Setup
    sut_engine = mcapi.Engine()
    sut_workflow = sut_engine.new_workflow()
    sut_workflow._instance.setModelUUID("15B9E8D5-602F-44D9-AF58-9CF0E6C27F9E")

    # Execute
    result: str = sut_workflow.get_workflow_uuid()

    # Verify
    assert result == "15B9E8D5-602F-44D9-AF58-9CF0E6C27F9E"


def test_auto_link() -> None:
    # Setup
    sut_engine = mcapi.Engine()
    sut_workflow = sut_engine.new_workflow()
    assert sut_workflow._instance.getCallCount("autoLink") == 0

    # Execute
    sut_workflow.auto_link("Workflow.source_comp", "Workflow.dest_comp")

    # Verify
    assert sut_workflow._instance.getCallCount("autoLink") == 1
    assert sut_workflow._instance.getArgumentRecord("autoLink", 0) == [
        "Workflow.source_comp", "Workflow.dest_comp"
    ]


def test_create_assembly() -> None:
    # Setup
    sut_engine = mcapi.Engine()
    sut_workflow = sut_engine.new_workflow()
    assert sut_workflow._instance.getCallCount("createAssembly") == 0
    test_assembly_name = "test_assembly"
    test_assembly_parent = "Workflow"
    test_assembly_type = "DataAssembly"

    # Execute
    sut_workflow.create_assembly(test_assembly_name, test_assembly_parent, test_assembly_type)

    # Verify
    assert sut_workflow._instance.getCallCount("createAssembly") == 1
    assert sut_workflow._instance.getArgumentRecord("createAssembly", 0) == [
        test_assembly_name, test_assembly_parent, test_assembly_type
    ]


def test_workflow_close():
    # Setup
    sut_engine = mcapi.Engine()
    sut_workflow: mcapi.Workflow = sut_engine.new_workflow("workflow.pxcz")

    # Check pre-reqs.
    try:
        sut_engine.new_workflow("workflow2.pxcz")
        assert False, "Should have failed by now."
    except Exception:
        pass

    # Execute
    sut_workflow.close_workflow()

    # Verify
    next_workflow = sut_engine.new_workflow("workflow.pxcz")
    assert isinstance(next_workflow, mcapi.Workflow)
    assert sut_engine._instance.getCallCount("closeModel") == 1


def test_save_workflow():
    # Setup
    sut_engine = mcapi.Engine()
    sut_workflow: mcapi.Workflow = sut_engine.new_workflow("workflow.pxcz")
    assert sut_workflow._instance.getCallCount("saveModel") == 0

    # Execute
    sut_workflow.save_workflow()

    # Verify
    assert sut_workflow._instance.getCallCount("saveModel") == 1


def test_save_workflow_as():
    # Setup
    sut_engine = mcapi.Engine()
    sut_workflow: mcapi.Workflow = sut_engine.new_workflow("workflow.pxcz")
    assert sut_workflow._instance.getCallCount("saveModelAs") == 1

    # Execute
    sut_workflow.save_workflow_as(r"C:\Temp\workflow.pxcz")

    # Verify
    assert sut_workflow._instance.getCallCount("saveModelAs") == 2
    argument = sut_workflow._instance.getArgumentRecord("saveModelAs", 1)[0]
    assert argument == r"C:\Temp\workflow.pxcz"


@pytest.mark.parametrize(
    'server_path,parent,name,x_pos,y_pos,expected_passed_x_pos,expected_passed_y_pos',
    [
        pytest.param('saserv://tests/add42', 'Adder', 'Workflow.model.workflow.model', 47, 42,
                     47, 42, id="fully specified position"),
        # It's difficult to test these cases, because the mock expects Missing.Value,
        # and that really screws with the reflection-based method matching in pythonnet,
        # since it seems Missing.Value has special meaning in that case.
        # Passing None doesn't work and neither does leaving the method off.
        # This is probably something that the real GRPC api will have to solve.
        # pytest.param('saserv://tests/add42', 'Adder', 'Workflow.model.workflow.model', None, 42,
        #             Missing.Value, 42, id="missing x value"),
        # pytest.param('saserv://tests/add42', 'Adder', 'Workflow.model.workflow.model', 47, None,
        #             47, Missing.Value, id="missing y value")
    ]
)
def test_create_component(
        server_path: str,
        name: str,
        parent: str,
        x_pos: Optional[object],
        y_pos: Optional[object],
        expected_passed_x_pos,
        expected_passed_y_pos
) -> None:
    # Setup
    sut_engine = mcapi.Engine()
    sut_workflow: mcapi.Workflow = sut_engine.new_workflow("workflow.pxcz")
    assert sut_workflow._instance.getCallCount("createComponent") == 0

    # Execute
    sut_workflow.create_component(server_path, name, parent, x_pos, y_pos)

    # Verify
    assert sut_workflow._instance.getCallCount("createComponent") == 1
    assert sut_workflow._instance.getArgumentRecord("createComponent", 0) == [
        server_path, name, parent, expected_passed_x_pos, expected_passed_y_pos]


def test_create_link() -> None:
    # Setup
    sut_engine = mcapi.Engine()
    sut_workflow: mcapi.Workflow = sut_engine.new_workflow("workflow.pxcz")
    assert sut_workflow._instance.getCallCount("createLink") == 0
    test_var_name = "inputs.var1"
    test_eqn = "Workflow.comp.output4"

    # Execute
    sut_workflow.create_link(test_var_name, test_eqn)

    # Verify
    assert sut_workflow._instance.getCallCount("createLink") == 1
    assert sut_workflow._instance.getArgumentRecord("createLink", 0) == [
        test_var_name, test_eqn
    ]


def test_get_variable() -> None:
    # Setup
    sut_engine = mcapi.Engine()
    sut_workflow: mcapi.Workflow = sut_engine.new_workflow("workflow.pxcz")
    test_var_name = "test_assembly_var"
    sut_workflow._instance.createAssemblyVariable(test_var_name, "Input", "Model")
    assert sut_workflow._instance.getCallCount("getVariable") == 0

    # Execute
    result = sut_workflow.get_variable("Model.test_assembly_var")

    # Verify
    assert sut_workflow._instance.getCallCount("getVariable") == 1
    assert sut_workflow._instance.getArgumentRecord("getVariable", 0) == ["Model.test_assembly_var"]
    assert result._variable.getFullName() == "Model.test_assembly_var"


@pytest.mark.parametrize(
    'variables',
    [
        pytest.param(None),
        pytest.param("Model.a,Model.b,Model.c"),
    ]
)
def test_run(variables: Optional[str]) -> None:
    # Setup
    global workflow

    # SUT
    workflow.run(variables)

    # Verification
    assert workflow._instance.getCallCount("run") == 1
    expected_arg: str = variables or ''
    assert workflow._instance.getArgumentRecord("run", 0) == [expected_arg]


@pytest.mark.parametrize(
    'index',
    [
        pytest.param(0),
        pytest.param(2),
    ]
)
def test_get_datamonitor(index: int) -> None:
    # Setup
    global workflow
    for x in range(index + 1):
        workflow.create_data_monitor("comp", "DM" + str(x), 0, 0)

    # SUT
    result: mcapi.IDataMonitor = workflow.get_data_monitor("comp", index)

    # Verification
    assert result.title == "DM" + str(index)


def test_create_datamonitor() -> None:
    # Setup
    global workflow

    # SUT
    result: mcapi.IDataMonitor = workflow.create_data_monitor("comp", "DM0", 0, 0)

    # Verification
    assert result.title == "DM0"


def test_remove_datamonitor() -> None:
    # Setup
    global workflow
    workflow.create_data_monitor("comp", "DM0", 0, 0)

    # SUT
    result: bool = workflow.remove_data_monitor("comp", 0)

    # Verification
    assert result is True


def test_remove_datamonitor_at_invalid_index() -> None:
    # Setup
    global workflow

    # SUT
    result: bool = workflow.remove_data_monitor("comp", 0)

    # Verification
    assert result is False


def test_get_data_explorer() -> None:
    # Setup
    global workflow
    workflow.create_data_explorer("", "")

    # SUT
    result: mcapi.DataExplorer = workflow.get_data_explorer(0)

    # Verification
    assert result is not None
    # TODO: more verification when DE is fleshed out


def test_get_data_explorer_invalid_index() -> None:
    # Setup
    global workflow

    # SUT
    result: mcapi.DataExplorer = workflow.get_data_explorer(0)

    # Verification
    assert result is None
