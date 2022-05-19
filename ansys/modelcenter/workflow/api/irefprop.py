import clr

clr.AddReference('phoenix-mocks/Phoenix.Mock.v45')
from Phoenix.Mock import MockRefArrayProp


class IRefArrayProp:
    """
    Array variable that references other variables without creating a \
    full link relationship.
    """

    def __init__(self, instance: MockRefArrayProp):
        """
        Initialize.

        Parameters
        ----------
        name : str
            The name of the variable.
        type_ : str
            The type of the variable.
        """
        self._wrapped = instance

    @property
    def enum_values(self) -> str:
        """Enumerated values of the reference array property."""
        return self._wrapped.enumValues

    @enum_values.setter
    def enum_values(self, value: str) -> None:
        """Enumerated values of the reference array property."""
        self._wrapped.enumValues = value

    @property
    def is_input(self) -> bool:
        """Gets a flag that is true if this property is an input."""
        # boolean isInput;
        return self._wrapped.isInput

    @is_input.setter
    def is_input(self, value):
        """Gets a flag that is true if this property is an input."""
        self._wrapped.isInput = value

    @property
    def title(self) -> str:
        """Title of the reference array property."""
        return self._wrapped.title

    @title.setter
    def title(self, value: str) -> None:
        """Title of the reference array property."""
        self._wrapped.title = value

    @property
    def description(self) -> str:
        """Description of the reference array property."""
        return self._wrapped.description

    @description.setter
    def description(self, value):
        """Description of the reference array property."""
        self._wrapped.description = value

    def get_name(self) -> str:
        """
        Name of the reference array property.

        Returns
        -------
        str
            The name of the reference array property.
        """
        return self._wrapped.getName()

    def get_type(self) -> str:
        """
        Type of the reference array property.

        Returns
        -------
        str
            The type of the reference array property.
        """
        return self._wrapped.getType()


class IRefProp(IRefArrayProp):
    """
    Variable that references other variables without creating a full \
    link relationship.

    Implements IRefArrayProp.
    """
    pass
