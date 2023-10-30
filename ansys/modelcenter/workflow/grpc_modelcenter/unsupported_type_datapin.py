"""Classes for representing variables that exist in ModelCenter with unsupported state types."""
from typing import TYPE_CHECKING

import ansys.tools.variableinterop as atvi
from overrides import overrides

from .base_datapin import BaseDatapin

if TYPE_CHECKING:
    from .engine import Engine
from ansys.api.modelcenter.v0.element_messages_pb2 import ElementId


class DatapinWithUnsupportedTypeException(BaseException):
    """This exception is raised when attempting to interact with a datapin of unsupported type."""

    def __init__(self):
        """Create a new instance."""
        super(DatapinWithUnsupportedTypeException, self).__init__(
            "The pyModelCenter API does not currently support this interaction on datapins of "
            "this type."
        )


class UnsupportedTypeDatapin(BaseDatapin):
    """
    Represents a datapin with an unsupported datatype.

    Generally speaking, it will be possible to perform interactions that don't require
    retrieving or otherwise interacting with the datapin's state or metadata. Attempts to
    set or get the state or metadata will raise a DatapinWithUnsupportedTypeException.
    """

    def __init__(self, element_id: ElementId, engine: "Engine"):
        """Construct a new instance."""
        super(BaseDatapin, self).__init__(element_id=element_id, engine=engine)

    @overrides
    def set_metadata(self, new_metadata: atvi.CommonVariableMetadata) -> None:
        raise DatapinWithUnsupportedTypeException()

    @overrides
    def set_state(self, state: atvi.VariableState) -> None:
        raise DatapinWithUnsupportedTypeException()

    @overrides
    def get_metadata(self) -> atvi.CommonVariableMetadata:
        raise DatapinWithUnsupportedTypeException()
