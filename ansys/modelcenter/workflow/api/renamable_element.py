"""Defines an interface for workflow elements that can be renamed."""
from abc import ABC, abstractmethod
import ansys.engineeringworkflow.api as aew_api


class IRenamableElement(aew_api.IElement, ABC):
    """An interface for workflow elements that can be renamed."""

    @abstractmethod
    def rename(self, new_name: str) -> None:
        """
        Rename this item.

        Parameters
        ----------
        new_name : str
            The new short name for the item.
        """
