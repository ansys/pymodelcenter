"""Defines a decorator and standard exception types for interpreting errors from the gRPC client."""

import functools
from typing import Mapping, Type

import ansys.engineeringworkflow.api as aew_api
import grpc


class UnexpectedEngineError(Exception):
    """
    Raised when the gRPC client raises an error that's unexpected for the call that was made.

    Note that this does not necessarily mean that the gRPC client raised an error with code
    UNKNOWN or INTERNAL, just that the code raised isn't well-defined for the call that was
    made. For example, some gRPC methods take only a target element as an argument;
    we would expect the client to raise NOT_FOUND if that element is invalid, so a
    FAILED_PRECONDITION or INVALID_ARGUMENT would be unexpected and could indicate an issue
    within the Python API or the gRPC servicing code.
    """

    def __init__(self, message: str, code: grpc.StatusCode):
        """Initialize a new instance."""
        super(UnexpectedEngineError, self).__init__(
            f"The ModelCenter engine reported an unexpected error:\n"
            f"Message:{message}\n"
            f"Code:{code}\n"
        )


class EngineDisconnectedError(Exception):
    """Raised when the gRPC client indicates that the ModelCenter service is not available."""

    def __init__(self, message: str):
        """Initialize a new instance."""
        super(EngineDisconnectedError, self).__init__(
            f"The connection to the ModelCenter engine is not available. Did you make a call to "
            f"shut it down?\nDetail: {message}"
        )


class InvalidInstanceError(Exception):
    """Raised when a gRPC error indicates that the target element ID is not valid anymore."""

    def __init__(self, message: str):
        """Initialize a new instance."""
        super(InvalidInstanceError, self).__init__(
            f"The ModelCenter engine was not able to locate the target element. "
            f"The element may have been deleted or its workflow unloaded.\nDetail: {message}"
        )


class ValueOutOfRangeError(ValueError):
    """Raised when a gRPC error indicates that an argument value is out of range."""

    ...


__DEFAULT_STATUS_EXCEPTION_TYPE_MAP: Mapping[grpc.StatusCode, Type[Exception]] = {
    grpc.StatusCode.UNAVAILABLE: EngineDisconnectedError,
    grpc.StatusCode.INTERNAL: aew_api.EngineInternalError,
}
"""
The default map of entirely unambiguous status codes to the exception types they should raise.

Do not attempt to modify this map at runtime.
"""


def interpret_rpc_error(additional_codes: Mapping[grpc.StatusCode, Type[Exception]] = {}):
    """
    Decorate a function so that grpc.RpcErrors it raises are wrapped in a more meaningful way.

    By default, the status codes UNAVAILABLE and INTERNAL are mapped to EngineDisconnectedError
    and EngineInternalError. Callers can specify additional mappings in the additional_codes
    parameter. The key should be the status code, and the value should be the exception type.
    The type should take a single parameter in its constructor that is the message from the
    gRPC error.

    Take care when specifying additional codes to ensure that the wrapped gRPC call is supposed
    to raise the code in question for a particular reason. This module also supplies some
    predefined maps that represent commonplace mappings between gRPC error codes and exception
    types. These are not universally applicable, but can be passed to the decorator when
    appropriate for the gRPC call in question. Remember that you can create a merged dictionary
    on the fly with the following syntax: {**DICT_ONE, **DICT_TWO, additional_key: additional_value}

    If a code is not specified (or one of the default codes) it will be wrapped as
    UnexpectedEngineError.

    Parameters
    ----------
        additional_codes: Mapping[grpc.StatusCode, Type[Exception]]
            a map of additional codes to wrap
    """

    def interpret_rpc_error_parameterized(orig_func):
        @functools.wraps(orig_func)
        def wrapped_rpc_use_method(*args, **kwargs):
            code_to_exception_type = {**__DEFAULT_STATUS_EXCEPTION_TYPE_MAP, **additional_codes}
            try:
                return orig_func(*args, **kwargs)
            except grpc.RpcError as thrown_rpc_error:
                thrown_status: grpc.StatusCode = thrown_rpc_error.code()
                if thrown_status in code_to_exception_type:
                    # If we know how to wrap it, do so:
                    raise code_to_exception_type[thrown_status](
                        thrown_rpc_error.details()
                    ) from thrown_rpc_error
                else:
                    raise UnexpectedEngineError(
                        thrown_rpc_error.details(), thrown_status
                    ) from thrown_rpc_error

        return wrapped_rpc_use_method

    return interpret_rpc_error_parameterized


WRAP_NAME_COLLISION: Mapping[grpc.StatusCode, Type[Exception]] = {
    grpc.StatusCode.ALREADY_EXISTS: aew_api.NameCollisionError
}
"""
Pass this to wrap_rpcerror to wrap ALREADY_EXISTS as a NameCollisionError.

Do not attempt to modify this map.
"""


WRAP_TARGET_NOT_FOUND: Mapping[grpc.StatusCode, Type[Exception]] = {
    grpc.StatusCode.NOT_FOUND: InvalidInstanceError
}
"""
Pass this to wrap_rpcerror when NOT_FOUND indicates that the calling instance is invalid.

Do not attempt to modify this map.
"""


WRAP_INVALID_ARG: Mapping[grpc.StatusCode, Type[Exception]] = {
    grpc.StatusCode.INVALID_ARGUMENT: ValueError
}
"""
Pass this to wrap_rpcerror when responsibility for invalid arguments is the caller's.

Note that this is not always the case. For example, sometimes the arguments passed to the
gRPC method are entirely calculated by the API, and there is no way for the user to cause
it to produce invalid arguments; in this case you should wrap this code as an internal error.

Do not attempt to modify this map.
"""

WRAP_OUT_OF_BOUNDS: Mapping[grpc.StatusCode, Type[Exception]] = {
    grpc.StatusCode.OUT_OF_RANGE: ValueOutOfRangeError
}
"""
Pass this to wrap_rpcerror when the responsibility for out-of-range arguments is the caller's.

Note that this is not always the case. For example, sometimes the arguments passed to the
gRPC method are entirely calculated by the API, and there is no way for the user to cause
it to produce invalid arguments; in this case you should wrap this code as an internal error.

Do not attempt to modify this map.
"""
