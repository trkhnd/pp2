import pygame
from ball import Ball


def main():
    pygame.init()

    width, height = 800, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Moving Ball Game")

    clock = pygame.time.Clock()
    ball = Ball(
        x=width // 2,
        y=height // 2,
        radius=25,
        screen_width=width,
        screen_height=height
    )

    running = True
    while running:
        screen.fill((255, 255, 255))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    ball.move_up()
                elif event.key == pygame.K_DOWN:
                    ball.move_down()
                elif event.key == pygame.K_LEFT:
                    ball.move_left()
                elif event.key == pygame.K_RIGHT:
                    ball.move_right()

        ball.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()