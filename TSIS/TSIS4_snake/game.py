import pygame
import random
import os

from config import WIDTH, HEIGHT, CELL_SIZE, GAME_TOP, GRID_WIDTH, GRID_HEIGHT


class SnakeGame:
    def __init__(self, username, personal_best, settings):
        self.username = username
        self.personal_best = personal_best
        self.settings = settings

        self.snake = [(10, 10), (9, 10), (8, 10)]
        self.direction = (1, 0)
        self.next_direction = (1, 0)

        self.score = 0
        self.level = 1
        self.food_eaten = 0

        self.base_speed = 8
        self.speed = self.base_speed

        self.game_over = False
        self.game_over_sound_played = False

        self.normal_food = None
        self.poison_food = None
        self.powerup = None

        self.food_spawn_time = 0
        self.poison_spawn_time = 0
        self.powerup_spawn_time = 0

        self.food_lifetime = 7000
        self.poison_lifetime = 7000
        self.powerup_lifetime = 8000

        self.active_powerup = None
        self.active_powerup_end = 0
        self.shield = False

        self.obstacles = []

        self.font = pygame.font.SysFont("Arial", 24)
        self.big_font = pygame.font.SysFont("Arial", 42)

        self.sounds = {}
        self.load_sounds()

        self.spawn_food()
        self.spawn_poison()
        self.spawn_powerup()

    def load_sounds(self):
        if not self.settings["sound"]:
            return

        try:
            pygame.mixer.init()

            if os.path.exists("assets/eat.wav"):
                self.sounds["eat"] = pygame.mixer.Sound("assets/eat.wav")

            if os.path.exists("assets/powerup.wav"):
                self.sounds["powerup"] = pygame.mixer.Sound("assets/powerup.wav")

            if os.path.exists("assets/gameover.wav"):
                self.sounds["gameover"] = pygame.mixer.Sound("assets/gameover.wav")

        except Exception as e:
            print("Sound loading error:", e)
            self.sounds = {}

    def play_sound(self, name):
        if not self.settings["sound"]:
            return

        if name in self.sounds:
            self.sounds[name].play()

    def set_game_over(self):
        if not self.game_over_sound_played:
            self.play_sound("gameover")
            self.game_over_sound_played = True

        self.game_over = True

    def random_empty_cell(self):
        while True:
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
            pos = (x, y)

            if (
                pos not in self.snake
                and pos not in self.obstacles
                and pos != self.normal_food
                and pos != self.poison_food
            ):
                if self.powerup is not None:
                    if pos == self.powerup["pos"]:
                        continue

                return pos

    def spawn_food(self):
        self.normal_food = self.random_empty_cell()
        self.food_value = random.choice([1, 1, 1, 2, 3])
        self.food_spawn_time = pygame.time.get_ticks()

    def spawn_poison(self):
        self.poison_food = self.random_empty_cell()
        self.poison_spawn_time = pygame.time.get_ticks()

    def spawn_powerup(self):
        if self.powerup is not None:
            return

        pos = self.random_empty_cell()
        kind = random.choice(["speed", "slow", "shield"])

        self.powerup = {
            "pos": pos,
            "type": kind
        }

        self.powerup_spawn_time = pygame.time.get_ticks()

    def generate_obstacles(self):
        self.obstacles = []

        if self.level < 3:
            return

        amount = min(5 + self.level * 2, 25)

        head = self.snake[0]

        protected_cells = [
            head,
            (head[0] + 1, head[1]),
            (head[0] - 1, head[1]),
            (head[0], head[1] + 1),
            (head[0], head[1] - 1)
        ]

        attempts = 0

        while len(self.obstacles) < amount and attempts < 500:
            attempts += 1

            x = random.randint(1, GRID_WIDTH - 2)
            y = random.randint(1, GRID_HEIGHT - 2)
            pos = (x, y)

            if pos in self.snake:
                continue

            if pos in protected_cells:
                continue

            if pos in self.obstacles:
                continue

            if pos == self.normal_food or pos == self.poison_food:
                continue

            if self.powerup is not None and pos == self.powerup["pos"]:
                continue

            self.obstacles.append(pos)

    def change_direction(self, new_direction):
        dx, dy = new_direction
        current_dx, current_dy = self.direction

        if (dx, dy) == (-current_dx, -current_dy):
            return

        self.next_direction = new_direction

    def apply_powerup(self, power_type):
        now = pygame.time.get_ticks()

        if power_type == "speed":
            self.active_powerup = "speed"
            self.active_powerup_end = now + 5000
            self.speed = self.base_speed + 5

        elif power_type == "slow":
            self.active_powerup = "slow"
            self.active_powerup_end = now + 5000
            self.speed = max(4, self.base_speed - 4)

        elif power_type == "shield":
            self.active_powerup = "shield"
            self.shield = True

    def update_powerup_timer(self):
        now = pygame.time.get_ticks()

        if self.active_powerup in ["speed", "slow"]:
            if now >= self.active_powerup_end:
                self.active_powerup = None
                self.speed = self.base_speed

    def update(self):
        if self.game_over:
            return

        now = pygame.time.get_ticks()

        self.update_powerup_timer()

        if now - self.food_spawn_time > self.food_lifetime:
            self.spawn_food()

        if now - self.poison_spawn_time > self.poison_lifetime:
            self.spawn_poison()

        if self.powerup is None:
            if random.randint(1, 180) == 1:
                self.spawn_powerup()
        else:
            if now - self.powerup_spawn_time > self.powerup_lifetime:
                self.powerup = None

        self.direction = self.next_direction

        head_x, head_y = self.snake[0]
        dx, dy = self.direction

        new_head = (head_x + dx, head_y + dy)

        out_of_bounds = (
            new_head[0] < 0
            or new_head[0] >= GRID_WIDTH
            or new_head[1] < 0
            or new_head[1] >= GRID_HEIGHT
        )

        hit_self = new_head in self.snake
        hit_obstacle = new_head in self.obstacles

        if out_of_bounds or hit_self or hit_obstacle:
            if self.shield:
                self.shield = False
                self.active_powerup = None
                self.play_sound("powerup")
                return
            else:
                self.set_game_over()
                return

        self.snake.insert(0, new_head)

        if new_head == self.normal_food:
            self.play_sound("eat")

            self.score += self.food_value * 10
            self.food_eaten += 1

            if self.food_eaten % 3 == 0:
                self.level += 1
                self.base_speed += 1
                self.speed = self.base_speed
                self.generate_obstacles()

            self.spawn_food()

        elif new_head == self.poison_food:
            self.play_sound("eat")

            self.score = max(0, self.score - 10)

            for _ in range(2):
                if len(self.snake) > 0:
                    self.snake.pop()

            if len(self.snake) <= 1:
                self.set_game_over()
                return

            self.spawn_poison()

        elif self.powerup is not None and new_head == self.powerup["pos"]:
            self.play_sound("powerup")

            self.apply_powerup(self.powerup["type"])
            self.score += 25
            self.powerup = None
            self.snake.pop()

        else:
            self.snake.pop()

    def draw_cell(self, screen, pos, color):
        x, y = pos

        rect = pygame.Rect(
            x * CELL_SIZE,
            GAME_TOP + y * CELL_SIZE,
            CELL_SIZE,
            CELL_SIZE
        )

        pygame.draw.rect(screen, color, rect)

    def draw_grid(self, screen):
        if not self.settings["grid"]:
            return

        for x in range(0, WIDTH, CELL_SIZE):
            pygame.draw.line(
                screen,
                (45, 45, 45),
                (x, GAME_TOP),
                (x, HEIGHT)
            )

        for y in range(GAME_TOP, HEIGHT, CELL_SIZE):
            pygame.draw.line(
                screen,
                (45, 45, 45),
                (0, y),
                (WIDTH, y)
            )

    def draw(self, screen):
        screen.fill((20, 20, 25))

        pygame.draw.rect(screen, (30, 30, 40), (0, 0, WIDTH, GAME_TOP))

        hud_lines = [
            f"Player: {self.username}",
            f"Score: {self.score}",
            f"Level: {self.level}",
            f"Best: {self.personal_best}"
        ]

        x = 15

        for line in hud_lines:
            text = self.font.render(line, True, (255, 255, 255))
            screen.blit(text, (x, 20))
            x += 180

        if self.active_powerup == "speed":
            power_text = "Power: Speed Boost"

        elif self.active_powerup == "slow":
            power_text = "Power: Slow Motion"

        elif self.active_powerup == "shield":
            power_text = "Power: Shield"

        else:
            power_text = "Power: None"

        text = self.font.render(power_text, True, (255, 255, 0))
        screen.blit(text, (15, 52))

        self.draw_grid(screen)

        for obstacle in self.obstacles:
            self.draw_cell(screen, obstacle, (110, 110, 110))

        if self.normal_food:
            if self.food_value == 1:
                color = (255, 60, 60)
            elif self.food_value == 2:
                color = (255, 180, 40)
            else:
                color = (255, 240, 40)

            self.draw_cell(screen, self.normal_food, color)

        if self.poison_food:
            self.draw_cell(screen, self.poison_food, (120, 0, 0))

        if self.powerup:
            if self.powerup["type"] == "speed":
                color = (0, 200, 255)
            elif self.powerup["type"] == "slow":
                color = (160, 80, 255)
            else:
                color = (80, 120, 255)

            self.draw_cell(screen, self.powerup["pos"], color)

        snake_color = tuple(self.settings["snake_color"])

        for index, segment in enumerate(self.snake):
            if index == 0:
                self.draw_cell(screen, segment, (0, 255, 120))
            else:
                self.draw_cell(screen, segment, snake_color)

        pygame.draw.rect(
            screen,
            (255, 255, 255),
            (0, GAME_TOP, WIDTH, HEIGHT - GAME_TOP),
            3
        )