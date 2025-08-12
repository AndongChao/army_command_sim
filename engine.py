from typing import Dict, List, Tuple
import random
from config import GRID_SIZE, BREAKTHROUGH_RATIO, LOSS_RATIO
from world import Vec2
from units import BaseUnit, ForceStructure

Cell = Tuple[int, int]

class Engine:
    def __init__(self):
        self.units: Dict[int, BaseUnit] = {}
        self.structures = [None, None]
        self.uid_seq = 1
        self.turn_index = 0
        self.turn_time = 0.0
        self.units_reached_edge = [0, 0]  # top for red, bottom for blue depending on side
        self.side_totals = [0, 0]

    def _add_unit(self, side: int, unit_type: str, pos: Vec2, echelon: str, parent: int = None) -> int:
        uid = self.uid_seq; self.uid_seq += 1
        u = BaseUnit.make(uid, side, unit_type, pos, echelon, parent)
        self.units[uid] = u
        return uid

    def _spawn_side(self, side: int, edge: str):
        # edge: "top" (blue) or "bottom" (red)
        y_band = range(2, 30) if edge == "top" else range(GRID_SIZE - 30, GRID_SIZE - 2)
        army_hq = self._add_unit(side, "infantry",
                                 Vec2(GRID_SIZE // 2, y_band.start if edge == "top" else y_band.stop - 1),
                                 "army")
        structure = ForceStructure(army_hq=army_hq)

        for d in range(2):
            dx = GRID_SIZE // 4 + d * (GRID_SIZE // 4)
            dy = (y_band.start + 6) if edge == "top" else (y_band.stop - 7)
            div_hq = self._add_unit(side, "infantry", Vec2(dx, dy), "div", army_hq)
            structure.div_hqs.append(div_hq)
            for b in range(2):
                bx = dx - 10 + b * 20
                by = (y_band.start + 10) if edge == "top" else (y_band.stop - 11)
                bde_hq = self._add_unit(side, "infantry", Vec2(bx, by), "bde", div_hq)
                structure.bde_hqs.append(bde_hq)
                for r in range(2):
                    rx = bx - 6 + r * 12
                    ry = (y_band.start + 14) if edge == "top" else (y_band.stop - 15)
                    reg_hq = self._add_unit(side, "infantry", Vec2(rx, ry), "reg", bde_hq)
                    structure.reg_hqs.append(reg_hq)
                    for i in range(12):
                        ut = random.choices(
                            population=["infantry","mech_infantry","tank","artillery","air_defense","drone"],
                            weights=[24,18,12,8,6,6], k=1
                        )[0]
                        px = max(0, min(99, rx + random.randint(-5, 5)))
                        py = random.choice(list(y_band))
                        if edge == "top":
                            py = min(py + random.randint(0,6), y_band.stop - 1)
                        else:
                            py = max(py - random.randint(0,6), y_band.start)
                        uid = self._add_unit(side, ut, Vec2(px, py), "bn", reg_hq)
                        structure.battalions.append(uid)
        self.structures[side] = structure
        self.side_totals[side] = len(structure.battalions)

    def setup_battle(self):
        self._spawn_side(0, "top")    # blue
        self._spawn_side(1, "bottom") # red

    def cell_key(self, p: Vec2) -> Cell:
        return (p.x, p.y)

    def occupancy(self) -> Dict[Cell, List[int]]:
        occ: Dict[Cell, List[int]] = {}
        for uid, u in self.units.items():
            if not u.alive: continue
            occ.setdefault(self.cell_key(u.pos), []).append(uid)
        return occ

    def resolve_combat(self):
        alive = {uid: u for uid, u in self.units.items() if u.alive}
        s0 = [u for u in alive.values() if u.side == 0]
        s1 = [u for u in alive.values() if u.side == 1]
        for a in s0:
            for b in s1:
                d = a.pos.dist(b.pos)
                if d <= a.range: b.take_damage(max(0, a.attack - b.defense))
                if d <= b.range: a.take_damage(max(0, b.attack - a.defense))

    def _alternatives(self, u: BaseUnit, goal: Vec2, occ: Dict[Cell, List[int]]):
        cand = []
        base = u.pos.dist(goal)
        for dx in (-1,0,1):
            for dy in (-1,0,1):
                if dx==0 and dy==0: continue
                np = Vec2(max(0,min(99,u.pos.x+dx)), max(0,min(99,u.pos.y+dy)))
                if np.dist(goal) >= base: continue
                key = self.cell_key(np)
                if any(self.units[i].alive and self.units[i].side != u.side for i in occ.get(key, [])): 
                    continue
                if any(self.units[i].alive and self.units[i].side == u.side for i in occ.get(key, [])): 
                    continue
                cand.append(np)
        return cand

    def try_move_unit(self, u: BaseUnit, goal: Vec2, occ: Dict[Cell, List[int]]):
        if not u.alive: return
        next_pos = u.pos.step_towards(goal, u.speed)
        if next_pos.x==u.pos.x and next_pos.y==u.pos.y: return
        key = self.cell_key(next_pos)
        enemy = any(self.units[i].alive and self.units[i].side != u.side for i in occ.get(key, []))
        friend = any(self.units[i].alive and self.units[i].side == u.side for i in occ.get(key, []))
        if enemy or friend:
            alts = self._alternatives(u, goal, occ)
            if not alts: return
            next_pos = random.choice(alts)
        u.pos = next_pos
        if u.echelon == "bn":
            if (u.side == 0 and u.pos.y >= 99) or (u.side == 1 and u.pos.y <= 0):
                u.alive = False
                self.units_reached_edge[u.side] += 1

    def step(self, dt: float, ai0, ai1, recon0, recon1):
        self.turn_time += dt
        u0 = {uid:u for uid,u in self.units.items() if u.alive and u.side==0}
        u1 = {uid:u for uid,u in self.units.items() if u.alive and u.side==1}
        recon0.update(dt, friendly_units=u0, enemy_units=u1)
        recon1.update(dt, friendly_units=u1, enemy_units=u0)
        c0 = recon0.get_known_enemy_positions()
        c1 = recon1.get_known_enemy_positions()
        occ = self.occupancy()
        goals = {}
        for uid,u in self.units.items():
            if not u.alive: continue
            goals[uid] = (ai0 if u.side==0 else ai1).plan(u, self.units, c0 if u.side==0 else c1)
        order = list(goals.keys()); random.shuffle(order)
        for uid in order:
            self.try_move_unit(self.units[uid], goals[uid], occ)
            occ = self.occupancy()
        self.resolve_combat()
        return self.check_victory()

    def check_victory(self):
        alive0 = [u for u in self.units.values() if u.alive and u.side==0 and u.echelon=="bn"]
        alive1 = [u for u in self.units.values() if u.alive and u.side==1 and u.echelon=="bn"]
        lost0 = self.side_totals[0] - len(alive0)
        lost1 = self.side_totals[1] - len(alive1)
        hq0_alive = self.units[self.structures[0].army_hq].alive if self.structures[0] else True
        hq1_alive = self.units[self.structures[1].army_hq].alive if self.structures[1] else True
        b0 = self.units_reached_edge[0] >= max(1, int(self.side_totals[0]*0.20))
        b1 = self.units_reached_edge[1] >= max(1, int(self.side_totals[1]*0.20))
        l0 = (lost0 >= int(self.side_totals[0]*0.50)) or (not hq0_alive)
        l1 = (lost1 >= int(self.side_totals[1]*0.50)) or (not hq1_alive)
        if b0 and l1 and not (b1 and l0): return 0
        if b1 and l0 and not (b0 and l1): return 1
        if b0 and l1 and b1 and l0:
            r0 = self.units_reached_edge[0]/max(1,self.side_totals[0])
            r1 = self.units_reached_edge[1]/max(1,self.side_totals[1])
            if r0!=r1: return 0 if r0>r1 else 1
            if lost0!=lost1: return 0 if lost1>lost0 else 1
        return None

    def end_turn(self):
        self.turn_index += 1
        self.turn_time = 0.0
