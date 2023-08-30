"""Contains definition for ReferenceDatapin and ReferenceArrayDatapin."""
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Iterable, Mapping, MutableSequence, Optional, Union, overload

from ansys.api.modelcenter.v0.grpc_modelcenter_workflow_pb2_grpc import (
    ModelCenterWorkflowServiceStub,
)
import ansys.api.modelcenter.v0.variable_value_messages_pb2 as var_msgs
import ansys.api.modelcenter.v0.workflow_messages_pb2 as wkfl_msgs
import ansys.engineeringworkflow.api as aew_api
import ansys.tools.variableinterop as atvi
from overrides import overrides

import ansys.modelcenter.workflow.api as mc_api

from . import var_value_convert
from ..api import IDatapinReferenceBase, IReferenceArrayProperty, IReferenceProperty
from .base_datapin import BaseDatapin
from .reference_datapin_metadata import ReferenceDatapinMetadata
from .var_metadata_convert import convert_grpc_reference_metadata, fill_reference_metadata_message
from .var_value_convert import convert_grpc_value_to_atvi

if TYPE_CHECKING:
    from .engine import Engine

from ansys.api.modelcenter.v0.element_messages_pb2 import ElementId

from .grpc_error_interpretation import (
    WRAP_OUT_OF_BOUNDS,
    WRAP_TARGET_NOT_FOUND,
    interpret_rpc_error,
)


class ReferenceArrayDatapinElement(mc_api.IDatapinReferenceBase):
    """
    Represents a single element in a ReferenceArrayDatapin.

    .. note::
        This class should not be directly instantiated by clients. Get a Workflow object from
        an instantiated Engine, and use it to get a valid instance of a ReferenceArrayDatapin,
        which can then be indexed to get an object of this type.
    """

    def __init__(
        self,
        parent_client: ModelCenterWorkflowServiceStub,
        parent_element_id: ElementId,
        index: int,
        parent_engine: "Engine",
    ):
        """
        Initialize a new instance.

        Parameters
        ----------
        parent_client: ModelCenterWorkflowServiceStub
            The client used by the parent array
        parent_element_id: ElementId
            The id of the parent array.
        index: int
            This reference variable's index in the parent array.
        parent_engine: Engine
            The Engine that created the parent array datapin.
        """
        self._client = parent_client
        self._parent_element_id = parent_element_id
        self._index = index
        self._engine = parent_engine

    @property
    @interpret_rpc_error({**WRAP_TARGET_NOT_FOUND, **WRAP_OUT_OF_BOUNDS})
    @overrides
    def equation(self) -> str:
        request = var_msgs.GetReferenceEquationRequest(
            target=self._parent_element_id, index=self._index
        )
        response: var_msgs.GetReferenceEquationResponse = (
            self._client.ReferenceVariableGetReferenceEquation(request)
        )
        return response.equation

    @equation.setter
    @interpret_rpc_error({**WRAP_TARGET_NOT_FOUND, **WRAP_OUT_OF_BOUNDS})
    @overrides
    def equation(self, equation: str) -> None:
        request = var_msgs.SetReferenceEquationRequest(
            target=self._parent_element_id, index=self._index, equation=equation
        )
        self._client.ReferenceVariableSetReferenceEquation(request)

    @property
    @interpret_rpc_error({**WRAP_TARGET_NOT_FOUND, **WRAP_OUT_OF_BOUNDS})
    @overrides
    def is_direct(self) -> bool:
        request = var_msgs.GetReferenceIsDirectRequest(
            target=self._parent_element_id, index=self._index
        )
        response: var_msgs.GetReferenceIsDirectResponse = self._client.ReferenceVariableGetIsDirect(
            request
        )
        return response.is_direct

    @interpret_rpc_error({**WRAP_TARGET_NOT_FOUND, **WRAP_OUT_OF_BOUNDS})
    @overrides
    def get_value(self, hid: Optional[str] = None) -> atvi.VariableState:
        if hid is not None:
            raise ValueError("This engine implementation does not yet support HIDs.")
        request = var_msgs.GetReferenceValueRequest(
            target=self._parent_element_id, index=self._index
        )
        response = self._client.ReferenceVariableGetValue(request)
        interop_value: atvi.IVariableValue
        try:
            interop_value = convert_grpc_value_to_atvi(response.value, self._engine.is_local)
        except ValueError as convert_failure:
            raise aew_api.EngineInternalError(
                "Unexpected failure converting gRPC value response"
            ) from convert_failure
        return atvi.VariableState(value=interop_value, is_valid=response.is_valid)

    @interpret_rpc_error({**WRAP_TARGET_NOT_FOUND, **WRAP_OUT_OF_BOUNDS})
    @overrides
    def set_value(self, value: atvi.VariableState) -> None:
        if (
            not isinstance(value.value, atvi.BooleanValue)
            and not isinstance(value.value, atvi.RealValue)
            and not isinstance(value.value, atvi.IntegerValue)
            and not isinstance(value.value, atvi.StringValue)
            and not isinstance(value.value, atvi.FileValue)
        ):
            raise atvi.IncompatibleTypesException(
                value.value.variable_type, atvi.VariableType.UNKNOWN
            )
        new_value = var_value_convert.convert_interop_value_to_grpc(value.value)
        request = var_msgs.SetReferenceValueRequest(
            target=self._parent_element_id, index=self._index, new_value=new_value
        )
        response = self._client.ReferenceVariableSetValue(request)
        return response.was_changed


