import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Screen settings
WIDTH = 600
HEIGHT = 600
CELL_SIZE = 20

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# Create screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Clock for controlling speed
clock = pygame.time.Clock()

# Font
font = pygame.font.SysFont("Arial", 24)

# Snake initial position
snake = [(100, 100), (80, 100), (60, 100)]
direction = (20, 0)

# Food position
food = None

# Score and level
score = 0
level = 1
speed = 7


# Function to generate food NOT on snake
def generate_food():
    while True:
        x = random.randrange(0, WIDTH, CELL_SIZE)
        y = random.randrange(0, HEIGHT, CELL_SIZE)
        if (x, y) not in snake:
            return (x, y)


food = generate_food()


# Draw everything
def draw():
    screen.fill(BLACK)

    # Draw snake
    for segment in snake:
        pygame.draw.rect(screen, GREEN, (*segment, CELL_SIZE, CELL_SIZE))

    # Draw food
    pygame.draw.rect(screen, RED, (*food, CELL_SIZE, CELL_SIZE))

    # Draw score and level
    score_text = font.render(f"Score: {score}", True, WHITE)
    level_text = font.render(f"Level: {level}", True, WHITE)

    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (10, 40))

    pygame.display.flip()


# Game over function
def game_over():
    text = font.render("GAME OVER", True, RED)
    screen.blit(text, (WIDTH // 2 - 80, HEIGHT // 2))
    pygame.display.flip()
    pygame.time.delay(2000)
    pygame.quit()
    sys.exit()


# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Control snake
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != (0, 20):
                direction = (0, -20)
            elif event.key == pygame.K_DOWN and direction != (0, -20):
                direction = (0, 20)
            elif event.key == pygame.K_LEFT and direction != (20, 0):
                direction = (-20, 0)
            elif event.key == pygame.K_RIGHT and direction != (-20, 0):
                direction = (20, 0)

    # Move snake
    head_x = snake[0][0] + direction[0]
    head_y = snake[0][1] + direction[1]
    new_head = (head_x, head_y)

    #  Check wall collision
    if head_x < 0 or head_x >= WIDTH or head_y < 0 or head_y >= HEIGHT:
        game_over()

    #  Check self collision
    if new_head in snake:
        game_over()

    snake.insert(0, new_head)

    #  Check food collision
    if new_head == food:
        score += 1

        # Level system (every 4 points)
        if score % 4 == 0:
            level += 1
            speed += 2  # increase speed

        food = generate_food()
    else:
        snake.pop()

    draw()

    clock.tick(speed)