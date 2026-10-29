import random

class Garden:
    WIDTH, HEIGHT = 24, 16
    START = (2, 2)
    FLOWERS = {(4, 3), (19, 3), (5, 12), (18, 12), (11, 7), (21, 9)}
    WATER = {(8, 4), (9, 4), (8, 5), (15, 10), (15, 11)}
    TREES = {(3, 8), (4, 8), (3, 9), (12, 2), (13, 2), (12, 3), (20, 6), (20, 7), (21, 7)}
    ROCKS = {(7, 11), (7, 12), (16, 4), (17, 4), (10, 13)}
    WALLS = WATER | TREES | ROCKS

    def __init__(self):
        self.reset()

    def reset(self):
        self.position = self.START
        self.energy = 100
        self.steps = 0
        self.episode_reward = 0.0
        self.collected = set()
        return self.state()

    def state(self):
        # Coarse energy buckets keep the Q-table manageable.
        energy_bucket = min(4, self.energy // 20)
        return (self.position[0], self.position[1], energy_bucket)

    def step(self, action):
        dx, dy = [(0, -1), (1, 0), (0, 1), (-1, 0)][action]
        x, y = self.position
        target = (x + dx, y + dy)
        reward = -0.12
        done = False
        info = "Lain explora el jardín."

        if not (0 <= target[0] < self.WIDTH and 0 <= target[1] < self.HEIGHT):
            reward -= 1.5
            info = "Borde del jardín: movimiento bloqueado."
        elif target in self.WALLS:
            reward -= 2.0
            info = "Obstáculo: Lain aprende a rodearlo."
        else:
            self.position = target
            self.energy = max(0, self.energy - 1)
            if target in self.FLOWERS and target not in self.collected:
                self.collected.add(target)
                self.energy = min(100, self.energy + 35)
                reward += 8.0
                info = "¡Lain encontró una flor! +energía, recompensa positiva."
            elif target in self.FLOWERS:
                reward += 0.2
                info = "Lain vuelve a visitar una flor."
            elif target in self.WATER:
                reward -= 1.0
                info = "Agua profunda: mejor mantener distancia."
            else:
                info = "Lain explora el césped."

        self.steps += 1
        if self.energy <= 0:
            reward -= 5.0
            done = True
            info = "Lain agotó su energía. Episodio terminado."
        elif len(self.collected) == len(self.FLOWERS):
            reward += 10.0
            done = True
            info = "¡Jardín explorado! Lain encontró todas las flores."

        self.episode_reward += reward
        return self.state(), reward, done, info
