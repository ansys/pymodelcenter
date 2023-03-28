"""Module contains definitions for file array variables."""
from abc import ABC, abstractmethod

import ansys.common.variableinterop as acvi
from overrides import overrides

from ansys.modelcenter.workflow.api.iarray import IArray

from .ifilevariable import IFileVariableBase


# TODO/REDUCE: Consider dropping for Phase II.
class IFileArray(IFileVariableBase, IArray, ABC):
    """Represents a file array variable in the workflow."""

    @property
    @abstractmethod
    def save_with_model(self) -> bool:
        """
        Get a flag indicating whether the file content is saved with the workflow.

        Returns
        -------
        bool :
            `True` if the file content is to be saved with the workflow.
        """
        raise NotImplementedError()

    @save_with_model.setter
    @abstractmethod
    def save_with_model(self, value: bool) -> None:
        """
        Set the flag indicating whether the file content is saved with the workflow.

        Parameters
        ----------
        value : bool
            Set to `True` if the file content is to be saved with the workflow.
        """
        raise NotImplementedError()

    @overrides
    @abstractmethod
    def get_metadata(self) -> acvi.FileArrayMetadata:
        raise NotImplementedError()
