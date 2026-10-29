# LAIN — Artificial Life Laboratory

A small, interactive Python/Pygame laboratory where Lain explores a garden and learns with tabular Q-Learning.

## Features
- Garden environment with grass, trees, water, flowers, energy and hazards.
- Q-Learning agent with epsilon-greedy exploration.
- Manual and automatic training.
- Live panel showing energy, episode, steps, reward, epsilon and recent action.
- Save/load learned Q-values in `lain_memory.json`.
- Reset the agent or environment and experiment with training speed.

## Requirements
- Python 3.10+
- Pygame

## Run
```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
python main.py
```

## Controls
- **SPACE**: pause/resume autonomous learning
- **T**: train faster
- **N**: one learning step
- **R**: reset Lain's position/episode (keeps learned Q-values)
- **S**: save learned memory
- **L**: load memory
- **Mouse**: use the on-screen buttons
- **Click garden**: place a flower/energy tile (when in edit mode)

## Git workflow
From this project directory:
```bash
git init
git add .
git commit -m "feat: create Lain garden learning laboratory"
git branch -M main
git remote add origin https://github.com/YOUR-USER/YOUR-REPO.git
git push -u origin main
```

If the repository already exists, replace the remote URL with its exact URL. Do not commit virtual environments or generated memory files.

## Learning notes
Lain uses a compact state representation: grid position and current energy bucket. Actions are up, right, down, and left. The reward function encourages reaching flowers/energy tiles, discourages collisions and low energy, and gives a small penalty per step to encourage efficient exploration. This is an educational prototype, not a general-purpose or conscious AI.
