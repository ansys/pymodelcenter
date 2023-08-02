from typing import Optional, Type, Union
import unittest

from ansys.modelcenter.workflow.grpc_modelcenter.abstract_workflow_element import (
    AbstractWorkflowElement,
)
from ansys.modelcenter.workflow.grpc_modelcenter.proto.element_messages_pb2 import ElementId
from ansys.modelcenter.workflow.grpc_modelcenter.proto.variable_value_messages_pb2 import (
    ArrayDimensions,
    DoubleArrayValue,
    DoubleVariableMetadata,
    NumericVariableMetadata,
    SetDoubleArrayValueRequest,
    SetDoubleValueRequest,
    SetDoubleVariableMetadataRequest,
    SetMetadataResponse,
    SetVariableValueResponse,
    VariableState,
    VariableType,
    VariableValue,
)
from ansys.modelcenter.workflow.grpc_modelcenter.real_datapin import RealArrayDatapin, RealDatapin
import ansys.tools.variableinterop as atvi
import pytest

from .grpc_server_test_utils.client_creation_monkeypatch import monkeypatch_client_creation
from .test_datapin import (
    do_get_state_test,
    do_get_state_test_with_hid,
    do_get_type_test,
    do_test_is_input_component,
    do_test_is_input_workflow,
)


class MockWorkflowClientForDoubleVarTest:
    def __init__(self):
        pass

    def DoubleVariableSetMetadata(
        self, request: SetDoubleVariableMetadataRequest
    ) -> SetMetadataResponse:
        return SetMetadataResponse()

    def DoubleVariableGetMetadata(self, request: ElementId) -> DoubleVariableMetadata:
        return DoubleVariableMetadata()

    def DoubleVariableSetValue(self, request: SetDoubleValueRequest) -> SetVariableValueResponse:
        return SetVariableValueResponse()

    def DoubleArraySetValue(self, request: SetDoubleArrayValueRequest) -> SetVariableValueResponse:
        return SetVariableValueResponse()


