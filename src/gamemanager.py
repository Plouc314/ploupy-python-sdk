from .game import Game
from .models.game import GameState
from .exceptions import InvalidGameIdException


class GameManager:
    def __init__(self) -> None:
        self._games: dict[str, Game] = []

    def add_game(self, game: Game):
        self._games[game._gid] = game

    def update_state(self, state: GameState):
        """
        Update state of concerned game

        Raises InvalidGameIdException in case of invalid gid
        """
        game = self._games.get(state.gid)
        if game is None:
            raise InvalidGameIdException()

        game._update_state(state)
