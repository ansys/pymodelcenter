"""Implementation of Arrayish wrapper class."""
from typing import Callable, Sequence, Type, TypeVar, Union, overload

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

    def __init__(self, instance, converter: Union[Type[VT], Callable[[object], VT]]) -> None:
        """
        Initialize an ModelCenter arrayish type.

        Parameters
        ----------
        instance :
            The ModelCenter interface object to wrap.
        converter : Type or Callable
            A means to convert from the type return by the instance
            API call.  This could be a type which has an appropriate
            constructor or a callable with the appropriate return type.
        """
        self._instance = instance
        self._converter = converter

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
                return self._converter(self._instance.Item(index))
            else:
                raise IndexError
        elif isinstance(index, str):
            return self._converter(self._instance.Item(index))
        elif isinstance(index, slice):
            # TODO: Return an efficient list instead of pulling all the items in the range
            ret = []
            len_ = len(self)
            for i in range(index.stop)[index]:
                if i < len_:
                    val = self._converter(self._instance.Item(i))
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
