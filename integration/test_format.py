"""Integration tests around Format functionality."""

from numpy import float64

import ansys.modelcenter.workflow.api as mcapi


def test_formatting_string_to_string(engine) -> None:
    # Arrange
    formatter: mcapi.IFormat = engine.get_formatter(fmt="General")

    # Act
    result: str = formatter.string_to_string("1234.5678")

    # Assert
    assert result == "1234.57"


def test_formatting_real_to_string(engine) -> None:
    # Arrange
    formatter: mcapi.IFormat = engine.get_formatter(fmt="(#,##0.00000)")

    # Act
    result: str = formatter.real_to_string(float64(-1234.5678))

    # Assert
    assert result == "(1,234.56780)"


def test_formatting_integer_to_string(engine) -> None:
    # Arrange
    formatter: mcapi.IFormat = engine.get_formatter(fmt="$#,##")

    # Act
    result: str = formatter.integer_to_string(123456789)

    # Assert
    assert result == "$123,456,789"


def test_formatting_real_to_editable_string(engine) -> None:
    # Arrange
    formatter: mcapi.IFormat = engine.get_formatter(fmt="?/?")

    # Act
    result: str = formatter.real_to_string(float64(0.75))

    # Assert
    assert result == "3/4"


def test_formatting_integer_to_editable_string(engine) -> None:
    # Arrange
    formatter: mcapi.IFormat = engine.get_formatter(fmt="0%")

    # Act
    result: str = formatter.integer_to_string(5)

    # Assert
    assert result == "500%"


def test_formatting_string_to_real(engine) -> None:
    # Arrange
    formatter: mcapi.IFormat = engine.get_formatter(fmt="(#,##0.00000)")

    # Act
    result: float64 = formatter.string_to_real("(1,234.56780)")

    # Assert
    assert result == float64(-1234.5678)


def test_formatting_string_to_integer(engine) -> None:
    # Arrange
    formatter: mcapi.IFormat = engine.get_formatter(fmt="$#,##")

    # Act
    result: str = formatter.string_to_integer("$123,456,789")

    # Assert
    assert result == 123456789