class ReferenceDatapinBase(BaseDatapin, ABC):
    """Implementation common between scalar and array reference datapins."""

    @interpret_rpc_error(WRAP_TARGET_NOT_FOUND)
    @overrides
    def get_metadata(self) -> ReferenceDatapinMetadata:
        response = self._client.ReferenceVariableGetMetadata(self._element_id)
        return convert_grpc_reference_metadata(response)

    @interpret_rpc_error(WRAP_TARGET_NOT_FOUND)
    @overrides
    def set_metadata(self, new_metadata: atvi.CommonVariableMetadata) -> None:
        if not isinstance(new_metadata, ReferenceDatapinMetadata):
            raise TypeError(
                f"The provided metadata object is not the correct type."
                f"Expected {ReferenceDatapinMetadata} "
                f"but received {new_metadata.__class__}"
            )
        request = var_msgs.SetReferenceVariableMetadataRequest(target=self._element_id)
        fill_reference_metadata_message(new_metadata, request.new_metadata)
        self._client.ReferenceVariableSetMetadata(request)


class ReferenceDatapin(ReferenceDatapinBase, mc_api.IReferenceDatapin):
    """
    Represents a reference datapin.

    .. note::
        This class should not be directly instantiated by clients. Get a Workflow object from
        an instantiated Engine, and use it to get a valid instance of this object.
    """

    def __init__(self, element_id: ElementId, engine: "Engine"):
        """
        Initialize a new instance.

        Parameters
        ----------
        element_id: ElementId
            The id of the variable.
        engine: Engine
            The Engine that created this datapin.
        """
        super(ReferenceDatapin, self).__init__(element_id=element_id, engine=engine)

    @overrides
    def __eq__(self, other):
        return isinstance(other, ReferenceDatapin) and self.element_id == other.element_id

    @interpret_rpc_error({**WRAP_TARGET_NOT_FOUND, **WRAP_OUT_OF_BOUNDS})
    @overrides
    def set_value(self, value: atvi.VariableState) -> None:
        if (
            not isinstance(value.value, atvi.BooleanValue)
            and not isinstance(value.value, atvi.RealValue)
            and not isinstance(value.value, atvi.IntegerValue)
            and not isinstance(value.value, atvi.StringValue)
            and not isinstance(value.value, atvi.FileValue)
        ):
            raise atvi.IncompatibleTypesException(
                value.value.variable_type, atvi.VariableType.UNKNOWN
            )
        new_value = var_value_convert.convert_interop_value_to_grpc(value.value)
        request = var_msgs.SetReferenceValueRequest(target=self._element_id, new_value=new_value)
        response = self._client.ReferenceVariableSetValue(request)
        return response.was_changed

    @property
    @interpret_rpc_error(WRAP_TARGET_NOT_FOUND)
    @overrides
    def equation(self) -> str:
        request = var_msgs.GetReferenceEquationRequest(target=self._element_id)
        response: var_msgs.GetReferenceEquationResponse = (
            self._client.ReferenceVariableGetReferenceEquation(request)
        )
        return response.equation

    @equation.setter
    @interpret_rpc_error(WRAP_TARGET_NOT_FOUND)
    @overrides
    def equation(self, equation: str) -> None:
        request = var_msgs.SetReferenceEquationRequest(target=self._element_id, equation=equation)
        self._client.ReferenceVariableSetReferenceEquation(request)

    @property
    @interpret_rpc_error(WRAP_TARGET_NOT_FOUND)
    @overrides
    def is_direct(self) -> bool:
        request = var_msgs.GetReferenceIsDirectRequest(target=self._element_id)
        response: var_msgs.GetReferenceIsDirectResponse = self._client.ReferenceVariableGetIsDirect(
            request
        )
        return response.is_direct

    @interpret_rpc_error(WRAP_TARGET_NOT_FOUND)
    @overrides
    def get_value(self, hid: Optional[str] = None) -> atvi.VariableState:
        if hid is not None:
            raise ValueError("This engine implementation does not yet support HIDs.")
        request = var_msgs.GetReferenceValueRequest(target=self._element_id)
        response = self._client.ReferenceVariableGetValue(request)
        interop_value: atvi.IVariableValue
        try:
            interop_value = convert_grpc_value_to_atvi(response.value, self._engine.is_local)
        except ValueError as convert_failure:
            raise aew_api.EngineInternalError(
                "Unexpected failure converting gRPC value response"
            ) from convert_failure
        return atvi.VariableState(value=interop_value, is_valid=response.is_valid)

    @interpret_rpc_error(WRAP_TARGET_NOT_FOUND)
    @overrides
    def get_reference_properties(self) -> Mapping[str, IReferenceProperty]:
        response: var_msgs.ReferencePropertyNames = (
            self._client.ReferenceVariableGetReferenceProperties(self._element_id)
        )

        from . import ReferenceProperty

        return {
            name: ReferenceProperty(element_id=self._element_id, name=name, engine=self._engine)
            for name in response.names
        }


