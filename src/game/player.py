from ..models.game import PlayerState
from ..exceptions import InvalidStateException

from .factory import Factory
from .turret import Turret
from .probe import Probe


class Player:
    def __init__(self, state: PlayerState) -> None:
        self._assert_complete_state(state)
        self._uid: str = state.uid
        self._username: str = state.username
        self._money: int = state.money
        self._income: int = state.income
        self._factories: list[Factory] = [Factory(s) for s in state.factories]
        self._turrets: list[Turret] = [Turret(s) for s in state.turrets]
        self._probes: list[Probe] = [Probe(s) for s in state.probes]
        self._alive = True
        self._death_cause: str | None = None

        self._map_factories: dict[str, Factory] = {f.id: f for f in self._factories}
        self._map_turrets: dict[str, Turret] = {t.id: t for t in self._turrets}
        self._map_probes: dict[str, Probe] = {p.id: p for p in self._probes}

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
        return self._factories.copy()

    @property
    def turrets(self) -> list[Turret]:
        return self._turrets.copy()

    @property
    def probes(self) -> list[Probe]:
        return self._probes.copy()

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

    def _update_state(self, state: PlayerState):
        """
        Update instance with given state
        """
        if state.money is not None:
            self._money = state.money
        if state.income is not None:
            self._income = state.income
        if state.death is not None:
            self._die(state.death)

        for fs in state.factories:
            factory = self._map_factories.get(fs.id)
            if factory is not None:
                factory._update_state(fs)

        for ts in state.turrets:
            turret = self._map_turrets.get(ts.id)
            if turret is not None:
                turret._update_state(ts)

        for ps in state.probes:
            probe = self._map_probes.get(ps.id)
            if probe is not None:
                probe._update_state(ps)
