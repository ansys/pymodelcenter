from typing import Union, List

from ansys.modelcenter.workflow.api.arrayish import Arrayish
from tests.mock_access import MockAccess


class MockAPIItem:
    """
    A mock ModelCenter API item returned as an item by the arrayish \
    MockAPIInstance ModelCenter API object's items.
    """
    def __init__(self, name: str):
        """
        Initialize a mock item.

        Parameters
        ----------
        name : str
            Name of the MockAPIItem.
        """
        self._name = name

    @property
    def Name(self) -> str:
        """The name of the mock API item."""
        return self._name


class MockAPIInstance(MockAccess):
    """A mock Arrayish ModelCenter API interface object."""

    def __init__(self):
        """Initialize the mock interface object."""
        MockAccess.__init__(self)
        self._list = [
            MockAPIItem("zero"),
            MockAPIItem("one"),
            MockAPIItem("two"),
            MockAPIItem("three"),
            MockAPIItem("four"),
        ]
        self._dict = {}
        for mock_item in self._list:
            name: str = mock_item.Name
            self._dict[name] = mock_item

    def Item(self, id_: Union[int, str]) -> MockAPIItem:
        """
        Get a reference to the specified object.

        Parameters
        ----------
        id_ : int or str
            ID of the specified object. ID can be a name or an index.

        Returns
        -------
        Reference to the specified object.
        """
        self.record_call("Item", id_)
        if isinstance(id_, int):
            return self._list[id_]
        elif isinstance(id_, str):
            return self._dict[id_]
        else:
            raise TypeError

    @property
    def Count(self) -> int:
        """Number of objects managed by the mock arrayish interface."""
        self.record_call("Count")
        return len(self._list)


class MockItem:
    """
    A python object that wraps the MockAPIItem.

    Logically equivalent to IAssembly, IComponent, IGroup, IVariableLink,
    or IVariable in their relationship to IAssemblies, IComponents,
    IVariableLinks and IVariables.
    """

    def __init__(self, instance: MockAPIItem):
        """
        Initialize mock item with the given instance.

        Parameters
        ----------
        instance : MockAPIItem
            API object instance to wrap.
        """
        self._instance: MockAPIItem = instance

    @property
    def name(self) -> str:
        """Get the name of the object"""
        return self._instance.Name


class TestArrayish(Arrayish[MockItem]):
    """Test Arrayish class to validate Arrayish[] functionality."""

    def __init__(self, instance: MockAPIInstance):
        """Initialize the test arrayish object."""
        Arrayish.__init__(self, instance, MockItem)


def test_iterable():
    """Test that Arrayish is iterable."""
    instance = MockAPIInstance()
    test_arrayish = TestArrayish(instance)
    results = []

    # SUT
    for mock_item in test_arrayish:
        name: str = mock_item.name
        results.append(name)

    # Verify
    assert results == ["zero", "one", "two", "three", "four"]


def test_random_access():
    """Test that Arrayish is randomly accessible without being \
    inefficient in its calls to the wrapper arrayish API instance."""
    instance = MockAPIInstance()
    test_arrayish = TestArrayish(instance)

    # SUT
    result3 = test_arrayish[3]
    result1 = test_arrayish["one"]

    # Verify

    assert result3.name == "three", "returned value for 4th item"
    assert result1.name == "one", "returned value for 2nd item"
    assert instance.get_call_count("Item") == 2, "Item[] only called twice"
    args: List[str] = instance.get_argument_record("Item", 0)
    assert len(args) == 1
    assert args[0] == "3"
    args: List[str] = instance.get_argument_record("Item", 1)
    assert len(args) == 1
    assert args[0] == "one"
