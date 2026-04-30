import pygame
from collections import deque


def draw_shape(surface, tool, start_pos, end_pos, color, brush_size):
    x1, y1 = start_pos
    x2, y2 = end_pos

    left = min(x1, x2)
    top = min(y1, y2)
    width = abs(x2 - x1)
    height = abs(y2 - y1)

    if width == 0 or height == 0:
        return

    if tool == "rectangle":
        pygame.draw.rect(surface, color, (left, top, width, height), brush_size)

    elif tool == "circle":
        radius = max(width, height) // 2
        center = (x1, y1)
        pygame.draw.circle(surface, color, center, radius, brush_size)

    elif tool == "square":
        side = min(width, height)
        rect = pygame.Rect(left, top, side, side)
        pygame.draw.rect(surface, color, rect, brush_size)

    elif tool == "right_triangle":
        points = [
            (x1, y1),
            (x1, y2),
            (x2, y2)
        ]
        pygame.draw.polygon(surface, color, points, brush_size)

    elif tool == "equilateral_triangle":
        points = [
            ((x1 + x2) // 2, y1),
            (x1, y2),
            (x2, y2)
        ]
        pygame.draw.polygon(surface, color, points, brush_size)

    elif tool == "rhombus":
        points = [
            ((x1 + x2) // 2, y1),
            (x2, (y1 + y2) // 2),
            ((x1 + x2) // 2, y2),
            (x1, (y1 + y2) // 2)
        ]
        pygame.draw.polygon(surface, color, points, brush_size)


def flood_fill(surface, start_pos, fill_color):
    width, height = surface.get_size()
    x, y = start_pos

    if x < 0 or x >= width or y < 0 or y >= height:
        return

    target_color = surface.get_at((x, y))
    fill_color = pygame.Color(fill_color)

    if target_color == fill_color:
        return

    queue = deque()
    queue.append((x, y))

    while queue:
        px, py = queue.popleft()

        if px < 0 or px >= width or py < 0 or py >= height:
            continue

        if surface.get_at((px, py)) != target_color:
            continue

        surface.set_at((px, py), fill_color)

        queue.append((px + 1, py))
        queue.append((px - 1, py))
        queue.append((px, py + 1))
        queue.append((px, py - 1))