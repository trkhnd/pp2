import pygame
import os
from datetime import datetime
from tools import draw_shape, flood_fill


pygame.init()

WIDTH = 1000
HEIGHT = 700
TOOLBAR_HEIGHT = 90

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS2 Paint Application")

clock = pygame.time.Clock()

canvas = pygame.Surface((WIDTH, HEIGHT - TOOLBAR_HEIGHT))
canvas.fill((255, 255, 255))

font = pygame.font.SysFont("Arial", 18)
text_font = pygame.font.SysFont("Arial", 32)

current_tool = "pencil"
current_color = (0, 0, 0)
brush_size = 5

drawing = False
start_pos = None
last_pos = None

text_mode = False
text_position = None
text_value = ""

tools = [
    "pencil",
    "line",
    "rectangle",
    "circle",
    "square",
    "right_triangle",
    "equilateral_triangle",
    "rhombus",
    "eraser",
    "fill",
    "text"
]

colors = [
    (0, 0, 0),
    (255, 0, 0),
    (0, 180, 0),
    (0, 0, 255),
    (255, 255, 0),
    (255, 165, 0),
    (128, 0, 128),
    (255, 255, 255)
]

tool_buttons = []
color_buttons = []
size_buttons = []


def canvas_mouse_pos(pos):
    x, y = pos
    return x, y - TOOLBAR_HEIGHT


def is_on_canvas(pos):
    x, y = pos
    return 0 <= x < WIDTH and TOOLBAR_HEIGHT <= y < HEIGHT


def save_canvas():
    if not os.path.exists("saves"):
        os.makedirs("saves")

    time_name = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"saves/paint_{time_name}.png"
    pygame.image.save(canvas, filename)
    print(f"Saved: {filename}")


def draw_button(rect, text, active=False):
    if active:
        color = (180, 220, 255)
    else:
        color = (220, 220, 220)

    pygame.draw.rect(screen, color, rect)
    pygame.draw.rect(screen, (0, 0, 0), rect, 2)

    label = font.render(text, True, (0, 0, 0))
    label_rect = label.get_rect(center=rect.center)
    screen.blit(label, label_rect)


def draw_toolbar():
    global tool_buttons, color_buttons, size_buttons

    screen.fill((200, 200, 200), (0, 0, WIDTH, TOOLBAR_HEIGHT))

    tool_buttons = []
    x = 10
    y = 10

    for tool in tools:
        rect = pygame.Rect(x, y, 80, 30)
        tool_buttons.append((rect, tool))

        short_name = tool.replace("_", " ")[:10]
        draw_button(rect, short_name, current_tool == tool)

        x += 85
        if x + 80 > WIDTH:
            x = 10
            y += 35

    color_buttons = []
    x = 10
    y = 55

    for color in colors:
        rect = pygame.Rect(x, y, 30, 25)
        color_buttons.append((rect, color))

        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, (0, 0, 0), rect, 2)

        if current_color == color:
            pygame.draw.rect(screen, (255, 0, 0), rect, 4)

        x += 35

    size_buttons = []

    sizes = [
        (2, "S"),
        (5, "M"),
        (10, "L")
    ]

    x = 330
    y = 55

    for size, name in sizes:
        rect = pygame.Rect(x, y, 40, 25)
        size_buttons.append((rect, size))
        draw_button(rect, name, brush_size == size)
        x += 45

    info = f"Tool: {current_tool} | Size: {brush_size}px | Ctrl+S: Save | 1/2/3: Brush size"
    info_text = font.render(info, True, (0, 0, 0))
    screen.blit(info_text, (470, 60))


def handle_toolbar_click(pos):
    global current_tool, current_color, brush_size, text_mode, text_value

    for rect, tool in tool_buttons:
        if rect.collidepoint(pos):
            current_tool = tool
            text_mode = False
            text_value = ""
            return True

    for rect, color in color_buttons:
        if rect.collidepoint(pos):
            current_color = color
            return True

    for rect, size in size_buttons:
        if rect.collidepoint(pos):
            brush_size = size
            return True

    return False


running = True

while running:
    screen.fill((255, 255, 255))
    screen.blit(canvas, (0, TOOLBAR_HEIGHT))

    preview_surface = canvas.copy()

    if drawing and start_pos is not None and last_pos is not None:
        if current_tool == "line":
            pygame.draw.line(preview_surface, current_color, start_pos, last_pos, brush_size)

        elif current_tool in [
            "rectangle",
            "circle",
            "square",
            "right_triangle",
            "equilateral_triangle",
            "rhombus"
        ]:
            draw_shape(preview_surface, current_tool, start_pos, last_pos, current_color, brush_size)

    screen.blit(preview_surface, (0, TOOLBAR_HEIGHT))

    if text_mode and text_position is not None:
        text_surface = text_font.render(text_value + "|", True, current_color)
        tx, ty = text_position
        screen.blit(text_surface, (tx, ty + TOOLBAR_HEIGHT))

    draw_toolbar()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()

            if keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]:
                if event.key == pygame.K_s:
                    save_canvas()

            if event.key == pygame.K_1:
                brush_size = 2

            elif event.key == pygame.K_2:
                brush_size = 5

            elif event.key == pygame.K_3:
                brush_size = 10

            if text_mode:
                if event.key == pygame.K_RETURN:
                    if text_value != "":
                        final_text = text_font.render(text_value, True, current_color)
                        canvas.blit(final_text, text_position)

                    text_mode = False
                    text_value = ""
                    text_position = None

                elif event.key == pygame.K_ESCAPE:
                    text_mode = False
                    text_value = ""
                    text_position = None

                elif event.key == pygame.K_BACKSPACE:
                    text_value = text_value[:-1]

                else:
                    text_value += event.unicode

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if event.pos[1] < TOOLBAR_HEIGHT:
                    handle_toolbar_click(event.pos)

                elif is_on_canvas(event.pos):
                    pos = canvas_mouse_pos(event.pos)

                    if current_tool == "fill":
                        flood_fill(canvas, pos, current_color)

                    elif current_tool == "text":
                        text_mode = True
                        text_position = pos
                        text_value = ""

                    else:
                        drawing = True
                        start_pos = pos
                        last_pos = pos

        if event.type == pygame.MOUSEMOTION:
            if drawing and is_on_canvas(event.pos):
                pos = canvas_mouse_pos(event.pos)

                if current_tool == "pencil":
                    pygame.draw.line(canvas, current_color, last_pos, pos, brush_size)
                    last_pos = pos

                elif current_tool == "eraser":
                    pygame.draw.line(canvas, (255, 255, 255), last_pos, pos, brush_size)
                    last_pos = pos

                else:
                    last_pos = pos

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and drawing:
                if is_on_canvas(event.pos):
                    end_pos = canvas_mouse_pos(event.pos)

                    if current_tool == "line":
                        pygame.draw.line(canvas, current_color, start_pos, end_pos, brush_size)

                    elif current_tool in [
                        "rectangle",
                        "circle",
                        "square",
                        "right_triangle",
                        "equilateral_triangle",
                        "rhombus"
                    ]:
                        draw_shape(canvas, current_tool, start_pos, end_pos, current_color, brush_size)

                drawing = False
                start_pos = None
                last_pos = None

    pygame.display.update()
    clock.tick(60)

pygame.quit()