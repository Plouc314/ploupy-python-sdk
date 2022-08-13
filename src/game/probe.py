import numpy as np

from ..models.game import ProbeState
from ..exceptions import InvalidStateException


class Probe:
    def __init__(self, state: ProbeState) -> None:
        self._assert_complete_state(state)
        self._id: str = state.id
        self._pos: np.ndarray = state.pos.pos
        self._target: np.ndarray | None = (
            None if state.target is None else state.target.coord
        )
        self._alive = True
        self._death_cause: str | None = None

    def _assert_complete_state(self, state: ProbeState):
        if None in (state.pos):
            raise InvalidStateException()

    @property
    def id(self) -> str:
        return self._id

    @property
    def pos(self) -> np.ndarray:
        return self._pos.copy()

    @property
    def target(self) -> np.ndarray:
        if self._target is None:
            return None
        return self._target.copy()

    @property
    def alive(self) -> bool:
        return self._alive

    @property
    def death_cause(self) -> str | None:
        return self._death_cause

    def _die(self, death_cause: str):
        """ """
        self._alive = False
        self._death_cause = death_cause

    def _update_state(self, state: ProbeState):
        """
        Update instance with given state
        """
        if state.pos is not None:
            self._pos = state.pos.pos
        if state.target is not None:
            self._target = state.target.coord
        if state.death is not None:
            self._die(state.death)
