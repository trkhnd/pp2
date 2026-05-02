import pygame
import random
import sys

pygame.init()

# -----------------------------
# Screen settings
# -----------------------------
WIDTH = 600
HEIGHT = 600
CELL_SIZE = 20

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Practice 11 Snake")

clock = pygame.time.Clock()

# -----------------------------
# Colors
# -----------------------------
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 220, 80)
DARK_GREEN = (0, 150, 60)
RED = (255, 60, 60)
ORANGE = (255, 150, 40)
PURPLE = (170, 60, 255)
GRAY = (40, 40, 40)

# -----------------------------
# Fonts
# -----------------------------
font = pygame.font.SysFont("Arial", 28)
small_font = pygame.font.SysFont("Arial", 20)

# -----------------------------
# Game variables
# -----------------------------
snake = [(10, 10), (9, 10), (8, 10)]
direction = (1, 0)
next_direction = (1, 0)

food = None
food_weight = 1
food_spawn_time = 0
food_lifetime = 5000  # 5000 milliseconds = 5 seconds

score = 0
level = 1
foods_eaten = 0
speed = 8

running = True
game_over = False


def random_cell():
    """
    Returns a random grid cell.
    """
    x = random.randint(0, WIDTH // CELL_SIZE - 1)
    y = random.randint(0, HEIGHT // CELL_SIZE - 1)
    return x, y


def spawn_food():
    """
    Creates food in a random position.
    Food must not appear on the snake body.
    Food has random weight.
    """
    global food, food_weight, food_spawn_time

    while True:
        new_food = random_cell()

        if new_food not in snake:
            food = new_food
            break

    # Weighted food: 1 is common, 2 and 3 are rarer
    food_weight = random.choice([1, 1, 1, 2, 3])

    # Remember when this food appeared
    food_spawn_time = pygame.time.get_ticks()


def get_food_color(weight):
    """
    Returns food color depending on food weight.
    """
    if weight == 1:
        return RED
    elif weight == 2:
        return ORANGE
    else:
        return PURPLE


def draw_cell(pos, color):
    """
    Draws one grid cell.
    """
    x, y = pos

    rect = pygame.Rect(
        x * CELL_SIZE,
        y * CELL_SIZE,
        CELL_SIZE,
        CELL_SIZE
    )

    pygame.draw.rect(screen, color, rect)
    pygame.draw.rect(screen, BLACK, rect, 1)


def draw_game():
    """
    Draws snake, food, score, level, and timer.
    """
    screen.fill(GRAY)

    # Draw food
    draw_cell(food, get_food_color(food_weight))

    # Draw food weight number
    fx, fy = food
    text = small_font.render(str(food_weight), True, WHITE)
    text_rect = text.get_rect(
        center=(
            fx * CELL_SIZE + CELL_SIZE // 2,
            fy * CELL_SIZE + CELL_SIZE // 2
        )
    )
    screen.blit(text, text_rect)

    # Draw snake
    for index, segment in enumerate(snake):
        if index == 0:
            draw_cell(segment, GREEN)
        else:
            draw_cell(segment, DARK_GREEN)

    # Draw top information
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    level_text = font.render(f"Level: {level}", True, WHITE)
    screen.blit(level_text, (200, 10))

    # Show remaining food time
    current_time = pygame.time.get_ticks()
    remaining = max(0, food_lifetime - (current_time - food_spawn_time))
    remaining_seconds = remaining // 1000

    timer_text = font.render(f"Food: {remaining_seconds}s", True, WHITE)
    screen.blit(timer_text, (380, 10))


def draw_game_over():
    """
    Draws game over screen.
    """
    screen.fill(BLACK)

    title = font.render("GAME OVER", True, RED)
    title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 60))
    screen.blit(title, title_rect)

    score_text = font.render(f"Final Score: {score}", True, WHITE)
    score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(score_text, score_rect)

    restart_text = small_font.render("Press R to restart or Q to quit", True, WHITE)
    restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
    screen.blit(restart_text, restart_rect)


def restart_game():
    """
    Resets the whole game.
    """
    global snake, direction, next_direction
    global score, level, foods_eaten, speed, game_over

    snake = [(10, 10), (9, 10), (8, 10)]
    direction = (1, 0)
    next_direction = (1, 0)

    score = 0
    level = 1
    foods_eaten = 0
    speed = 8
    game_over = False

    spawn_food()


# Spawn first food before game starts
spawn_food()

while running:
    clock.tick(speed)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_over and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                restart_game()
            elif event.key == pygame.K_q:
                running = False

        if not game_over and event.type == pygame.KEYDOWN:
            # Change direction, but do not allow instant reverse
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                if direction != (0, 1):
                    next_direction = (0, -1)

            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                if direction != (0, -1):
                    next_direction = (0, 1)

            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                if direction != (1, 0):
                    next_direction = (-1, 0)

            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                if direction != (-1, 0):
                    next_direction = (1, 0)

    if not game_over:
        current_time = pygame.time.get_ticks()

        # If food lives longer than timer, remove it and spawn new food
        if current_time - food_spawn_time > food_lifetime:
            spawn_food()

        direction = next_direction

        head_x, head_y = snake[0]
        dx, dy = direction

        new_head = (head_x + dx, head_y + dy)

        # Check border collision
        if (
            new_head[0] < 0
            or new_head[0] >= WIDTH // CELL_SIZE
            or new_head[1] < 0
            or new_head[1] >= HEIGHT // CELL_SIZE
        ):
            game_over = True

        # Check self collision
        elif new_head in snake:
            game_over = True

        else:
            snake.insert(0, new_head)

            # If snake eats food
            if new_head == food:
                score += food_weight * 10
                foods_eaten += 1

                # Level up every 3 food items
                if foods_eaten % 3 == 0:
                    level += 1
                    speed += 1

                spawn_food()

            else:
                # If no food eaten, remove tail
                snake.pop()

        draw_game()

    else:
        draw_game_over()

    pygame.display.update()

pygame.quit()
sys.exit()