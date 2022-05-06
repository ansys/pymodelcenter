"""Implementation of Arrayish wrapper class."""
from typing import Sequence, Type, TypeVar, Union, overload

VT = TypeVar('VT')
"""A generic value type."""


class Arrayish(Sequence[VT]):
    # TODO: Rename to something like LazyLoadList
    """
    A generic wrapper around an arrayish ModelCenter interface type.

    Parameters:
    -----------
    VT :
        The value type, the type of the values contained within this
        array.
    """

    def __init__(self, instance, value_type: Type[VT]) -> None:
        """
        Initialize an ModelCenter arrayish type.

        Parameters
        ----------
        instance :
            The ModelCenter interface object to wrap.
        value_type : Type
            The type of the contained values.
        """
        self._instance = instance
        self._value_type: Type = value_type

    @overload
    def __getitem__(self, i: int) -> VT: ...

    @overload
    def __getitem__(self, s: slice) -> Sequence[VT]: ...

    @overload
    def __getitem__(self, s: str) -> VT: ...

    def __getitem__(self, index: Union[int, slice, str]) -> Union[Sequence[VT], VT]:
        """
        Get the object or objects specified.

        Parameters
        ----------
        index : int, slice or str
            index or name of the object to fetch, or slice of objects
            to fetch.

        Returns
        -------
        Object specified or sequence of objects specified.
        """
        if isinstance(index, int):
            # This check is actually important when attempting to use this type in python idioms
            # (list comprehensions, for-each, etc)
            # Python just keeps calling __getitem__ until it gets an IndexError specifically.
            if index < len(self):
                return self._value_type(self._instance.Item(index))
            else:
                raise IndexError
        elif isinstance(index, str):
            return self._value_type(self._instance.Item(index))
        elif isinstance(index, slice):
            # TODO: Return an efficient list instead of pulling all the items in the range
            ret = []
            len_ = len(self)
            for i in range(index.stop)[index]:
                if i < len_:
                    val = self._value_type(self._instance.Item(i))
                    ret.append(val)
            return ret
        else:
            raise TypeError

    def __len__(self) -> int:
        """
        Get the number of contained object, the length of the \
        sequence of objects.

        Returns
        -------
        Length of the sequence.
        """
        return self._instance.Count
