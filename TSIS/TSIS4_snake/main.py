import pygame
import sys
import json
import os

from config import WIDTH, HEIGHT
from game import SnakeGame
from db import create_tables, save_game_result, get_top_scores, get_personal_best


pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS4 Snake Game")

clock = pygame.time.Clock()

FONT_SMALL = pygame.font.SysFont("Arial", 24)
FONT_MEDIUM = pygame.font.SysFont("Arial", 32)
FONT_BIG = pygame.font.SysFont("Arial", 52)

SETTINGS_FILE = "settings.json"

DEFAULT_SETTINGS = {
    "snake_color": [0, 220, 80],
    "grid": True,
    "sound": True
}


def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS.copy()

    with open(SETTINGS_FILE, "r") as file:
        data = json.load(file)

    settings = DEFAULT_SETTINGS.copy()
    settings.update(data)
    return settings


def save_settings(settings):
    with open(SETTINGS_FILE, "w") as file:
        json.dump(settings, file, indent=4)


settings = load_settings()


class Button:
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text

    def draw(self):
        mouse = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse):
            color = (190, 220, 255)
        else:
            color = (220, 220, 220)

        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        pygame.draw.rect(screen, (20, 20, 20), self.rect, 3, border_radius=10)

        label = FONT_MEDIUM.render(self.text, True, (0, 0, 0))
        label_rect = label.get_rect(center=self.rect.center)
        screen.blit(label, label_rect)

    def clicked(self, event):
        return (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.rect.collidepoint(event.pos)
        )


def draw_text(text, x, y, font, color=(255, 255, 255), center=False):
    surface = font.render(str(text), True, color)

    if center:
        rect = surface.get_rect(center=(x, y))
        screen.blit(surface, rect)
    else:
        screen.blit(surface, (x, y))


play_button = Button(300, 220, 200, 55, "Play")
leaderboard_button = Button(300, 295, 200, 55, "Leaderboard")
settings_button = Button(300, 370, 200, 55, "Settings")
quit_button = Button(300, 445, 200, 55, "Quit")

retry_button = Button(270, 430, 260, 55, "Retry")
menu_button = Button(270, 505, 260, 55, "Main Menu")
back_button = Button(300, 590, 200, 55, "Back")

grid_button = Button(270, 220, 260, 55, "Grid")
sound_button = Button(270, 300, 260, 55, "Sound")
color_button = Button(270, 380, 260, 55, "Snake Color")
save_back_button = Button(270, 500, 260, 55, "Save & Back")

state = "name"
username = ""
game = None
personal_best = 0
result_saved = False

colors = [
    [0, 220, 80],
    [0, 180, 255],
    [255, 80, 80],
    [255, 220, 40],
    [180, 80, 255]
]


def start_game():
    global game, personal_best, result_saved

    personal_best = get_personal_best(username)
    game = SnakeGame(username, personal_best, settings)
    result_saved = False


