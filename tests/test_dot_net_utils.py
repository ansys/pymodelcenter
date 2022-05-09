from typing import List

from System import String as DotNetString
from System.Collections.Generic import List as DotNetList

from ansys.modelcenter.workflow.api.dot_net_utils import DotNetListConverter


def test_list_to_dot_net():
    """Testing of the DotNetListConverter.to_dot_net static method."""
    source = ["one", "two", "three"]

    # SUT
    result = DotNetListConverter.to_dot_net(source, DotNetString)

    # Verify
    assert isinstance(result, DotNetList[DotNetString])
    assert result.Count == 3
    assert result.get_Item(0) == "one"
    assert result.get_Item(1) == "two"
    assert result.get_Item(2) == "three"


def test_list_from_dot_net():
    """Testing of the DotNetListConvert.from_dot_net static method."""
    source = DotNetList[DotNetString]()
    for i in ["one", "two", "three"]:
        s = DotNetString(i)
        source.Add(s)

    # SUT
    result: List[str] = DotNetListConverter.from_dot_net(source, str)

    # Verify
    assert isinstance(result, list)
    assert len(result) == 3
    i = result[0]
    assert isinstance(i, str)
    assert i == "one"
    i = result[1]
    assert isinstance(i, str)
    assert i == "two"
    i = result[2]
    assert isinstance(i, str)
    assert i == "three"
