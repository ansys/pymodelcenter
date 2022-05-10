from System import Tuple as DotNetTuple
from System.Collections.Generic import List as DotNetList
import clr

import ansys.modelcenter.workflow.api as mcapi

clr.AddReference("phoenix-mocks/Phoenix.Mock.v45")
from Phoenix.Mock import MockIfComponent

mock: MockIfComponent
sut: mcapi.IIfComponent


def setup_function(_):
    """
    Setup called before each test function in this module.

    Parameters
    ----------
    _ :
        The function about to test.
    """
    global mock, sut
    mock = MockIfComponent("Mock If Component")
    sut = mcapi.IIfComponent(mock)


def test_exclusive() -> None:
    """Testing of the exclusive property."""
    assert sut.exclusive is False

    sut.exclusive = True

    assert sut.exclusive is True


def test_run_last_branch_by_default() -> None:
    """Testing of the run_last_branch_by_default property."""
    assert sut.run_last_branch_by_default is False

    sut.run_last_branch_by_default = True

    assert sut.run_last_branch_by_default is True


def test_num_branches() -> None:
    """Testing of the get_num_branches method."""
    result: int = sut.num_branches

    assert result == 0


def test_get_branch_condition() -> None:
    """Testing of the get_branch_condition method."""
    # pythonnet has an issue with calling Add on a List property in the current version
    # This is a workaround
    list_ = DotNetList[DotNetTuple[str, str]]()
    list_.Add(DotNetTuple[str, str]("branch1", "condition1"))
    mock.Branches = list_

    result: str = sut.get_branch_condition(0)

    assert result == "condition1"


def test_set_branch_condition() -> None:
    """Testing of the set_branch_condition method."""
    # pythonnet has an issue with calling Add on a List property in the current version
    # This is a workaround
    list_ = DotNetList[DotNetTuple[str, str]]()
    list_.Add(DotNetTuple[str, str]("branch1", "condition1"))
    mock.Branches = list_

    sut.set_branch_condition(0, "new condition")

    result: str = sut.get_branch_condition(0)
    assert result == "new condition"


def test_get_branch_name() -> None:
    """Testing of the get_branch_name method."""
    # pythonnet has an issue with calling Add on a List property in the current version
    # This is a workaround
    list_ = DotNetList[DotNetTuple[str, str]]()
    list_.Add(DotNetTuple[str, str]("branch1", "condition1"))
    mock.Branches = list_

    result: str = sut.get_branch_name(0)

    assert result == "branch1"


def test_rename_branch() -> None:
    """Testing of the rename_branch method."""
    # pythonnet has an issue with calling Add on a List property in the current version
    # This is a workaround
    list_ = DotNetList[DotNetTuple[str, str]]()
    list_.Add(DotNetTuple[str, str]("branch1", "condition1"))
    mock.Branches = list_

    sut.rename_branch(0, "new name")

    result: str = sut.get_branch_name(0)
    assert result == "new name"
