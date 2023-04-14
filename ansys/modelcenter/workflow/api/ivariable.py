"""Contains common base class for all variables."""
from abc import ABC, abstractmethod

import ansys.common.variableinterop as acvi
import ansys.engineeringworkflow.api as aew_api


class IVariable(aew_api.IVariable, ABC):
    """Represents a variable in the workflow."""

    @abstractmethod
    def set_metadata(self, new_metadata: acvi.CommonVariableMetadata) -> None:
        """Get the standard metadata for this variable."""
