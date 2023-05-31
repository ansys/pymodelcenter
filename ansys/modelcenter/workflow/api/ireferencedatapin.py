"""Contains definitions for scalar reference datapins."""
from abc import ABC

from .idatapin import IDatapin
from .ireferencedatapinbase import IReferenceDatapinBase


class IReferenceDatapin(IDatapin, IReferenceDatapinBase, ABC):
    """
    Represents a reference datapin in the workflow.

    Reference datapins allow components to have configurable connections to other datapins
    without creating a full link relationship.
    """
