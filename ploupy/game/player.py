from __future__ import annotations
from typing import TYPE_CHECKING

from ..models.game.entities import FactoryState, ProbeState, TurretState

from ..models.core import GameConfig
from ..order import OrderMixin
from .entity import Entity
from ..models.game import PlayerState
from ..core import InvalidStateException

from .factory import Factory
from .turret import Turret
from .probe import Probe

if TYPE_CHECKING:
    from .game import Game


class Player(Entity):
    def __init__(self, state: PlayerState, game: Game) -> None:
        super().__init__()
        self._assert_complete_state(state)
        self._game = game
        self._config: GameConfig = game.config
        self._uid: str = state.uid
        self._username: str = state.username
        self._money: int = state.money
        self._income: int = state.income
        self._factories: dict[str, Factory] = {
            s.id: Factory(s, self, game) for s in state.factories
        }
        self._turrets: dict[str, Turret] = {
            s.id: Turret(s, self, game) for s in state.turrets
        }
        self._probes: dict[str, Probe] = {
            s.id: Probe(s, self, game) for s in state.probes
        }

        # store currently attacking probes
        # -> to notify of their attack only once
        self._attacking_probes: list[Probe] = []

    def _assert_complete_state(self, state: PlayerState):
        if None in (state.money, state.income):
            raise InvalidStateException()

    @property
    def username(self) -> str:
        return self._username

    @property
    def money(self) -> str:
        return self._money

    @property
    def income(self) -> str:
        return self._income

    @property
    def factories(self) -> list[Factory]:
        return list(self._factories.values())

    @property
    def turrets(self) -> list[Turret]:
        return list(self._turrets.values())

    @property
    def probes(self) -> list[Probe]:
        return list(self._probes.values())

    def can_build_factory(self) -> bool:
        """
        Return if the player can build a factory

        Note: this does not take the tile into account,
        `tile.can_build` should also be called.
        """
        return self._money >= self._config.factory_price

    def can_build_turret(self) -> bool:
        """
        Return if the player can build a turret

        Note: this does not take the tile into account,
        `tile.can_build` should also be called.
        """
        return self._money >= self._config.turret_price

    async def on_income(self, new: int, old: int) -> None:
        """
        Called when the money is updated
        """

    async def on_factory_build(self, factory: Factory) -> None:
        """ """

    async def on_turret_build(self, turret: Turret) -> None:
        """ """

    async def on_probe_build(self, probe: Probe) -> None:
        """ """

    async def on_probes_attack(self, probes: list[Probe]) -> None:
        """"""

    async def _update_state(self, state: PlayerState):
        """
        Update instance with given state
        """
        if state.money is not None:
            old = self._money
            self._money = state.money
            await self.on_income(self._money, old)

        if state.income is not None:
            self._income = state.income

        if state.death is not None:
            self._die(state.death)

        await self._update_factories(state.factories)
        await self._update_turrets(state.turrets)
        await self._update_probes(state.probes)

    async def _update_factories(self, factories_states: list[FactoryState]):
        """
        Update factories
        """

        for fs in factories_states:
            factory = self._factories.get(fs.id)
            if factory is None:
                factory = Factory(fs, self, self._game)
                self._factories[fs.id] = factory
                await self.on_factory_build(factory)
            else:
                await factory._update_state(fs)

        Entity._remove_deads(self._factories)

    async def _update_turrets(self, turrets_states: list[TurretState]):
        """
        Update turrets
        """
        for ts in turrets_states:
            turret = self._turrets.get(ts.id)
            if turret is None:
                turret = Turret(ts, self, self._game)
                self._turrets[ts.id] = turret
                await self.on_turret_build(turret)
            else:
                await turret._update_state(ts)

        Entity._remove_deads(self._turrets)

    async def _update_probes(self, probes_states: list[ProbeState]):
        """
        Update probes
        """
        probes: list[Probe] = []
        for ps in probes_states:
            probe = self._probes.get(ps.id)
            if probe is None:
                probe = Probe(ps, self, self._game)
                self._probes[ps.id] = probe
                await self.on_probe_build(probe)
            else:
                await probe._update_state(ps)
            probes.append(probe)

        # handle probes_attack callback
        new_attacking_probes = []
        for probe in probes:
            if not probe.attacking or not probe.alive:
                continue
            if not probe in self._attacking_probes:
                self._attacking_probes.append(probe)
                new_attacking_probes.append(probe)

        if len(new_attacking_probes) > 0:
            await self.on_probes_attack(new_attacking_probes)

        Entity._remove_deads(self._probes)