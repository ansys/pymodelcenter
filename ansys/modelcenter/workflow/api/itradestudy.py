"""Defines interfaces and types for working with trade studies."""

from abc import ABC, abstractmethod
from typing import Mapping, Sequence

import ansys.engineeringworkflow.api as aew_api
import ansys.tools.variableinterop as atvi


class TradeStudyRun:
    """A structure that represents a snapshot of the state of a trade study run."""

    def __init__(
        self,
        input_values: Mapping[str, atvi.VariableState],
        output_values: Mapping[str, atvi.VariableState],
        run_state: aew_api.WorkflowInstanceState,
    ):
        """Initialize a new instance."""
        self._input_values: Mapping[str, atvi.VariableState] = input_values
        self._output_values: Mapping[str, atvi.VariableState] = output_values
        self._run_state: aew_api.WorkflowInstanceState = run_state

    @property
    def input_values(self) -> Mapping[str, atvi.VariableState]:
        """Get the input values for this run."""
        return self._input_values

    @property
    def output_values(self) -> Mapping[str, atvi.VariableState]:
        """Get the output values for this run."""
        return self._output_values

    @property
    def run_state(self) -> aew_api.WorkflowInstanceState:
        """Get the state of this run."""
        return self._run_state

    # TODO: something to get error messages?


class ITradeStudy(ABC):
    """Represents a trade study."""

    @abstractmethod
    def study_state(self) -> aew_api.WorkflowInstanceState:
        """The state of the trade study overall."""
        # TODO: Define rules for the state.
        #       For example, if any run is errored, does that mean the whole thing?
        #       Even if there are still other runs in progress?
        #       Is this enum appropriate for this or do we need another one?

    # TODO: is this even what we want? Or something more involved?
    #       A stream of completed runs as they come in, for example.
    #       We could do both, or implement a simpler version first and add
    #       something more complex later if we see customer / ACE demand.
    @abstractmethod
    def get_current_run_state(self) -> Sequence[TradeStudyRun]:
        """Get the current run table."""

    def add_runs(self, additional_runs: Sequence[TradeStudyRun]) -> None:
        """
        Append additional runs to the trade study.

        The engine will immediately attempt to schedule these runs.
        """
