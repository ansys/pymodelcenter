"""Collection of utility classes and functions to aid in converting \
between Dot-Net and Python types."""

from typing import Generic, Iterable, List, Type, TypeVar

from System import Boolean as DotNetBoolean
from System import Double as DotNetDouble
from System import Int64 as DotNetInt64
from System import String as DotNetString
from System.Collections.Generic import List as DotNetList

N = TypeVar('N', DotNetBoolean, DotNetDouble, DotNetInt64, DotNetString)
"""
The four Dot-Net primitive types that are supported.
"""

P = TypeVar('P', int, float, str, bool)
"""
The four Python primitive types that are supported.
"""


class DotNetListConverter(Generic[P, N]):

    @staticmethod
    # def to_dot_net(source: Iterable[P]) -> DotNetList[N]:
    def to_dot_net(source: Iterable[P], inner_dot_net_type: Type[N]) -> List[N]:
        """
        Convert the given Python collection of basic values \
        (Iterable[P]) into a Dot Net list of values (List<N>).

        Parameters
        ----------
        source : Iterable[P]
            Python list to convert to Dot-Net list.
        inner_dot_net_type : Type
            The Inner type to use for the Dot-Net list items.

        Returns
        -------
        An equivalent Dot-Net list.
        """
        result = DotNetList[inner_dot_net_type]()
        for item in source:
            result.Add(item)
        return result

    @staticmethod
    def from_dot_net(source: DotNetList, inner_python_type: Type[P]) -> List[P]:
        """
        Convert the given Dot Net List of basic values (List<N>) \
        into a Python List of basic values (List[P]).

        Parameters
        ----------
        source : Iterable[N]
            Dot-Net list to convert to Python list.
        inner_python_type : Type
            The Inner type to use for the Python list items.

        Returns
        -------
        An equivalent Python list.
        """
        result: List[P] = []
        for item in source:
            result.append(inner_python_type(item))
        return result
