import pygame


pygame.font.init()

FONT_SMALL = pygame.font.SysFont("Arial", 24)
FONT_MEDIUM = pygame.font.SysFont("Arial", 32)
FONT_BIG = pygame.font.SysFont("Arial", 52)


class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse_pos):
            color = (180, 220, 255)
        else:
            color = (220, 220, 220)

        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        pygame.draw.rect(screen, (30, 30, 30), self.rect, 3, border_radius=10)

        label = FONT_MEDIUM.render(self.text, True, (0, 0, 0))
        label_rect = label.get_rect(center=self.rect.center)
        screen.blit(label, label_rect)

    def is_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos)


def draw_text(screen, text, x, y, size="small", color=(255, 255, 255), center=False):
    if size == "big":
        font = FONT_BIG
    elif size == "medium":
        font = FONT_MEDIUM
    else:
        font = FONT_SMALL

    surface = font.render(str(text), True, color)

    if center:
        rect = surface.get_rect(center=(x, y))
        screen.blit(surface, rect)
    else:
        screen.blit(surface, (x, y))


def draw_panel(screen, rect, color=(35, 35, 45)):
    pygame.draw.rect(screen, color, rect, border_radius=15)
    pygame.draw.rect(screen, (255, 255, 255), rect, 3, border_radius=15)