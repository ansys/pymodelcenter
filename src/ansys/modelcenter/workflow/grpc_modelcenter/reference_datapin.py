# Copyright (C) 2022 - 2024 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
"""Defines the reference datapin classes.

These classes include ``ReferenceDatapin`` and ``ReferenceArrayDatapin``.
"""
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Mapping, Optional, Sequence, Union, overload

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
    WRAP_INVALID_ARG,
    WRAP_OUT_OF_BOUNDS,
    WRAP_TARGET_NOT_FOUND,
    interpret_rpc_error,
)


class ReferenceArrayDatapinElement(mc_api.IDatapinReferenceBase):
    """Represents a single element in an reference array datapin.

    .. note::
        This class should not be directly instantiated by clients. Get a ``Workflow`` object from
        an instantiated ``Engine`` instance and use it to get a valid ``ReferenceArrayDatapin``
        instance, which can then be indexed to get an object of this type.
    """

    def __init__(
        self,
        parent_client: ModelCenterWorkflowServiceStub,
        parent_element_id: ElementId,
        index: int,
        parent_engine: "Engine",
    ):
        """Initialize an instance.

        Parameters
        ----------
        parent_client : ModelCenterWorkflowServiceStub
            Client used by the parent array.
        parent_element_id : ElementId
            ID of the parent array.
        index : int
            Index of the reference datapin in the parent array.
        parent_engine : Engine
            Engine to use to create the parent array datapin.
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
    @interpret_rpc_error({**WRAP_TARGET_NOT_FOUND, **WRAP_OUT_OF_BOUNDS, **WRAP_INVALID_ARG})
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
    def get_state(self, hid: Optional[str] = None) -> atvi.VariableState:
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
                "Unexpected failure occurred converting gRPC value response."
            ) from convert_failure
        return atvi.VariableState(value=interop_value, is_valid=response.is_valid)

    @interpret_rpc_error({**WRAP_TARGET_NOT_FOUND, **WRAP_OUT_OF_BOUNDS})
    @overrides
    def set_state(self, state: atvi.VariableState) -> None:
        if (
            not isinstance(state.value, atvi.BooleanValue)
            and not isinstance(state.value, atvi.RealValue)
            and not isinstance(state.value, atvi.IntegerValue)
            and not isinstance(state.value, atvi.StringValue)
            and not isinstance(state.value, atvi.FileValue)
        ):
            raise atvi.IncompatibleTypesException(
                state.value.variable_type, atvi.VariableType.UNKNOWN
            )
        new_value = var_value_convert.convert_interop_value_to_grpc(state.value)
        request = var_msgs.SetReferenceValueRequest(
            target=self._parent_element_id, index=self._index, new_value=new_value
        )
        response = self._client.ReferenceVariableSetValue(request)
        return response.was_changed


class ReferenceDatapinBase(BaseDatapin, ABC):
    """Defines the base class for reference datapins.

    This class is for implementing what is common between scalar and
    array reference datapins.
    """

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
                f"Expected {ReferenceDatapinMetadata}, "
                f"but received {new_metadata.__class__}."
            )
        request = var_msgs.SetReferenceVariableMetadataRequest(target=self._element_id)
        fill_reference_metadata_message(new_metadata, request.new_metadata)
        self._client.ReferenceVariableSetMetadata(request)


class ReferenceDatapin(ReferenceDatapinBase, mc_api.IReferenceDatapin):
    """Represents a reference datapin.

    .. note::
        This class should not be directly instantiated by clients. Get a ``Workflow`` object from
        an instantiated ``Engine`` instance and use it to get a valid instance of this object.
    """

    def __init__(self, element_id: ElementId, engine: "Engine"):
        """Initialize an instance.

        Parameters
        ----------
        element_id : ElementId
            ID of the datapin.
        engine: Engine
            `Engine to use to create the datapin.
        """
        super(ReferenceDatapin, self).__init__(element_id=element_id, engine=engine)

    @overrides
    def __eq__(self, other):
        return isinstance(other, ReferenceDatapin) and self.element_id == other.element_id

    @interpret_rpc_error({**WRAP_TARGET_NOT_FOUND, **WRAP_OUT_OF_BOUNDS})
    @overrides
    def set_state(self, state: atvi.VariableState) -> None:
        if (
            not isinstance(state.value, atvi.BooleanValue)
            and not isinstance(state.value, atvi.RealValue)
            and not isinstance(state.value, atvi.IntegerValue)
            and not isinstance(state.value, atvi.StringValue)
            and not isinstance(state.value, atvi.FileValue)
        ):
            raise atvi.IncompatibleTypesException(
                state.value.variable_type, atvi.VariableType.UNKNOWN
            )
        new_value = var_value_convert.convert_interop_value_to_grpc(state.value)
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
    @interpret_rpc_error({**WRAP_TARGET_NOT_FOUND, **WRAP_INVALID_ARG})
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
    def get_state(self, hid: Optional[str] = None) -> atvi.VariableState:
        if hid is not None:
            raise ValueError("This engine implementation does not yet support HIDs.")
        request = var_msgs.GetReferenceValueRequest(target=self._element_id)
        response = self._client.ReferenceVariableGetValue(request)
        interop_value: atvi.IVariableValue
        try:
            interop_value = convert_grpc_value_to_atvi(response.value, self._engine.is_local)
        except ValueError as convert_failure:
            raise aew_api.EngineInternalError(
                "Unexpected failure occurred converting gRPC value response."
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
    """Represents a reference array datapin.

    .. note::
        This class should not be directly instantiated by clients. Get a ``Workflow`` object from
        an instantiated ``Engine`` instance  and use it to get a valid instance of this object.
    """

    @overrides
    def __init__(self, element_id: ElementId, engine: "Engine"):
        """Initialize an instance.

        Parameters
        ----------
        element_id : ElementId
            ID of the datapin.
        engine : Engine
            Engine to use to create the datapin.
        """
        super(ReferenceArrayDatapin, self).__init__(element_id=element_id, engine=engine)

    @overrides
    def __eq__(self, other):
        return isinstance(other, ReferenceArrayDatapin) and self.element_id == other.element_id

    @overload
    @abstractmethod
    def __getitem__(self, index: int) -> IDatapinReferenceBase:
        """Get an reference array datapin element at a given index.

        Parameters
        ----------
        index : int
            Index in the reference array datapin.

        Returns
        -------
        ``ReferenceArrayDatapinElement`` at the given index.
        """
        return self.__getitem__(index)

    @overload
    @abstractmethod
    def __getitem__(self, index: slice) -> Sequence[IDatapinReferenceBase]:
        """Get a subsection of the reference array datapins.

        Parameters
        ----------
        index : slice
            Slice to take from the array.

        Returns
        -------
        ``Sequence`` of ``ReferenceArrayDatapinElements``.
        """
        return self.__getitem__(index)

    def __getitem__(
        self, index: Union[int, slice]
    ) -> Union[IDatapinReferenceBase, Sequence[IDatapinReferenceBase]]:
        """Implementation of __getitem__ for ``ReferenceArrayDatapins``.

        Parameters
        ----------
        index: int | slice
            Index in the reference array datapin or a slice of the
            reference array datapin to return.

        Returns
        -------
        ``ReferenceArrayDatapinElement`` at the given index or a slice
        of the reference array datapin.
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

    @interpret_rpc_error(WRAP_TARGET_NOT_FOUND)
    def __len__(self) -> int:
        """Get the length of the reference array.

        Returns
        -------
        Length of the reference array.
        """
        response: var_msgs.IntegerValue = self._client.ReferenceArrayGetLength(self._element_id)
        assert response.value >= 0
        return response.value

    @interpret_rpc_error({**WRAP_TARGET_NOT_FOUND, **WRAP_OUT_OF_BOUNDS})
    @overrides
    def set_length(self, new_size: int) -> None:
        request = wkfl_msgs.SetReferenceArrayLengthRequest(
            target=self._element_id, new_size=new_size
        )
        self._client.ReferenceArraySetLength(request)

    @interpret_rpc_error({**WRAP_TARGET_NOT_FOUND, **WRAP_OUT_OF_BOUNDS, **WRAP_INVALID_ARG})
    @overrides
    def set_state(self, state: atvi.VariableState) -> None:
        if not isinstance(state.value, atvi.RealArrayValue):
            raise atvi.IncompatibleTypesException(
                state.value.variable_type, atvi.VariableType.REAL_ARRAY
            )
        new_value = var_value_convert.convert_interop_value_to_grpc(state.value).double_array_value
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
