from typing import Any, List, Optional

import pytest
import ansys.modelcenter.workflow.api as mcapi
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


def py_list_to_net_list(src : List) -> DotNetList:
    """
    Convert the given Python list to a Dot Net Object List.

    Parameters
    ----------
    src : List
        Python list to convert, each entry will become an entry in the
        resulting dot net list.

    Returns
    -------
    A DotNetList of objects. i.e. in Dot Net terminology: List<Object>
    """
    result = DotNetList[DotNetObject]()
    for item in src:
        if isinstance(item, list):
            item_list = py_list_to_net_typed_list(item)
            result.Add(item_list)
        else:
            result.Add(item)
    return result


def py_list_to_net_typed_list(src : List) -> DotNetList:
    """
    Convert the given Python list to a Dot Net List of the appropriate \
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
    A DotNet list of
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
    pytest.param("root.b", BooleanValue(False), id = "bool"),
    pytest.param("root.i", IntegerValue(42), id = "int"),
    pytest.param("root.r", RealValue(3.14), id = "real"),
    pytest.param("root.s", StringValue("sVal"), id = "str"),
    pytest.param("root.ba", BooleanArrayValue(values=[True, False, True]), id = "bool array"),
    pytest.param("root.ia", IntegerArrayValue(values=[86, 42, 1]), id = "int array"),
    pytest.param("root.ra", RealArrayValue(values=[1.414, 0.717, 3.14]), id = "real array"),
    pytest.param("root.sa", StringArrayValue(values=["one", "two", "three"]), id = "str array"),
]


@pytest.mark.parametrize("var_name,expected", get_value_tests)
def test_get_value(var_name: str, expected: IVariableValue):
    """
    Testing of get_value_tests method pulling each of the different
    variable types.
    """
    global mock_mc, workflow
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
    mock_mc.createAssemblyVariable('b', "Input", "root")
    mock_mc.createAssemblyVariable('i', "Input", "root")
    mock_mc.createAssemblyVariable('r', "Input", "root")
    mock_mc.createAssemblyVariable('s', "Input", "root")
    mock_mc.createAssemblyVariable('ba', "Input", "root")
    mock_mc.createAssemblyVariable('ia', "Input", "root")
    mock_mc.createAssemblyVariable('ra', "Input", "root")
    mock_mc.createAssemblyVariable('sa', "Input", "root")
    mock_mc.SetMockValues(vars_, vals)

    # SUT
    result = workflow.get_value(var_name)

    # Verify
    assert result == expected
    assert type(result) == type(expected)
    assert mock_mc.getCallCount("getValue")
