"""Contains definitions for scalar reference datapins."""
from abc import ABC

from .idatapin import IDatapin
from .idatapinreferencebase import IDatapinReferenceBase


class IReferenceDatapin(IDatapin, IDatapinReferenceBase, ABC):
    """
    Represents a reference datapin in the workflow.

    Reference datapins allow components to have configurable connections to other datapins
    without creating a full link relationship.
    """
