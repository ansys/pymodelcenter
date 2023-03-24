"""Defines the level of access to an item of component metadata."""
from enum import Enum


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
