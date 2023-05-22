"""Contains common base class for all variables."""
from abc import ABC, abstractmethod
from typing import Collection

import ansys.engineeringworkflow.api as aew_api
import ansys.tools.variableinterop as atvi


class IDatapin(aew_api.IDatapin, ABC):
    """Represents a datapin in the workflow."""

    @abstractmethod
    def set_metadata(self, new_metadata: atvi.CommonVariableMetadata) -> None:
        """Get the standard metadata for this datapin."""

    @abstractmethod
    def get_dependents(
        self, only_fetch_direct_dependents: bool, follow_suspended_links: bool
    ) -> Collection[aew_api.IDatapin]:
        """Get the dependent (output) datapins for this datapin."""

    @abstractmethod
    def get_precedents(
        self, only_fetch_direct_precedents: bool, follow_suspended_links: bool
    ) -> Collection[aew_api.IDatapin]:
        """Gets the precedent (input) datapins for this datapin."""
