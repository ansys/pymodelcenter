"""Collection of tests of CustomMetadataOwner"""

from collections.abc import Callable
from typing import Any, List, Tuple, Union
from xml.etree import ElementTree
from xml.etree.ElementTree import Element

import clr
import pytest

import ansys.modelcenter.workflow.api as mcapi
from ansys.modelcenter.workflow.api.custom_metadata_owner import CustomMetadataOwner

clr.AddReference("phoenix-mocks/Phoenix.Mock.v45")
from Phoenix.Mock import MockAssembly, MockComponent, MockVariable

target_instances = [
    ("assembly", lambda: MockAssembly("assemblyName")),
    ("component", lambda: MockComponent("componentName")),
    ("variable", lambda: MockVariable("variableName", 0, 1)),
]
"""
List of different types of instances to use as the inner type in \
target CustomMetadataOwner.

Each entry in the list is a tuple.
* a string identifier of the inner type to use.
* a lambda usable to construct an instance to use.
"""

xml_str = """<?xml version="1.0"?>
<comment>
  <to>John</to>
  <from>Victoria</from>
  <heading>Assurance</heading>
  <body>Everything's fine.</body>
</comment>
"""
"""An XML value."""

test_values = [
    ("str", "Some string value", mcapi.ComponentMetadataType.STRING),
    ("float", 3.14, mcapi.ComponentMetadataType.DOUBLE),
    ("bool", True, mcapi.ComponentMetadataType.BOOLEAN),
    ("int", 42, mcapi.ComponentMetadataType.LONG),
    ("xml", ElementTree.fromstring(xml_str), mcapi.ComponentMetadataType.XML),
    ("not-xml", "<This is not XML>", mcapi.ComponentMetadataType.STRING),
]
"""
List of different metadata values to use in tests.

Each entry in the list is a tuple.
* a string identifier of the test
* metadata value to use in test
* expected metadata type enum value at MCAPI setMetadata call
"""


def get_tests() -> List[pytest.param]:
    """
    Construct a list of tests by permuting the target_instances and \
    test_values lists and adding varying access and archive values.
    """
    tests = []
    access_start = 0
    archive = False
    for target_type in target_instances:
        type_name = target_type[0]
        type_ = target_type[1]
        access_num = access_start
        for test_value in test_values:
            value_name = test_value[0]
            value = test_value[1]
            expected_type = test_value[2]
            access = mcapi.ComponentMetadataAccess(access_num % 3)
            tests.append(
                pytest.param(
                    type_, (value, access, archive), expected_type, id=type_name + "-" + value_name
                )
            )
            access_num += 1
            archive = not archive
        access_start += 1
    return tests


@pytest.mark.parametrize("get_instance,params,expected_metadata_type", get_tests())
def test_custom_metadata_owner(
    get_instance: Callable,
    params: Tuple[Any, mcapi.ComponentMetadataAccess, bool],
    expected_metadata_type: mcapi.ComponentMetadataType,
) -> None:
    """
    Testing of the CustomMetadataOwner set_custom_metadata and \
    get_custom_metadata methods.

    Parameters
    ----------
    get_instance : Callable
        Callable to get a test instance.
    params : Tuple
        A collection of parameter values to use in call to
        set_custom_metadata.
    expected_metadata_type : mcapi.ComponentMetadataType
        Expected type given to the MCAPI setMetadata call.
    """
    # Setup
    instance = get_instance()
    target = CustomMetadataOwner(instance)
    (value, access, archive) = params
    instance.clearCallCounts()

    # SUT
    target.set_custom_metadata("md_name", value, access, archive)
    result = target.get_custom_metadata("md_name")

    # Verify:
    # Verify what went in, came out.
    assert type(result) == type(value)
    if isinstance(value, Element) and isinstance(result, Element):
        assert ElementTree.tostring(result) == ElementTree.tostring(value)
    else:
        assert result == value
    # Verify MCAPI setMetadata call
    assert instance.getCallCount("setMetadata") == 1
    set_args = instance.getArgumentRecord("setMetadata", 0)
    assert set_args[0] == "md_name"
    assert set_args[1] == expected_metadata_type.value
    assert set_args[3] == access.value
    assert set_args[4] == archive
    # Verify MCAPI getMetadata call
    assert instance.getCallCount("getMetadata") == 1
    get_args = instance.getArgumentRecord("getMetadata", 0)
    assert set_args[0] == "md_name"


@pytest.mark.parametrize(
    "instance,name,value,access,archive",
    [
        pytest.param(
            MockAssembly("assemblyName"),
            "none_metadata",
            None,
            mcapi.ComponentMetadataAccess.PUBLIC,
            True,
        ),
        pytest.param(
            MockComponent("componentName"),
            "list_metadata",
            [0, 1, 2],
            mcapi.ComponentMetadataAccess.PUBLIC,
            True,
        ),
    ],
)
def test_set_metadata_invalid(
    instance: CustomMetadataOwner.InstanceType,
    name: str,
    value: Union[str, int, float, bool],
    access: mcapi.ComponentMetadataAccess,
    archive: bool,
) -> None:
    """Testing of the set_metadata method."""
    target: CustomMetadataOwner = CustomMetadataOwner(instance)
    with pytest.raises(TypeError, match="Assembly or component metadata"):

        # SUT
        target.set_custom_metadata(name, value, access, archive)

    # Verify
    assert instance.getCallCount("setMetadata") == 0
