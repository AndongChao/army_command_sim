from typing import Dict, Optional, List
from units import BaseUnit
from world import Vec2
from config import C2_MAX_OFFSET

class SimpleAI:
    def __init__(self, side: int, structure, recon):
        self.side = side
        self.structure = structure
        self.recon = recon

    def _children_of(self, uid: int, units: Dict[int, BaseUnit]) -> List[BaseUnit]:
        return [u for u in units.values() if u.alive and u.parent_hq == uid]

    def _axis_advance(self, pos: Vec2) -> Vec2:
        # vertical: blue(side=0) moves +y, red(side=1) moves -y
        if self.side == 0:
            return Vec2(pos.x, min(99, pos.y + 2))
        else:
            return Vec2(pos.x, max(0, pos.y - 2))

    def choose_target(self, unit: BaseUnit, enemy_contacts: Dict[int, Vec2]) -> Optional[Vec2]:
        if not enemy_contacts:
            return self._axis_advance(unit.pos)
        nearest = None
        best = 1e9
        for _, p in enemy_contacts.items():
            d = unit.pos.dist(p)
            if d < best:
                best = d
                nearest = p
        return nearest

    def c2_bias(self, unit: BaseUnit, units: Dict[int, BaseUnit], has_contacts: bool) -> Optional[Vec2]:
        if has_contacts: return None
        if unit.parent_hq is None: return None
        hq = units.get(unit.parent_hq)
        if not hq or not hq.alive: return None
        if unit.pos.dist(hq.pos) > C2_MAX_OFFSET:
            return hq.pos
        return None

    def plan_hq(self, unit: BaseUnit, units: Dict[int, BaseUnit]) -> Vec2:
        kids = self._children_of(unit.uid, units)
        if not kids:
            return self._axis_advance(unit.pos)
        cx = sum(k.pos.x for k in kids) / len(kids)
        cy = sum(k.pos.y for k in kids) / len(kids)
        bias = 2 if self.side == 0 else -2
        return Vec2(int(round(cx)), int(round(cy + bias)))

    def plan(self, unit: BaseUnit, units: Dict[int, BaseUnit], enemy_contacts: Dict[int, Vec2]) -> Vec2:
        if unit.echelon in ("reg", "bde", "div", "army"):
            return self.plan_hq(unit, units)
        has = bool(enemy_contacts)
        c2 = self.c2_bias(unit, units, has)
        if c2: return c2
        tgt = self.choose_target(unit, enemy_contacts)
        return tgt if tgt else unit.pos
