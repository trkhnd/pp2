import pygame
import sys

pygame.init()

# Screen settings
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Paint")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

colors = [BLACK, RED, GREEN, BLUE]
current_color = BLACK

# Fill background
screen.fill(WHITE)

# Brush settings
brush_size = 5
mode = "brush"  # brush, rect, circle, eraser

# For shapes
start_pos = None

clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Mouse pressed
        if event.type == pygame.MOUSEBUTTONDOWN:
            start_pos = event.pos

            # Check if clicking color palette
            x, y = event.pos
            if y < 50:
                index = x // 50
                if index < len(colors):
                    current_color = colors[index]

        # Mouse released → draw shapes
        if event.type == pygame.MOUSEBUTTONUP:
            if mode == "rect":
                end_pos = event.pos
                rect = pygame.Rect(
                    start_pos[0],
                    start_pos[1],
                    end_pos[0] - start_pos[0],
                    end_pos[1] - start_pos[1],
                )
                pygame.draw.rect(screen, current_color, rect, 2)

            elif mode == "circle":
                end_pos = event.pos
                radius = int(
                    ((end_pos[0] - start_pos[0]) ** 2 +
                     (end_pos[1] - start_pos[1]) ** 2) ** 0.5
                )
                pygame.draw.circle(screen, current_color, start_pos, radius, 2)

        # Keyboard controls
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_b:
                mode = "brush"
            elif event.key == pygame.K_r:
                mode = "rect"
            elif event.key == pygame.K_c:
                mode = "circle"
            elif event.key == pygame.K_e:
                mode = "eraser"

    # Drawing with mouse (brush or eraser)
    if pygame.mouse.get_pressed()[0]:
        x, y = pygame.mouse.get_pos()

        if mode == "brush":
            pygame.draw.circle(screen, current_color, (x, y), brush_size)

        elif mode == "eraser":
            pygame.draw.circle(screen, WHITE, (x, y), brush_size ** 2)

    # Draw color palette (top bar)
    for i, color in enumerate(colors):
        pygame.draw.rect(screen, color, (i * 50, 0, 50, 50))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()