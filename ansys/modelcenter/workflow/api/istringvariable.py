import ansys.common.variableinterop as acvi
import clr
from overrides import overrides

from ansys.modelcenter.workflow.api.ivariable import ScalarVariable

clr.AddReference('phoenix-mocks/Phoenix.Mock.v45')
from Phoenix.Mock import MockStringVariable


class IStringVariable(ScalarVariable[MockStringVariable]):
    """
    Represents a string variable on the workflow.
    """

    @overrides
    @property
    def value(self) -> acvi.StringValue:
        raise NotImplementedError

    @overrides
    @value.setter
    def value(self, new_value: acvi.IVariableValue):
        raise NotImplementedError

    @overrides
    @property
    def value_absolute(self) -> acvi.StringValue:
        raise NotImplementedError

    @overrides
    @property
    def standard_metadata(self) -> acvi.StringMetadata:
        raise NotImplementedError

    @standard_metadata.setter
    def standard_metadata(self, new_metadata: acvi.CommonVariableMetadata) -> None:
        """
        Get the standard metadata for this variable.
        """
        raise NotImplementedError
