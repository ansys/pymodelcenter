from typing import Sequence, Type, TypeVar, Union, overload

VT = TypeVar('VT')
"""A generic value type."""


class Arrayish(Sequence[VT]):
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
    def __getitem__(self, id_: slice) -> Sequence[VT]:
        """
        Get the object specified.

        Parameters
        ----------
        id_ : slice
            slice of the objects to fetch.

        Returns
        -------
        Sequence of Objects specified.
        """
        raise NotImplementedError

    def __getitem__(self, id_: int) -> VT:
        """
        Get the object specified.

        Parameters
        ----------
        id_ : int
            index of the object to fetch.

        Returns
        -------
        Object specified.
        """
        # This check is actually important when attempting to use this type in python idioms
        # (list comprehensions, for-each, etc)
        # Python just keeps calling __getitem__ until it gets an IndexError specifically.
        if isinstance(id_, int) and id_ >= len(self):
            raise IndexError
        return self._value_type(self._instance.Item(id_))

    def get_item(self, id_: Union[int, str]) -> VT:
        """
        Get the object specified.

        Parameters
        ----------
        id_ : int or str
            index or name of the object to fetch.

        Returns
        -------
        Object specified.
        """
        # This check is actually important when attempting to use this type in python idioms
        # (list comprehensions, for-each, etc)
        # Python just keeps calling __getitem__ until it gets an IndexError specifically.
        if isinstance(id_, int) and id_ >= len(self):
            raise IndexError
        return self._value_type(self._instance.Item(id_))

    def __len__(self) -> int:
        """
        Get the number of contained object, the length of the \
        sequence of objects.

        Returns
        -------
        Length of the sequence.
        """
        return self._instance.Count
