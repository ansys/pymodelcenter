from typing import Dict, List, Optional


class MockAccess:
    """
    Utility class usable to trace and control access to mock objects.
    """

    def __init__(self):
        """
        Initialize object.

        Setup calls tracking structure.
        """
        self._calls: Dict[str, List[List[str]]] = {}

    def _log_function_call(self, method_name: str, arguments: List[str]):
        """
        Log that a named method or function was called.

        Parameters
        ----------
        method_name : str
            Name of the method that was called.
        arguments :
            List of argument values given to the method call.
        """
        call_records: Optional[List[List[str]]] = self._calls.get(method_name)
        if call_records is None:
            call_records = []
            self._calls[method_name] = call_records
        call_records.append(arguments)

    def record_call(self, method_name: str, *argv) -> None:
        """
        Record the the named method was called with the given arguments.

        Parameters
        ----------
        method_name : str
            Name of the method called
        argv :
            List or arguments to the method
        """
        args: List[str] = []
        for arg in argv:
            args.append(str(arg))
        self._log_function_call(method_name, args)

    def get_call_count(self, method_name):
        """Get number of times the named method was called."""
        call_records: List[List[str]] = self._calls.get(method_name)
        if call_records is None:
            return 0
        return len(call_records)

    def get_argument_record(self, method_name: str, call_num: int):
        """
        Get the record of arguments that was given to the named method
        for the call number given.

        Parameters
        ----------
        method_name : str
            Name of the method to get the argument record of.
        call_num : int
            The call number to get the argument record of. Zero (0) for
            the first call, 1 for the second, etc.

        Returns
        -------
        A list of strings of the values of the arguments given to the
        method call.

        Raises
        ------
        IndexError : There is no call record for the given number of
            calls, the named method was not called enough times.
        """
        call_records: Optional[List[List[str]]] = self._calls.get(method_name)
        if call_records is None:
            raise IndexError
        return call_records[call_num]
