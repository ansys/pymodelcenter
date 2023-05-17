import sys

import ansys.tools.variableinterop as atvi
import pytest

import ansys.modelcenter.workflow.grpc_modelcenter.proto.variable_value_messages_pb2 as grpc_msg
import ansys.modelcenter.workflow.grpc_modelcenter.var_value_convert as test_module


@pytest.mark.parametrize("internal_value", [0, -1, 1, -47, 47, 2147483647, -2147483648])
def test_int_value_atvi_to_grpc(internal_value: int):
    # Setup
    original = atvi.IntegerValue(internal_value)

    # Execute
    converted = test_module.convert_interop_value_to_grpc(original)

    # Verify
    assert converted.HasField("int_value")
    assert converted.int_value == internal_value


@pytest.mark.parametrize("internal_value", [0, -1, 1, -47, 47, 2147483647, -2147483648])
def test_int_value_grpc_to_atvi(internal_value: int):
    # Setup
    original = grpc_msg.VariableValue(int_value=internal_value)

    # Execute
    converted = test_module.convert_grpc_value_to_atvi(original)

    # Verify
    assert isinstance(converted, atvi.IntegerValue)
    assert internal_value == converted


@pytest.mark.parametrize(
    "internal_value",
    [
        0.0,
        -1.0,
        1.0,
        867.5309,
        1.0 + sys.float_info.epsilon,
        sys.float_info.max,
        sys.float_info.min,
    ],
)
def test_double_value_atvi_to_grpc(internal_value: float):
    # Setup
    original = atvi.RealValue(internal_value)

    # Execute
    converted = test_module.convert_interop_value_to_grpc(original)

    # Verify
    assert converted.HasField("double_value")
    assert converted.double_value == internal_value


@pytest.mark.parametrize(
    "internal_value",
    [
        0.0,
        -1.0,
        1.0,
        867.5309,
        1.0 + sys.float_info.epsilon,
        sys.float_info.max,
        sys.float_info.min,
    ],
)
def test_double_value_grpc_to_atvi(internal_value: float):
    # Setup
    original = grpc_msg.VariableValue(double_value=internal_value)

    # Execute
    converted = test_module.convert_grpc_value_to_atvi(original)

    # Verify
    assert isinstance(converted, atvi.RealValue)
    assert internal_value == converted


@pytest.mark.parametrize(
    "internal_value", ["test", "has a space", "has a line\r\nbreak", "\t\r\n  ", " (╯°□°）╯︵ ┻━┻"]
)
def test_string_value_atvi_to_grpc(internal_value: str):
    # Setup
    original = atvi.StringValue(internal_value)

    # Execute
    converted = test_module.convert_interop_value_to_grpc(original)

    # Verify
    assert converted.HasField("string_value")
    assert converted.string_value == internal_value


@pytest.mark.parametrize(
    "internal_value", ["test", "has a space", "has a line\r\nbreak", "\t\r\n  ", " (╯°□°）╯︵ ┻━┻"]
)
def test_string_value_grpc_to_atvi(internal_value: str):
    # Setup
    original = grpc_msg.VariableValue(string_value=internal_value)

    # Execute
    converted = test_module.convert_grpc_value_to_atvi(original)

    # Verify
    assert isinstance(converted, atvi.StringValue)
    assert internal_value == converted


@pytest.mark.parametrize("internal_value", [True, False])
def test_boolean_value_atvi_to_grpc(internal_value: bool):
    # Setup
    original = atvi.BooleanValue(internal_value)

    # Execute
    converted = test_module.convert_interop_value_to_grpc(original)

    # Verify
    assert converted.HasField("bool_value")
    assert converted.bool_value == internal_value


@pytest.mark.parametrize("internal_value", [True, False])
def test_boolean_value_grpc_to_atvi(internal_value: bool):
    # Setup
    original = grpc_msg.VariableValue(bool_value=internal_value)

    # Execute
    converted = test_module.convert_grpc_value_to_atvi(original)

    # Verify
    assert isinstance(converted, atvi.BooleanValue)
    assert internal_value == converted


