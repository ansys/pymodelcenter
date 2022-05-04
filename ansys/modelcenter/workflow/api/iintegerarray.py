import ansys.common.variableinterop as acvi
import clr
from overrides import overrides

from ansys.modelcenter.workflow.api.iarray import IArray

clr.AddReference('phoenix-mocks/Phoenix.Mock.v45')
from Phoenix.Mock import MockIntegerArray


class IIntegerArray(IArray[MockIntegerArray]):
    """
    Represents an integer array variable on the workflow.
    """

    @overrides
    @property
    def value(self) -> acvi.IntegerArrayValue:
        raise NotImplementedError

    @overrides
    @value.setter
    def value(self, new_value: acvi.IVariableValue):
        raise NotImplementedError

    @overrides
    @property
    def value_absolute(self) -> acvi.IntegerArrayValue:
        raise NotImplementedError

    @overrides
    @property
    def standard_metadata(self) -> acvi.IntegerArrayMetadata:
        raise NotImplementedError

    @standard_metadata.setter
    def standard_metadata(self, new_metadata: acvi.CommonVariableMetadata) -> None:
        """
        Get the standard metadata for this variable.
        """
        raise NotImplementedError
