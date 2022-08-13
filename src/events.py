from .models.game import GameState
from .gamemanager import GameManager
from .sio import sio


class GamesEventsHandler:
    def __init__(self, game_manager: GameManager) -> None:
        self._game_manager = game_manager

    def _bind_events(self):
        """
        Bind events methods to sio instance
        """
        sio.event(self.connect)
        sio.event(self.connect_error)
        sio.event(self.disconnect)
        sio.on("game_state")(self.game_state)

    async def connect(self):
        pass

    async def connect_error(self, data):
        pass

    async def disconnect(self):
        pass

    async def game_state(self, data: dict):
        state = GameState(**data)
        self._game_manager.update_state(state)