class ReferenceArrayDatapin(ReferenceDatapinBase, mc_api.IReferenceArrayDatapin):
    """
    Represents a reference array datapin.

    .. note::
        This class should not be directly instantiated by clients. Get a Workflow object from
        an instantiated Engine, and use it to get a valid instance of this object.
    """

    @overrides
    def __init__(self, element_id: ElementId, engine: "Engine"):
        """
        Initialize a new instance.

        Parameters
        ----------
        element_id: ElementId
            The id of the variable.
        engine: Engine
            The Engine that created this datapin.
        """
        super(ReferenceArrayDatapin, self).__init__(element_id=element_id, engine=engine)

    @overrides
    def __eq__(self, other):
        return isinstance(other, ReferenceArrayDatapin) and self.element_id == other.element_id

    @overload
    @abstractmethod
    def __getitem__(self, index: int) -> IDatapinReferenceBase:
        """
        Gets a ReferenceArrayDatapinElement at the index provided.

        Parameters
        ----------
        index: int
            The index in the ReferenceArrayDatapin.

        Return
        ------
        The ReferenceArrayDatapinElement at the given index.
        """
        return self.__getitem__(index)

    @overload
    @abstractmethod
    def __getitem__(self, index: slice) -> MutableSequence[IDatapinReferenceBase]:
        """
        Gets a subsection of the ReferenceArrayDatapin.

        Parameters
        ----------
        index: slice
            The slice to take from the array.

        Return
        ------
        A Sequence of ReferenceArrayDatapinElements
        """
        return self.__getitem__(index)

    def __getitem__(
        self, index: Union[int, slice]
    ) -> Union[IDatapinReferenceBase, MutableSequence[IDatapinReferenceBase]]:
        """
        Implementation of __getitem__ for ReferenceArrayDatapins.

        Parameters
        ----------
        index: int | slice
            The index in the ReferenceArrayDatapin or a slice of the ReferenceArrayDatapin to
            return.

        Return
        ------
        The ReferenceArrayDatapinElement at the given index or a slice of the ReferenceArrayDatapin.
        """
        if isinstance(index, slice):
            raise NotImplementedError()
        elif isinstance(index, int):
            return ReferenceArrayDatapinElement(
                parent_client=self._client,
                parent_element_id=self._element_id,
                index=index,
                parent_engine=self._engine,
            )
        else:
            raise TypeError(
                "Indexing ReferenceArrayDatapin using "
                + type(index).__name__
                + " is not supported."
            )

    @overload
    @abstractmethod
    def __setitem__(self, index: int, value: IDatapinReferenceBase) -> None:
        """
        Sets a ReferenceArrayDatapinElement at the index provided.

        Parameters
        ----------
        index: int
            The index in the ReferenceArrayDatapin.
        value: IDatapinReferenceBase
            The element to set.
        """
        self.__setitem__(index, value)

    @overload
    @abstractmethod
    def __setitem__(self, index: slice, value: Iterable[IDatapinReferenceBase]) -> None:
        """
        Sets a subsection of the ReferenceArrayDatapinElement.

        Parameters
        ----------
        index: slice
            The slice to take from the array.
        value: Iterable[IDatapinReferenceBase]
            A sequence of elements to set.
        """
        self.__setitem__(index, value)

    def __setitem__(
        self,
        index: Union[int, slice],
        value: Union[IDatapinReferenceBase, Iterable[IDatapinReferenceBase]],
    ) -> None:
        """
        Implementation of __setitem__ for ReferenceArrayDatapins.

        Parameters
        ----------
        index: int | slice
            The index in the ReferenceArrayDatapin or a slice of the ReferenceArrayDatapin to set.
        value: IDatapinReferenceBase | Iterable[IDatapinReferenceBase]
            The element or sequence of elements to set.
        """
        if isinstance(index, slice) or isinstance(value, Iterable):
            raise NotImplementedError()
        elif isinstance(index, int):
            # set all properties of the array element
            self[index].equation = value.equation
        else:
            raise TypeError(
                "Indexing ReferenceArrayDatapin using "
                + type(index).__name__
                + " is not supported."
            )

    @overload
    @abstractmethod
    def __delitem__(self, index: int) -> None:
        """
        Delete an element at the index provided.

        Parameters
        ----------
        index: int
            The index of the element to delete.
        """
        self.__delitem__(index)

    @overload
    @abstractmethod
    def __delitem__(self, index: slice) -> None:
        """
        Delete a subsection of elements.

        Parameters
        ----------
        index: slice
            The slice to take from the array.
        """
        self.__delitem__(index)

    def __delitem__(self, index: Union[int, slice]) -> None:
        """
        Implementation of __delitem__ for ReferenceArrayDatapins.

        Parameters
        ----------
        index: int | slice
            The index in the ReferenceArrayDatapin or a slice of it to delete.
        """
        if isinstance(index, slice):
            raise NotImplementedError()
        elif isinstance(index, int):
            self.pop(index)
        else:
            raise TypeError(
                "Indexing ReferenceArrayDatapin using "
                + type(index).__name__
                + " is not supported."
            )

    @interpret_rpc_error(WRAP_TARGET_NOT_FOUND)
    def __len__(self) -> int:
        """
        Gets the length of this reference array.

        Return
        ------
        The length of the reference array.
        """
        response: var_msgs.IntegerValue = self._client.ReferenceArrayGetLength(self._element_id)
        assert response.value >= 0
        return response.value

    @interpret_rpc_error({**WRAP_TARGET_NOT_FOUND, **WRAP_OUT_OF_BOUNDS})
    def _set_length(self, new_size: int) -> None:
        request = wkfl_msgs.SetReferenceArrayLengthRequest(
            target=self._element_id, new_size=new_size
        )
        self._client.ReferenceArraySetLength(request)

    @overrides
    def append(self, value: IDatapinReferenceBase) -> None:
        self.extend([value])

    @overrides
    def clear(self) -> None:
        self._set_length(0)

    @overrides
    def extend(self, values: Iterable[IDatapinReferenceBase]) -> None:
        iter_length: int = sum(1 for i in values)
        current_length: int = len(self)
        self._set_length(current_length + iter_length)
        for idx, value in enumerate(values):
            self[current_length + idx] = value

    @overrides
    def reverse(self) -> None:
        raise NotImplementedError("Reversing this array is not supported.")

    @overrides
    def pop(self, index: int = -1) -> IDatapinReferenceBase:
        current_length: int = len(self)
        if index == -1:
            index = current_length - 1
        if index != current_length - 1:
            raise NotImplementedError(
                "Only removing elements at the end of the array is supported."
            )
        value: IDatapinReferenceBase = self[current_length - 1]
        self._set_length(current_length - 1)
        return value

    @overrides
    def insert(self, index: int, value: IDatapinReferenceBase) -> None:
        current_length: int = len(self)
        if index != current_length:
            raise NotImplementedError("Only adding elements at the end of the array is supported.")
        self._set_length(current_length + 1)
        self[current_length] = value

    @overrides
    def remove(self, value: IDatapinReferenceBase) -> None:
        raise NotImplementedError("Removing arbitrary elements is not supported.")

    @overrides
    def __iadd__(
        self: "ReferenceArrayDatapin", values: Iterable[IDatapinReferenceBase]
    ) -> "ReferenceArrayDatapin":
        self.extend(values)
        return self

    @interpret_rpc_error({**WRAP_TARGET_NOT_FOUND, **WRAP_OUT_OF_BOUNDS})
    @overrides
    def set_value(self, value: atvi.VariableState) -> None:
        if not isinstance(value.value, atvi.RealArrayValue):
            raise atvi.IncompatibleTypesException(
                value.value.variable_type, atvi.VariableType.REAL_ARRAY
            )
        new_value = var_value_convert.convert_interop_value_to_grpc(value.value).double_array_value
        request = var_msgs.SetDoubleArrayValueRequest(target=self._element_id, new_value=new_value)
        response = self._client.ReferenceArraySetReferencedValues(request)
        return response.was_changed

    @interpret_rpc_error(WRAP_TARGET_NOT_FOUND)
    @overrides
    def get_reference_properties(self) -> Mapping[str, IReferenceArrayProperty]:
        response: var_msgs.ReferencePropertyNames = (
            self._client.ReferenceVariableGetReferenceProperties(self._element_id)
        )

        from . import ReferenceArrayProperty

        return {
            name: ReferenceArrayProperty(
                element_id=self._element_id, name=name, engine=self._engine
            )
            for name in response.names
        }
