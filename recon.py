from dataclasses import dataclass
from typing import Dict
import random
from world import Vec2
from config import RECON_SCAN_PERIOD, MISID_PROB

@dataclass
class Contact:
    last_seen_at: float
    pos: Vec2
    mis_class: str

class ReconSystem:
    def __init__(self, side: int):
        self.side = side
        self.contacts: Dict[int, Contact] = {}
        self._accum = 0.0

    def update(self, dt: float, friendly_units: dict, enemy_units: dict):
        self._accum += dt
        if self._accum < RECON_SCAN_PERIOD:
            return
        self._accum = 0.0
        for _, fu in friendly_units.items():
            if not fu.alive: continue
            radius = fu.detection_radius()
            for euid, eu in enemy_units.items():
                if not eu.alive: continue
                if fu.pos.dist(eu.pos) <= radius:
                    cls = eu.unit_type
                    if random.random() < MISID_PROB:
                        pool = ["infantry", "mech_infantry", "tank", "artillery", "air_defense", "drone"]
                        if cls in pool and len(pool) > 1:
                            pool.remove(cls)
                        cls = random.choice(pool)
                    self.contacts[euid] = Contact(0.0, eu.pos, cls)
        # age contacts
        for cid in list(self.contacts.keys()):
            c = self.contacts[cid]
            c.last_seen_at += RECON_SCAN_PERIOD
            if c.last_seen_at > 120:
                del self.contacts[cid]

    def get_known_enemy_positions(self):
        return {eid: c.pos for eid, c in self.contacts.items()}