def test_integer_array_value_grpc_to_atvi_empty():
    # Setup
    original = grpc_msg.VariableValue(
        int_array_value=grpc_msg.IntegerArrayValue(
            values=[], dims=grpc_msg.ArrayDimensions(dims=[0])
        )
    )

    # Execute
    converted = test_module.convert_grpc_value_to_atvi(original)

    # Verify
    assert isinstance(converted, atvi.IntegerArrayValue)
    assert converted == []


def test_integer_array_value_grpc_to_atvi_one_dimensional():
    # Setup
    original = grpc_msg.VariableValue(
        int_array_value=grpc_msg.IntegerArrayValue(
            values=[47, -8675309, 9001], dims=grpc_msg.ArrayDimensions(dims=[3])
        )
    )

    # Execute
    converted = test_module.convert_grpc_value_to_atvi(original)

    # Verify
    assert isinstance(converted, atvi.IntegerArrayValue)
    assert converted == [47, -8675309, 9001]


def test_integer_array_value_grpc_to_atvi_multi_dimensional():
    # Setup
    original = grpc_msg.VariableValue(
        int_array_value=grpc_msg.IntegerArrayValue(
            values=[1, 2, 3, 10, 20, 30, 100, 200, 300], dims=grpc_msg.ArrayDimensions(dims=[3, 3])
        )
    )

    # Execute
    converted = test_module.convert_grpc_value_to_atvi(original)

    # Verify
    assert isinstance(converted, atvi.IntegerArrayValue)
    assert converted == [[1, 2, 3], [10, 20, 30], [100, 200, 300]]


def test_integer_array_value_atvi_to_grpc_empty():
    # Setup
    original = atvi.IntegerArrayValue(0, [])

    # Execute
    converted = test_module.convert_interop_value_to_grpc(original)

    # Verify
    assert converted.HasField("int_array_value")
    assert converted.int_array_value.values == []
    assert converted.int_array_value.dims.dims == [0]


def test_integer_array_value_atvi_to_grpc_one_dimensional():
    # Setup
    original = atvi.IntegerArrayValue(3, [47, -8675309, 9001])

    # Execute
    converted = test_module.convert_interop_value_to_grpc(original)

    # Verify
    assert converted.HasField("int_array_value")
    assert converted.int_array_value.values == [47, -8675309, 9001]
    assert converted.int_array_value.dims.dims == [3]


def test_integer_array_value_atvi_to_grpc_multi_dimensional():
    # Setup
    original = atvi.IntegerArrayValue((3, 3), [[1, 2, 3], [10, 20, 30], [100, 200, 300]])

    # Execute
    converted = test_module.convert_interop_value_to_grpc(original)

    # Verify
    assert converted.HasField("int_array_value")
    assert converted.int_array_value.values == [1, 2, 3, 10, 20, 30, 100, 200, 300]
    assert converted.int_array_value.dims.dims == [3, 3]


def test_double_array_value_grpc_to_atvi_empty():
    # Setup
    original = grpc_msg.VariableValue(
        double_array_value=grpc_msg.DoubleArrayValue(
            values=[], dims=grpc_msg.ArrayDimensions(dims=[0])
        )
    )

    # Execute
    converted = test_module.convert_grpc_value_to_atvi(original)

    # Verify
    assert isinstance(converted, atvi.RealArrayValue)
    assert converted == []


def test_double_array_value_grpc_to_atvi_one_dimensional():
    # Setup
    original = grpc_msg.VariableValue(
        double_array_value=grpc_msg.DoubleArrayValue(
            values=[47.0, -867.5309, 9000.1], dims=grpc_msg.ArrayDimensions(dims=[3])
        )
    )

    # Execute
    converted = test_module.convert_grpc_value_to_atvi(original)

    # Verify
    assert isinstance(converted, atvi.RealArrayValue)
    assert converted == [47.0, -867.5309, 9000.1]


