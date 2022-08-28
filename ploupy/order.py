import time
import asyncio
from typing import Any, Awaitable, Callable

from .core import ActionFailedException


class Order:

    MAX_RETRIES: int = 3
    """
    Maximum number of times the action will be sent to the server
    in case of `ActionFailedException`
    """
    RETRY_DELAY: float = 0.5
    """
    Delay to wait before retrying to send the action to the server
    """

    def __init__(
        self,
        on: Callable[[], bool],
        action: Callable[[], Awaitable[None]],
        with_timeout: float | None = None,
        with_retry: bool = True,
    ) -> None:
        self._on = on
        self._action = action
        self._aborted = False
        self._timeout = with_timeout
        self._with_retry = with_retry
        self._start_time = time.time()

    async def _exec_action(self, nth_try: int = 0):
        """
        Try to execute the action

        This can fails in the case the player spends money
        in between income events (for example on probe creation).
        """
        if nth_try >= self.MAX_RETRIES:
            return  # abort
        try:
            await self._action()
        except ActionFailedException:
            if not self._with_retry:
                return

            await asyncio.sleep(self.RETRY_DELAY)
            # retry
            await self._exec_action(nth_try=nth_try + 1)

    async def resolve(self) -> bool:
        """
        Try to resolve the order:
        Either the order is aborted (either manually or by
        timeout) or check if the conditions are met, if so
        execute the order's action.

        Note: the resolution of an order does not mean that
        it has been successfully executed, it can also have failed.

        Return if the order was resolved
        """
        if self._aborted:
            return True

        if self._timeout is not None:
            if time.time() > self._start_time + self._timeout:
                return True

        if self._on():
            await self._exec_action()
            return True
        return False

    def abort(self) -> None:
        """
        Abort the order, it won't be executed
        """
        self._aborted = True


class OrderMixin:
    """
    Internal mixin

    Add orders handler functionnalities
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._orders: list[Order] = []

    async def place_order(self, order: Order) -> None:
        """
        Place an order

        Try to resolve it directly, if not
        possible, add it to the orders pool
        and tries to resolve it on game state update
        """
        print("OrderMixin", order)
        if await order.resolve():
            return

        self._orders.append(order)

    async def _resolve_orders(self) -> None:
        """
        Try to resolve orders
        """
        to_remove = []
        for order in self._orders:
            if await order.resolve():
                to_remove.append(order)

        for order in to_remove:
            self._orders.remove(order)
