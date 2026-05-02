import pygame
import random
import sys

pygame.init()

# -----------------------------
# Screen settings
# -----------------------------
WIDTH = 400
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Practice 11 Racer")

clock = pygame.time.Clock()
FPS = 60

# -----------------------------
# Colors
# -----------------------------
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)
GREEN = (0, 180, 0)
RED = (220, 40, 40)
BLUE = (40, 120, 255)
YELLOW = (255, 215, 0)
ORANGE = (255, 140, 0)
PURPLE = (170, 60, 255)

# -----------------------------
# Fonts
# -----------------------------
font = pygame.font.SysFont("Arial", 28)
small_font = pygame.font.SysFont("Arial", 20)

# -----------------------------
# Road settings
# -----------------------------
road_rect = pygame.Rect(60, 0, 280, HEIGHT)

# -----------------------------
# Player car
# -----------------------------
player = pygame.Rect(WIDTH // 2 - 25, HEIGHT - 90, 50, 80)
player_speed = 6

# -----------------------------
# Enemy car
# -----------------------------
enemy = pygame.Rect(random.randint(80, 280), -100, 50, 80)
enemy_speed = 5

# -----------------------------
# Coin settings
# -----------------------------
coin_rect = pygame.Rect(random.randint(80, 300), -40, 30, 30)
coin_weight = random.choice([1, 2, 3])

score = 0
coins_collected = 0

# Enemy speed increases every N coins
N = 5
next_speed_increase = N

running = True
game_over = False


def reset_coin():
    """
    Creates a new coin with random position and random weight.
    Weight means how many points/coins the player gets.
    """
    global coin_rect, coin_weight

    coin_rect.x = random.randint(80, 300)
    coin_rect.y = random.randint(-200, -40)

    # Weighted coins: 1 is common, 2 and 3 are rarer
    coin_weight = random.choice([1, 1, 1, 2, 3])


def reset_enemy():
    """
    Moves enemy car back to the top with random x-position.
    """
    enemy.x = random.randint(80, 280)
    enemy.y = random.randint(-200, -100)


def get_coin_color(weight):
    """
    Returns coin color depending on coin weight.
    """
    if weight == 1:
        return YELLOW
    elif weight == 2:
        return ORANGE
    else:
        return PURPLE


def draw_game():
    """
    Draws road, player, enemy, coin, and score.
    """
    screen.fill(GREEN)

    # Draw road
    pygame.draw.rect(screen, GRAY, road_rect)

    # Draw road side lines
    pygame.draw.line(screen, WHITE, (60, 0), (60, HEIGHT), 4)
    pygame.draw.line(screen, WHITE, (340, 0), (340, HEIGHT), 4)

    # Draw middle dashed lines
    for y in range(0, HEIGHT, 80):
        pygame.draw.rect(screen, WHITE, (WIDTH // 2 - 5, y, 10, 40))

    # Draw player car
    pygame.draw.rect(screen, BLUE, player, border_radius=8)
    pygame.draw.rect(screen, BLACK, player, 2, border_radius=8)

    # Draw enemy car
    pygame.draw.rect(screen, RED, enemy, border_radius=8)
    pygame.draw.rect(screen, BLACK, enemy, 2, border_radius=8)

    # Draw coin
    pygame.draw.circle(screen, get_coin_color(coin_weight), coin_rect.center, 15)
    pygame.draw.circle(screen, BLACK, coin_rect.center, 15, 2)

    # Draw coin weight text
    coin_text = small_font.render(str(coin_weight), True, BLACK)
    coin_text_rect = coin_text.get_rect(center=coin_rect.center)
    screen.blit(coin_text, coin_text_rect)

    # Draw score
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    coins_text = small_font.render(f"Coins: {coins_collected}", True, WHITE)
    screen.blit(coins_text, (10, 45))

    speed_text = small_font.render(f"Enemy speed: {enemy_speed}", True, WHITE)
    screen.blit(speed_text, (10, 70))


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
    Resets all game variables.
    """
    global score, coins_collected, enemy_speed, next_speed_increase, game_over

    score = 0
    coins_collected = 0
    enemy_speed = 5
    next_speed_increase = N
    game_over = False

    player.x = WIDTH // 2 - 25
    player.y = HEIGHT - 90

    reset_enemy()
    reset_coin()


while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_over and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                restart_game()
            elif event.key == pygame.K_q:
                running = False

    if not game_over:
        keys = pygame.key.get_pressed()

        # Move player left/right
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player.x -= player_speed

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player.x += player_speed

        # Keep player inside road
        if player.left < road_rect.left:
            player.left = road_rect.left

        if player.right > road_rect.right:
            player.right = road_rect.right

        # Move enemy and coin down
        enemy.y += enemy_speed
        coin_rect.y += enemy_speed

        # If enemy goes out of screen, respawn it
        if enemy.top > HEIGHT:
            reset_enemy()

        # If coin goes out of screen, respawn it
        if coin_rect.top > HEIGHT:
            reset_coin()

        # Collision with coin
        if player.colliderect(coin_rect):
            score += coin_weight * 10
            coins_collected += coin_weight
            reset_coin()

            # Increase enemy speed after every N collected coins
            if coins_collected >= next_speed_increase:
                enemy_speed += 1
                next_speed_increase += N

        # Collision with enemy means game over
        if player.colliderect(enemy):
            game_over = True

        draw_game()

    else:
        draw_game_over()

    pygame.display.update()

pygame.quit()
sys.exit()