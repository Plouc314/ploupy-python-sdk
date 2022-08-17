import asyncio
import logging
import jwt
from typing import Type
from socketio import exceptions

from .core import InvalidBotKeyException, URL_SIO, setup_logger
from .behaviour import Behaviour
from .gamemanager import GameManager
from .events import EventsHandler
from .sio import sio

logger = logging.getLogger("ploupy")


class Bot:
    """
    Main bot class

    Handle runtime of the bot.
    Call `run` method to start.

    Args:
        bot_key: Authentification key, given on bot creation.
        behaviour_class: Client defined class that defines the bot
            behaviour, must inherit from `Behaviour` class
        log_level (optional): Level of ploupy logger, defaults to INFO
    """

    def __init__(
        self,
        bot_key: str,
        behaviour_class: Type[Behaviour],
        log_level: int = logging.INFO,
    ) -> None:
        self._bot_key = bot_key
        self._uid = self._extract_uid(bot_key)
        self._game_man = GameManager(self._uid, behaviour_class)
        self._events_handler = EventsHandler(self._game_man)

        setup_logger(log_level)

    def _extract_uid(self, bot_key: str) -> str:
        """
        Extract uid from bot_key.

        Note: do not verify token signature
        """
        try:
            headers = jwt.get_unverified_header(bot_key)
        except jwt.exceptions.DecodeError as e:
            raise InvalidBotKeyException(e) from None

        uid = headers.get("uid")
        if uid is None:
            raise InvalidBotKeyException("Missing 'uid' header.")

        return uid

    async def _run(self):
        try:
            await sio.connect(URL_SIO, headers={"bot-jwt": self._bot_key})
        except exceptions.ConnectionError:
            return  # the error is logged in connect_error

        # check if existing game
        # -> connect back to them
        await sio.emit("is_active_game", {})

        await sio.wait()

    async def _disconnect(self):
        await sio.disconnect()

    def run(self):
        """
        Run the bot

        Note: this method is blocking
        """
        try:
            asyncio.get_event_loop().run_until_complete(self._run())
        except RuntimeError:  # ctr-C causes a RuntimeError
            pass
        asyncio.get_event_loop().run_until_complete(self._disconnect())
