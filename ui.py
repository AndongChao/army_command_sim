import pygame
from typing import Optional
from config import WINDOW_SIZE, CELL_SIZE, COLORS
from units import BaseUnit

class ContinueButton:
    def __init__(self):
        self.rect = pygame.Rect(10, WINDOW_SIZE - 40, 120, 30)
    def draw(self, screen):
        pygame.draw.rect(screen, COLORS["ui_button"], self.rect, border_radius=6)
        font = pygame.font.SysFont(None, 18)
        text = font.render("Continue", True, COLORS["ui_button_text"])
        screen.blit(text, (self.rect.x + 18, self.rect.y + 7))
    def handle(self, event) -> bool:
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos)

def _tile_rect(x, y):
    return pygame.Rect(x*CELL_SIZE+1, y*CELL_SIZE+1, CELL_SIZE-2, CELL_SIZE-2)

def _stroke_tile(screen, rect, color):
    pygame.draw.rect(screen, COLORS["tile_fill"], rect)
    pygame.draw.rect(screen, color, rect, 1)

def _draw_pennant(screen, rect, color):
    # mast
    pygame.draw.line(screen, color, (rect.left+2, rect.top+rect.height-2), (rect.left+2, rect.top+2), 1)
    # flag triangle
    pygame.draw.polygon(screen, color, [(rect.left+2, rect.top+2), (rect.left+rect.width-3, rect.top+5), (rect.left+2, rect.top+8)], 1)

def _draw_unit_symbol(screen, rect, unit_type, color):
    cx = rect.centerx; cy = rect.centery
    if unit_type == "infantry":
        pygame.draw.line(screen, color, (rect.left+2, cy-2), (rect.right-2, cy-2), 1)
        pygame.draw.line(screen, color, (rect.left+2, cy+2), (rect.right-2, cy+2), 1)
    elif unit_type == "mech_infantry":
        pygame.draw.rect(screen, color, pygame.Rect(rect.left+2, rect.top+2, rect.width-4, rect.height-4), 1)
        pygame.draw.line(screen, color, (rect.left+3, cy), (rect.right-3, cy), 1)
    elif unit_type == "tank":
        pygame.draw.rect(screen, color, pygame.Rect(rect.left+3, cy-2, rect.width-6, 5), 1)
        pygame.draw.circle(screen, color, (cx, cy-4), 1, 1)
        pygame.draw.circle(screen, color, (cx, cy+4), 1, 1)
    elif unit_type == "artillery":
        pygame.draw.line(screen, color, (rect.left+2, rect.bottom-3), (rect.right-3, rect.top+3), 1)
        pygame.draw.line(screen, color, (rect.left+4, rect.bottom-4), (rect.left+8, rect.bottom-6), 1)
    elif unit_type == "air_defense":
        pygame.draw.polygon(screen, color, [(cx, rect.top+3), (rect.right-3, rect.bottom-3), (rect.left+3, rect.bottom-3)], 1)
    elif unit_type == "drone":
        pygame.draw.rect(screen, color, pygame.Rect(cx-1, cy-1, 2, 2), 0)
        pygame.draw.line(screen, color, (rect.left+2, cy), (rect.right-2, cy), 1)
        pygame.draw.line(screen, color, (cx, rect.top+2), (cx, rect.bottom-2), 1)
    else:
        pygame.draw.circle(screen, color, (cx, cy), 2, 1)

def draw_world(screen, units: dict, show_all: bool = True, side_recon: Optional[dict] = None):
    screen.fill(COLORS["bg"])
    for x in range(0, WINDOW_SIZE, CELL_SIZE):
        pygame.draw.line(screen, COLORS["grid"], (x, 0), (x, WINDOW_SIZE))
    for y in range(0, WINDOW_SIZE, CELL_SIZE):
        pygame.draw.line(screen, COLORS["grid"], (0, y), (WINDOW_SIZE, y))

    for u in units.values():
        if not u.alive: continue
        rect = _tile_rect(u.pos.x, u.pos.y)
        # color by side consistent with Russian convention display
        side_color = COLORS["army_blue"] if u.side == 0 else COLORS["army_red"]
        _stroke_tile(screen, rect, side_color)
        if u.echelon in ("reg","bde","div","army"):
            # draw pennant plus echelon color underline
            _draw_pennant(screen, rect, side_color)
            underline_color = {"reg":COLORS["hq_reg"], "bde":COLORS["hq_bde"], "div":COLORS["hq_div"], "army":COLORS["hq_army"]}[u.echelon]
            pygame.draw.line(screen, underline_color, (rect.left+2, rect.bottom-3), (rect.right-2, rect.bottom-3), 1)
        else:
            _draw_unit_symbol(screen, rect, u.unit_type, side_color)
