from typing import Optional

from ansys.modelcenter.workflow.api.metadata_owner import MetadataOwner

clr.AddReference("phoenix-mocks/Interop.ModelCenter")
from ModelCenter import IVariable as mcapiIVariable

class IVariable(MetadataOwner):
    """
    COM instance.
    """

    def __init__(self, instance: mcapiIVariable) -> None:
        """
        Initialize variable object.

        Parameters
        ----------
        instance :
            ModelCenter API IVariable interface object.
        """
        super().__init__(self, instance)

    @property
    def has_changed(self) -> bool:
        """
        Boolean which indicates if the variable has changed since the last time the boolean was
        reset. Typically used only by Plug-Ins for their own variables (to avoid conflicting use
        by different Plug-Ins , macros, or tools). Set the value to false and it will
        automatically flip to true any time the value changes.
        """
        raise NotImplementedError

    @property
    def hide(self) -> bool:
        """
        Hides the variable from the User Interface.
        Variable will not be visible in Component Tree, Data Explorer, or Data Monitors.
        """
        raise NotImplementedError

    @property
    def owning_component(self) -> object:
        """
        Gets the component that owns this variable.

        Returns
        -------
        object
            IDispatch* to an IComponent object.
        """
        raise NotImplementedError

    def is_valid(self) -> bool:
        """
        Returns whether or not the variable is valid.

        Returns
        -------
        bool
            True if variable is valid. False if the variable is not valid.
        """
        raise NotImplementedError

    def validate(self) -> None:
        """
        Validates the variable by running the component if needed.
        """
        raise NotImplementedError

    def get_name(self) -> str:
        """
        Get the name of the variable.

        Returns
        -------
        str
            The name of the variable.
        """
        return self._instance.getName()

    def get_full_name(self) -> str:
        """
        Gets the full %ModelCenter path of the variable.

        Returns
        -------
        str
            The full %ModelCenter path of the variable.
        """
        raise NotImplementedError

    def get_type(self) -> str:
        """
        Gets the type of the variable.

        Returns
        -------
        str
            The type of the variable as a string.
        """
        return self._instance.getType()

    def is_input(self) -> bool:
        """
        Finds out whether or not the variable is an input with respect to the model.  Returnszs
        the same value as \ref isInputToModel.
        """
        raise NotImplementedError

    def to_string(self) -> str:
        """
        Converts the variable value to a string, validating the variable if necessary.

        Returns
        -------
        str
            The value of the variable as a string.
        """
        raise NotImplementedError

    def from_string(self, value: str) -> None:
        """
        Sets the value of the variable from the specified string.

        Parameters
        ----------
        value
            New value.
        """
        raise NotImplementedError

    def to_string_absolute(self) -> str:
        """
        Converts the value of the variable to a string.

        Returns
        -------
        str
            The value of the variable as a string.
        """
        raise NotImplementedError

    def invalidate(self) -> None:
        """
        Marks the variable as invalid (needs to be computed).
        This will set all dependent variables invalid also.
        """
        raise NotImplementedError

    def direct_precedents(self, follow_suspended: Optional[object],
                          reserved: Optional[object]) -> object:
        """
        Returns a list of variables that are immediate precedents to the value of this variable.
        This function returns all variables that influence this variable and are directly
        connected via a link to it.

        Parameters
        ----------
        follow_suspended
            Optional boolean specifies whether links which are
            suspended should be included in the search. Default is false.
        reserved
            Reserved for future use.

        Returns
        -------
        object
            IDispatch* to an IVariables object.
        """
        raise NotImplementedError

    def direct_dependents(self, follow_suspended: Optional[object],
                          reserved: Optional[object]) -> object:
        """
        Returns a list of variables that are immediate dependents of the value of this variable.
        This function returns all variables that are influenced by this variable and are
        directly connected via a link to it.

        Parameters
        ----------
        follow_suspended
            Optional boolean specifies whether links which are
            suspended should be included in the search. Default is false.
        reserved
            Reserved for future use.

        Returns
        -------
        object
            IDispatch* to an IVariables object.
        """
        raise NotImplementedError

    def precedent_links(self, reserved: Optional[object]) -> object:
        """
        Returns a list of links that are immediate precedents to the value of this variable.
        All the returned links will have this variable as the LHS of the equation. Except
        for arrays, the returned list will be 1 element long.

        Parameters
        ----------
        reserved
            Reserved for future use.

        Returns
        -------
        object
            IDispatch* to an IVariableLinks object.
        """
        raise NotImplementedError

    def dependent_links(self, reserved: Optional[object]) -> object:
        """
        Returns a list of links that immediately depend on the value of this variable.
        All the returned links will have this variable as part of a RHS equation.

        Parameters
        ----------
        reserved
            Reserved for future use.

        Returns
        -------
        object
            IDispatch* to an IVariableLinks object.
        """
        raise NotImplementedError

    def precedents(self, follow_suspended: Optional[object], reserved: Optional[object]) -> object:
        """
        Returns a list of variables that are precedents to the value of this variable. This
        function returns all variables that influence this variable, not just directly connected
        ones.

        Parameters
        ----------
        follow_suspended
            Optional boolean specifies whether links which are
            suspended should be included in the search. Default is false.
        reserved
            Reserved for future use.

        Returns
        -------
        object
            IDispatch* to an IVariables object.
        """
        raise NotImplementedError

    def dependents(self, follow_suspended: Optional[object], reserved: Optional[object]) -> object:
        """
        Returns a list of variables that are dependent upon the value of this variable.
        This function returns all variables that are influenced by this variable,
        not just directly connected ones.

        Parameters
        ----------
        follow_suspended
            Optional boolean specifies whether links which are
            suspended should be included in the search. Default is false.
        reserved
            Reserved for future use.

        Returns
        -------
        object
            IDispatch* to an IVariables object.
        """
        raise NotImplementedError

    def is_input_to_component(self) -> bool:
        """
        Checks whether or not the variable is an input.
        Returns true if the variable was originally added as an input, ignoring the
        current state that can change based off of links.
        """
        raise NotImplementedError

    def is_input_to_model(self) -> bool:
        """
        Checks whether or not the variable is an input. A linked input returns false (Output).
        """
        raise NotImplementedError

    def set_metadata(self, name: str, type: object, value: object, access: object,
                     archive: bool) -> None:  # type = MetadataType, access = MetadataAccess
        """
        Sets the meta data value of the given meta data key name.

        Parameters
        ----------
        name
            Metadata specifier used to store the data.
        type
        value
        access
        archive
        """
        raise NotImplementedError

    def get_metadata(self, name: str) -> object:
        """
        Gets the meta data value of the given meta data key name.

        Parameters
        ----------
        name
            Metadata key name.

        Returns
        -------
        object
            Metadata value.
        """
        raise NotImplementedError
