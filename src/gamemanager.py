from .game import Game
from .models.game import GameState
from .exceptions import InvalidGameIdException


class GameManager:
    def __init__(self) -> None:
        self._games: dict[str, Game] = {}

    def get_game(self, gid: str) -> Game | None:
        """
        Return the game with the given gid
        """
        return self._games.get(gid)

    def add_game(self, game: Game):
        self._games[game._gid] = game
