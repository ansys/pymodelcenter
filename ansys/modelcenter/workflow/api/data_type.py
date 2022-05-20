from enum import IntEnum


class DataType(IntEnum):
    """Data types from MC API."""
    UNKNOWN = 0
    DOUBLE = 1
    INTEGER = 2
    STRING = 3
    BOOLEAN = 4
    FILE = 5
    REFERENCE = 6
    NUM_DATA_TYPES = 7
    DATA_TYPES_MASK = 255
    ARRAY = 256
    DOUBLE_ARRAY = 257
    INTEGER_ARRAY = 258
    STRING_ARRAY = 259
    BOOLEAN_ARRAY = 260
    FILE_ARRAY = 261
    REFERENCE_ARRAY = 262
    COLLECTION_TYPES_MASK = 65280


class VarType(IntEnum):
    """Basic set of variable types."""

    INPUT = 0
    """This is an input."""

    OUTPUT = 1
    """This in an output."""

    GROUP = 2
    """This is a group."""
