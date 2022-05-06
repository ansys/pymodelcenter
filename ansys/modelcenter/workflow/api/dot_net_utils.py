"""Collection of utility functions to aid in converting \
between Dot-Net and Python types."""

from typing import Iterable, List, Sequence, Type, TypeVar, TYPE_CHECKING

import clr
from System import Boolean as DotNetBoolean
from System import Double as DotNetDouble
from System import Int64 as DotNetInt64
from System import String as DotNetString
from System.Collections.Generic import List as DotNetList

if TYPE_CHECKING:
    from .ivariable import IVariable

from .ibooleanarray import IBooleanArray
from .ibooleanvariable import IBooleanVariable
from .idoublearray import IDoubleArray
from .idoublevariable import IDoubleVariable
from .ifilearray import IFileArray
from .ifilevariable import IFileVariable
from .iintegerarray import IIntegerArray
from .iintegervariable import IIntegerVariable
from .ireference_array import IReferenceArray
from .ireference_variable import IReferenceVariable
from .istringarray import IStringArray
from .istringvariable import IStringVariable

clr.AddReference("phoenix-mocks/Interop.ModelCenter")
from ModelCenter import IVariable as mcapiIVariable
from ModelCenter import IVariables as mcapiVariableSequence

N = TypeVar('N', DotNetBoolean, DotNetDouble, DotNetInt64, DotNetString)
"""
The four Dot-Net primitive types that are supported.
"""

P = TypeVar('P', int, float, str, bool)
"""
The four Python primitive types that are supported.
"""


def to_dot_net_list(source: Iterable[P], inner_dot_net_type: Type[N]) -> List[N]:
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


def from_dot_net_list(source: DotNetList, inner_python_type: Type[P]) -> List[P]:
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


def from_dot_net_to_ivariable(source: mcapiIVariable) -> 'IVariable':
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
    class_ = STR_TYPE_TO_CLASS[str_type]
    return class_(source)


def create_dot_net_variable_sequence(source: mcapiVariableSequence) -> 'Sequence[IVariable]':
    return [from_dot_net_to_ivariable(source.Item(var_index))
            for var_index in range(0, source.Count)]
