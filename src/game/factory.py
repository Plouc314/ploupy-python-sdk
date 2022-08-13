import numpy as np

from ..models.game import FactoryState
from ..exceptions import InvalidStateException


class Factory:
    def __init__(self, state: FactoryState) -> None:
        self._assert_complete_state(state)
        self._id: str = state.id
        self._coord: np.ndarray = state.coord.coord
        self._alive = True
        self._death_cause: str | None = None

    def _assert_complete_state(self, state: FactoryState):
        if None in (state.coord):
            raise InvalidStateException()

    @property
    def id(self) -> str:
        return self._id

    @property
    def coord(self) -> np.ndarray:
        return self._coord.copy()

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

    def _update_state(self, state: FactoryState):
        """
        Update instance with given state
        """
        if state.coord is not None:
            self._coord = state.coord.coord
        if state.death is not None:
            self._die(state.death)
