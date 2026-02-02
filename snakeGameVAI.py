import pygame
import random
import numpy as np
import sys

# Constants
WIDTH, HEIGHT = 600, 400
GRID_SIZE = 20
BLACK = (20, 20, 20)
GRAY = (40, 40, 40)
GREEN = (0, 255, 0)
RED = (213, 50, 80)

class SnakeGameAI:
    def __init__(self, render_speed=0):
        # render_speed: 0 = max speed (no delay), 60 = 60 FPS, etc.
        self.w = WIDTH
        self.h = HEIGHT
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake AI Training')
        self.clock = pygame.time.Clock()
        self.render_speed = render_speed
        self.reset()

    def reset(self):
        self.direction = "RIGHT"
        self.head = [self.w // 2, self.h // 2]
        self.snake = [
            list(self.head),
            [self.head[0]-GRID_SIZE, self.head[1]], 
            [self.head[0]-(2*GRID_SIZE), self.head[1]]
        ]
        self.score = 0
        self.food = self._place_food()
        self.frame_iteration = 0

    def _place_food(self):
        x = random.randrange(0, self.w // GRID_SIZE) * GRID_SIZE
        y = random.randrange(0, self.h // GRID_SIZE) * GRID_SIZE
        if [x, y] in self.snake:
            return self._place_food()
        return [x, y]

    def get_state(self):
        # 2D Grid for CNN Input: (Height, Width)
        state = np.zeros((self.h // GRID_SIZE, self.w // GRID_SIZE))
        for pt in self.snake:
            state[pt[1]//GRID_SIZE][pt[0]//GRID_SIZE] = 1 # Body
        state[self.food[1]//GRID_SIZE][self.food[0]//GRID_SIZE] = 2 # Food
        return state

    def is_collision(self, pt=None):
        if pt is None: pt = self.head
        # Boundary check
        if pt[0] >= self.w or pt[0] < 0 or pt[1] >= self.h or pt[1] < 0:
            return True
        # Self-collision check
        if pt in self.snake[1:]:
            return True
        return False

    def _move(self, action):
        # 0: UP, 1: DOWN, 2: LEFT, 3: RIGHT
        directions = ["UP", "DOWN", "LEFT", "RIGHT"]
        new_dir = directions[action]

        # Block 180-degree turns
        if (new_dir == "UP" and self.direction != "DOWN") or \
        (new_dir == "DOWN" and self.direction != "UP") or \
        (new_dir == "LEFT" and self.direction != "RIGHT") or \
        (new_dir == "RIGHT" and self.direction != "LEFT"):
            self.direction = new_dir

        # Create NEW head position (don't mutate!)
        x, y = self.head
        if self.direction == "UP": 
            y -= GRID_SIZE
        elif self.direction == "DOWN": 
            y += GRID_SIZE
        elif self.direction == "LEFT": 
            x -= GRID_SIZE
        elif self.direction == "RIGHT": 
            x += GRID_SIZE
        
        self.head = [x, y]  # <-- New list object!

    def play_step(self, action):
        self.frame_iteration += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        self._move(action) 
        # in move we mutate the self head as per the action
        # here becuase of reference issue snake[0] and self.head are same - which breaks the game logic
        self.snake.insert(0, list(self.head)) 

        reward = 0
        game_over = False
        
        # Death logic
        if self.is_collision() or self.frame_iteration > 100 * len(self.snake):
            game_over = True
            reward = -10
            self._update_ui()
            if self.render_speed > 0:
                self.clock.tick(self.render_speed)
            return reward, game_over, self.score
            

        # Eat/Move logic
        if self.head == self.food:
            self.score += 1
            reward = 10
            self.food = self._place_food()
        else:
            self.snake.pop()
        
        self._update_ui()
        if self.render_speed > 0:
            self.clock.tick(self.render_speed)
        return reward, game_over, self.score

    def _update_ui(self):
        self.display.fill(BLACK)
        
        # Draw Grid
        for x in range(0, self.w, GRID_SIZE):
            pygame.draw.line(self.display, GRAY, (x, 0), (x, self.h))
        for y in range(0, self.h, GRID_SIZE):
            pygame.draw.line(self.display, GRAY, (0, y), (self.w, y))
        
        # Draw Food & Snake
        pygame.draw.rect(self.display, RED, [self.food[0], self.food[1], GRID_SIZE, GRID_SIZE])
        for pt in self.snake:
            pygame.draw.rect(self.display, GREEN, [pt[0], pt[1], GRID_SIZE, GRID_SIZE])
        
        pygame.display.flip()