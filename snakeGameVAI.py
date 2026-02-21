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
        self.vx, self.vy = 1, 0
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
        state = np.zeros(11) # 11 vectors input feature
        '''
        state = [
                    danger_straight, 0
                    danger_right, 1 
                    danger_left, 2 
                    moving_left, 3
                    moving_right, 4
                    moving_up, 5
                    moving_down, 6
                    food_left, 7
                    food_right, 8
                    food_up,  9
                    food_down, 10
                ]
        '''
        # mapping danger directions
        state[0] = int(self.is_collision([self.head[0] + self.vx * GRID_SIZE, self.head[1] + self.vy * GRID_SIZE]))  # danger straight
        state[1] = int(self.is_collision([self.head[0] - self.vy * GRID_SIZE, self.head[1] + self.vx * GRID_SIZE]))  # danger right
        state[2] = int(self.is_collision([self.head[0] + self.vy * GRID_SIZE, self.head[1] - self.vx * GRID_SIZE]))  # danger left

        # mapping snake head direction to state indices
        # Set direction state based on velocity (no dictionary needed)
        if self.vx < 0:
            state[3] = 1  # moving LEFT
        elif self.vx > 0:
            state[4] = 1  # moving RIGHT
            
        if self.vy < 0:
            state[5] = 1  # moving UP
        elif self.vy > 0:
            state[6] = 1  # moving DOWN

        # mapping food direction relative to the snake head to state indices
        food_x = self.food[0] - self.head[0]
        food_y = self.food[1] - self.head[1]
        if food_x < 0:
            state[7] = 1  # food left
        elif food_x > 0:
            state[8] = 1  # food right
        # if food_x == 0, neither is set — correct

        if food_y < 0:
            state[9] = 1  # food up
        elif food_y > 0:
            state[10] = 1  # food down
        
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
        directions = [(0,-1), (0,1), (-1,0), (1,0)] 
        new_vx, new_vy = directions[action]
        if (new_vx, new_vy) != (-self.vx, -self.vy):
            self.vx, self.vy = new_vx, new_vy

        # Create NEW head position (don't mutate!)
        x, y = self.head
        x += self.vx * GRID_SIZE
        y += self.vy * GRID_SIZE
        self.head = [x, y]

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