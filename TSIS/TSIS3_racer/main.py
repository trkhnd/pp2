import pygame
import sys

from racer import RacerGame
from ui import Button, draw_text, draw_panel
from persistence import load_settings, save_settings, load_leaderboard, add_score


pygame.init()

WIDTH = 800
HEIGHT = 700

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS3 Racer Game")

clock = pygame.time.Clock()

settings = load_settings()

state = "name"
username = ""
game = None
last_result = None

play_button = Button(300, 220, 200, 55, "Play")
leaderboard_button = Button(300, 295, 200, 55, "Leaderboard")
settings_button = Button(300, 370, 200, 55, "Settings")
quit_button = Button(300, 445, 200, 55, "Quit")

retry_button = Button(270, 430, 260, 55, "Retry")
main_menu_button = Button(270, 505, 260, 55, "Main Menu")
back_button = Button(300, 590, 200, 55, "Back")

sound_button = Button(270, 210, 260, 50, "Sound")
color_button = Button(270, 290, 260, 50, "Car Color")
difficulty_button = Button(270, 370, 260, 50, "Difficulty")

car_colors = ["blue", "red", "green", "yellow"]
difficulties = ["easy", "normal", "hard"]


def start_new_game():
    global game, last_result
    game = RacerGame(WIDTH, HEIGHT, settings)
    last_result = None


def draw_name_screen():
    screen.fill((25, 25, 35))

    draw_text(screen, "TSIS3 Racer Game", WIDTH // 2, 120, "big", center=True)
    draw_text(screen, "Enter your name:", WIDTH // 2, 250, "medium", center=True)

    input_rect = pygame.Rect(250, 310, 300, 55)
    pygame.draw.rect(screen, (255, 255, 255), input_rect, border_radius=10)
    pygame.draw.rect(screen, (0, 0, 0), input_rect, 3, border_radius=10)

    show_name = username + "|"
    draw_text(screen, show_name, WIDTH // 2, 337, "medium", (0, 0, 0), center=True)

    draw_text(screen, "Press ENTER to continue", WIDTH // 2, 410, "small", center=True)


def draw_main_menu():
    screen.fill((25, 25, 35))

    draw_text(screen, "RACER GAME", WIDTH // 2, 120, "big", center=True)
    draw_text(screen, f"Player: {username}", WIDTH // 2, 170, "medium", center=True)

    play_button.draw(screen)
    leaderboard_button.draw(screen)
    settings_button.draw(screen)
    quit_button.draw(screen)


def draw_leaderboard_screen():
    screen.fill((25, 25, 35))

    draw_text(screen, "TOP 10 LEADERBOARD", WIDTH // 2, 70, "big", center=True)

    panel = pygame.Rect(100, 130, 600, 420)
    draw_panel(screen, panel)

    scores = load_leaderboard()

    draw_text(screen, "Rank", 130, 160, "small")
    draw_text(screen, "Name", 220, 160, "small")
    draw_text(screen, "Score", 390, 160, "small")
    draw_text(screen, "Distance", 520, 160, "small")

    y = 205

    if len(scores) == 0:
        draw_text(screen, "No scores yet.", WIDTH // 2, 330, "medium", center=True)

    for index, item in enumerate(scores):
        rank = index + 1

        draw_text(screen, rank, 140, y, "small")
        draw_text(screen, item["name"], 220, y, "small")
        draw_text(screen, item["score"], 390, y, "small")
        draw_text(screen, f'{item["distance"]}m', 520, y, "small")

        y += 35

    back_button.draw(screen)


def draw_settings_screen():
    screen.fill((25, 25, 35))

    draw_text(screen, "SETTINGS", WIDTH // 2, 100, "big", center=True)

    sound_button.text = f"Sound: {'ON' if settings['sound'] else 'OFF'}"
    color_button.text = f"Car Color: {settings['car_color']}"
    difficulty_button.text = f"Difficulty: {settings['difficulty']}"

    sound_button.draw(screen)
    color_button.draw(screen)
    difficulty_button.draw(screen)
    back_button.draw(screen)

    draw_text(screen, "Settings are saved to settings.json", WIDTH // 2, 500, "small", center=True)


def draw_game_over_screen():
    screen.fill((25, 25, 35))

    if last_result["finished"]:
        title = "FINISH!"
    else:
        title = "GAME OVER"

    draw_text(screen, title, WIDTH // 2, 100, "big", center=True)

    panel = pygame.Rect(230, 170, 340, 220)
    draw_panel(screen, panel)

    draw_text(screen, f"Player: {username}", WIDTH // 2, 210, "medium", center=True)
    draw_text(screen, f"Score: {last_result['score']}", WIDTH // 2, 255, "medium", center=True)
    draw_text(screen, f"Distance: {last_result['distance']}m", WIDTH // 2, 300, "medium", center=True)
    draw_text(screen, f"Coins: {last_result['coins']}", WIDTH // 2, 345, "medium", center=True)

    retry_button.draw(screen)
    main_menu_button.draw(screen)


def save_game_result():
    global last_result

    last_result = {
        "score": game.score,
        "distance": game.distance,
        "coins": game.coins_collected,
        "finished": game.finished
    }

    add_score(username, game.score, game.distance, game.coins_collected)


running = True

while running:
    if state == "game" and game is not None:
        game.update()

        if game.game_over or game.finished:
            save_game_result()
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
            if play_button.is_clicked(event):
                start_new_game()
                state = "game"

            elif leaderboard_button.is_clicked(event):
                state = "leaderboard"

            elif settings_button.is_clicked(event):
                state = "settings"

            elif quit_button.is_clicked(event):
                running = False

        elif state == "leaderboard":
            if back_button.is_clicked(event):
                state = "menu"

        elif state == "settings":
            if sound_button.is_clicked(event):
                settings["sound"] = not settings["sound"]
                save_settings(settings)

            elif color_button.is_clicked(event):
                index = car_colors.index(settings["car_color"])
                index = (index + 1) % len(car_colors)
                settings["car_color"] = car_colors[index]
                save_settings(settings)

            elif difficulty_button.is_clicked(event):
                index = difficulties.index(settings["difficulty"])
                index = (index + 1) % len(difficulties)
                settings["difficulty"] = difficulties[index]
                save_settings(settings)

            elif back_button.is_clicked(event):
                state = "menu"

        elif state == "game":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    game.move_left()

                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    game.move_right()

                elif event.key == pygame.K_ESCAPE:
                    state = "menu"

        elif state == "game_over":
            if retry_button.is_clicked(event):
                start_new_game()
                state = "game"

            elif main_menu_button.is_clicked(event):
                state = "menu"

    if state == "name":
        draw_name_screen()

    elif state == "menu":
        draw_main_menu()

    elif state == "leaderboard":
        draw_leaderboard_screen()

    elif state == "settings":
        draw_settings_screen()

    elif state == "game":
        game.draw(screen)

    elif state == "game_over":
        draw_game_over_screen()

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()