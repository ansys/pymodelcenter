from abc import ABC
from typing import Generic, TypeVar

from .ivariable import IVariable

WRAPPED_TYPE = TypeVar('WRAPPED_TYPE')


class IArray(IVariable[WRAPPED_TYPE], ABC, Generic[WRAPPED_TYPE]):
    """
    Base class for all array types.  Has common functionality for getting/setting array
    sizes and getting/setting values as strings.

    Arrays start at 0 length by default.  So you must set the size before you can
    assign individual array elements.

    Implements IVariable
    """

    @property
    def auto_size(self) -> bool:
        """
        Whether or not the array is set to automatically size itself.  If false and the
        array is linked from upstream, the upstream array must be exactly the same size
        or an error ensues.  If true, the array will resize itself when the link is validated.
        """
        raise NotImplementedError
