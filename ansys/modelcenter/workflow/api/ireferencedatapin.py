"""Contains definitions for scalar reference datapins."""
from abc import ABC

from .idatapin import IDatapin
from .idatapinreferencebase import IDatapinReferenceBase
from .ireferenceproperty import IReferencePropertyManager


class IReferenceDatapin(IDatapin, IDatapinReferenceBase, IReferencePropertyManager, ABC):
    """
    Represents a reference datapin in the workflow.

    Reference datapins allow components to have configurable connections to other datapins
    without creating a full link relationship.
    """
