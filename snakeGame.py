import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 400
GRID_SIZE = 20
FPS = 12

# Colors
WHITE = (255, 255, 255)
BLACK = (20, 20, 20)  # Slightly lighter black
RED = (213, 50, 80)
GREEN = (0, 255, 0)
GRAY = (40, 40, 40)   # For grid lines
BORDER_COLOR = (100, 100, 100)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Game - Grid Edition')
clock = pygame.time.Clock()

font_style = pygame.font.SysFont("bahnschrift", 20)
score_font = pygame.font.SysFont("bahnschrift", 30)

class SnakeGame:
    def __init__(self):
        self.high_score = 0
        self.reset_game()

    def reset_game(self):
        self.snake_pos = [[WIDTH // 2, HEIGHT // 2]]
        self.snake_direction = "RIGHT"
        self.food_pos = self._place_food()
        self.score = 0
        self.game_over = False

    def _place_food(self):
        # Place food on the grid within the borders
        x = random.randrange(1, (WIDTH // GRID_SIZE) - 1) * GRID_SIZE
        y = random.randrange(1, (HEIGHT // GRID_SIZE) - 1) * GRID_SIZE
        return [x, y]

    def draw_grid(self):
        for x in range(0, WIDTH, GRID_SIZE):
            pygame.draw.line(screen, GRAY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, GRID_SIZE):
            pygame.draw.line(screen, GRAY, (0, y), (WIDTH, y))

    def draw_ui(self):
        # Draw Border
        pygame.draw.rect(screen, BORDER_COLOR, [0, 0, WIDTH, HEIGHT], 2)
        # Draw Score
        score_text = score_font.render(f"Score: {self.score}  Best: {self.high_score}", True, WHITE)
        screen.blit(score_text, [10, 10])

    def center_message(self, text, color):
        msg = font_style.render(text, True, color)
        msg_rect = msg.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(msg, msg_rect)

    def run(self):
        while True:
            while self.game_over:
                screen.fill(BLACK)
                self.center_message("Game Over! Press C to Restart or Q to Quit", RED)
                pygame.display.update()

                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            pygame.quit()
                            sys.exit()
                        if event.key == pygame.K_c:
                            self.reset_game()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT and self.snake_direction != "RIGHT":
                        self.snake_direction = "LEFT"
                    elif event.key == pygame.K_RIGHT and self.snake_direction != "LEFT":
                        self.snake_direction = "RIGHT"
                    elif event.key == pygame.K_UP and self.snake_direction != "DOWN":
                        self.snake_direction = "UP"
                    elif event.key == pygame.K_DOWN and self.snake_direction != "UP":
                        self.snake_direction = "DOWN"

            # Movement
            head_x, head_y = self.snake_pos[0]
            if self.snake_direction == "UP": head_y -= GRID_SIZE
            elif self.snake_direction == "DOWN": head_y += GRID_SIZE
            elif self.snake_direction == "LEFT": head_x -= GRID_SIZE
            elif self.snake_direction == "RIGHT": head_x += GRID_SIZE

            new_head = [head_x, head_y]

            # Collision Check
            if (head_x < 0 or head_x >= WIDTH or head_y < 0 or head_y >= HEIGHT 
                or new_head in self.snake_pos):
                self.game_over = True
                self.high_score = max(self.score, self.high_score)
                continue

            self.snake_pos.insert(0, new_head)

            # Food Check
            if head_x == self.food_pos[0] and head_y == self.food_pos[1]:
                self.score += 1
                self.food_pos = self._place_food()
            else:
                self.snake_pos.pop()

            # Render Loop
            screen.fill(BLACK)
            self.draw_grid()
            pygame.draw.rect(screen, RED, [self.food_pos[0], self.food_pos[1], GRID_SIZE, GRID_SIZE])
            for pos in self.snake_pos:
                pygame.draw.rect(screen, GREEN, [pos[0], pos[1], GRID_SIZE, GRID_SIZE])
            
            self.draw_ui()
            pygame.display.update()
            clock.tick(FPS)

if __name__ == "__main__":
    game = SnakeGame()
    game.run()