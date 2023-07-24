"""Contains definitions for array reference datapins."""
from abc import ABC, abstractmethod
from typing import Mapping, Sequence

from overrides import overrides

from .idatapin import IDatapin
from .idatapinreferencebase import IDatapinReferenceBase
from .ireferenceproperty import (IReferenceArrayProperty,
                                 IReferencePropertyManager)


class IReferenceArrayDatapin(
    IDatapin, Sequence[IDatapinReferenceBase], IReferencePropertyManager, ABC
):
    """
    Represents a reference array datapin in the workflow.

    Reference array datapins are different to other array datapin types. Reference arrays are
    only allowed to be one-dimensional and their size cannot be changed by resetting their values.

    In particular, because reference arrays may refer to datapins of more than one type,
    getting their values is more complex than with other datapin types. Implementations of this
    interface will implement IDatapin.get_value and set_value in a manner that is
    intended mostly for convenience and feature parity with legacy ModelCenter APIs,
    but if you are attempting to work with reference arrays in particular,
    consider using get_reference_value and set_refererence_value to query and manipulate the values
    of individual referenced datapins.
    """

    @abstractmethod
    @overrides
    def get_reference_properties(self) -> Mapping[str, IReferenceArrayProperty]:
        ...
