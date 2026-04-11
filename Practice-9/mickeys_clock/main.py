import pygame
from clock import MickeyClock

pygame.init()
pygame.font.init()

WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mickey Mouse Clock")

clock = pygame.time.Clock()

# Load and scale hand image
hand_img = pygame.image.load("images/mickey_hand.png").convert_alpha()
hand_img = pygame.transform.scale(hand_img, (50, 200))

mickey_clock = MickeyClock(screen, hand_img)

running = True
while running:
    screen.fill((255, 255, 255))  # white background

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    mickey_clock.draw()

    pygame.display.flip()
    clock.tick(1)  # update every second

pygame.quit()