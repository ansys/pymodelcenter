"""Implementation of Assembly."""

from .proto.element_messages_pb2 import ElementId


class Assembly:
    """Represents an assembly in ModelCenter."""

    def __init__(self, element_id: ElementId):
        """
        Initialize a new instance.

        Parameters
        ----------
        element_id : ElementId
            The id of the .
        """
        self._element_id = element_id

    @property
    def element_id(self) -> str:
        """
        TODO.

        Returns
        -------
        TODO.
        """
        # TODO: readonly?
        return self._element_id
