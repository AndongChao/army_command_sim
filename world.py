import math
from dataclasses import dataclass
from config import GRID_SIZE

@dataclass
class Vec2:
    x: int
    y: int
    def dist(self, other: "Vec2") -> float:
        return math.hypot(self.x - other.x, self.y - other.y)
    def step_towards(self, target: "Vec2", max_step: int) -> "Vec2":
        dx = target.x - self.x
        dy = target.y - self.y
        d = math.hypot(dx, dy)
        if d == 0 or max_step <= 0:
            return Vec2(self.x, self.y)
        step = min(max_step, d)
        nx = self.x + int(round((dx / d) * step))
        ny = self.y + int(round((dy / d) * step))
        nx = max(0, min(GRID_SIZE - 1, nx))
        ny = max(0, min(GRID_SIZE - 1, ny))
        return Vec2(nx, ny)
