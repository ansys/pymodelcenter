from os import PathLike
from typing import Optional
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

    def ReferenceVariableGetValue(self, request):
        pass

    def ReferenceArraySetReferencedValues(self, request):
        pass

    def ReferenceVariableGetReferencedVariables(self, request):
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
        result: atvi.VariableState = sut.get_value()

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
            sut.get_value("some_hid")

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
        result: atvi.VariableState = sut[test_index].get_value()

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
            sut[0].get_value("some_hid")

        mock_grpc_method.assert_not_called()
