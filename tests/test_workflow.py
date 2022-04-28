"""Tests for Workflow."""
import pytest
from typing import List, Any, Optional,Type

import pytest
import ansys.common.variableinterop as acvi
import ansys.modelcenter.workflow.api as mcapi
from System import Boolean as DotNetBoolean
from System import Double as DotNetDouble
from System import Int64 as DotNetInt64
from System import Object as DotNetObject
from System import String as DotNetString
from System.Collections.Generic import List as DotNetList


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
    workflow = engine.new_workflow()


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
    pytest.param(BooleanValue(True), "True", id="bool"),
    pytest.param(IntegerValue(42), "42", id="int"),
    pytest.param(RealValue(3.14), "3.14", id="read"),
    pytest.param(StringValue("strVal"), "strVal", id="str"),
    pytest.param(BooleanArrayValue(values=[True, False]), "True,False", id="bool[]"),
    pytest.param(IntegerArrayValue(values=[86, 42]), "86,42", id="int[]"),
    pytest.param(RealArrayValue(values=[0.717, 1.414]), "0.717,1.414", id="real[]"),
    pytest.param(StringArrayValue(values=["one", "two"]), '"one","two"', id="str[]"),
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
    Setup some values usable fo testing get_value and \
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
def test_get_value(var_name: str, expected: IVariableValue):
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
    pytest.param("root.ba[1]", BooleanValue(False), id="bool array indexed"),
    pytest.param("root.ia[2]", IntegerValue(1), id="int array indexed"),
    pytest.param("root.ra[0]", RealValue(1.414), id="real array indexed"),
    pytest.param("root.sa[1]", StringValue("two"), id="str array indexed"),
])


@pytest.mark.parametrize(
    "var_name,expected", value_absolute_tests
)
def test_get_value_absolute(var_name: str, expected: IVariableValue):
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
        pytest.param(None,           1, 0, IAssembly,  id="root"),
        pytest.param("root.aName",   0, 1, IAssembly,  id="named"),
        pytest.param("root.noExist", 0, 1, None,       id="missing")
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

