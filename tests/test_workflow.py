import pytest
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

def test_workflow_directory() -> None:
    """
    Testing of workflow_directory method.
    """
    engine = mcapi.Engine()
    engine._instance.modelDirectory = "D:\\Some\\Path\\model.ext"
    workflow = engine.new_workflow()
    engine._instance.clearCallCounts()

    # SUT
    result = workflow.workflow_directory

    # Verify
    assert isinstance(result, str)
    assert result == "D:\\Some\\Path\\model.ext"
    # assert engine._instance.getCallCount("modelDirectory") == 1
    assert engine._instance.getTotalCallCount() == 1

def test_workflow_file_name():
    """
    Testing of workflow_file_name method.
    """
    engine = mcapi.Engine()
    engine._instance.modelFileName = "model.ext"
    workflow = engine.new_workflow()
    engine._instance.clearCallCounts()

    # SUT
    result = workflow.workflow_file_name

    # Verify
    assert isinstance(result, str)
    assert result == "model.ext"
    # assert engine._instance.getCallCount("modelFileName") == 1
    assert engine._instance.getTotalCallCount() == 1

def test_set_value():
    """
    Testing of set_value method.
    """
    engine = mcapi.Engine()
    workflow = engine.new_workflow()

    # SUT
    workflow.set_value("var.name", "value")

    # Verify
    assert engine._instance.getCallCount("setValue") == 1
    args = engine._instance.getLastArgumentRecord("setValue")
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
#     engine = mcapi.Engine()
#     vars = ['b', 'i', 'r', 's', 'ba', 'ia', 'ra', 'sa']
#     vals = [
#         False, 42, 3.14, "sVal",
#         [True, False, True],
#         [86, 42, 1],
#         [1.414, 0.717, 3.14],
#         ["one", "two", "three"]
#     ]
#     engine._instance.SetMockVariables(vars, vals)
#     workflow = engine.new_workflow()
#
#     # SUT
#     result = workflow.get_value(var_name)
#
#     # Verify
#     assert result == expected
#     assert type(result) == type(expected)
#     assert engine._instance.getCallCount("getValue")
