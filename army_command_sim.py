import pygame
import random
import math

# === CONFIGURATION ===
GRID_SIZE = 100
CELL_SIZE = 8  # pixels per grid cell
WINDOW_SIZE = GRID_SIZE * CELL_SIZE
TURN_DURATION_MS = 30000  # 30 seconds per turn

# === UNIT TYPES ===
UNIT_TYPES = {
    "infantry": {"speed": 1, "range": 2, "attack": 5, "defense": 3, "hp": 10},
    "mech_infantry": {"speed": 2, "range": 3, "attack": 7, "defense": 5, "hp": 15},
    "tank": {"speed": 3, "range": 5, "attack": 12, "defense": 8, "hp": 20},
    "artillery": {"speed": 1, "range": 8, "attack": 15, "defense": 2, "hp": 8},
    "air_defense": {"speed": 1, "range": 6, "attack": 10, "defense": 6, "hp": 12},
    "drone": {"speed": 4, "range": 4, "attack": 4, "defense": 1, "hp": 5},
}

# === COLORS ===
COLORS = {
    "army1": (0, 0, 255),
    "army2": (255, 0, 0),
    "hq": (255, 255, 0),
    "background": (30, 30, 30),
}

class Unit:
    def __init__(self, unit_type, x, y, side, is_hq=False):
        self.unit_type = unit_type
        self.x = x
        self.y = y
        self.side = side
        self.is_hq = is_hq
        stats = UNIT_TYPES[unit_type]
        self.speed = stats["speed"]
        self.range = stats["range"]
        self.attack = stats["attack"]
        self.defense = stats["defense"]
        self.hp = stats["hp"]

    def move_towards(self, target_x, target_y):
        dx = target_x - self.x
        dy = target_y - self.y
        dist = math.hypot(dx, dy)
        if dist > 0:
            step = min(self.speed, dist)
            self.x += int(round((dx / dist) * step))
            self.y += int(round((dy / dist) * step))

        # Clamp to map
        self.x = max(0, min(GRID_SIZE - 1, self.x))
        self.y = max(0, min(GRID_SIZE - 1, self.y))

    def in_range(self, other):
        return math.hypot(self.x - other.x, self.y - other.y) <= self.range

    def attack_unit(self, other):
        damage = max(0, self.attack - other.defense)
        if damage > 0:
            other.hp -= damage

class Army:
    def __init__(self, side, start_edge):
        self.units = []
        self.side = side
        self.start_edge = start_edge
        self.populate_army()

    def populate_army(self):
        formation_depth = 30
        for _ in range(50):  # Generate battalions
            unit_type = random.choice(list(UNIT_TYPES.keys()))
            if self.start_edge == "left":
                x = random.randint(0, formation_depth)
            else:
                x = GRID_SIZE - 1 - random.randint(0, formation_depth)
            y = random.randint(0, GRID_SIZE - 1)
            self.units.append(Unit(unit_type, x, y, self.side))
        # Add HQ
        if self.start_edge == "left":
            self.units.append(Unit("infantry", 5, GRID_SIZE // 2, self.side, is_hq=True))
        else:
            self.units.append(Unit("infantry", GRID_SIZE - 6, GRID_SIZE // 2, self.side, is_hq=True))

    def get_hq(self):
        for unit in self.units:
            if unit.is_hq:
                return unit
        return None

class Simulation:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
        pygame.display.set_caption("Army Command Simulator (Prototype)")
        self.clock = pygame.time.Clock()
        self.running = True
        self.paused = False

        self.army1 = Army("army1", "left")
        self.army2 = Army("army2", "right")

    def update(self):
        # Basic AI: move toward nearest enemy or shoot if in range
        for army, enemy in [(self.army1, self.army2), (self.army2, self.army1)]:
            for unit in list(army.units):
                if unit.hp <= 0:
                    continue
                # Find nearest enemy
                living_enemies = [e for e in enemy.units if e.hp > 0]
                if not living_enemies:
                    continue
                target = min(living_enemies, key=lambda e: math.hypot(e.x - unit.x, e.y - unit.y))
                if unit.in_range(target):
                    unit.attack_unit(target)
                else:
                    unit.move_towards(target.x, target.y)

        # Remove dead units
        self.army1.units = [u for u in self.army1.units if u.hp > 0]
        self.army2.units = [u for u in self.army2.units if u.hp > 0]

    def draw(self):
        self.screen.fill(COLORS["background"])
        for army in [self.army1, self.army2]:
            for unit in army.units:
                color = COLORS[army.side]
                if unit.is_hq:
                    color = COLORS["hq"]
                pygame.draw.rect(
                    self.screen,
                    color,
                    (unit.x * CELL_SIZE, unit.y * CELL_SIZE, CELL_SIZE, CELL_SIZE),
                )
        pygame.display.flip()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.paused = not self.paused

            if not self.paused:
                self.update()
            self.draw()
            self.clock.tick(10)  # ~10 FPS

if __name__ == "__main__":
    Simulation().run()
