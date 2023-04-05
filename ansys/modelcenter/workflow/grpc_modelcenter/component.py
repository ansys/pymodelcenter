"""Definition of Component."""
from typing import Collection, Sequence

import ansys.common.variableinterop as acvi
import ansys.engineeringworkflow.api as aew_api
from overrides import overrides

import ansys.modelcenter.workflow.api as mc_api

from .abstract_renamable import AbstractRenamableElement


class Component(AbstractRenamableElement, mc_api.IComponent):
    """A component in a Workflow."""

    def __init__(self, elem_id: str):
        """
        Initialize component object.

        Parameters
        ----------
        elem_id: str
        The id string of the component.
        """
        self._id = elem_id

    @property  # type: ignore
    @overrides
    def name(self):
        raise NotImplementedError()

    @property  # type: ignore
    @overrides
    def element_id(self) -> str:
        return self._id

    @property  # type: ignore
    @overrides
    def parent_element_id(self) -> str:
        raise NotImplementedError()

    @overrides
    def get_property(self, property_name: str) -> aew_api.Property:
        raise NotImplementedError()

    @overrides
    def get_properties(self) -> Collection[aew_api.Property]:
        raise NotImplementedError()

    @overrides
    def set_property(self, property_name: str, property_value: acvi.IVariableValue) -> None:
        super().set_custom_metadata_value(property_name, property_value)

    @overrides
    def get_variables(self) -> Collection[mc_api.IVariable]:
        raise NotImplementedError()

    @property  # type: ignore
    @overrides
    def pacz_url(self):
        raise NotImplementedError()

    @property  # type: ignore
    @overrides
    def groups(self) -> Sequence[mc_api.IGroup]:
        raise NotImplementedError()

    @property  # type: ignore
    @overrides
    def associated_files(self) -> Collection[str]:
        raise NotImplementedError()

    @associated_files.setter  # type: ignore
    @overrides
    def associated_files(self, source: Collection[str]):
        raise NotImplementedError()

    @property  # type: ignore
    @overrides
    def index_in_parent(self) -> int:
        raise NotImplementedError()

    @property  # type: ignore
    @overrides
    def parent_assembly(self) -> mc_api.IAssembly:
        raise NotImplementedError()

    @overrides
    def get_source(self) -> str:
        raise NotImplementedError()

    @overrides
    def get_variable(self, name: str) -> mc_api.IVariable:
        raise NotImplementedError()

    @overrides
    def get_type(self) -> str:
        raise NotImplementedError()

    @overrides
    def invoke_method(self, method: str) -> None:
        raise NotImplementedError()

    @overrides
    def invalidate(self) -> None:
        raise NotImplementedError()

    @overrides
    def reconnect(self) -> None:
        raise NotImplementedError()

    @overrides
    def download_values(self) -> None:
        raise NotImplementedError()
