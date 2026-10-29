import os
import math
import pygame
from .agent import QLearningAgent, ACTION_NAMES
from .environment import Garden

WIDTH, HEIGHT = 1120, 760
CELL = 36
GRID_X, GRID_Y = 36, 142
PANEL_X = 910
MEMORY_FILE = "lain_memory.json"

class LainLab:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("LAIN — Artificial Life Laboratory")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("consolas", 17)
        self.small = pygame.font.SysFont("consolas", 13)
        self.big = pygame.font.SysFont("consolas", 27, bold=True)
        self.agent = QLearningAgent()
        self.garden = Garden()
        self.running = True
        self.paused = False
        self.fast = False
        self.edit_mode = False
        self.episode = 1
        self.total_steps = 0
        self.last_reward = 0.0
        self.message = "Hola, soy Lain. ¡Vamos a explorar!"
        self.step_counter = 0
        self.buttons = []
        self.cloud_offset = 0

    def text(self, text, x, y, color=(230, 240, 235), font=None):
        surf = (font or self.font).render(str(text), True, color)
        self.screen.blit(surf, (x, y))

    def button(self, label, rect, action, active=False):
        color = (64, 105, 87) if active else (45, 66, 65)
        pygame.draw.rect(self.screen, color, rect, border_radius=8)
        pygame.draw.rect(self.screen, (113, 160, 133), rect, 1, border_radius=8)
        surf = self.small.render(label, True, (245, 250, 245))
        self.screen.blit(surf, surf.get_rect(center=rect.center))
        self.buttons.append((rect, action))

    def draw_background(self):
        self.screen.fill((134, 204, 238))
        # Sky gradient
        for y in range(0, 122):
            c = (max(95, 134 - y // 5), max(170, 204 - y // 8), 238)
            pygame.draw.line(self.screen, c, (0, y), (WIDTH, y))
        # Soft clouds
        self.cloud_offset = (self.cloud_offset + 0.12) % (WIDTH + 180)
        for cx, cy in [(140, 42), (460, 66), (760, 36)]:
            x = int((cx + self.cloud_offset) % (WIDTH + 140) - 100)
            pygame.draw.ellipse(self.screen, (242, 250, 255), (x, cy, 82, 24))
            pygame.draw.ellipse(self.screen, (250, 253, 255), (x + 18, cy - 12, 36, 32))
        pygame.draw.rect(self.screen, (95, 177, 91), (0, 120, WIDTH, HEIGHT - 120))
        pygame.draw.rect(self.screen, (70, 143, 76), (0, 120, WIDTH, 14))
        # Garden plot
        pygame.draw.rect(self.screen, (99, 170, 89), (GRID_X - 8, GRID_Y - 8, Garden.WIDTH*CELL+16, Garden.HEIGHT*CELL+16), border_radius=14)

    def draw_garden(self):
        for y in range(Garden.HEIGHT):
            for x in range(Garden.WIDTH):
                rect = pygame.Rect(GRID_X+x*CELL, GRID_Y+y*CELL, CELL, CELL)
                base = (111, 184, 94) if (x+y) % 2 else (105, 178, 89)
                pygame.draw.rect(self.screen, base, rect)
                if (x*13 + y*7) % 11 == 0:
                    pygame.draw.line(self.screen, (139, 201, 111), (rect.x+8, rect.y+25), (rect.x+12, rect.y+18), 2)
                if (x,y) in Garden.WATER:
                    pygame.draw.rect(self.screen, (67, 155, 210), rect.inflate(-3,-3), border_radius=7)
                    pygame.draw.arc(self.screen, (151, 220, 242), rect.inflate(-10,-17), 0, math.pi, 2)
                elif (x,y) in Garden.TREES:
                    pygame.draw.rect(self.screen, (105, 73, 46), (rect.x+14, rect.y+18, 9, 17))
                    pygame.draw.circle(self.screen, (39, 119, 62), (rect.centerx, rect.centery-3), 17)
                    pygame.draw.circle(self.screen, (53, 145, 72), (rect.centerx-7, rect.centery-8), 10)
                elif (x,y) in Garden.ROCKS:
                    pygame.draw.ellipse(self.screen, (126, 137, 136), rect.inflate(-7,-12))
                    pygame.draw.ellipse(self.screen, (171, 181, 178), (rect.x+10, rect.y+10, 11, 6))
                elif (x,y) in Garden.FLOWERS:
                    pygame.draw.line(self.screen, (42, 117, 53), (rect.centerx, rect.centery+9), (rect.centerx, rect.centery+1), 3)
                    for dx,dy,col in [(-5,0,(255,111,161)),(5,0,(255,199,75)),(0,-5,(255,240,150)),(0,5,(255,111,161))]:
                        pygame.draw.circle(self.screen, col, (rect.centerx+dx, rect.centery+dy-2), 4)
                    pygame.draw.circle(self.screen, (126, 77, 32), (rect.centerx, rect.centery-2), 3)

        # Lain: tiny friendly bot
        x,y = self.garden.position
        cx,cy = GRID_X+x*CELL+CELL//2, GRID_Y+y*CELL+CELL//2
        pygame.draw.ellipse(self.screen, (53, 98, 88), (cx-13,cy+13,26,7))
        pygame.draw.rect(self.screen, (235, 246, 240), (cx-12,cy-12,24,25), border_radius=8)
        pygame.draw.rect(self.screen, (100, 185, 194), (cx-9,cy-8,18,12), border_radius=5)
        pygame.draw.circle(self.screen, (28, 59, 68), (cx-4,cy-3), 2)
        pygame.draw.circle(self.screen, (28, 59, 68), (cx+4,cy-3), 2)
        pygame.draw.arc(self.screen, (28, 59, 68), (cx-4,cy+1,8,5), 0, math.pi, 1)
        pygame.draw.circle(self.screen, (255, 255, 255), (cx-7,cy-9), 2)

    def draw_panel(self):
        pygame.draw.rect(self.screen, (26, 40, 45), (PANEL_X, 130, 190, 590), border_radius=13)
        self.text("LAIИ LAB", PANEL_X+15, 148, (139, 224, 179), self.big)
        self.text("AGENTE: Q-LEARNING", PANEL_X+15, 185, (163, 192, 190), self.small)
        pygame.draw.line(self.screen, (69, 98, 94), (PANEL_X+14, 210), (WIDTH-18, 210))
        stats = [
            ("Energía", f"{self.garden.energy}%"),
            ("Episodio", self.episode),
            ("Pasos", self.total_steps),
            ("Recompensa", f"{self.garden.episode_reward:.1f}"),
            ("Exploración ε", f"{self.agent.epsilon:.3f}"),
            ("Flores", f"{len(self.garden.collected)}/{len(Garden.FLOWERS)}"),
        ]
        yy = 226
        for label, val in stats:
            self.text(label, PANEL_X+15, yy, (162, 183, 177), self.small)
            self.text(val, PANEL_X+15, yy+18, (245, 247, 226), self.font)
            yy += 57
        pygame.draw.line(self.screen, (69, 98, 94), (PANEL_X+14, yy), (WIDTH-18, yy))
        self.text("ÚLTIMO EVENTO", PANEL_X+15, yy+14, (139, 224, 179), self.small)
        words = self.message.split()
        lines, line = [], ""
        for word in words:
            if len(line + word) > 23:
                lines.append(line); line = ""
            line += word + " "
        if line: lines.append(line)
        for i, line in enumerate(lines[:4]):
            self.text(line, PANEL_X+15, yy+34+i*17, (224, 231, 218), self.small)

    def draw(self):
        self.buttons = []
        self.draw_background()
        self.text("LAIN", 38, 24, (255,255,255), self.big)
        self.text("Un pequeño agente. Un jardín. Un mundo por aprender.", 130, 34, (255,255,255), self.font)
        self.draw_garden()
        self.draw_panel()
        # Bottom control deck
        pygame.draw.rect(self.screen, (25, 43, 44), (26, 704, 864, 43), border_radius=10)
        self.button("▶ / PAUSA [SPACE]", pygame.Rect(38, 711, 150, 29), "pause", self.paused)
        self.button("ENTRENAR [T]", pygame.Rect(198, 711, 125, 29), "fast", self.fast)
        self.button("PASO [N]", pygame.Rect(333, 711, 90, 29), "step")
        self.button("REINICIAR [R]", pygame.Rect(433, 711, 125, 29), "reset")
        self.button("GUARDAR [S]", pygame.Rect(568, 711, 110, 29), "save")
        self.button("CARGAR [L]", pygame.Rect(688, 711, 100, 29), "load")
        self.button("EDITAR FLORES", pygame.Rect(798, 711, 90, 29), "edit", self.edit_mode)
        pygame.display.flip()

    def do_step(self):
        state = self.garden.state()
        action = self.agent.choose(state)
        next_state, reward, done, info = self.garden.step(action)
        self.agent.learn(state, action, reward, next_state, done)
        self.last_reward = reward
        self.total_steps += 1
        self.message = f"{ACTION_NAMES[action]}: {info}"
        if done:
            self.episode += 1
            self.garden.reset()

    def reset_episode(self):
        self.garden.reset()
        self.episode += 1
        self.message = "Nuevo episodio. La memoria aprendida se conserva."

    def handle_action(self, action):
        if action == "pause": self.paused = not self.paused
        elif action == "fast": self.fast = not self.fast; self.paused = not self.fast
        elif action == "step": self.do_step()
        elif action == "reset": self.reset_episode()
        elif action == "save":
            self.agent.save(MEMORY_FILE); self.message = "Memoria de Lain guardada."
        elif action == "load":
            if os.path.exists(MEMORY_FILE):
                self.agent.load(MEMORY_FILE); self.message = "Memoria aprendida cargada."
            else: self.message = "Aún no existe lain_memory.json."
        elif action == "edit": self.edit_mode = not self.edit_mode

    def run(self):
        while self.running:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT: self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE: self.handle_action("pause")
                    elif event.key == pygame.K_t: self.handle_action("fast")
                    elif event.key == pygame.K_n: self.handle_action("step")
                    elif event.key == pygame.K_r: self.handle_action("reset")
                    elif event.key == pygame.K_s: self.handle_action("save")
                    elif event.key == pygame.K_l: self.handle_action("load")
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pos = event.pos
                    for rect, action in self.buttons:
                        if rect.collidepoint(pos): self.handle_action(action); break
                    else:
                        gx = (pos[0] - GRID_X) // CELL
                        gy = (pos[1] - GRID_Y) // CELL
                        if self.edit_mode and 0 <= gx < Garden.WIDTH and 0 <= gy < Garden.HEIGHT:
                            tile = (gx, gy)
                            if tile not in Garden.WALLS:
                                Garden.FLOWERS.add(tile)
                                self.message = "Flor experimental añadida al jardín."
            if not self.paused:
                self.step_counter += 1
                delay = 2 if self.fast else 28
                if self.step_counter >= delay:
                    self.step_counter = 0
                    self.do_step()
            self.draw()
