"""Definitions of file variable."""
from abc import ABC, abstractmethod

import ansys.common.variableinterop as acvi
from overrides import overrides

from ansys.modelcenter.workflow.api.ivariable import IVariable


class IFileVariableBase(ABC):
    """Defines methods beyond the IVariable / IArray for both scalar and array file variables."""

    @property
    @abstractmethod
    def save_with_model(self) -> bool:
        """
        Flag to indicate whether the file content to be saved with the Model file.

        Returns
        -------
        bool :
            `True` if the file content is to be saved with the Model file.
        """

    @save_with_model.setter
    @abstractmethod
    def save_with_model(self, value: bool) -> None:
        """
        Flag to indicate whether the file content to be saved with the Model file.

        Parameters
        ----------
        value : bool
            Set to `True` if the file content is to be saved with the Model file.
        """

    @property
    @abstractmethod
    def direct_transfer(self) -> bool:
        """
        Flag to indicate whether direct file transfer is used for incoming link.

        Returns
        -------
        bool :
            `True` if direct file transfer is used for incoming link.
        """

    @direct_transfer.setter
    @abstractmethod
    def direct_transfer(self, value: bool) -> None:
        """
        Flag to indicate whether direct file transfer is used for incoming link.

        Parameters
        ----------
        value : bool
            Set to `True` if direct file transfer is used for incoming link.
        """


# TODO/REDUCE: Consider dropping for Phase II.
class IFileVariable(IFileVariableBase, IVariable, ABC):
    """Represents a file variable in the workflow."""

    @overrides
    @abstractmethod
    def get_metadata(self) -> acvi.FileMetadata:
        ...  # pragma: no cover