def test_double_array_value_grpc_to_atvi_multi_dimensional():
    # Setup
    original = grpc_msg.VariableValue(
        double_array_value=grpc_msg.DoubleArrayValue(
            values=[1.1, 2.1, 3.1, 1.2, 2.2, 3.2, 1.3, 2.3, 3.3],
            dims=grpc_msg.ArrayDimensions(dims=[3, 3]),
        )
    )

    # Execute
    converted = test_module.convert_grpc_value_to_atvi(original)

    # Verify
    assert isinstance(converted, atvi.RealArrayValue)
    assert converted == [[1.1, 2.1, 3.1], [1.2, 2.2, 3.2], [1.3, 2.3, 3.3]]


def test_double_array_value_atvi_to_grpc_empty():
    # Setup
    original = atvi.RealArrayValue(0, [])

    # Execute
    converted = test_module.convert_interop_value_to_grpc(original)

    # Verify
    assert converted.HasField("double_array_value")
    assert converted.double_array_value.values == []
    assert converted.double_array_value.dims.dims == [0]


def test_double_array_value_atvi_to_grpc_one_dimensional():
    # Setup
    original = atvi.RealArrayValue(3, [47.0, -867.5309, 9000.1])

    # Execute
    converted = test_module.convert_interop_value_to_grpc(original)

    # Verify
    assert converted.HasField("double_array_value")
    assert converted.double_array_value.values == [47.0, -867.5309, 9000.1]
    assert converted.double_array_value.dims.dims == [3]


def test_double_array_value_atvi_to_grpc_multi_dimensional():
    # Setup
    original = atvi.RealArrayValue((3, 3), [[1.1, 2.1, 3.1], [1.2, 2.2, 3.2], [1.3, 2.3, 3.3]])

    # Execute
    converted = test_module.convert_interop_value_to_grpc(original)

    # Verify
    assert converted.HasField("double_array_value")
    assert converted.double_array_value.values == [1.1, 2.1, 3.1, 1.2, 2.2, 3.2, 1.3, 2.3, 3.3]
    assert converted.double_array_value.dims.dims == [3, 3]


def test_string_array_value_grpc_to_atvi_empty():
    # Setup
    original = grpc_msg.VariableValue(
        string_array_value=grpc_msg.StringArrayValue(
            values=[], dims=grpc_msg.ArrayDimensions(dims=[0])
        )
    )

    # Execute
    converted = test_module.convert_grpc_value_to_atvi(original)

    # Verify
    assert isinstance(converted, atvi.StringArrayValue)
    assert converted.size == 0


def test_string_array_value_grpc_to_atvi_one_dimensional():
    # Setup
    original = grpc_msg.VariableValue(
        string_array_value=grpc_msg.StringArrayValue(
            values=["test", "check", "trial"], dims=grpc_msg.ArrayDimensions(dims=[3])
        )
    )

    # Execute
    converted = test_module.convert_grpc_value_to_atvi(original)

    # Verify
    assert isinstance(converted, atvi.StringArrayValue)
    assert converted == ["test", "check", "trial"]


def test_string_array_value_grpc_to_atvi_multi_dimensional():
    # Setup
    original = grpc_msg.VariableValue(
        string_array_value=grpc_msg.StringArrayValue(
            values=[
                "one",
                "two",
                "three",
                "first",
                "second",
                "third",
                "primary",
                "secondary",
                "tertiary",
            ],
            dims=grpc_msg.ArrayDimensions(dims=[3, 3]),
        )
    )

    # Execute
    converted = test_module.convert_grpc_value_to_atvi(original)

    # Verify
    assert isinstance(converted, atvi.StringArrayValue)
    assert converted == [
        ["one", "two", "three"],
        ["first", "second", "third"],
        ["primary", "secondary", "tertiary"],
    ]


def test_string_array_value_atvi_to_grpc_empty():
    # Setup
    original = atvi.StringArrayValue(0, [])

    # Execute
    converted = test_module.convert_interop_value_to_grpc(original)

    # Verify
    assert converted.HasField("string_array_value")
    assert converted.string_array_value.values == []
    assert converted.string_array_value.dims.dims == [0]


