# Copyright (C) 2022 - 2025 ANSYS, Inc. and/or its affiliates.
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

from os import PathLike
from typing import Optional, Type, Union
import unittest.mock

import ansys.api.modelcenter.v0.element_messages_pb2 as elem_msgs
import ansys.api.modelcenter.v0.variable_value_messages_pb2 as var_msgs
import ansys.api.modelcenter.v0.workflow_messages_pb2 as wkfl_msgs
import ansys.tools.variableinterop as atvi
import pytest

from ansys.modelcenter.workflow.api import IReferenceArrayProperty, IReferenceProperty
import ansys.modelcenter.workflow.grpc_modelcenter as grpcmc
from ansys.modelcenter.workflow.grpc_modelcenter import ReferenceArrayProperty, ReferenceProperty
from ansys.modelcenter.workflow.grpc_modelcenter.abstract_workflow_element import (
    AbstractWorkflowElement,
)

from .grpc_server_test_utils.client_creation_monkeypatch import monkeypatch_client_creation
from .grpc_server_test_utils.mock_file_value import MockFileValue
from .test_datapin import do_get_state_test, do_get_state_test_with_hid


class MockWorkflowClientForRefVarTest:
    def __init__(self):
        pass

    def ReferenceVariableGetReferenceEquation(self, request):
        pass

    def ReferenceVariableSetReferenceEquation(self, request):
        pass

    def ReferenceVariableGetIsDirect(self, request):
        pass

    def ReferenceVariableSetValue(self, request):
        pass

    def ReferenceVariableGetValue(self, request):
        pass

    def ReferenceArraySetReferencedValues(self, request):
        pass

    def ReferenceVariableGetReferencedVariables(self, request):
        pass

    def ReferenceArrayGetLength(self, request):
        pass

    def ReferenceArraySetLength(self, request):
        pass

    def ReferenceVariableGetMetadata(
        self, request: elem_msgs.ElementId
    ) -> var_msgs.ReferenceVariableMetadata:
        return var_msgs.ReferenceVariableMetadata()

    def ReferenceVariableSetMetadata(
        self, request: var_msgs.SetReferenceVariableMetadataRequest
    ) -> var_msgs.SetMetadataResponse:
        return var_msgs.SetMetadataResponse()

    def ReferenceVariableGetReferenceProperties(self):
        pass


