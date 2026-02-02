# Snake AI - Deep Q-Learning with CNN

Training a neural network to play Snake using reinforcement learning.

## What's in here

- `snakeGameVAI.py` - The Snake game environment built with Pygame
- `snakeAI.ipynb` - CNN model, DQN agent, and training loop

## How it works

The AI sees the game as a 20x30 grid where:
- 0 = empty space
- 1 = snake body
- 2 = food

A CNN processes this grid and outputs Q-values for 4 actions (up, down, left, right). The agent learns through experience replay and the Bellman equation.

## Setup

```bash
pip install torch pygame numpy
```

## Training

```python
import pygame
pygame.init()

from snakeGameVAI import SnakeGameAI, WIDTH, HEIGHT, GRID_SIZE
# ... import Agent, SnakeCNN from notebook

train()
```

Set `render_speed=60` in SnakeGameAI to watch it play, or `render_speed=0` for fast training.

## Model saves

Models save to `model/snake_cnn.pth` automatically:
- Every 50 games
- On new high score
- When you Ctrl+C

Training resumes from the last checkpoint when you run again.

## Network architecture

```
Input: (1, 20, 30) grid
  -> Conv2d(1, 16, 3x3) + ReLU
  -> Conv2d(16, 32, 3x3) + ReLU
  -> Flatten
  -> Linear(32*20*30, 128) + ReLU
  -> Linear(128, 4)
Output: Q-values for [UP, DOWN, LEFT, RIGHT]
```

## Hyperparameters

- Learning rate: 0.001
- Gamma (discount): 0.9
- Epsilon: decays from 1.0 to 0.01 over ~200 games
- Replay buffer: 100k transitions
- Batch size: 1000

## Known issues

Still debugging - snake collision logic and training performance - WIP.
