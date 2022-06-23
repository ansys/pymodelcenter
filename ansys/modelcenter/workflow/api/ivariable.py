from abc import ABC, abstractmethod
from overrides import overrides
from typing import Collection
from typing import Generic, Optional, Sequence, TypeVar, Union

import ansys.common.variableinterop as acvi

import ansys.modelcenter.workflow.api.arrayish as arrayish
import ansys.modelcenter.workflow.api.dot_net_utils as utils
import ansys.modelcenter.workflow.api.icomponent as icomponent
from ansys.engineeringworkflow.api import IVariable as IAnsysVariable
from ansys.engineeringworkflow.api import Property

from .custom_metadata_owner import CustomMetadataOwner
from .i18n import i18n
from .variable_links import VariableLink, dotnet_links_to_iterable

WRAPPED_TYPE = TypeVar('WRAPPED_TYPE')


class IVariable(CustomMetadataOwner, IAnsysVariable, Generic[WRAPPED_TYPE]):
    """
    Represents a variable in the workflow.
    """
    def __init__(self, wrapped: WRAPPED_TYPE):
        super().__init__(wrapped)
        self._wrapped = wrapped

    # ansys.engineeringworkflow.api.IElement

    @property  # type: ignore
    @overrides
    def name(self):
        return self._wrapped.getName()

    @property  # type: ignore
    @overrides
    def element_id(self) -> str:
        # TODO: Should return UUID of the element probably. Not available via COM.
        raise NotImplementedError

    @property  # type: ignore
    @overrides
    def parent_element_id(self) -> str:
        # TODO: Should return UUID of the element probably. Not available via COM.
        raise NotImplementedError

    @overrides
    def get_property(self, property_name: str) -> Property:
        # TODO: Is property a metadata?
        raise NotImplementedError

    @overrides
    def get_properties(self) -> Collection[Property]:
        # TODO: Is property a metadata or a custom metadata?
        raise NotImplementedError

    @overrides
    def set_property(self, property_name: str, property_value: acvi.IVariableValue) -> None:
        # TODO: Is property a metadata?
        raise NotImplementedError

    # ansys.engineeringworkflow.api.IVariable

    @overrides
    def get_metadata(self) -> acvi.CommonVariableMetadata:
        return self.standard_metadata

    @overrides
    def set_value(self, value: acvi.VariableState) -> None:
        self._wrapped.fromString(value.value.to_api_string())

    @overrides
    def get_value(self, hid: Optional[str]) -> acvi.VariableState:
        if hid is not None:
            raise NotImplemented(i18n('Exceptions', 'ERROR_METADATA_TYPE_NOT_ALLOWED'))
        return acvi.VariableState(self.value, self._wrapped.isValid())

    # ModelCenter

    @property
    @abstractmethod
    def value(self) -> acvi.IVariableValue:
        """
        Get or set the value of the variable.
        If the variable is invalid, the workflow will run to the extent necessary to
        validate the variable.
        """
        raise NotImplementedError

    @value.setter
    @abstractmethod
    def value(self, new_value: Union[float, acvi.IVariableValue]) -> None:
        raise NotImplementedError

    @property
    @abstractmethod
    def value_absolute(self) -> acvi.IVariableValue:
        """
        Get the value of the variable without attempting to validate it.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def standard_metadata(self) -> acvi.CommonVariableMetadata:
        """
        Get the standard metadata for this variable.
        """
        raise NotImplementedError

    @standard_metadata.setter
    @abstractmethod
    def standard_metadata(self, new_metadata: acvi.CommonVariableMetadata) -> None:
        """
        Get the standard metadata for this variable.
        """
        raise NotImplementedError

    @property
    def has_changed(self) -> bool:
        """
        Indicates if the variable has changed since the last time it was reset.

        Typically, used only by Plug-Ins for their own variables (to avoid conflicting use
        by different Plug-Ins, macros, or tools). Set the value to `False`, and it will
        automatically flip to `True` any time the variable value changes.

        Returns
        -------
        bool :
            `True` if the variable has changed since the last time the property was reset.
        """
        return self._wrapped.hasChanged

    @has_changed.setter
    def has_changed(self, value: bool) -> None:
        """
        Reset the value to `False`, and it will automatically flip to `True` any time the variable
        value changes.

        Parameters
        ----------
        value : bool
            Set the value to `False` to reset the property.
        """
        self._wrapped.hasChanged = value

    @property
    def hide(self) -> bool:
        """
        Hide the variable from the User Interface.
        Variable will not be visible in Component Tree, Data Explorer, or Data Monitors.

        Returns
        -------
        bool :
            `True` if the variable is hidden.
        """
        return self._wrapped.hide

    @hide.setter
    def hide(self, value: bool) -> None:
        """
        Hide the variable from the User Interface.
        Variable will not be visible in Component Tree, Data Explorer, or Data Monitors.

        Parameters
        ----------
        value : bool
            Set the value to `True` to hide the variable.
        """
        self._wrapped.hide = value

    @property
    def owning_component(self) -> 'IComponent':
        """
        The component that owns this variable.

        Returns
        -------
        IComponent :
            Owning IComponent object.
        """
        component: object = self._wrapped.OwningComponent
        if component is not None:
            return icomponent.IComponent(component)
        else:
            return None

    def is_valid(self) -> bool:
        """
        Indicates if the variable is valid.

        Returns
        -------
        bool
            ``True`` if variable is valid. ``False`` if the variable is not valid.
        """
        return self._wrapped.isValid()

    def validate(self) -> None:
        """
        Validates the variable by running the component if needed.
        """
        self._wrapped.validate()

    def get_full_name(self) -> str:
        """
        Gets the full %ModelCenter path of the variable.

        Returns
        -------
        str
            The full %ModelCenter path of the variable.
        """
        return self._wrapped.getFullName()

    def get_type(self) -> str:
        """
        Gets the type of the variable.

        Returns
        -------
        str
            The type of the variable as a string.
        """
        return self._wrapped.getType()

    def invalidate(self) -> None:
        """
        Marks the variable as invalid (needs to be computed).
        This will set all dependent variables invalid also.
        """
        self._wrapped.invalidate()

    def direct_precedents(self, follow_suspended: bool = False,
                          reserved: Optional[object] = None) -> Sequence['IVariable']:
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
        return arrayish.Arrayish(self._wrapped.directPrecedents(
            follow_suspended), utils.from_dot_net_to_ivariable)

    def direct_dependents(self, follow_suspended: bool = False,
                          reserved: Optional[object] = None) -> Sequence['IVariable']:
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
        return arrayish.Arrayish(self._wrapped.directDependents(
            follow_suspended), utils.from_dot_net_to_ivariable)

    def precedent_links(self, reserved: Optional[object] = None) -> Sequence[VariableLink]:
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
        return dotnet_links_to_iterable(self._wrapped.precedentLinks(reserved))

    def dependent_links(self, reserved: Optional[object] = None) -> Sequence[VariableLink]:
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
        return dotnet_links_to_iterable(self._wrapped.dependentLinks(reserved))

    def precedents(self,
                   follow_suspended: bool = False,
                   reserved: Optional[object] = None) -> Sequence['IVariable']:
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
            Parameter reserved for future use.

        Returns
        -------
        object
            IDispatch* to an IVariables object.
        """
        return arrayish.Arrayish(self._wrapped.precedents(follow_suspended),
                                 utils.from_dot_net_to_ivariable)

    def dependents(self,
                   follow_suspended: bool = False,
                   reserved: Optional[object] = None) -> Sequence['IVariable']:
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
            Parameter reserved for future use.

        Returns
        -------
        object
            IDispatch* to an IVariables object.
        """
        return arrayish.Arrayish(self._wrapped.dependents(follow_suspended),
                                 utils.from_dot_net_to_ivariable)

    def is_input_to_component(self) -> bool:
        """
        Checks whether the variable is an input.
        Returns ``True`` if the variable was originally added as an input, ignoring the
        current state that can change based off of links.
        """
        return self._wrapped.isInputToComponent()

    def is_input_to_model(self) -> bool:
        """
        Checks whether the variable is an input. A linked input returns ``False`` (Output).
        """
        return self._wrapped.isInputToModel()


class ScalarVariable(IVariable[WRAPPED_TYPE], ABC, Generic[WRAPPED_TYPE]):
    """
    Base class with methods common to scalar variables.
    """

    @abstractmethod
    def set_initial_value(self, value: acvi.IVariableValue) -> None:
        """
        Set the initial value for the variable.

        Parameters
        ----------
        value : acvi.IVariableValue
            The new initial value. Should be coercible to the appropriate type.
        """
        raise NotImplementedError


class FormattableVariable(IVariable[WRAPPED_TYPE], ABC, Generic[WRAPPED_TYPE]):
    """
    Base class for variables which accept a format.
    """

    @property
    def format(self) -> str:
        """
        Get a format string for displaying the variable to the user.
        """
        return self._wrapped.format

    @format.setter
    def format(self, value: str) -> str:
        """
        Set the format string for displaying the variable to the user.
        """
        self._wrapped.format = value
