from dataclasses import dataclass, field
from typing import Optional, List
from config import UNIT_TYPES, DETECTION_RADIUS
from world import Vec2

Echelon = str  # "bn" | "reg" | "bde" | "div" | "army"

@dataclass
class BaseUnit:
    uid: int
    side: int
    pos: Vec2
    unit_type: str
    hp: int
    attack: int
    defense: int
    range: int
    speed: int
    echelon: Echelon
    parent_hq: Optional[int] = None
    alive: bool = True

    def take_damage(self, dmg: int):
        if dmg <= 0: return
        self.hp -= dmg
        if self.hp <= 0:
            self.alive = False

    @staticmethod
    def make(uid: int, side: int, unit_type: str, pos: Vec2, echelon: Echelon, parent_hq: Optional[int] = None):
        s = UNIT_TYPES[unit_type]
        return BaseUnit(uid=uid, side=side, pos=pos, unit_type=unit_type, hp=s["hp"], attack=s["attack"],
                        defense=s["defense"], range=s["range"], speed=s["speed"], echelon=echelon, parent_hq=parent_hq)

    def detection_radius(self) -> int:
        r = DETECTION_RADIUS
        if self.unit_type == "drone":
            r += 4
        return r

@dataclass
class ForceStructure:
    army_hq: int
    div_hqs: List[int] = field(default_factory=list)
    bde_hqs: List[int] = field(default_factory=list)
    reg_hqs: List[int] = field(default_factory=list)
    battalions: List[int] = field(default_factory=list)
