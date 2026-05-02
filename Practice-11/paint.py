import pygame
import sys
import math

pygame.init()

# -----------------------------
# Screen settings
# -----------------------------
WIDTH = 900
HEIGHT = 650
TOOLBAR_HEIGHT = 90

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Practice 11 Paint")

clock = pygame.time.Clock()
FPS = 60

# -----------------------------
# Colors
# -----------------------------
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (210, 210, 210)
LIGHT_BLUE = (180, 220, 255)

colors = [
    BLACK,
    (255, 0, 0),
    (0, 180, 0),
    (0, 0, 255),
    (255, 255, 0),
    (255, 165, 0),
    (128, 0, 128),
    WHITE
]

# -----------------------------
# Canvas
# -----------------------------
canvas = pygame.Surface((WIDTH, HEIGHT - TOOLBAR_HEIGHT))
canvas.fill(WHITE)

# -----------------------------
# Fonts
# -----------------------------
font = pygame.font.SysFont("Arial", 18)

# -----------------------------
# Drawing variables
# -----------------------------
current_tool = "pencil"
current_color = BLACK
brush_size = 4

drawing = False
start_pos = None
last_pos = None

# -----------------------------
# Tools
# -----------------------------
tools = [
    "pencil",
    "rectangle",
    "circle",
    "eraser",
    "square",
    "right_triangle",
    "equilateral_triangle",
    "rhombus"
]

tool_buttons = []
color_buttons = []


def canvas_mouse_pos(pos):
    """
    Converts screen mouse position to canvas position.
    We subtract toolbar height because canvas starts below toolbar.
    """
    x, y = pos
    return x, y - TOOLBAR_HEIGHT


def is_on_canvas(pos):
    """
    Checks whether the mouse is inside the canvas area.
    """
    x, y = pos
    return 0 <= x < WIDTH and TOOLBAR_HEIGHT <= y < HEIGHT


def draw_button(rect, text, active=False):
    """
    Draws one toolbar button.
    Active button becomes blue.
    """
    color = LIGHT_BLUE if active else GRAY

    pygame.draw.rect(screen, color, rect)
    pygame.draw.rect(screen, BLACK, rect, 2)

    label = font.render(text, True, BLACK)
    label_rect = label.get_rect(center=rect.center)
    screen.blit(label, label_rect)


def draw_toolbar():
    """
    Draws toolbar with tool buttons and color buttons.
    """
    global tool_buttons, color_buttons

    # Toolbar background
    pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, TOOLBAR_HEIGHT))

    # Draw tool buttons
    tool_buttons = []
    x = 10
    y = 10

    for tool in tools:
        rect = pygame.Rect(x, y, 95, 30)
        tool_buttons.append((rect, tool))

        short_name = tool.replace("_", " ")[:12]
        draw_button(rect, short_name, current_tool == tool)

        x += 100

        if x + 95 > WIDTH:
            x = 10
            y += 35

    # Draw color buttons
    color_buttons = []
    x = 10
    y = 55

    for color in colors:
        rect = pygame.Rect(x, y, 30, 25)
        color_buttons.append((rect, color))

        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, BLACK, rect, 2)

        # Highlight selected color
        if current_color == color:
            pygame.draw.rect(screen, (255, 0, 0), rect, 4)

        x += 35

    info = f"Tool: {current_tool} | Brush: {brush_size}"
    info_text = font.render(info, True, BLACK)
    screen.blit(info_text, (330, 60))


def handle_toolbar_click(pos):
    """
    Checks if user clicked a tool button or color button.
    """
    global current_tool, current_color

    # Tool selection
    for rect, tool in tool_buttons:
        if rect.collidepoint(pos):
            current_tool = tool
            return True

    # Color selection
    for rect, color in color_buttons:
        if rect.collidepoint(pos):
            current_color = color
            return True

    return False


def draw_shape(surface, tool, start, end, color, thickness):
    """
    Draws selected shape using start and end mouse positions.
    """
    x1, y1 = start
    x2, y2 = end

    left = min(x1, x2)
    top = min(y1, y2)
    width = abs(x2 - x1)
    height = abs(y2 - y1)

    if width == 0 or height == 0:
        return

    # Rectangle
    if tool == "rectangle":
        pygame.draw.rect(surface, color, (left, top, width, height), thickness)

    # Circle
    elif tool == "circle":
        radius = max(width, height) // 2
        pygame.draw.circle(surface, color, start, radius, thickness)

    # Square
    elif tool == "square":
        side = min(width, height)

        if x2 < x1:
            left = x1 - side
        else:
            left = x1

        if y2 < y1:
            top = y1 - side
        else:
            top = y1

        pygame.draw.rect(surface, color, (left, top, side, side), thickness)

    # Right triangle
    elif tool == "right_triangle":
        points = [
            (x1, y1),
            (x1, y2),
            (x2, y2)
        ]
        pygame.draw.polygon(surface, color, points, thickness)

    # Equilateral-like triangle
    elif tool == "equilateral_triangle":
        points = [
            ((x1 + x2) // 2, y1),
            (x1, y2),
            (x2, y2)
        ]
        pygame.draw.polygon(surface, color, points, thickness)

    # Rhombus
    elif tool == "rhombus":
        points = [
            ((x1 + x2) // 2, y1),
            (x2, (y1 + y2) // 2),
            ((x1 + x2) // 2, y2),
            (x1, (y1 + y2) // 2)
        ]
        pygame.draw.polygon(surface, color, points, thickness)


running = True

while running:
    screen.fill(WHITE)

    # Make a temporary copy for live preview
    preview = canvas.copy()

    # Live preview for shape tools
    if drawing and start_pos is not None and last_pos is not None:
        if current_tool in [
            "rectangle",
            "circle",
            "square",
            "right_triangle",
            "equilateral_triangle",
            "rhombus"
        ]:
            draw_shape(preview, current_tool, start_pos, last_pos, current_color, brush_size)

    # Draw canvas under toolbar
    screen.blit(preview, (0, TOOLBAR_HEIGHT))

    # Draw toolbar on top
    draw_toolbar()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Keyboard shortcuts for brush size
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                brush_size = 2
            elif event.key == pygame.K_2:
                brush_size = 4
            elif event.key == pygame.K_3:
                brush_size = 8

        # Mouse pressed
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if event.pos[1] < TOOLBAR_HEIGHT:
                    handle_toolbar_click(event.pos)

                elif is_on_canvas(event.pos):
                    drawing = True
                    start_pos = canvas_mouse_pos(event.pos)
                    last_pos = start_pos

        # Mouse movement
        if event.type == pygame.MOUSEMOTION:
            if drawing and is_on_canvas(event.pos):
                pos = canvas_mouse_pos(event.pos)

                # Pencil draws immediately
                if current_tool == "pencil":
                    pygame.draw.line(canvas, current_color, last_pos, pos, brush_size)
                    last_pos = pos

                # Eraser draws white line
                elif current_tool == "eraser":
                    pygame.draw.line(canvas, WHITE, last_pos, pos, brush_size * 2)
                    last_pos = pos

                # Shapes only update preview position
                else:
                    last_pos = pos

        # Mouse released
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and drawing:
                if is_on_canvas(event.pos):
                    end_pos = canvas_mouse_pos(event.pos)

                    # Draw final shape on real canvas
                    if current_tool in [
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
    clock.tick(FPS)

pygame.quit()
sys.exit()