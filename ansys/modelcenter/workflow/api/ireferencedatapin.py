"""Contains definitions for scalar reference datapins."""
from abc import ABC, abstractmethod
from typing import Mapping

from overrides import overrides

from .idatapin import IDatapin
from .idatapinreferencebase import IDatapinReferenceBase
from .ireferenceproperty import IReferenceProperty, IReferencePropertyManager


class IReferenceDatapin(IDatapin, IDatapinReferenceBase, IReferencePropertyManager, ABC):
    """
    Represents a reference datapin in the workflow.

    Reference datapins allow components to have configurable connections to other datapins
    without creating a full link relationship.
    """

    @abstractmethod
    @overrides
    def get_reference_properties(self) -> Mapping[str, IReferenceProperty]:
        ...
