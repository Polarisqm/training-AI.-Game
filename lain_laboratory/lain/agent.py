import random

ACTIONS = [(0, -1), (1, 0), (0, 1), (-1, 0)]
ACTION_NAMES = ["Norte", "Este", "Sur", "Oeste"]

class QLearningAgent:
    def __init__(self, alpha=0.18, gamma=0.92, epsilon=1.0, epsilon_min=0.04, epsilon_decay=0.9994):
        self.q = {}
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay
        self.last_action = 0

    def _key(self, state):
        return tuple(state)

    def values(self, state):
        return self.q.setdefault(self._key(state), [0.0] * 4)

    def choose(self, state):
        vals = self.values(state)
        if random.random() < self.epsilon:
            action = random.randrange(4)
        else:
            best = max(vals)
            candidates = [i for i, v in enumerate(vals) if v == best]
            action = random.choice(candidates)
        self.last_action = action
        return action

    def learn(self, state, action, reward, next_state, done):
        current = self.values(state)
        target = reward if done else reward + self.gamma * max(self.values(next_state))
        current[action] += self.alpha * (target - current[action])
        self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)

    def save(self, path):
        import json
        payload = {
            "q": {"|".join(map(str, k)): v for k, v in self.q.items()},
            "epsilon": self.epsilon,
            "alpha": self.alpha,
            "gamma": self.gamma,
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)

    def load(self, path):
        import json
        with open(path, "r", encoding="utf-8") as f:
            payload = json.load(f)
        self.q = {tuple(map(int, k.split("|"))): list(v) for k, v in payload.get("q", {}).items()}
        self.epsilon = payload.get("epsilon", self.epsilon)
        self.alpha = payload.get("alpha", self.alpha)
        self.gamma = payload.get("gamma", self.gamma)