def draw_name_screen():
    screen.fill((25, 25, 35))

    draw_text("TSIS4 SNAKE", WIDTH // 2, 130, FONT_BIG, center=True)
    draw_text("Enter username:", WIDTH // 2, 250, FONT_MEDIUM, center=True)

    input_rect = pygame.Rect(250, 310, 300, 55)

    pygame.draw.rect(screen, (255, 255, 255), input_rect, border_radius=10)
    pygame.draw.rect(screen, (0, 0, 0), input_rect, 3, border_radius=10)

    draw_text(username + "|", WIDTH // 2, 338, FONT_MEDIUM, (0, 0, 0), center=True)
    draw_text("Press ENTER to continue", WIDTH // 2, 410, FONT_SMALL, center=True)


def draw_menu():
    screen.fill((25, 25, 35))

    draw_text("SNAKE GAME", WIDTH // 2, 120, FONT_BIG, center=True)
    draw_text(f"Player: {username}", WIDTH // 2, 170, FONT_MEDIUM, center=True)

    play_button.draw()
    leaderboard_button.draw()
    settings_button.draw()
    quit_button.draw()


def draw_leaderboard():
    screen.fill((25, 25, 35))

    draw_text("TOP 10 LEADERBOARD", WIDTH // 2, 70, FONT_BIG, center=True)

    draw_text("Rank", 80, 140, FONT_SMALL)
    draw_text("Name", 160, 140, FONT_SMALL)
    draw_text("Score", 340, 140, FONT_SMALL)
    draw_text("Level", 470, 140, FONT_SMALL)
    draw_text("Date", 570, 140, FONT_SMALL)

    try:
        rows = get_top_scores()
    except Exception as e:
        draw_text("Database error. Check PostgreSQL connection.", WIDTH // 2, 300, FONT_MEDIUM, center=True)
        draw_text(str(e)[:70], WIDTH // 2, 350, FONT_SMALL, center=True)
        rows = []

    y = 190

    for i, row in enumerate(rows):
        name, score, level, played_at = row
        date_text = str(played_at).split(".")[0]

        draw_text(i + 1, 90, y, FONT_SMALL)
        draw_text(name, 160, y, FONT_SMALL)
        draw_text(score, 350, y, FONT_SMALL)
        draw_text(level, 485, y, FONT_SMALL)
        draw_text(date_text[:16], 570, y, FONT_SMALL)

        y += 35

    back_button.draw()


def draw_settings():
    screen.fill((25, 25, 35))

    draw_text("SETTINGS", WIDTH // 2, 100, FONT_BIG, center=True)

    grid_button.text = f"Grid: {'ON' if settings['grid'] else 'OFF'}"
    sound_button.text = f"Sound: {'ON' if settings['sound'] else 'OFF'}"
    color_button.text = f"Color: {settings['snake_color']}"

    grid_button.draw()
    sound_button.draw()
    color_button.draw()
    save_back_button.draw()


def draw_game_over():
    screen.fill((25, 25, 35))

    draw_text("GAME OVER", WIDTH // 2, 100, FONT_BIG, center=True)

    draw_text(f"Player: {username}", WIDTH // 2, 190, FONT_MEDIUM, center=True)
    draw_text(f"Final Score: {game.score}", WIDTH // 2, 245, FONT_MEDIUM, center=True)
    draw_text(f"Level Reached: {game.level}", WIDTH // 2, 300, FONT_MEDIUM, center=True)
    draw_text(f"Personal Best: {max(personal_best, game.score)}", WIDTH // 2, 355, FONT_MEDIUM, center=True)

    retry_button.draw()
    menu_button.draw()


try:
    create_tables()
except Exception as e:
    print("Database connection error:")
    print(e)


running = True

while running:
    if state == "game" and game:
        game.update()

        if game.game_over and not result_saved:
            try:
                save_game_result(username, game.score, game.level)
            except Exception as e:
                print("Could not save result:")
                print(e)

            result_saved = True
            state = "game_over"

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if state == "name":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if username.strip() != "":
                        state = "menu"

                elif event.key == pygame.K_BACKSPACE:
                    username = username[:-1]

                else:
                    if event.unicode.isprintable() and len(username) < 12:
                        username += event.unicode

        elif state == "menu":
            if play_button.clicked(event):
                start_game()
                state = "game"

            elif leaderboard_button.clicked(event):
                state = "leaderboard"

            elif settings_button.clicked(event):
                state = "settings"

            elif quit_button.clicked(event):
                running = False

        elif state == "leaderboard":
            if back_button.clicked(event):
                state = "menu"

        elif state == "settings":
            if grid_button.clicked(event):
                settings["grid"] = not settings["grid"]

            elif sound_button.clicked(event):
                settings["sound"] = not settings["sound"]

            elif color_button.clicked(event):
                index = colors.index(settings["snake_color"])
                index = (index + 1) % len(colors)
                settings["snake_color"] = colors[index]

            elif save_back_button.clicked(event):
                save_settings(settings)
                state = "menu"

        elif state == "game":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    game.change_direction((0, -1))

                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    game.change_direction((0, 1))

                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    game.change_direction((-1, 0))

                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    game.change_direction((1, 0))

                elif event.key == pygame.K_ESCAPE:
                    state = "menu"

        elif state == "game_over":
            if retry_button.clicked(event):
                start_game()
                state = "game"

            elif menu_button.clicked(event):
                state = "menu"

    if state == "name":
        draw_name_screen()

    elif state == "menu":
        draw_menu()

    elif state == "leaderboard":
        draw_leaderboard()

    elif state == "settings":
        draw_settings()

    elif state == "game":
        game.draw(screen)

    elif state == "game_over":
        draw_game_over()

    pygame.display.update()

    if state == "game" and game:
        clock.tick(game.speed)
    else:
        clock.tick(60)

pygame.quit()
sys.exit()