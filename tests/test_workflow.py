from typing import Any, Optional

# import pytest
import ansys.modelcenter.workflow.api as mcapi

# from ansys.common.variableinterop import (
#     BooleanArrayValue,
#     BooleanValue,
#     IntegerArrayValue,
#     IntegerValue,
#     IVariableValue,
#     RealArrayValue,
#     RealValue,
#     StringArrayValue,
#     StringValue,
# )

# import clr
# clr.AddReference('phoenix-mocks/Phoenix.Mock.v45')
#
# from Phoenix.Mock import MockModelCenter


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


def test_set_value():
    """
    Testing of set_value method.
    """
    global mock_mc, workflow

    # SUT
    workflow.set_value("var.name", "value")

    # Verify
    assert mock_mc.getCallCount("setValue") == 1
    args = mock_mc.getLastArgumentRecord("setValue")
    assert args[0] == "var.name"
    assert args[1] == "value"

# get_value_tests = [
#     pytest.param("b", BoolealValue(False), id = "bool"),
#     pytest.param("i", IntegerValue(42), id = "int"),
#     pytest.param("r", RealValue(3.14), id = "real"),
#     pytest.param("s", StringValue("sVal"), id = "str"),
#     pytest.param("ba", BooleanArrayValue([True, False, True]), id = "bool array"),
#     pytest.param("ia", IntegerArrayValue([86, 42, 1]), id = "int array"),
#     pytest.param("ra", RealArrayValue([1.414, 0.717, 3.14]), id = "real array"),
#     pytest.param("ba", StringArrayValue(["one", "two", "three"]), id = "str array"),
# ]
#
# pytest.mark.parametrize("var_name,expected", get_value_tests)
# def test_get_value(var_name: str, expected: IVariableValue):
#     """
#     Testing of get_value_tests method pulling each of the different
#     variable types.
#     """
#     global mock_mc, workflow
#     vars = ['b', 'i', 'r', 's', 'ba', 'ia', 'ra', 'sa']
#     vals = [
#         False, 42, 3.14, "sVal",
#         [True, False, True],
#         [86, 42, 1],
#         [1.414, 0.717, 3.14],
#         ["one", "two", "three"]
#     ]
#     mock_mc.SetMockVariables(vars, vals)
#
#     # SUT
#     result = workflow.get_value(var_name)
#
#     # Verify
#     assert result == expected
#     assert type(result) == type(expected)
#     assert mock_mc.getCallCount("getValue")