@pytest.mark.parametrize(
    "description_string,sut_type,expected_metadata_type",
    [
        ("", RealDatapin, atvi.RealMetadata),
        ("This is a mock datapin description.", RealDatapin, atvi.RealMetadata),
        ("", RealArrayDatapin, atvi.RealArrayMetadata),
        ("This is a mock datapin description.", RealArrayDatapin, atvi.RealArrayMetadata),
    ],
)
def test_retrieved_metadata_should_include_description(
    monkeypatch,
    engine,
    description_string: str,
    sut_type: Union[Type[RealDatapin], Type[RealArrayDatapin]],
    expected_metadata_type: Union[Type[atvi.RealMetadata], Type[atvi.RealArrayMetadata]],
):
    # Set up
    mock_client = MockWorkflowClientForDoubleVarTest()
    mock_response = DoubleVariableMetadata()
    sut_element_id = ElementId(id_string="VAR_UNDER_TEST_ID")
    mock_response.base_metadata.description = description_string
    with unittest.mock.patch.object(
        mock_client, "DoubleVariableGetMetadata", return_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = sut_type(sut_element_id, engine=engine)

        result: atvi.RealMetadata = sut.get_metadata()

        mock_grpc_method.assert_called_once_with(sut_element_id)
        assert isinstance(
            result, expected_metadata_type
        ), "The metadata should have the correct type."
        assert (
            result.description == description_string
        ), "The description string should match what was supplied by the gRPC client."


@pytest.mark.parametrize(
    "sut_type,expected_metadata_type",
    [(RealDatapin, atvi.RealMetadata), (RealArrayDatapin, atvi.RealArrayMetadata)],
)
def test_retrieved_metadata_should_include_custom_metadata_empty(
    monkeypatch,
    engine,
    sut_type: Union[Type[RealDatapin], Type[RealArrayDatapin]],
    expected_metadata_type: Union[Type[atvi.RealMetadata], Type[atvi.RealArrayMetadata]],
):
    # Set up
    mock_client = MockWorkflowClientForDoubleVarTest()
    mock_response = DoubleVariableMetadata()
    sut_element_id = ElementId(id_string="VAR_UNDER_TEST_ID")
    with unittest.mock.patch.object(
        mock_client, "DoubleVariableGetMetadata", return_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = sut_type(sut_element_id, engine=engine)

        # Execute
        result: atvi.RealMetadata = sut.get_metadata()

        # Verify
        mock_grpc_method.assert_called_once_with(sut_element_id)
        assert isinstance(
            result, expected_metadata_type
        ), "The metadata should have the correct type."
        assert (
            len(result.custom_metadata) == 0
        ), "There should be no entries in the custom metadata map."


@pytest.mark.parametrize(
    "sut_type,expected_metadata_type",
    [(RealDatapin, atvi.RealMetadata), (RealArrayDatapin, atvi.RealArrayMetadata)],
)
def test_retrieved_metadata_should_include_custom_metadata_populated(
    monkeypatch,
    engine,
    sut_type: Union[Type[RealDatapin], Type[RealArrayDatapin]],
    expected_metadata_type: Union[Type[atvi.RealMetadata], Type[atvi.RealArrayMetadata]],
):
    # Set up
    mock_client = MockWorkflowClientForDoubleVarTest()
    mock_response = DoubleVariableMetadata()
    mock_response.base_metadata.custom_metadata["test_integer_value"].MergeFrom(
        VariableValue(int_value=47)
    )
    mock_response.base_metadata.custom_metadata["test_double_value"].MergeFrom(
        VariableValue(double_value=-867.5309)
    )
    sut_element_id = ElementId(id_string="VAR_UNDER_TEST_ID")
    with unittest.mock.patch.object(
        mock_client, "DoubleVariableGetMetadata", return_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = sut_type(sut_element_id, engine=engine)

        # Execute
        result: atvi.RealArrayMetadata = sut.get_metadata()

        # Verify
        mock_grpc_method.assert_called_once_with(sut_element_id)
        assert isinstance(
            result, expected_metadata_type
        ), "The metadata should have the correct type."
        expected_custom_metadata = {
            "test_integer_value": atvi.IntegerValue(47),
            "test_double_value": atvi.RealValue(-867.5309),
        }
        assert (
            result.custom_metadata == expected_custom_metadata
        ), "The custom metadata should have been transferred correctly."


@pytest.mark.parametrize(
    "sut_type,expected_metadata_type,upper_bound,set_upper_bound,expected_upper_bound,"
    "lower_bound,set_lower_bound,expected_lower_bound",
    [
        (RealDatapin, atvi.RealMetadata, 0.0, False, None, 0.0, False, None),
        (RealDatapin, atvi.RealMetadata, -4.7, True, -4.7, 9000.1, True, 9000.1),
        (RealDatapin, atvi.RealMetadata, 0.0, False, None, 9000.1, True, 9000.1),
        (RealDatapin, atvi.RealMetadata, -4.7, True, -4.7, 0.0, False, None),
        (RealArrayDatapin, atvi.RealArrayMetadata, 0.0, False, None, 0.0, False, None),
        (RealArrayDatapin, atvi.RealArrayMetadata, -4.7, True, -4.7, 9000.1, True, 9000.1),
        (RealArrayDatapin, atvi.RealArrayMetadata, 0.0, False, None, 9000.1, True, 9000.1),
        (RealArrayDatapin, atvi.RealArrayMetadata, -4.7, True, -4.7, 0.0, False, None),
    ],
)
def test_retrieved_metadata_should_convert_bounds(
    monkeypatch,
    engine,
    sut_type: Union[Type[RealDatapin], Type[RealArrayDatapin]],
    expected_metadata_type: Union[Type[atvi.RealMetadata], Type[atvi.RealArrayMetadata]],
    upper_bound: float,
    set_upper_bound: bool,
    expected_upper_bound: Optional[float],
    lower_bound: float,
    set_lower_bound: bool,
    expected_lower_bound: Optional[float],
):
    # Set up
    mock_client = MockWorkflowClientForDoubleVarTest()
    mock_response = DoubleVariableMetadata()
    if set_upper_bound:
        mock_response.upper_bound = upper_bound
    if set_lower_bound:
        mock_response.lower_bound = lower_bound
    sut_element_id = ElementId(id_string="VAR_UNDER_TEST_ID")
    with unittest.mock.patch.object(
        mock_client, "DoubleVariableGetMetadata", return_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = sut_type(sut_element_id, engine=engine)

        # Execute
        result: atvi.RealMetadata = sut.get_metadata()

        # Verify
        mock_grpc_method.assert_called_once_with(sut_element_id)
        assert isinstance(
            result, expected_metadata_type
        ), "The metadata should have the correct type."
        assert (
            result.lower_bound == expected_lower_bound
        ), "The lower bound should be correctly set."
        assert (
            result.upper_bound == expected_upper_bound
        ), "The upper bound should be correctly set."


@pytest.mark.parametrize(
    "sut_type",
    [
        RealDatapin,
        RealArrayDatapin,
    ],
)
def test_set_metadata_invalid_custom_metadata(
    monkeypatch, engine, sut_type: Union[Type[RealDatapin], Type[RealArrayDatapin]]
):
    # Set up
    mock_client = MockWorkflowClientForDoubleVarTest()
    mock_response = SetMetadataResponse()
    sut_element_id = ElementId(id_string="VAR_UNDER_TEST_ID")
    with unittest.mock.patch.object(
        mock_client, "DoubleVariableSetMetadata", return_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = sut_type(sut_element_id, engine=engine)
        new_metadata = atvi.FileMetadata()

        # Execute
        with pytest.raises(TypeError):
            sut.set_metadata(new_metadata)

        # Verify
        mock_grpc_method.assert_not_called()


@pytest.mark.parametrize(
    "description,sut_type,metadata_type",
    [
        ("", RealDatapin, atvi.RealMetadata),
        ("This is a mock datapin description.", RealDatapin, atvi.RealMetadata),
        ("", RealArrayDatapin, atvi.RealArrayMetadata),
        ("This is a mock datapin description.", RealArrayDatapin, atvi.RealArrayMetadata),
    ],
)
def test_set_metadata_empty_custom_metadata(
    monkeypatch,
    engine,
    description: str,
    sut_type: Union[Type[RealDatapin], Type[RealArrayDatapin]],
    metadata_type: Union[Type[atvi.RealMetadata], Type[atvi.RealArrayMetadata]],
):
    # Set up
    mock_client = MockWorkflowClientForDoubleVarTest()
    mock_response = SetMetadataResponse()
    sut_element_id = ElementId(id_string="VAR_UNDER_TEST_ID")
    with unittest.mock.patch.object(
        mock_client, "DoubleVariableSetMetadata", return_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = sut_type(sut_element_id, engine=engine)
        new_metadata = metadata_type()
        new_metadata.description = description

        # Execute
        sut.set_metadata(new_metadata)

        # Verify
        expected_request = SetDoubleVariableMetadataRequest(target=sut_element_id)
        expected_request.new_metadata.base_metadata.description = description
        expected_request.new_metadata.numeric_metadata.MergeFrom(
            NumericVariableMetadata(units="", display_format="")
        )
        mock_grpc_method.assert_called_once_with(expected_request)


@pytest.mark.parametrize(
    "description,sut_type,metadata_type",
    [
        ("", RealDatapin, atvi.RealMetadata),
        ("This is a mock datapin description.", RealDatapin, atvi.RealMetadata),
        ("", RealArrayDatapin, atvi.RealArrayMetadata),
        ("This is a mock datapin description.", RealArrayDatapin, atvi.RealArrayMetadata),
    ],
)
def test_set_metadata_populated_custom_metadata(
    monkeypatch,
    engine,
    description: str,
    sut_type: Union[Type[RealDatapin], Type[RealArrayDatapin]],
    metadata_type: Union[Type[atvi.RealMetadata], Type[atvi.RealArrayMetadata]],
):
    # Set up
    mock_client = MockWorkflowClientForDoubleVarTest()
    mock_response = SetMetadataResponse()
    sut_element_id = ElementId(id_string="VAR_UNDER_TEST_ID")
    with unittest.mock.patch.object(
        mock_client, "DoubleVariableSetMetadata", return_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = sut_type(sut_element_id, engine=engine)
        new_metadata = metadata_type()
        new_metadata.description = description
        new_metadata.custom_metadata["int_value"] = atvi.IntegerValue(47)
        new_metadata.custom_metadata["real_value"] = atvi.RealValue(-867.5309)

        # Execute
        sut.set_metadata(new_metadata)

        # Verify
        expected_request = SetDoubleVariableMetadataRequest(target=sut_element_id)
        expected_request.new_metadata.base_metadata.description = description
        expected_request.new_metadata.base_metadata.custom_metadata["int_value"].MergeFrom(
            VariableValue(int_value=47)
        )
        expected_request.new_metadata.base_metadata.custom_metadata["real_value"].MergeFrom(
            VariableValue(double_value=-867.5309)
        )
        expected_request.new_metadata.numeric_metadata.MergeFrom(
            NumericVariableMetadata(units="", display_format="")
        )
        mock_grpc_method.assert_called_once_with(expected_request)


@pytest.mark.parametrize(
    "sut_type,metadata_type,original_lower_bound,expected_lower_bound,expected_lower_bound_set,"
    "original_upper_bound,expected_upper_bound,expected_upper_bound_set",
    [
        (RealDatapin, atvi.RealMetadata, None, 0.0, False, None, 0.0, False),
        (RealDatapin, atvi.RealMetadata, -4.7, -4.7, True, 9000.1, 9000.1, True),
        (RealDatapin, atvi.RealMetadata, None, 0.0, False, 9000.1, 9000.1, True),
        (RealDatapin, atvi.RealMetadata, -4.7, -4.7, True, None, 0.0, False),
        (RealArrayDatapin, atvi.RealArrayMetadata, None, 0.0, False, None, 0.0, False),
        (RealArrayDatapin, atvi.RealArrayMetadata, -4.7, -4.7, True, 9000.1, 9000.1, True),
        (RealArrayDatapin, atvi.RealArrayMetadata, None, 0.0, False, 9000.1, 9000.1, True),
        (RealArrayDatapin, atvi.RealArrayMetadata, -4.7, -4.7, True, None, 0.0, False),
    ],
)
def test_set_metadata_should_convert_bounds(
    monkeypatch,
    engine,
    sut_type: Union[Type[RealDatapin], Type[RealArrayDatapin]],
    metadata_type: Union[Type[atvi.RealMetadata], Type[atvi.RealArrayMetadata]],
    original_lower_bound: Optional[float],
    expected_lower_bound: float,
    expected_lower_bound_set: bool,
    original_upper_bound: Optional[float],
    expected_upper_bound: float,
    expected_upper_bound_set: bool,
):
    # Set up
    mock_client = MockWorkflowClientForDoubleVarTest()
    mock_response = SetMetadataResponse()
    sut_element_id = ElementId(id_string="VAR_UNDER_TEST_ID")
    with unittest.mock.patch.object(
        mock_client, "DoubleVariableSetMetadata", return_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = sut_type(sut_element_id, engine=engine)
        new_metadata = metadata_type()
        new_metadata.lower_bound = original_lower_bound
        new_metadata.upper_bound = original_upper_bound

        # Execute
        sut.set_metadata(new_metadata)

        # Verify
        expected_request = SetDoubleVariableMetadataRequest(target=sut_element_id)
        expected_request.new_metadata.base_metadata.description = ""
        if expected_upper_bound_set:
            expected_request.new_metadata.upper_bound = expected_upper_bound
        if expected_lower_bound_set:
            expected_request.new_metadata.lower_bound = expected_lower_bound
        expected_request.new_metadata.numeric_metadata.MergeFrom(
            NumericVariableMetadata(units="", display_format="")
        )
        mock_grpc_method.assert_called_once_with(expected_request)


@pytest.mark.parametrize(
    "sut_type,metadata_type",
    [
        (RealDatapin, atvi.RealMetadata),
        (RealArrayDatapin, atvi.RealArrayMetadata),
    ],
)
def test_set_metadata_populated_enums(
    monkeypatch,
    engine,
    sut_type: Union[Type[RealDatapin], Type[RealArrayDatapin]],
    metadata_type: Union[Type[atvi.RealMetadata], Type[atvi.RealArrayMetadata]],
):
    # Set up
    mock_client = MockWorkflowClientForDoubleVarTest()
    mock_response = SetMetadataResponse()
    sut_element_id = ElementId(id_string="VAR_UNDER_TEST_ID")
    with unittest.mock.patch.object(
        mock_client, "DoubleVariableSetMetadata", return_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = sut_type(sut_element_id, engine=engine)
        new_metadata = metadata_type()
        new_metadata.enumerated_values = [atvi.RealValue(1.1), atvi.RealValue(2.2)]
        new_metadata.enumerated_aliases = ["a", "b"]

        # Execute
        sut.set_metadata(new_metadata)

        # Verify
        expected_request = SetDoubleVariableMetadataRequest(target=sut_element_id)
        expected_request.new_metadata.base_metadata.description = ""
        expected_request.new_metadata.enum_values.MergeFrom(
            [atvi.RealValue(1.1), atvi.RealValue(2.2)]
        )
        expected_request.new_metadata.enum_aliases.MergeFrom(["a", "b"])
        expected_request.new_metadata.numeric_metadata.MergeFrom(
            NumericVariableMetadata(units="", display_format="")
        )
        mock_grpc_method.assert_called_once_with(expected_request)


@pytest.mark.parametrize(
    "set_value,expected_value_in_request",
    [
        (atvi.RealValue(4.7), 4.7),
        (atvi.RealValue(-867.5309), -867.5309),
        (atvi.BooleanValue(True), 1.0),
        (atvi.BooleanValue(False), 0.0),
    ],
)
def test_scalar_set_allowed(monkeypatch, engine, set_value, expected_value_in_request):
    # Set up
    mock_client = MockWorkflowClientForDoubleVarTest()
    mock_response = SetVariableValueResponse()
    sut_element_id = ElementId(id_string="VAR_UNDER_TEST_ID")
    with unittest.mock.patch.object(
        mock_client, "DoubleVariableSetValue", retun_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = RealDatapin(sut_element_id, engine=engine)
        new_value = atvi.VariableState(set_value, True)

        # Execute
        sut.set_value(new_value)

        # Verify
        expected_request = SetDoubleValueRequest(
            target=sut_element_id, new_value=expected_value_in_request
        )
        mock_grpc_method.assert_called_once_with(expected_request)


@pytest.mark.parametrize(
    "set_value",
    [
        atvi.IntegerValue(0),
        atvi.StringValue("0.0"),
        atvi.IntegerArrayValue(),
        atvi.RealArrayValue(),
        atvi.BooleanArrayValue(),
        atvi.StringArrayValue(),
    ],
)
def test_scalar_set_disallowed(monkeypatch, engine, set_value):
    # Set up
    mock_client = MockWorkflowClientForDoubleVarTest()
    mock_response = SetVariableValueResponse()
    sut_element_id = ElementId(id_string="VAR_UNDER_TEST_ID")
    with unittest.mock.patch.object(
        mock_client, "DoubleVariableSetValue", return_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = RealDatapin(sut_element_id, engine=engine)
        new_value = atvi.VariableState(set_value, True)

        # Execute / verify:
        with pytest.raises(TypeError):
            sut.set_value(new_value)

        # Verify
        mock_grpc_method.assert_not_called()


@pytest.mark.parametrize(
    "set_value,expected_value_in_request",
    [
        (
            atvi.RealArrayValue(shape_=(0,), values=[]),
            DoubleArrayValue(dims=ArrayDimensions(dims=[0]), values=[]),
        ),
        (
            atvi.RealArrayValue(shape_=(2,), values=[-9.4, 3.87]),
            DoubleArrayValue(dims=ArrayDimensions(dims=[2]), values=[-9.4, 3.87]),
        ),
        (
            atvi.RealArrayValue(
                shape_=(3, 3), values=[[-9.4, 3.87, 5.29], [-49.599, 1.0, 4.22], [99.999, 4.5, 3.1]]
            ),
            DoubleArrayValue(
                dims=ArrayDimensions(dims=[3, 3]),
                values=[-9.4, 3.87, 5.29, -49.599, 1.0, 4.22, 99.999, 4.5, 3.1],
            ),
        ),
        (
            atvi.BooleanArrayValue(shape_=(2, 2), values=[[True, False], [False, True]]),
            DoubleArrayValue(dims=ArrayDimensions(dims=[2, 2]), values=[1.0, 0.0, 0.0, 1.0]),
        ),
    ],
)
def test_array_set_allowed(monkeypatch, engine, set_value, expected_value_in_request):
    # Set up
    mock_client = MockWorkflowClientForDoubleVarTest()
    mock_response = SetVariableValueResponse()
    sut_element_id = ElementId(id_string="VAR_UNDER_TEST_ID")
    with unittest.mock.patch.object(
        mock_client, "DoubleArraySetValue", retun_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = RealArrayDatapin(sut_element_id, engine=engine)
        new_value = atvi.VariableState(set_value, True)

        # Execute
        sut.set_value(new_value)

        # Verify
        expected_request = SetDoubleArrayValueRequest(
            target=sut_element_id, new_value=expected_value_in_request
        )
        mock_grpc_method.assert_called_once_with(expected_request)


@pytest.mark.parametrize(
    "set_value",
    [
        atvi.IntegerValue(0),
        atvi.RealValue(0.0),
        atvi.BooleanValue(True),
        atvi.StringValue("0.0"),
        atvi.IntegerArrayValue(),
        atvi.StringArrayValue(),
    ],
)
def test_array_set_disallowed(monkeypatch, engine, set_value):
    # Set up
    mock_client = MockWorkflowClientForDoubleVarTest()
    mock_response = SetVariableValueResponse()
    sut_element_id = ElementId(id_string="VAR_UNDER_TEST_ID")
    with unittest.mock.patch.object(
        mock_client, "DoubleArraySetValue", return_value=mock_response
    ) as mock_grpc_method:
        monkeypatch_client_creation(monkeypatch, AbstractWorkflowElement, mock_client)
        sut = RealArrayDatapin(sut_element_id, engine=engine)
        new_value = atvi.VariableState(set_value, True)

        # Execute / verify:
        with pytest.raises(TypeError):
            sut.set_value(new_value)

        # Verify
        mock_grpc_method.assert_not_called()


def test_scalar_get_type(monkeypatch, engine):
    do_get_type_test(
        monkeypatch, engine, RealDatapin, VariableType.VARTYPE_REAL, atvi.VariableType.REAL
    )


def test_array_get_type(monkeypatch, engine):
    do_get_type_test(
        monkeypatch,
        engine,
        RealArrayDatapin,
        VariableType.VARTYPE_REAL_ARRAY,
        atvi.VariableType.REAL_ARRAY,
    )


@pytest.mark.parametrize(
    "value_in_response,validity_in_response,expected_atvi_state",
    [
        (-867.5309, True, atvi.VariableState(atvi.RealValue(-867.5309), True)),
        (47.47, False, atvi.VariableState(atvi.RealValue(47.47), False)),
    ],
)
def test_scalar_get_state(
    monkeypatch, engine, value_in_response, validity_in_response, expected_atvi_state
):
    do_get_state_test(
        monkeypatch,
        engine,
        RealDatapin,
        VariableState(
            is_valid=validity_in_response, value=VariableValue(double_value=value_in_response)
        ),
        expected_atvi_state,
    )


def test_scalar_get_state_with_hid(monkeypatch, engine):
    do_get_state_test_with_hid(monkeypatch, engine, RealDatapin)


def test_array_get_state_with_hid(monkeypatch, engine):
    do_get_state_test_with_hid(monkeypatch, engine, RealArrayDatapin)


@pytest.mark.parametrize(
    "value_in_response,validity_in_response,expected_atvi_state",
    [
        (
            DoubleArrayValue(
                dims=ArrayDimensions(dims=[2, 2]), values=[-867.5309, 9000.1, -1.0, 1.0]
            ),
            True,
            atvi.VariableState(
                atvi.RealArrayValue(shape_=(2, 2), values=[[-867.5309, 9000.1], [-1.0, 1.0]]), True
            ),
        ),
        (
            DoubleArrayValue(dims=ArrayDimensions(dims=[2, 2]), values=[1.0, 1.1, 2.0, 2.1]),
            False,
            atvi.VariableState(
                atvi.RealArrayValue(shape_=(2, 2), values=[[1.0, 1.1], [2.0, 2.1]]), False
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
        RealArrayDatapin,
        VariableState(
            is_valid=validity_in_response, value=VariableValue(double_array_value=value_in_response)
        ),
        expected_atvi_state,
    )


@pytest.mark.parametrize(
    "sut_type, flag_in_response",
    [
        (RealDatapin, True),
        (RealDatapin, False),
        (RealArrayDatapin, True),
        (RealArrayDatapin, False),
    ],
)
def test_is_input_component(monkeypatch, engine, sut_type, flag_in_response):
    do_test_is_input_component(monkeypatch, engine, sut_type, flag_in_response)


@pytest.mark.parametrize(
    "sut_type, flag_in_response",
    [
        (RealDatapin, True),
        (RealDatapin, False),
        (RealArrayDatapin, True),
        (RealArrayDatapin, False),
    ],
)
def test_is_input_workflow(monkeypatch, engine, sut_type, flag_in_response):
    do_test_is_input_workflow(monkeypatch, engine, sut_type, flag_in_response)
