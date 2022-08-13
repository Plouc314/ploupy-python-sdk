from ..models.game import MapState

from .tile import Tile


class Map:
    def __init__(self, state: MapState) -> None:
        self._tiles: list[Tile] = [Tile(s) for s in state.tiles]

        self._map_tiles: dict[str, Tile] = {t.id: t for t in self._tiles}

    @property
    def tiles(self) -> list[Tile]:
        return self._tiles.copy()

    def _update_state(self, state: MapState):
        """
        Update instance with given state
        """
        for ts in state.tiles:
            tile = self._map_tiles.get(ts.id)
            if tile is not None:
                tile._update_state(ts)
