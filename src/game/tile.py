import numpy as np

from ..models.game import TileState
from ..exceptions import InvalidStateException


class Tile:
    def __init__(self, state: TileState) -> None:
        self._assert_complete_state(state)
        self._id: str = state.id
        self._coord: np.ndarray = state.coord.coord
        self._owner: str | None = state.owner
        self._occupation: int = state.occupation

    def _assert_complete_state(self, state: TileState):
        if None in (state.coord, state.occupation):
            raise InvalidStateException()

    @property
    def id(self) -> str:
        return self._id

    @property
    def coord(self) -> np.ndarray:
        return self._coord.copy()

    @property
    def owner(self) -> str | None:
        return self._owner

    @property
    def occupation(self) -> int:
        return self._occupation

    def _update_state(self, state: TileState):
        """
        Update instance with given state
        """
        if state.coord is not None:
            self._coord = state.coord.coord
        self._owner = state.owner
        if state.occupation is not None:
            self._occupation = state.occupation
