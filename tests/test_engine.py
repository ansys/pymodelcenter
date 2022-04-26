import clr
clr.AddReference('phoenix-mocks/Phoenix.Mock.v45')

from Phoenix.Mock import MockModelCenter

from ansys.modelcenter.workflow.api import Engine
from typing import Any
import pytest


@pytest.mark.parametrize(
    "actual_value,expected_result",
    [
        pytest.param(0, False, id='zero is false'),
        pytest.param(1, True, id='one is true'),
        pytest.param(-1, True, id='negative one is true'),
    ]
)
def test_is_interactive(actual_value: int, expected_result: bool) -> None:
    """
    Test that the is_interactive implementation properly calls and interprets results
    from the mock.
    """
    # Setup
    # Construct a mock MC.
    mock_mc: Any = MockModelCenter()
    # Construct an instance of the API adaptor.
    sut: Engine = Engine(mock_mc)
    # Configure the mock to report a particular result when asked if it is interactive.
    mock_mc.IsInteractive = actual_value

    # Execute
    result: bool = sut.is_interactive

    # Verify
    assert result == expected_result


def test_process_id() -> None:
    # Setup
    # Construct a mock MC.
    mock_mc: Any = MockModelCenter()
    # Construct an instance of the API adaptor.
    sut: Engine = Engine(mock_mc)
    # The mock contains a hardcoded implementation for the tested method.

    # Execute
    result: int = sut.process_id

    # Verify
    assert result == 4294967290
