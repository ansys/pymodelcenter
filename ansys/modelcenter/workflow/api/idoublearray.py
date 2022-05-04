import ansys.common.variableinterop as acvi
import clr
from overrides import overrides

from ansys.modelcenter.workflow.api.iarray import IArray

clr.AddReference('phoenix-mocks/Phoenix.Mock.v45')
from Phoenix.Mock import MockDoubleArray


class IDoubleArray(IArray[MockDoubleArray]):
    """
    Represents a double array variable on the workflow.
    """

    @overrides
    @property
    def value(self) -> acvi.RealArrayValue:
        raise NotImplementedError

    @overrides
    @value.setter
    def value(self, new_value: acvi.IVariableValue):
        raise NotImplementedError

    @overrides
    @property
    def value_absolute(self) -> acvi.RealArrayValue:
        raise NotImplementedError

    @overrides
    @property
    def standard_metadata(self) -> acvi.RealArrayMetadata:
        raise NotImplementedError

    @standard_metadata.setter
    def standard_metadata(self, new_metadata: acvi.CommonVariableMetadata) -> None:
        """
        Get the standard metadata for this variable.
        """
        raise NotImplementedError
