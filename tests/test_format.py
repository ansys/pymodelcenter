"""Tests for Format."""
import pytest

import ansys.modelcenter.workflow.api as mcapi

engine: mcapi.Engine


def setup_function(_):
    """
    Setup called before each test function in this module.

    Parameters
    ----------
    _ :
        The function about to test.
    """
    global engine
    engine = mcapi.Engine()


def test_get_format() -> None:
    """Verifies the getter of the format property."""
    # Setup
    sut: mcapi.Format = engine.get_formatter("")

    # SUT
    result: str = sut.format

    # Verification
    assert result == "General"


def test_set_format() -> None:
    """Verifies the setter of the format property."""
    # Setup
    sut: mcapi.Format = engine.get_formatter("")

    # SUT
    sut.format = "mockFormat"
    result: str = sut.format

    # Verification
    assert result == "mockFormat"


@pytest.mark.parametrize(
    "format_, string",
    [
        pytest.param("General", "5"),
        pytest.param("mockFormat", "ඞ5"),
    ],
)
def test_string_to_integer(format_: str, string: str) -> None:
    """Verifies the string_to_integer method."""
    # Setup
    sut: mcapi.Format = engine.get_formatter(format_)

    # SUT
    result: int = sut.string_to_integer(string)

    # Verification
    assert isinstance(result, int)
    assert result == 5


@pytest.mark.parametrize(
    "format_, string",
    [
        pytest.param("General", "5.5"),
        pytest.param("mockFormat", "ඞ5.5"),
    ],
)
def test_string_to_real(format_: str, string: str) -> None:
    """Verifies the string_to_real method."""
    # Setup
    sut: mcapi.Format = engine.get_formatter(format_)

    # SUT
    result: float = sut.string_to_real(string)

    # Verification
    assert isinstance(result, float)
    assert result == 5.5


@pytest.mark.parametrize(
    "format_, expected",
    [
        pytest.param("General", "5"),
        pytest.param("mockFormat", "ඞ5"),
    ],
)
def test_integer_to_string(format_: str, expected: str) -> None:
    """Verifies the integer_to_string method."""
    # Setup
    sut: mcapi.Format = engine.get_formatter(format_)

    # SUT
    result: str = sut.integer_to_string(5)

    # Verification
    assert isinstance(result, str)
    assert result == expected


@pytest.mark.parametrize(
    "format_, expected",
    [
        pytest.param("General", "5.5"),
        pytest.param("mockFormat", "ඞ5.5"),
    ],
)
def test_real_to_string(format_: str, expected: str) -> None:
    """Verifies the real_to_string method."""
    # Setup
    sut: mcapi.Format = engine.get_formatter(format_)

    # SUT
    result: str = sut.real_to_string(5.5)

    # Verification
    assert isinstance(result, str)
    assert result == expected


@pytest.mark.parametrize(
    "format_, expected",
    [
        pytest.param("General", "abc"),
        pytest.param("mockFormat", "ඞabc"),
    ],
)
def test_string_to_string(format_: str, expected: str) -> None:
    """Verifies the string_to_string method."""
    # Setup
    sut: mcapi.Format = engine.get_formatter(format_)

    # SUT
    result: str = sut.string_to_string("abc")

    # Verification
    assert isinstance(result, str)
    assert result == expected


@pytest.mark.parametrize(
    "format_, expected",
    [
        pytest.param("General", "5"),
        pytest.param("mockFormat", "ඞ5"),
    ],
)
def test_integer_to_editable_string(format_: str, expected: str) -> None:
    """Verifies the integer_to_editable_string method."""
    # Setup
    sut: mcapi.Format = engine.get_formatter(format_)

    # SUT
    result: str = sut.integer_to_editable_string(5)

    # Verification
    assert isinstance(result, str)
    assert result == expected


@pytest.mark.parametrize(
    "format_, expected",
    [
        pytest.param("General", "5.5"),
        pytest.param("mockFormat", "ඞ5.5"),
    ],
)
def test_real_to_editable_string(format_: str, expected: str) -> None:
    """Verifies the real_to_editable_string method."""
    # Setup
    sut: mcapi.Format = engine.get_formatter(format_)

    # SUT
    result: str = sut.real_to_editable_string(5.5)

    # Verification
    assert isinstance(result, str)
    assert result == expected
