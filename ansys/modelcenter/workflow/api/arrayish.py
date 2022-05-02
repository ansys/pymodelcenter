from typing import Sequence, Type, TypeVar, Union

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

    def __getitem__(self, id_: Union[int, str]) -> VT:
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
