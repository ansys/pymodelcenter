"""
Defines mirrors of component-metadata-related ModelCenter enums for working with the ModelCenter \
mocks.

This should probably be re-visited once we are no longer using the mock as a backend.
"""
from enum import Enum


class ComponentMetadataType(Enum):
    """
    Represents the type of a component metadata.

    The values are meant to match up with ModelCenter.MetadataType from Interop.ModelCenter.
    This is a temporary strategy designed to work around an inability to access that enum
    directly.
    """
    STRING = 0
    DOUBLE = 1
    LONG = 2
    BOOLEAN = 3
    XML = 4


class ComponentMetadataAccess(Enum):
    """
    Represents the level of access to a component metadata.

    The values are meant to match up with ModelCenter.MetadataType from Interop.ModelCenter.
    This is a temporary strategy designed to work around an inability to access that enum
    directly.
    """
    PRIVATE = 0
    READONLY = 1
    PUBLIC = 2
