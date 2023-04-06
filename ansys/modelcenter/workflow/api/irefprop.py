"""Contains definitions for array variable that references other variables."""
from abc import ABC, abstractmethod
from typing import Generic, Literal, TypeVar, Union

import ansys.common.variableinterop as acvi

RefPropValueTypes = Literal[
    3,  # acvi.VariableType.BOOLEAN,
    1,  # acvi.VariableType.INTEGER,
    2,  # acvi.VariableType.REAL,
    4,  # acvi.VariableType.STRING,
]

RefPropertyValue = Union[acvi.BooleanValue, acvi.IntegerValue, acvi.RealValue, acvi.StringValue]


# TODO: Need to better understand use cases for reference properties
#       & potentially revisit this interface.
class IReferencePropertyBase(ABC):
    """Common methods for reference properties on scalar and array reference variables."""

    @property
    @abstractmethod
    def enum_values(self) -> str:
        """Get the property's enumerated values."""
        raise NotImplementedError()

    @enum_values.setter
    @abstractmethod
    def enum_values(self, value: str) -> None:
        """Set the property's enumerated values."""
        raise NotImplementedError()

    @property
    @abstractmethod
    def is_input(self) -> bool:
        """Get whether the property is an input."""
        raise NotImplementedError()

    @is_input.setter
    def is_input(self, value):
        """Set whether the property is an input."""
        raise NotImplementedError()

    @property
    @abstractmethod
    def title(self) -> str:
        """Get the title of the property."""
        raise NotImplementedError()

    @title.setter
    @abstractmethod
    def title(self, value: str) -> None:
        """Set the title of the property."""
        raise NotImplementedError()

    @property
    @abstractmethod
    def description(self) -> str:
        """Get the description of the property."""
        raise NotImplementedError()

    @description.setter
    @abstractmethod
    def description(self, value):
        """Set the description of the property."""
        raise NotImplementedError()

    @abstractmethod
    def get_name(self) -> str:
        """
        Get the name of the property.

        Returns
        -------
        The name of the reference array property.
        """
        raise NotImplementedError()

    @abstractmethod
    def get_type(self) -> RefPropValueTypes:
        """
        Get the value type of the property.

        Returns
        -------
        The value type of the reference array property.
        """
        raise NotImplementedError()


class IReferenceProperty(IReferencePropertyBase, ABC):
    """Represents a reference property of a scalar reference variable."""

    @abstractmethod
    def set_value(
        self, value: Union[acvi.BooleanValue, acvi.IntegerValue, acvi.RealValue, acvi.StringValue]
    ):
        """Set the value of the reference property."""
        raise NotImplementedError()

    @abstractmethod
    def get_value(self) -> RefPropValueTypes:
        """Get the value of the reference property."""
        raise NotImplementedError()


class IReferenceArrayProperty(IReferencePropertyBase, ABC):
    """Represents a reference property of a scalar reference variable."""

    @abstractmethod
    def set_value(
        self,
        index: int,
        value: Union[acvi.BooleanValue, acvi.IntegerValue, acvi.RealValue, acvi.StringValue],
    ):
        """Set the value of the reference property at the specified index."""
        raise NotImplementedError()

    @abstractmethod
    def get_value(self, index: int) -> RefPropValueTypes:
        """Get the value of the reference property at the specified index."""
        raise NotImplementedError()


REF_PROPERTY_RETURN = TypeVar(
    "REF_PROPERTY_RETURN", bound=Union[IReferenceProperty, IReferenceArrayProperty]
)


class IReferencePropertyOwner(ABC, Generic[REF_PROPERTY_RETURN]):
    """Defines common methods for variables with reference properties."""

    def create_reference_prop(
        self, name: str, prop_value_type: RefPropValueTypes
    ) -> REF_PROPERTY_RETURN:
        """Create a reference property with the specified name and type."""
        raise NotImplementedError()

    def get_reference_prop(self, name: str) -> REF_PROPERTY_RETURN:
        """Get a reference property with the specified name."""
        raise NotImplementedError()
