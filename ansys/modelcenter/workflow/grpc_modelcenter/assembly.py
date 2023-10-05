"""Implementation of Assembly."""

from typing import TYPE_CHECKING, Optional, Tuple

import ansys.tools.variableinterop as atvi
from overrides import overrides

import ansys.modelcenter.workflow.api as mc_api
import ansys.modelcenter.workflow.grpc_modelcenter.abstract_control_statement as abstractcs

from .create_datapin import create_datapin

if TYPE_CHECKING:
    from .engine import Engine

from ansys.api.modelcenter.v0.element_messages_pb2 import (
    AddAssemblyRequest,
    AddAssemblyVariableRequest,
    AddAssemblyVariableResponse,
    ElementId,
    ElementName,
)
from ansys.api.modelcenter.v0.workflow_messages_pb2 import (
    DeleteAssemblyVariableRequest,
    ElementIdOrName,
    NamedElementWorkflow,
)

from .grpc_error_interpretation import (
    WRAP_INVALID_ARG,
    WRAP_NAME_COLLISION,
    WRAP_TARGET_NOT_FOUND,
    InvalidInstanceError,
    interpret_rpc_error,
)
from .var_value_convert import interop_type_to_grpc_type_enum, interop_type_to_mc_type_string


class Assembly(
    abstractcs.AbstractControlStatement,
    mc_api.IAssembly,
):
    """
    Represents an assembly in ModelCenter.

    .. note::
        This class should not be directly instantiated by clients. Get a Workflow object from
        an instantiated Engine, and use it to get a valid instance of this object.
    """

    def __init__(self, element_id: ElementId, engine: "Engine"):
        """
        Initialize a new instance.

        Parameters
        ----------
        element_id : ElementId
            The id of the .
        engine: Engine
            The engine that created this assembly.
        """
        super(Assembly, self).__init__(element_id=element_id, engine=engine)

    @overrides
    def __eq__(self, other):
        return isinstance(other, Assembly) and self.element_id == other.element_id

    @property
    @overrides
    def parent_element_id(self) -> str:
        result: str
        try:
            result = super().parent_element_id
        except InvalidInstanceError:
            # return empty string instead of an error if this is the root
            if self.full_name.find(".") == -1:
                result = ""
            else:
                raise
        return result

    @interpret_rpc_error({**WRAP_TARGET_NOT_FOUND, **WRAP_NAME_COLLISION, **WRAP_INVALID_ARG})
    @overrides
    def add_datapin(self, name: str, mc_type: atvi.VariableType) -> mc_api.IDatapin:
        type_in_request: str = interop_type_to_mc_type_string(mc_type)
        result: AddAssemblyVariableResponse = self._client.AssemblyAddVariable(
            AddAssemblyVariableRequest(
                name=ElementName(name=name),
                target_assembly=self._element_id,
                variable_type=type_in_request,
            )
        )
        return create_datapin(interop_type_to_grpc_type_enum(mc_type), result.id, self._engine)

    @interpret_rpc_error(WRAP_TARGET_NOT_FOUND)
    @overrides
    def delete_datapin(self, name: str) -> bool:
        assembly_name = self.name
        var_name = f"{assembly_name}.{name}"
        request = DeleteAssemblyVariableRequest(
            target=ElementIdOrName(
                target_name=NamedElementWorkflow(element_full_name=ElementName(name=var_name))
            )
        )
        return self._client.AssemblyDeleteVariable(request).existed

    @interpret_rpc_error({**WRAP_TARGET_NOT_FOUND, **WRAP_NAME_COLLISION, **WRAP_INVALID_ARG})
    @overrides
    def add_assembly(
        self,
        name: str,
        av_pos: Optional[Tuple[int, int]] = None,
        assembly_type: Optional[mc_api.AssemblyType] = None,
    ) -> mc_api.IAssembly:
        request = AddAssemblyRequest(
            name=ElementName(name=name),
            parent=self._element_id,
            assembly_type=assembly_type.value
            if assembly_type is not None
            else mc_api.AssemblyType.ASSEMBLY.value,
        )
        if av_pos is not None:
            (x_pos, y_pos) = av_pos
            request.av_pos.x_pos = x_pos
            request.av_pos.y_pos = y_pos
        response = self._client.AssemblyAddAssembly(request)
        return Assembly(response.id, self._engine)
