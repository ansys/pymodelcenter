"""Classes for representing variables that exist in ModelCenter with unsupported value types."""

import ansys.common.variableinterop as acvi
import grpc
from overrides import overrides

from .base_datapin import BaseDatapin
from .proto.element_messages_pb2 import ElementId


class DatapinWithUnsupportedTypeException(BaseException):
    """This exception is raised when attempting to interact with a datapin of unsupported type."""

    def __init__(self):
        """Create a new instance."""
        super(DatapinWithUnsupportedTypeException, self).__init__(
            "The pyModelCenter API does not currently support this interaction on variables of "
            "this type."
        )


class UnsupportedTypeDatapin(BaseDatapin):
    """
    Represents a datapin with an unsupported datatype.

    Generally speaking, it will be possible to perform interactions that don't require
    retrieving or otherwise interacting with the datapin's value or metadata. Attempts to
    set or get the value or metadata will raise a DatapinWithUnsupportedTypeException.
    """

    def __init__(self, element_id: ElementId, channel: grpc.Channel):
        """Construct a new instance."""
        super(BaseDatapin, self).__init__(element_id=element_id, channel=channel)

    @overrides
    def set_metadata(self, new_metadata: acvi.CommonVariableMetadata) -> None:
        raise DatapinWithUnsupportedTypeException()

    @overrides
    def set_value(self, value: acvi.VariableState) -> None:
        raise DatapinWithUnsupportedTypeException()

    @overrides
    def get_metadata(self) -> acvi.CommonVariableMetadata:
        raise DatapinWithUnsupportedTypeException()