def test_get_reference_equation(monkeypatch, engine) -> None:
    # Arrange
    test_equation = "ඞ"

    mock_client = MockWorkflowClientForRefVarTest()
    mock_response = var_msgs.GetReferenceEquationResponse(equation=test_equation)
    with unittest.mock.patch.object(
        mock_client, "ReferenceVariableGetReferenceEquation", return_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut_element_id = elem_msgs.ElementId(id_string="VAR_UNDER_TEST_ID")
        sut = grpcmc.ReferenceDatapin(sut_element_id, engine)

        # Act
        equation: str = sut.equation

        # Assert
        expected_request = var_msgs.GetReferenceEquationRequest(target=sut_element_id)
        mock_grpc_method.assert_called_once_with(expected_request)
        assert equation == test_equation


def test_set_reference_equation(monkeypatch, engine) -> None:
    # Arrange
    mock_client = MockWorkflowClientForRefVarTest()
    mock_response = var_msgs.SetReferenceEquationResponse()
    with unittest.mock.patch.object(
        mock_client, "ReferenceVariableSetReferenceEquation", return_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut_element_id = elem_msgs.ElementId(id_string="VAR_UNDER_TEST_ID")
        sut = grpcmc.ReferenceDatapin(sut_element_id, engine)

        # Act
        sut.equation = "ඞ"

        # Assert
        expected_request = var_msgs.SetReferenceEquationRequest(target=sut_element_id, equation="ඞ")
        mock_grpc_method.assert_called_once_with(expected_request)


@pytest.mark.parametrize("is_direct", [True, False])
def test_get_is_direct(monkeypatch, engine, is_direct) -> None:
    # Arrange
    mock_client = MockWorkflowClientForRefVarTest()
    mock_response = var_msgs.GetReferenceIsDirectResponse(is_direct=is_direct)
    with unittest.mock.patch.object(
        mock_client, "ReferenceVariableGetIsDirect", return_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut_element_id = elem_msgs.ElementId(id_string="VAR_UNDER_TEST_ID")
        sut = grpcmc.ReferenceDatapin(sut_element_id, engine)

        # Act
        result_is_direct: bool = sut.is_direct

        # Assert
        expected_request = var_msgs.GetReferenceIsDirectRequest(target=sut_element_id)
        mock_grpc_method.assert_called_once_with(expected_request)
        assert is_direct == result_is_direct


@pytest.mark.parametrize(
    "set_value,expected_value_in_request",
    [
        (atvi.BooleanValue(True), var_msgs.VariableValue(bool_value=True)),
        (atvi.RealValue(4.7), var_msgs.VariableValue(double_value=4.7)),
        (atvi.IntegerValue(47), var_msgs.VariableValue(int_value=47)),
        (
            atvi.StringValue("This is a test string value."),
            var_msgs.VariableValue(string_value="This is a test string value."),
        ),
    ],
)
def test_scalar_set_allowed(monkeypatch, engine, set_value, expected_value_in_request):
    # Arrange
    mock_client = MockWorkflowClientForRefVarTest()
    mock_response = var_msgs.SetVariableValueResponse()
    with unittest.mock.patch.object(
        mock_client, "ReferenceVariableSetValue", return_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut_element_id = elem_msgs.ElementId(id_string="VAR_UNDER_TEST_ID")
        sut = grpcmc.ReferenceDatapin(sut_element_id, engine)
        new_state = atvi.VariableState(set_value, True)

        # Act
        sut.set_state(new_state)

        # Assert
        expected_request = var_msgs.SetReferenceValueRequest(
            target=sut_element_id, new_value=expected_value_in_request
        )
        mock_grpc_method.assert_called_once_with(expected_request)


@pytest.mark.parametrize(
    "set_value",
    [
        atvi.IntegerArrayValue(),
        atvi.RealArrayValue(),
        atvi.BooleanArrayValue(),
        atvi.StringArrayValue(),
    ],
)
def test_scalar_set_disallowed(monkeypatch, engine, set_value):
    # Arrange
    mock_client = MockWorkflowClientForRefVarTest()
    mock_response = var_msgs.SetVariableValueResponse()
    with unittest.mock.patch.object(
        mock_client, "ReferenceVariableSetValue", return_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut_element_id = elem_msgs.ElementId(id_string="VAR_UNDER_TEST_ID")
        sut = grpcmc.ReferenceDatapin(sut_element_id, engine)
        new_state = atvi.VariableState(set_value, True)

        # Act
        with pytest.raises(atvi.IncompatibleTypesException):
            sut.set_state(new_state)

        # Assert
        mock_grpc_method.assert_not_called()


@pytest.mark.parametrize(
    "variable_value,is_valid,expected_result",
    [
        (
            var_msgs.VariableValue(double_value=-867.5309),
            True,
            atvi.VariableState(atvi.RealValue(-867.5309), True),
        ),
        (
            var_msgs.VariableValue(
                double_array_value=var_msgs.DoubleArrayValue(
                    dims=var_msgs.ArrayDimensions(dims=[2, 2]), values=[1.0, 1.1, 2.0, 2.1]
                )
            ),
            False,
            atvi.VariableState(
                atvi.RealArrayValue(shape_=(2, 2), values=[[1.0, 1.1], [2.0, 2.1]]), False
            ),
        ),
        (
            var_msgs.VariableValue(bool_value=True),
            False,
            atvi.VariableState(atvi.BooleanValue(True), False),
        ),
        (
            var_msgs.VariableValue(
                bool_array_value=var_msgs.BooleanArrayValue(
                    dims=var_msgs.ArrayDimensions(dims=[2, 2]), values=[True, False, False, True]
                )
            ),
            True,
            atvi.VariableState(
                atvi.BooleanArrayValue(shape_=(2, 2), values=[[True, False], [False, True]]), True
            ),
        ),
        (
            var_msgs.VariableValue(int_value=47),
            True,
            atvi.VariableState(atvi.IntegerValue(47), True),
        ),
        (
            var_msgs.VariableValue(
                int_array_value=var_msgs.IntegerArrayValue(
                    dims=var_msgs.ArrayDimensions(dims=[2, 2]), values=[-8675309, 47, -1, 0]
                )
            ),
            False,
            atvi.VariableState(
                atvi.IntegerArrayValue(shape_=(2, 2), values=[[-8675309, 47], [-1, 0]]), False
            ),
        ),
        (
            var_msgs.VariableValue(string_value="(╯°□°）╯︵ ┻━┻"),
            True,
            atvi.VariableState(atvi.StringValue("(╯°□°）╯︵ ┻━┻"), True),
        ),
        (
            var_msgs.VariableValue(
                string_array_value=var_msgs.StringArrayValue(
                    dims=var_msgs.ArrayDimensions(dims=[2, 2]),
                    values=["primary", "secondary", "first", "second"],
                )
            ),
            False,
            atvi.VariableState(
                atvi.StringArrayValue(
                    shape_=(2, 2), values=[["primary", "secondary"], ["first", "second"]]
                ),
                False,
            ),
        ),
        (
            var_msgs.VariableValue(file_value=var_msgs.FileValue()),
            True,
            atvi.VariableState(MockFileValue(""), True),
        ),
        (
            var_msgs.VariableValue(
                file_array_value=var_msgs.FileArrayValue(
                    dims=var_msgs.ArrayDimensions(dims=[2, 2]),
                    values=[
                        var_msgs.FileValue(),
                        var_msgs.FileValue(),
                        var_msgs.FileValue(),
                        var_msgs.FileValue(),
                    ],
                )
            ),
            False,
            atvi.VariableState(
                atvi.FileArrayValue(
                    shape_=(2, 2),
                    values=[
                        [MockFileValue(""), MockFileValue("")],
                        [MockFileValue(""), MockFileValue("")],
                    ],
                ),
                False,
            ),
        ),
    ],
)
def test_get_value(monkeypatch, engine, variable_value, is_valid, expected_result) -> None:
    # Arrange
    def mock_read(self, to_read: PathLike, mime_type: Optional[str], encoding: Optional[str]):
        return MockFileValue(str(to_read))

    monkeypatch.setattr(atvi.NonManagingFileScope, "read_from_file", mock_read)

    mock_response = var_msgs.VariableState(value=variable_value, is_valid=is_valid)

    mock_client = MockWorkflowClientForRefVarTest()
    sut_element_id = elem_msgs.ElementId(id_string="VAR_UNDER_TEST_ID")

    with unittest.mock.patch.object(
        mock_client, "ReferenceVariableGetValue", return_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = grpcmc.ReferenceDatapin(element_id=sut_element_id, engine=engine)

        # Act
        result: atvi.VariableState = sut.get_state()

        # Assert
        expected_request = var_msgs.GetReferenceValueRequest(target=sut_element_id)
        mock_grpc_method.assert_called_once_with(expected_request)

        assert result.value == expected_result.value
        assert result.is_valid == expected_result.is_valid


def test_get_value_with_hid(monkeypatch, engine) -> None:
    # Arrange
    mock_client = MockWorkflowClientForRefVarTest()
    sut_element_id = elem_msgs.ElementId(id_string="VAR_UNDER_TEST_ID")

    with unittest.mock.patch.object(
        mock_client, "ReferenceVariableGetValue", return_value=var_msgs.VariableState()
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = grpcmc.ReferenceDatapin(element_id=sut_element_id, engine=engine)

        # Act/Assert
        with pytest.raises(ValueError, match="does not yet support HIDs."):
            sut.get_state("some_hid")

        mock_grpc_method.assert_not_called()


@pytest.mark.parametrize(
    "set_value,expected_value_in_request",
    [
        (
            atvi.RealArrayValue(shape_=(0,), values=[]),
            var_msgs.DoubleArrayValue(dims=var_msgs.ArrayDimensions(dims=[0]), values=[]),
        ),
        (
            atvi.RealArrayValue(shape_=(2,), values=[-9.4, 3.87]),
            var_msgs.DoubleArrayValue(dims=var_msgs.ArrayDimensions(dims=[2]), values=[-9.4, 3.87]),
        ),
        (
            atvi.RealArrayValue(
                shape_=(3, 3), values=[[-9.4, 3.87, 5.29], [-49.599, 1.0, 4.22], [99.999, 4.5, 3.1]]
            ),
            var_msgs.DoubleArrayValue(
                dims=var_msgs.ArrayDimensions(dims=[3, 3]),
                values=[-9.4, 3.87, 5.29, -49.599, 1.0, 4.22, 99.999, 4.5, 3.1],
            ),
        ),
    ],
)
def test_array_set_allowed(monkeypatch, engine, set_value, expected_value_in_request):
    # Arrange
    mock_client = MockWorkflowClientForRefVarTest()
    mock_response = var_msgs.SetVariableValueResponse()
    sut_element_id = elem_msgs.ElementId(id_string="VAR_UNDER_TEST_ID")
    with unittest.mock.patch.object(
        mock_client, "ReferenceArraySetReferencedValues", return_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = grpcmc.ReferenceArrayDatapin(sut_element_id, engine=engine)
        new_state = atvi.VariableState(set_value, True)

        # Act
        sut.set_state(new_state)

        # Assert
        expected_request = var_msgs.SetDoubleArrayValueRequest(
            target=sut_element_id, new_value=expected_value_in_request
        )
        mock_grpc_method.assert_called_once_with(expected_request)


@pytest.mark.parametrize(
    "set_value",
    [
        atvi.IntegerValue(),
        atvi.RealValue(),
        atvi.BooleanValue(),
        atvi.StringValue(),
        MockFileValue(),
        atvi.IntegerArrayValue(),
        atvi.BooleanArrayValue(),
        atvi.StringArrayValue(),
        atvi.FileArrayValue(),
    ],
)
def test_array_set_disallowed(monkeypatch, engine, set_value):
    # Arrange
    mock_client = MockWorkflowClientForRefVarTest()
    mock_response = var_msgs.SetVariableValueResponse()
    with unittest.mock.patch.object(
        mock_client, "ReferenceArraySetReferencedValues", return_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut_element_id = elem_msgs.ElementId(id_string="VAR_UNDER_TEST_ID")
        sut = grpcmc.ReferenceArrayDatapin(sut_element_id, engine)
        new_state = atvi.VariableState(set_value, True)

        # Act
        with pytest.raises(atvi.IncompatibleTypesException):
            sut.set_state(new_state)

        # Assert
        mock_grpc_method.assert_not_called()


def test_array_get_state_with_hid(monkeypatch, engine):
    do_get_state_test_with_hid(monkeypatch, engine, grpcmc.ReferenceArrayDatapin)


@pytest.mark.parametrize(
    "value_in_response,validity_in_response,expected_atvi_state",
    [
        (
            var_msgs.DoubleArrayValue(
                dims=var_msgs.ArrayDimensions(
                    dims=[
                        4,
                    ]
                ),
                values=[-867.5309, 9000.1, -1.0, 1.0],
            ),
            True,
            atvi.VariableState(
                atvi.RealArrayValue(shape_=(4,), values=[-867.5309, 9000.1, -1.0, 1.0]), True
            ),
        ),
        (
            var_msgs.DoubleArrayValue(
                dims=var_msgs.ArrayDimensions(
                    dims=[
                        4,
                    ]
                ),
                values=[1.0, 1.1, 2.0, 2.1],
            ),
            False,
            atvi.VariableState(
                atvi.RealArrayValue(shape_=(4,), values=[1.0, 1.1, 2.0, 2.1]), False
            ),
        ),
    ],
)
def test_array_get_state(
    monkeypatch, engine, value_in_response, validity_in_response, expected_atvi_state
):
    do_get_state_test(
        monkeypatch,
        engine,
        grpcmc.ReferenceArrayDatapin,
        var_msgs.VariableState(
            is_valid=validity_in_response,
            value=var_msgs.VariableValue(double_array_value=value_in_response),
        ),
        expected_atvi_state,
    )


@pytest.mark.parametrize("is_direct", [True, False])
def test_array_index_get_is_direct(monkeypatch, engine, is_direct) -> None:
    # Arrange
    mock_client = MockWorkflowClientForRefVarTest()
    mock_is_direct_response = var_msgs.GetReferenceIsDirectResponse(is_direct=is_direct)
    test_index = 4

    with unittest.mock.patch.object(
        mock_client, "ReferenceVariableGetIsDirect", return_value=mock_is_direct_response
    ) as mock_is_direct_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut_element_id = elem_msgs.ElementId(id_string="VAR_UNDER_TEST_ID")
        sut = grpcmc.ReferenceArrayDatapin(sut_element_id, engine)

        # Act
        response: bool = sut[test_index].is_direct

        # Assert
        is_direct_expected_request = var_msgs.GetReferenceIsDirectRequest(
            target=sut_element_id, index=test_index
        )
        mock_is_direct_grpc_method.assert_called_once_with(is_direct_expected_request)
        assert response == is_direct


def test_array_index_get_reference_equation(monkeypatch, engine) -> None:
    # Arrange
    test_index = 4
    test_equation = "ඞ"

    mock_client = MockWorkflowClientForRefVarTest()
    mock_response = var_msgs.GetReferenceEquationResponse(equation=test_equation)

    with unittest.mock.patch.object(
        mock_client, "ReferenceVariableGetReferenceEquation", return_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut_element_id = elem_msgs.ElementId(id_string="VAR_UNDER_TEST_ID")
        sut = grpcmc.ReferenceArrayDatapin(sut_element_id, engine)

        # Act
        equation: str = sut[test_index].equation

        # Assert
        expected_request = var_msgs.GetReferenceEquationRequest(
            target=sut_element_id, index=test_index
        )
        mock_grpc_method.assert_called_once_with(expected_request)
        assert equation == test_equation


def test_array_index_set_reference_equation(monkeypatch, engine) -> None:
    # Arrange
    test_index = 4

    mock_client = MockWorkflowClientForRefVarTest()
    mock_response = var_msgs.SetReferenceEquationResponse()
    with unittest.mock.patch.object(
        mock_client, "ReferenceVariableSetReferenceEquation", return_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut_element_id = elem_msgs.ElementId(id_string="VAR_UNDER_TEST_ID")
        sut = grpcmc.ReferenceArrayDatapin(sut_element_id, engine)

        # Act
        sut[4].equation = "ඞ"

        # Assert
        expected_request = var_msgs.SetReferenceEquationRequest(
            target=sut_element_id, index=test_index, equation="ඞ"
        )
        mock_grpc_method.assert_called_once_with(expected_request)


@pytest.mark.parametrize(
    "description_string,sut_type",
    [
        ("", grpcmc.ReferenceDatapin),
        ("This is a mock datapin description.", grpcmc.ReferenceDatapin),
        ("", grpcmc.ReferenceArrayDatapin),
        ("This is a mock datapin description.", grpcmc.ReferenceArrayDatapin),
    ],
)
def test_retrieved_metadata_should_include_description(
    monkeypatch,
    engine,
    description_string: str,
    sut_type: Union[Type[grpcmc.ReferenceArrayDatapin], Type[grpcmc.ReferenceDatapin]],
):
    # Set up
    mock_client = MockWorkflowClientForRefVarTest()
    mock_response = var_msgs.ReferenceVariableMetadata()
    sut_element_id = elem_msgs.ElementId(id_string="VAR_UNDER_TEST_ID")
    mock_response.base_metadata.description = description_string
    with unittest.mock.patch.object(
        mock_client, "ReferenceVariableGetMetadata", return_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = sut_type(sut_element_id, engine=engine)

        # Execute
        result: grpcmc.ReferenceDatapinMetadata = sut.get_metadata()

        # Verify
        mock_grpc_method.assert_called_once_with(sut_element_id)
        assert isinstance(
            result, grpcmc.ReferenceDatapinMetadata
        ), "The metadata should have the correct type."
        assert (
            result.description == description_string
        ), "The description string should match what was supplied by the gRPC client."


@pytest.mark.parametrize(
    "sut_type",
    [grpcmc.ReferenceDatapin, grpcmc.ReferenceArrayDatapin],
)
def test_retrieved_metadata_should_include_custom_metadata_empty(
    monkeypatch,
    engine,
    sut_type: Union[Type[grpcmc.ReferenceDatapin], Type[grpcmc.ReferenceArrayDatapin]],
):
    # Set up
    mock_client = MockWorkflowClientForRefVarTest()
    mock_response = var_msgs.ReferenceVariableMetadata()
    sut_element_id = elem_msgs.ElementId(id_string="VAR_UNDER_TEST_ID")
    with unittest.mock.patch.object(
        mock_client, "ReferenceVariableGetMetadata", return_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = sut_type(sut_element_id, engine)

        # Execute
        result: grpcmc.ReferenceDatapinMetadata = sut.get_metadata()

        # Verify
        mock_grpc_method.assert_called_once_with(sut_element_id)
        assert isinstance(
            result, grpcmc.ReferenceDatapinMetadata
        ), "The metadata should have the correct type."
        assert (
            len(result.custom_metadata) == 0
        ), "There should be no entries in the custom metadata map."


@pytest.mark.parametrize(
    "sut_type",
    [grpcmc.ReferenceDatapin, grpcmc.ReferenceArrayDatapin],
)
def test_retrieved_metadata_should_include_custom_metadata_populated(
    monkeypatch,
    engine,
    sut_type: Union[Type[grpcmc.ReferenceDatapin], Type[grpcmc.ReferenceArrayDatapin]],
):
    # Set up
    mock_client = MockWorkflowClientForRefVarTest()
    mock_response = var_msgs.ReferenceVariableMetadata()
    mock_response.base_metadata.custom_metadata["test_integer_value"].MergeFrom(
        var_msgs.VariableValue(int_value=47)
    )
    mock_response.base_metadata.custom_metadata["test_double_value"].MergeFrom(
        var_msgs.VariableValue(double_value=-867.5309)
    )
    sut_element_id = elem_msgs.ElementId(id_string="VAR_UNDER_TEST_ID")
    with unittest.mock.patch.object(
        mock_client, "ReferenceVariableGetMetadata", return_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = sut_type(sut_element_id, engine)

        # Execute
        result: grpcmc.ReferenceDatapinMetadata = sut.get_metadata()

        # Verify
        mock_grpc_method.assert_called_once_with(sut_element_id)
        assert isinstance(
            result, grpcmc.ReferenceDatapinMetadata
        ), "The metadata should have the correct type."
        expected_custom_metadata = {
            "test_integer_value": atvi.IntegerValue(47),
            "test_double_value": atvi.RealValue(-867.5309),
        }
        assert (
            result.custom_metadata == expected_custom_metadata
        ), "The custom metadata should have been transferred correctly."


@pytest.mark.parametrize(
    "description,sut_type",
    [
        ("", grpcmc.ReferenceDatapin),
        ("This is a mock datapin description.", grpcmc.ReferenceDatapin),
        ("", grpcmc.ReferenceArrayDatapin),
        ("This is a mock datapin description.", grpcmc.ReferenceArrayDatapin),
    ],
)
def test_set_metadata_empty_custom_metadata(
    monkeypatch,
    engine,
    description: str,
    sut_type: Union[Type[grpcmc.ReferenceDatapin], Type[grpcmc.ReferenceArrayDatapin]],
):
    # Set up
    mock_client = MockWorkflowClientForRefVarTest()
    mock_response = var_msgs.SetMetadataResponse()
    sut_element_id = elem_msgs.ElementId(id_string="VAR_UNDER_TEST_ID")
    with unittest.mock.patch.object(
        mock_client, "ReferenceVariableSetMetadata", return_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = sut_type(sut_element_id, engine)
        new_metadata = grpcmc.ReferenceDatapinMetadata()
        new_metadata.description = description

        # Execute
        sut.set_metadata(new_metadata)

        # Verify
        expected_request = var_msgs.SetReferenceVariableMetadataRequest(target=sut_element_id)
        expected_request.new_metadata.base_metadata.description = description
        mock_grpc_method.assert_called_once_with(expected_request)


@pytest.mark.parametrize(
    "description,sut_type",
    [
        ("", grpcmc.ReferenceDatapin),
        ("This is a mock datapin description.", grpcmc.ReferenceDatapin),
        ("", grpcmc.ReferenceArrayDatapin),
        ("This is a mock datapin description.", grpcmc.ReferenceArrayDatapin),
    ],
)
def test_set_metadata_populated_custom_metadata(
    monkeypatch,
    engine,
    description: str,
    sut_type: Union[Type[grpcmc.ReferenceDatapin], Type[grpcmc.ReferenceArrayDatapin]],
):
    # Set up
    mock_client = MockWorkflowClientForRefVarTest()
    mock_response = var_msgs.SetMetadataResponse()
    sut_element_id = elem_msgs.ElementId(id_string="VAR_UNDER_TEST_ID")
    with unittest.mock.patch.object(
        mock_client, "ReferenceVariableSetMetadata", return_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = sut_type(sut_element_id, engine)
        new_metadata = grpcmc.ReferenceDatapinMetadata()
        new_metadata.description = description
        new_metadata.custom_metadata["int_value"] = atvi.IntegerValue(47)
        new_metadata.custom_metadata["real_value"] = atvi.RealValue(-867.5309)

        # Execute
        sut.set_metadata(new_metadata)

        # Verify
        expected_request = var_msgs.SetReferenceVariableMetadataRequest(target=sut_element_id)
        expected_request.new_metadata.base_metadata.description = description
        expected_request.new_metadata.base_metadata.custom_metadata["int_value"].MergeFrom(
            var_msgs.VariableValue(int_value=47)
        )
        expected_request.new_metadata.base_metadata.custom_metadata["real_value"].MergeFrom(
            var_msgs.VariableValue(double_value=-867.5309)
        )
        mock_grpc_method.assert_called_once_with(expected_request)


@pytest.mark.parametrize(
    "variable_value,is_valid,expected_result",
    [
        (
            var_msgs.VariableValue(double_value=-867.5309),
            True,
            atvi.VariableState(atvi.RealValue(-867.5309), True),
        ),
        (
            var_msgs.VariableValue(
                double_array_value=var_msgs.DoubleArrayValue(
                    dims=var_msgs.ArrayDimensions(dims=[2, 2]), values=[1.0, 1.1, 2.0, 2.1]
                )
            ),
            False,
            atvi.VariableState(
                atvi.RealArrayValue(shape_=(2, 2), values=[[1.0, 1.1], [2.0, 2.1]]), False
            ),
        ),
        (
            var_msgs.VariableValue(bool_value=True),
            False,
            atvi.VariableState(atvi.BooleanValue(True), False),
        ),
        (
            var_msgs.VariableValue(
                bool_array_value=var_msgs.BooleanArrayValue(
                    dims=var_msgs.ArrayDimensions(dims=[2, 2]), values=[True, False, False, True]
                )
            ),
            True,
            atvi.VariableState(
                atvi.BooleanArrayValue(shape_=(2, 2), values=[[True, False], [False, True]]), True
            ),
        ),
        (
            var_msgs.VariableValue(int_value=47),
            True,
            atvi.VariableState(atvi.IntegerValue(47), True),
        ),
        (
            var_msgs.VariableValue(
                int_array_value=var_msgs.IntegerArrayValue(
                    dims=var_msgs.ArrayDimensions(dims=[2, 2]), values=[-8675309, 47, -1, 0]
                )
            ),
            False,
            atvi.VariableState(
                atvi.IntegerArrayValue(shape_=(2, 2), values=[[-8675309, 47], [-1, 0]]), False
            ),
        ),
        (
            var_msgs.VariableValue(string_value="(╯°□°）╯︵ ┻━┻"),
            True,
            atvi.VariableState(atvi.StringValue("(╯°□°）╯︵ ┻━┻"), True),
        ),
        (
            var_msgs.VariableValue(
                string_array_value=var_msgs.StringArrayValue(
                    dims=var_msgs.ArrayDimensions(dims=[2, 2]),
                    values=["primary", "secondary", "first", "second"],
                )
            ),
            False,
            atvi.VariableState(
                atvi.StringArrayValue(
                    shape_=(2, 2), values=[["primary", "secondary"], ["first", "second"]]
                ),
                False,
            ),
        ),
        (
            var_msgs.VariableValue(file_value=var_msgs.FileValue()),
            True,
            atvi.VariableState(MockFileValue(""), True),
        ),
        (
            var_msgs.VariableValue(
                file_array_value=var_msgs.FileArrayValue(
                    dims=var_msgs.ArrayDimensions(dims=[2, 2]),
                    values=[
                        var_msgs.FileValue(),
                        var_msgs.FileValue(),
                        var_msgs.FileValue(),
                        var_msgs.FileValue(),
                    ],
                )
            ),
            False,
            atvi.VariableState(
                atvi.FileArrayValue(
                    shape_=(2, 2),
                    values=[
                        [MockFileValue(""), MockFileValue("")],
                        [MockFileValue(""), MockFileValue("")],
                    ],
                ),
                False,
            ),
        ),
    ],
)
def test_array_index_get_value(
    monkeypatch, engine, variable_value, is_valid, expected_result
) -> None:
    # Arrange
    test_index = 4

    def mock_read(self, to_read: PathLike, mime_type: Optional[str], encoding: Optional[str]):
        return MockFileValue(str(to_read))

    monkeypatch.setattr(atvi.NonManagingFileScope, "read_from_file", mock_read)

    mock_response = var_msgs.VariableState(value=variable_value, is_valid=is_valid)

    mock_client = MockWorkflowClientForRefVarTest()
    sut_element_id = elem_msgs.ElementId(id_string="VAR_UNDER_TEST_ID")

    with unittest.mock.patch.object(
        mock_client, "ReferenceVariableGetValue", return_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = grpcmc.ReferenceArrayDatapin(element_id=sut_element_id, engine=engine)

        # Act
        result: atvi.VariableState = sut[test_index].get_state()

        # Assert
        expected_request = var_msgs.GetReferenceValueRequest(
            target=sut_element_id, index=test_index
        )
        mock_grpc_method.assert_called_once_with(expected_request)

        assert result.value == expected_result.value
        assert result.is_valid == expected_result.is_valid


def test_array_index_get_value_with_hid(monkeypatch, engine) -> None:
    # Arrange
    mock_client = MockWorkflowClientForRefVarTest()
    sut_element_id = elem_msgs.ElementId(id_string="VAR_UNDER_TEST_ID")

    with unittest.mock.patch.object(
        mock_client, "ReferenceVariableGetValue", return_value=var_msgs.VariableState()
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = grpcmc.ReferenceArrayDatapin(element_id=sut_element_id, engine=engine)

        # Act/Assert
        with pytest.raises(ValueError, match="does not yet support HIDs."):
            sut[0].get_state("some_hid")

        mock_grpc_method.assert_not_called()


def test_array_get_length(monkeypatch, engine) -> None:
    # Arrange
    mock_client = MockWorkflowClientForRefVarTest()
    sut_element_id = elem_msgs.ElementId(id_string="VAR_UNDER_TEST_ID")

    test_value = 5
    mock_response = var_msgs.IntegerValue(value=test_value)

    with unittest.mock.patch.object(
        mock_client, "ReferenceArrayGetLength", return_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = grpcmc.ReferenceArrayDatapin(element_id=sut_element_id, engine=engine)

        # Act
        length = len(sut)

        # Assert
        mock_grpc_method.assert_called_once_with(sut_element_id)
        assert length == test_value


def test_get_reference_properties(monkeypatch, engine) -> None:
    # Arrange
    mock_client = MockWorkflowClientForRefVarTest()
    sut_element_id = elem_msgs.ElementId(id_string="VAR_UNDER_TEST_ID")

    response_values = ["multiple", "test", "values"]
    mock_response = var_msgs.ReferencePropertyNames(names=response_values)

    with unittest.mock.patch.object(
        mock_client, "ReferenceVariableGetReferenceProperties", return_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = grpcmc.ReferenceDatapin(element_id=sut_element_id, engine=engine)

        # Act
        result = sut.get_reference_properties()

        # Assert
        assert len(result) == len(response_values)

        for name in response_values:
            if name in result.keys():
                ref_prop: IReferenceProperty = result[name]

                assert type(ref_prop) == ReferenceProperty
                assert ref_prop._element_id == sut_element_id
                assert ref_prop.name == name
                assert ref_prop._engine == engine
            else:
                assert False, f"{name} not found in reference property map."


def test_get_reference_array_properties(monkeypatch, engine) -> None:
    # Arrange
    mock_client = MockWorkflowClientForRefVarTest()
    sut_element_id = elem_msgs.ElementId(id_string="VAR_UNDER_TEST_ID")

    response_values = ["multiple", "test", "values"]
    mock_response = var_msgs.ReferencePropertyNames(names=response_values)

    with unittest.mock.patch.object(
        mock_client, "ReferenceVariableGetReferenceProperties", return_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = grpcmc.ReferenceArrayDatapin(element_id=sut_element_id, engine=engine)

        # Act
        result = sut.get_reference_properties()

        # Assert
        assert len(result) == len(response_values)

        for name in response_values:
            if name in result.keys():
                ref_prop: IReferenceArrayProperty = result[name]

                assert type(ref_prop) == ReferenceArrayProperty
                assert ref_prop._element_id == sut_element_id
                assert ref_prop.name == name
                assert ref_prop._engine == engine
            else:
                assert False, f"{name} not found in reference property map."


def test_array_set_length_0(monkeypatch, engine) -> None:
    # Arrange
    mock_client = MockWorkflowClientForRefVarTest()
    sut_element_id = elem_msgs.ElementId(id_string="VAR_UNDER_TEST_ID")

    with unittest.mock.patch.object(
        mock_client,
        "ReferenceArrayGetLength",
        return_value=var_msgs.IntegerValue(value=5),
    ):
        with unittest.mock.patch.object(
            mock_client,
            "ReferenceArraySetLength",
            return_value=wkfl_msgs.SetReferenceArrayLengthResponse(),
        ) as mock_grpc_method:
            monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
            sut = grpcmc.ReferenceArrayDatapin(element_id=sut_element_id, engine=engine)

            # Act
            sut.set_length(0)

            # Assert
            expected_request = wkfl_msgs.SetReferenceArrayLengthRequest(
                target=sut_element_id, new_size=0
            )
            mock_grpc_method.assert_called_once_with(expected_request)


def test_array_extend(monkeypatch, engine) -> None:
    # Arrange: ReferenceDatapin that has an equation
    mock_client = MockWorkflowClientForRefVarTest()
    monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)

    with unittest.mock.patch.object(
        mock_client, "ReferenceArrayGetLength", return_value=var_msgs.IntegerValue(value=5)
    ):
        with unittest.mock.patch.object(
            mock_client,
            "ReferenceArraySetLength",
            return_value=wkfl_msgs.SetReferenceArrayLengthResponse(),
        ) as mock_grpc_method:
            sut_element_id = elem_msgs.ElementId(id_string="VAR_UNDER_TEST_ID")
            sut = grpcmc.ReferenceArrayDatapin(element_id=sut_element_id, engine=engine)

            # Act
            sut.set_length(7)

            # Assert
            expected_length_request = wkfl_msgs.SetReferenceArrayLengthRequest(
                target=sut_element_id, new_size=7
            )
            mock_grpc_method.assert_called_once_with(expected_length_request)
