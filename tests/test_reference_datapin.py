from typing import Type, Union
import unittest.mock

import ansys.tools.variableinterop as atvi
import pytest

import ansys.modelcenter.workflow.grpc_modelcenter as grpcmc
from ansys.modelcenter.workflow.grpc_modelcenter.abstract_workflow_element import (
    AbstractWorkflowElement,
)
import ansys.modelcenter.workflow.grpc_modelcenter.proto.element_messages_pb2 as elem_msgs
import ansys.modelcenter.workflow.grpc_modelcenter.proto.variable_value_messages_pb2 as var_msgs

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

    def ReferenceArraySetReferencedValues(self, request):
        pass

    def ReferenceVariableGetReferencedVariables(self, request):
        pass

    def ReferenceVariableGetMetadata(
        self, request: elem_msgs.ElementId
    ) -> var_msgs.ReferenceVariableMetadata:
        return var_msgs.ReferenceVariableMetadata()

    def ReferenceVariableSetMetadata(
        self, request: var_msgs.SetReferenceVariableMetadataRequest
    ) -> var_msgs.SetMetadataResponse:
        return var_msgs.SetMetadataResponse()


def test_get_reference_equation(monkeypatch, engine) -> None:
    # Arrange
    mock_client = MockWorkflowClientForRefVarTest()
    mock_response = var_msgs.GetReferenceEquationResponse()
    with unittest.mock.patch.object(
        mock_client, "ReferenceVariableGetReferenceEquation", retun_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut_element_id = elem_msgs.ElementId(id_string="VAR_UNDER_TEST_ID")
        sut = grpcmc.ReferenceDatapin(sut_element_id, engine)

        # Act
        equation: str = sut.equation

        # Assert
        expected_request = var_msgs.GetReferenceEquationRequest(target=sut_element_id)
        mock_grpc_method.assert_called_once_with(expected_request)


def test_set_reference_equation(monkeypatch, engine) -> None:
    # Arrange
    mock_client = MockWorkflowClientForRefVarTest()
    mock_response = var_msgs.SetReferenceEquationResponse()
    with unittest.mock.patch.object(
        mock_client, "ReferenceVariableSetReferenceEquation", retun_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut_element_id = elem_msgs.ElementId(id_string="VAR_UNDER_TEST_ID")
        sut = grpcmc.ReferenceDatapin(sut_element_id, engine)

        # Act
        sut.equation = "ඞ"

        # Assert
        expected_request = var_msgs.SetReferenceEquationRequest(target=sut_element_id, equation="ඞ")
        mock_grpc_method.assert_called_once_with(expected_request)


def test_get_is_direct(monkeypatch, engine) -> None:
    # Arrange
    mock_client = MockWorkflowClientForRefVarTest()
    mock_response = var_msgs.GetReferenceIsDirectResponse()
    with unittest.mock.patch.object(
        mock_client, "ReferenceVariableGetIsDirect", retun_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut_element_id = elem_msgs.ElementId(id_string="VAR_UNDER_TEST_ID")
        sut = grpcmc.ReferenceDatapin(sut_element_id, engine)

        # Act
        is_direct: bool = sut.is_direct

        # Assert
        expected_request = var_msgs.GetReferenceIsDirectRequest(target=sut_element_id)
        mock_grpc_method.assert_called_once_with(expected_request)


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
        mock_client, "ReferenceVariableSetValue", retun_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut_element_id = elem_msgs.ElementId(id_string="VAR_UNDER_TEST_ID")
        sut = grpcmc.ReferenceDatapin(sut_element_id, engine)
        new_value = atvi.VariableState(set_value, True)

        # Act
        sut.set_value(new_value)

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
        new_value = atvi.VariableState(set_value, True)

        # Act
        with pytest.raises(atvi.IncompatibleTypesException):
            sut.set_value(new_value)

        # Assert
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
        mock_client, "ReferenceArraySetReferencedValues", retun_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = grpcmc.ReferenceArrayDatapin(sut_element_id, engine=engine)
        new_value = atvi.VariableState(set_value, True)

        # Act
        sut.set_value(new_value)

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
        new_value = atvi.VariableState(set_value, True)

        # Act
        with pytest.raises(atvi.IncompatibleTypesException):
            sut.set_value(new_value)

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
        assert response == is_direct

        is_direct_expected_request = var_msgs.GetReferenceIsDirectRequest(
            target=sut_element_id, index=test_index
        )
        mock_is_direct_grpc_method.assert_called_once_with(is_direct_expected_request)


def test_array_index_get_reference_equation(monkeypatch, engine) -> None:
    # Arrange
    test_index = 4

    mock_client = MockWorkflowClientForRefVarTest()
    mock_response = var_msgs.GetReferenceEquationResponse()

    with unittest.mock.patch.object(
        mock_client, "ReferenceVariableGetReferenceEquation", retun_value=mock_response
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


def test_array_index_set_reference_equation(monkeypatch, engine) -> None:
    # Arrange
    test_index = 4

    mock_client = MockWorkflowClientForRefVarTest()
    mock_response = var_msgs.SetReferenceEquationResponse()
    with unittest.mock.patch.object(
        mock_client, "ReferenceVariableSetReferenceEquation", retun_value=mock_response
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
