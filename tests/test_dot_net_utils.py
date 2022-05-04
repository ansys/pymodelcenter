from typing import List

from System import String as DotNetString
from System.Collections.Generic import List as DotNetList
import clr
import pytest

import ansys.modelcenter.workflow.api as mcapi
from ansys.modelcenter.workflow.api.dot_net_utils import DotNetListConverter, IVariableConverter

clr.AddReference("phoenix-mocks/Phoenix.Mock.v45")
from Phoenix.Mock import (
    MockBooleanArray,
    MockBooleanVariable,
    MockDoubleArray,
    MockDoubleVariable,
    MockFileArray,
    MockFileVariable,
    MockIntegerArray,
    MockIntegerVariable,
    MockReferenceArray,
    MockReferenceVariable,
    MockStringArray,
    MockStringVariable,
)


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


i_variable_converter_from_dot_net_tests = [
    pytest.param(MockBooleanVariable, mcapi.IBooleanVariable, id="boolean"),
    pytest.param(MockDoubleVariable, mcapi.IDoubleVariable, id="double"),
    pytest.param(MockFileVariable, mcapi.IFileVariable, id="file"),
    pytest.param(MockIntegerVariable, mcapi.IIntegerVariable, id="integer"),
    pytest.param(MockReferenceVariable, mcapi.IReferenceVariable, id="reference"),
    pytest.param(MockStringVariable, mcapi.IStringVariable, id="string"),
    pytest.param(MockBooleanArray, mcapi.IBooleanArray, id="boolean[]"),
    pytest.param(MockDoubleArray, mcapi.IDoubleArray, id="double[]"),
    pytest.param(MockFileArray, mcapi.IFileArray, id="file[]"),
    pytest.param(MockIntegerArray, mcapi.IIntegerArray, id="integer[]"),
    pytest.param(MockReferenceArray, mcapi.IReferenceArray, id="reference[]"),
    pytest.param(MockStringArray, mcapi.IStringArray, id="string[]"),
]


@pytest.mark.parametrize("source_type,expected_type", i_variable_converter_from_dot_net_tests)
def test_i_variable_converter_from_dot_net(source_type, expected_type):
    source = source_type("name", 0)

    # SUT
    result = IVariableConverter.from_dot_net(source)

    # Verify
    assert isinstance(result, expected_type)
