GRID_SIZE = 100
CELL_SIZE = 8
WINDOW_SIZE = GRID_SIZE * CELL_SIZE
SIM_TPS = 10
RENDER_FPS = SIM_TPS // 3
TURN_DURATION_SEC = 30

# vertical orientation (Blue starts TOP, Red starts BOTTOM)
ORIENTATION = "vertical"

UNIT_TYPES = {
    "infantry":       {"speed": 1, "range": 2, "attack": 5,  "defense": 3, "hp": 10},
    "mech_infantry":  {"speed": 2, "range": 3, "attack": 7,  "defense": 5, "hp": 15},
    "tank":           {"speed": 3, "range": 5, "attack": 12, "defense": 8, "hp": 20},
    "artillery":      {"speed": 1, "range": 8, "attack": 15, "defense": 2, "hp": 8},
    "air_defense":    {"speed": 1, "range": 6, "attack": 10, "defense": 6, "hp": 12},
    "drone":          {"speed": 4, "range": 4, "attack": 4,  "defense": 1, "hp": 5},
}

COLORS = {
    "bg": (28, 28, 28),
    "grid": (40, 40, 40),
    "army_blue": (60, 140, 255),  # enemy color in Russian convention, but we use as Blue side
    "army_red": (240, 70, 70),    # friendly in Russian convention; our Red side
    # HQ echelon pennant colors
    "hq_reg": (180, 255, 120),
    "hq_bde": (255, 200, 100),
    "hq_div": (255, 255, 120),
    "hq_army": (255, 255, 0),
    "ui_button": (70, 70, 70),
    "ui_button_text": (230, 230, 230),
    "tile_fill": (18, 18, 18),
    "tile_stroke": (230, 230, 230),
}

# Recon
RECON_SCAN_PERIOD = 2.0
MISID_PROB = 0.20
DETECTION_RADIUS = 10
C2_MAX_OFFSET = 8
C2_PENALTY_SPEED = 0.7

# Victory
BREAKTHROUGH_RATIO = 0.20
LOSS_RATIO = 0.50

ALLOW_STACKING = False
