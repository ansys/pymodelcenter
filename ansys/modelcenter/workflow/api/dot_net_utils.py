"""Collection of utility classes and functions to aid in converting \
between Dot-Net and Python types."""

import clr

from typing import Generic, Iterable, List, Type, TypeVar

from System import Boolean as DotNetBoolean
from System import Double as DotNetDouble
from System import Int64 as DotNetInt64
from System import String as DotNetString
from System.Collections.Generic import List as DotNetList

from .idoublevariable import IDoubleVariable
from .idoublearray import IDoubleArray
from .iintegervariable import IIntegerVariable
from .iintegerarray import IIntegerArray
from .istringvariable import IStringVariable
from .istringarray import IStringArray
from .ibooleanvariable import IBooleanVariable
from .ibooleanarray import IBooleanArray
from .ifilevariable import IFileVariable
from .ifilearray import IFileArray
from .ireference_variable import IReferenceVariable
from .ireference_array import IReferenceArray
from .ivariable import IVariable

clr.AddReference("phoenix-mocks/Interop.ModelCenter")
from ModelCenter import IVariable as mcapiIVariable


N = TypeVar('N', DotNetBoolean, DotNetDouble, DotNetInt64, DotNetString)
"""
The four Dot-Net primitive types that are supported.
"""

P = TypeVar('P', int, float, str, bool)
"""
The four Python primitive types that are supported.
"""


class DotNetListConverter(Generic[P, N]):
    """Static Utility class of methods to convert between Python list \
    of basic values and Dot Net list of values."""

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


class IVariableConverter:
    """Static utility class usable to construct IVariable objects \
    of the correct type based off the announced from a MCAPI \
    IVariable objects."""

    STR_TYPE_TO_CLASS = {
        "double": IDoubleVariable,
        "integer": IIntegerVariable,
        "string": IStringVariable,
        "boolean": IBooleanVariable,
        "file": IFileVariable,
        "reference": IReferenceVariable,

        "double[]": IDoubleArray,
        "integer[]": IIntegerArray,
        "string[]": IStringArray,
        "boolean[]": IBooleanArray,
        "file[]": IFileArray,
        "reference[]": IReferenceArray,
    }
    """
    A mapping from the string value returned by IVariable.get_type() (or \
    the ModelCenter API IVariable.getType()) to the corresponding \
    IVariable descendant type.
    """

    @staticmethod
    def from_dot_net(source: mcapiIVariable) -> IVariable:
        """
        Construct the appropriate IVariable type wrapping the given \
        MCAP IVariable value.

        Parameters
        ----------
        source : mcapiIVariable
            The MCAPI IVariable value to wrap in the appropriate IVariable
            value.

        Returns
        -------
        An IVariable value of the appropriate type.,
        """
        str_type = source.getType()
        class_ = IVariableConverter.STR_TYPE_TO_CLASS[str_type]
        return class_(source)
