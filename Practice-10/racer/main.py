import pygame
import sys
import random
import time

# Initialize pygame (ALWAYS FIRST)
pygame.init()

# Screen settings
WIDTH = 400
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer Game")

# FPS (speed control)
FPS = 60
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Font (for score display)
font = pygame.font.SysFont("Arial", 24)

# Player car (rectangle)
player = pygame.Rect(180, 500, 40, 60)

# Enemy car
enemy = pygame.Rect(random.randint(0, WIDTH-40), -100, 40, 60)
enemy_speed = 5

# Coin settings
coin = pygame.Rect(random.randint(0, WIDTH-20), -50, 20, 20)
coin_speed = 4
coin_count = 0  # counter

# Game loop
running = True
while running:

    # Fill background
    screen.fill(GRAY)

    # EVENT HANDLING
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # PLAYER MOVEMENT
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and player.left > 0:
        player.move_ip(-5, 0)

    if keys[pygame.K_RIGHT] and player.right < WIDTH:
        player.move_ip(5, 0)

    # ENEMY MOVEMENT (goes down)
    enemy.move_ip(0, enemy_speed)

    # If enemy goes off screen → respawn
    if enemy.top > HEIGHT:
        enemy.top = -100
        enemy.left = random.randint(0, WIDTH-40)

    # COIN MOVEMENT
    coin.move_ip(0, coin_speed)

    # If coin goes off screen → respawn
    if coin.top > HEIGHT:
        coin.top = -50
        coin.left = random.randint(0, WIDTH-20)

    # COLLISION (player hits enemy → GAME OVER)
    if player.colliderect(enemy):
        text = font.render("GAME OVER", True, RED)
        screen.blit(text, (120, 250))
        pygame.display.update()
        time.sleep(2)
        pygame.quit()
        sys.exit()

    # COIN COLLECTION
    if player.colliderect(coin):
        coin_count += 1  # increase counter

        # Respawn coin safely
        coin.top = -50
        coin.left = random.randint(0, WIDTH-20)

    # DRAW OBJECTS
    pygame.draw.rect(screen, WHITE, player)   # player
    pygame.draw.rect(screen, RED, enemy)      # enemy
    pygame.draw.rect(screen, YELLOW, coin)    # coin

    # DRAW COIN COUNTER (top-right)
    coin_text = font.render(f"Coins: {coin_count}", True, WHITE)
    screen.blit(coin_text, (WIDTH - 120, 10))

    # Update display
    pygame.display.update()

    # Control speed
    clock.tick(FPS)

pygame.quit()