def test_string_array_value_atvi_to_grpc_one_dimensional():
    # Setup
    original = atvi.StringArrayValue(3, ["test", "check", "inspect"])

    # Execute
    converted = test_module.convert_interop_value_to_grpc(original)

    # Verify
    assert converted.HasField("string_array_value")
    assert converted.string_array_value.values == ["test", "check", "inspect"]
    assert converted.string_array_value.dims.dims == [3]


def test_string_array_value_atvi_to_grpc_multi_dimensional():
    # Setup
    original = atvi.StringArrayValue(
        (3, 3),
        [
            ["one", "two", "three"],
            ["first", "second", "third"],
            ["primary", "secondary", "tertiary"],
        ],
    )

    # Execute
    converted = test_module.convert_interop_value_to_grpc(original)

    # Verify
    assert converted.HasField("string_array_value")
    assert converted.string_array_value.values == [
        "one",
        "two",
        "three",
        "first",
        "second",
        "third",
        "primary",
        "secondary",
        "tertiary",
    ]
    assert converted.string_array_value.dims.dims == [3, 3]


def test_bool_array_value_grpc_to_atvi_empty():
    # Setup
    original = grpc_msg.VariableValue(
        bool_array_value=grpc_msg.BooleanArrayValue(
            values=[], dims=grpc_msg.ArrayDimensions(dims=[0])
        )
    )

    # Execute
    converted = test_module.convert_grpc_value_to_atvi(original)

    # Verify
    assert isinstance(converted, atvi.BooleanArrayValue)
    assert converted == []


def test_bool_array_value_grpc_to_atvi_one_dimensional():
    # Setup
    original = grpc_msg.VariableValue(
        bool_array_value=grpc_msg.BooleanArrayValue(
            values=[True, False, False], dims=grpc_msg.ArrayDimensions(dims=[3])
        )
    )

    # Execute
    converted = test_module.convert_grpc_value_to_atvi(original)

    # Verify
    assert isinstance(converted, atvi.BooleanArrayValue)
    assert converted == [True, False, False]


def test_bool_array_value_grpc_to_atvi_multi_dimensional():
    # Setup
    original = grpc_msg.VariableValue(
        bool_array_value=grpc_msg.BooleanArrayValue(
            values=[True, True, True, False, False, False, True, False, True],
            dims=grpc_msg.ArrayDimensions(dims=[3, 3]),
        )
    )

    # Execute
    converted = test_module.convert_grpc_value_to_atvi(original)

    # Verify
    assert isinstance(converted, atvi.BooleanArrayValue)
    assert converted == [[True, True, True], [False, False, False], [True, False, True]]


def test_bool_array_value_atvi_to_grpc_empty():
    # Setup
    original = atvi.BooleanArrayValue(0, [])

    # Execute
    converted = test_module.convert_interop_value_to_grpc(original)

    # Verify
    assert converted.HasField("bool_array_value")
    assert converted.bool_array_value.values == []
    assert converted.bool_array_value.dims.dims == [0]


def test_bool_array_value_atvi_to_grpc_one_dimensional():
    # Setup
    original = atvi.BooleanArrayValue(3, [True, False, True])

    # Execute
    converted = test_module.convert_interop_value_to_grpc(original)

    # Verify
    assert converted.HasField("bool_array_value")
    assert converted.bool_array_value.values == [True, False, True]
    assert converted.bool_array_value.dims.dims == [3]


def test_bool_array_value_atvi_to_grpc_multi_dimensional():
    # Setup
    original = atvi.BooleanArrayValue(
        (3, 3), [[True, True, True], [False, False, True], [True, False, False]]
    )

    # Execute
    converted = test_module.convert_interop_value_to_grpc(original)

    # Verify
    assert converted.HasField("bool_array_value")
    assert converted.bool_array_value.values == [
        True,
        True,
        True,
        False,
        False,
        True,
        True,
        False,
        False,
    ]
    assert converted.bool_array_value.dims.dims == [3, 3]
