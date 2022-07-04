import clr

import ansys.modelcenter.workflow.api as mcapi

clr.AddReference("phoenix-mocks/Phoenix.Mock.v45")
from Phoenix.Mock import MockScriptComponent

mock: MockScriptComponent
sut: mcapi.IScriptComponent


def setup_function(_):
    """
    Setup called before each test function in this module.

    Parameters
    ----------
    _ :
        The function about to test.
    """
    global mock, sut
    mock = MockScriptComponent("Mock Script Component")
    sut = mcapi.IScriptComponent(mock)


def test_language() -> None:
    """Testing of the language property."""
    assert sut.language != "JavaScript"

    sut.language = "JavaScript"

    assert sut.language == "JavaScript"


def test_timeout() -> None:
    """Testing of the timeout property."""
    assert sut.timeout != 5.0

    sut.timeout = 5.0

    assert sut.timeout == 5.0


def test_forward_schedule() -> None:
    """Testing of the forward_schedule property."""
    assert sut.forward_schedule is not True

    sut.forward_schedule = True

    assert sut.forward_schedule is True


def test_pre_validate() -> None:
    """Testing of the pre_validate property."""
    assert sut.pre_validate is not True

    sut.pre_validate = True

    assert sut.pre_validate is True


def test_source() -> None:
    """Testing of the source property."""
    assert sut.source_script == ""

    sut.source_script = "a script source"

    assert sut.source_script == "a script source"


def test_set_source_from_file() -> None:
    """Testing of the set_source_from_file method."""
    sut.set_source_from_file("/path/to/a/file.js")

    assert mock.getCallCount("setSourceFromString") == 1


def test_add_variable() -> None:
    """Testing of the add_variable method."""
    variable = sut.add_variable("boolean_var", "bool", "input")

    assert variable is not None
    assert mock.getCallCount("addVariable") == 1
    assert mock.Variables.Count == 1


def test_remove_variable() -> None:
    """Testing of the remove_variable method."""
    sut.remove_variable("boolean_var")

    assert mock.getCallCount("removeVariable") == 1


def test_set_variables() -> None:
    """Testing of the set_variables method."""
    sut.set_variables(
        "bool b, int i, double r, string s", "bool[] b_a, int[] i_a, double[] r_a, string[] s_a"
    )

    assert mock.getCallCount("setVariables") == 1
    assert mock.Variables.Count == 8
