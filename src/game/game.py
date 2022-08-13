from ..models.core import GameConfig
from ..models.game import GameState
from ..exceptions import InvalidStateException

from .map import Map
from .player import Player


class Game:
    def __init__(self, state: GameState) -> None:
        self._assert_complete_state(state)
        self._gid = state.gid
        self._config: GameConfig = state.config
        self._map: Map = Map(state.map)
        self._players: list[Player] = [Player(s) for s in state.players]

        self._map_players: dict[str, Player] = {p._uid: p for p in self._players}

    def _assert_complete_state(self, state: GameState):
        if None in (state.config, state.map):
            raise InvalidStateException()

    @property
    def config(self) -> GameConfig:
        return self._config

    @property
    def map(self) -> Map:
        return self._map

    @property
    def players(self) -> list[Player]:
        return self._players.copy()

    def _update_state(self, state: GameState):
        """
        Update instance with given state
        """

        if state.map is not None:
            self._map._update_state(state.map)

        for ps in state.players:
            player = self._map_players.get(ps.uid)
            if player is not None:
                player._update_state(ps)
