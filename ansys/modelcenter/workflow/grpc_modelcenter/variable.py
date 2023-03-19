"""Provides an object-oriented way to interact with ModelCenter variables via gRPC."""
from typing import Collection

from ansys.common import variableinterop as acvi
from ansys.engineeringworkflow.api import Property
from grpc import Channel
from overrides import overrides

import ansys.modelcenter.workflow.api as api

from .proto.element_messages_pb2 import ElementId


class Variable(api.IVariable):
    """Represents a variable in the workflow."""

    @overrides
    def get_properties(self) -> Collection[Property]:
        pass

    @property  # type: ignore
    @overrides
    def value(self) -> acvi.IVariableValue:
        # TODO
        raise NotImplementedError

    @property  # type: ignore
    @overrides
    def value_absolute(self) -> acvi.IVariableValue:
        # TODO
        raise NotImplementedError

    @property  # type: ignore
    @overrides
    def standard_metadata(self) -> acvi.CommonVariableMetadata:
        # TODO
        raise NotImplementedError

    def __init__(self, element_id: ElementId, channel: Channel):
        """
        Initialize a new instance.

        Parameters
        ----------
        element_id : ElementId
            The id of the element.
        """
        self._element_id = element_id

    @property  # type: ignore
    @overrides
    def element_id(self) -> str:
        return self._element_id.id_string
