import clr

clr.AddReference('phoenix-mocks/Phoenix.Mock.v45')
from Phoenix.Mock import MockRefArrayProp


class IRefArrayProp:
    """
    Array variable that references other variables without creating a \
    full link relationship.
    """

    def __init__(self, name: str, type_: str, instance: MockRefArrayProp = None):
        """
        Initialize.

        Parameters
        ----------
        name : str
            The name of the variable.
        type_ : str
            The type of the variable.
        """
        if instance:
            self._instance = instance
        else:
            self._instance = MockRefArrayProp(name, type_)

    @property
    def enum_values(self) -> str:
        """Enumerated values of the reference array property."""
        return self._instance.enumValues

    @enum_values.setter
    def enum_values(self, value: str) -> None:
        """Enumerated values of the reference array property."""
        self._instance.enumValues = value

    @property
    def is_input(self) -> bool:
        """Gets a flag that is true if this property is an input."""
        # boolean isInput;
        return self._instance.isInput

    @is_input.setter
    def is_input(self, value):
        """Gets a flag that is true if this property is an input."""
        self._instance.isInput = value

    @property
    def title(self) -> str:
        """Title of the reference array property."""
        return self._instance.title

    @title.setter
    def title(self, value: str) -> None:
        """Title of the reference array property."""
        self._instance.title = value

    @property
    def description(self) -> str:
        """Description of the reference array property."""
        return self._instance.description

    @description.setter
    def description(self, value):
        """Description of the reference array property."""
        self._instance.description = value

    def get_name(self) -> str:
        """
        Name of the reference array property.

        Returns
        -------
        str
            The name of the reference array property.
        """
        return self._instance.getName()

    def get_type(self) -> str:
        """
        Type of the reference array property.

        Returns
        -------
        str
            The type of the reference array property.
        """
        return self._instance.getType()


class IRefProp(IRefArrayProp):
    """
    Variable that references other variables without creating a full \
    link relationship.

    Implements IRefArrayProp.
    """
    pass
