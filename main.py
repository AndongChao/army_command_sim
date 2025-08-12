import pygame
from config import WINDOW_SIZE, SIM_TPS, RENDER_FPS, TURN_DURATION_SEC
from engine import Engine
from ai import SimpleAI
from recon import ReconSystem
from ui import draw_world, ContinueButton

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
        pygame.display.set_caption("Army Command Simulator – Vertical & Soviet/Russian Tiles")
        self.clock_render = pygame.time.Clock()

        self.engine = Engine()
        self.engine.setup_battle()

        self.recon0 = ReconSystem(side=0)  # blue (top)
        self.recon1 = ReconSystem(side=1)  # red (bottom)
        self.ai0 = SimpleAI(0, self.engine.structures[0], self.recon0)
        self.ai1 = SimpleAI(1, self.engine.structures[1], self.recon1)

        self.paused = False
        self.turn_paused = False
        self.continue_btn = ContinueButton()
        self.winner = None

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.paused = not self.paused
                if self.turn_paused and self.continue_btn.handle(event):
                    self.turn_paused = False

            if not self.paused and not self.turn_paused and self.winner is None:
                dt = 1.0 / SIM_TPS
                self.winner = self.engine.step(dt, self.ai0, self.ai1, self.recon0, self.recon1)
                if self.engine.turn_time >= TURN_DURATION_SEC:
                    self.turn_paused = True
                    self.engine.end_turn()

            self.clock_render.tick(RENDER_FPS)
            draw_world(self.screen, self.engine.units, show_all=True)
            if self.turn_paused:
                self.continue_btn.draw(self.screen)

            if self.winner is not None:
                font = pygame.font.SysFont(None, 28)
                msg = f"Winner: {'Blue' if self.winner==0 else 'Red'}"
                text = font.render(msg, True, (255, 255, 255))
                self.screen.blit(text, (WINDOW_SIZE // 2 - 80, 10))

            pygame.display.flip()

if __name__ == "__main__":
    Game().run()
