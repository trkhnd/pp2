import pygame
import random
import os


class RacerGame:
    def __init__(self, width, height, settings):
        self.width = width
        self.height = height
        self.settings = settings

        self.road_left = 220
        self.road_width = 360
        self.road_right = self.road_left + self.road_width

        self.lane_count = 4
        self.lane_width = self.road_width // self.lane_count
        self.lanes = []

        for i in range(self.lane_count):
            lane_x = self.road_left + i * self.lane_width + self.lane_width // 2
            self.lanes.append(lane_x)

        self.player_width = 45
        self.player_height = 75

        self.player_lane = 1
        self.player_x = self.lanes[self.player_lane] - self.player_width // 2
        self.player_y = self.height - 120
        self.player_rect = pygame.Rect(
            self.player_x,
            self.player_y,
            self.player_width,
            self.player_height
        )

        self.car_colors = {
            "blue": (40, 120, 255),
            "red": (240, 60, 60),
            "green": (40, 200, 100),
            "yellow": (240, 220, 40)
        }

        self.player_color = self.car_colors.get(
            settings["car_color"],
            (40, 120, 255)
        )

        self.traffic = []
        self.obstacles = []
        self.coins = []
        self.powerups = []
        self.road_events = []

        self.distance = 0
        self.finish_distance = 15000
        self.coins_collected = 0
        self.score = 0

        self.active_powerup = None
        self.powerup_timer = 0
        self.shield_active = False

        self.game_over = False
        self.finished = False

        self.road_offset = 0

        self.spawn_timer_traffic = 0
        self.spawn_timer_obstacle = 0
        self.spawn_timer_coin = 0
        self.spawn_timer_powerup = 0
        self.spawn_timer_event = 0

        self.base_speed = self.get_start_speed()
        self.speed = self.base_speed

        self.font = pygame.font.SysFont("Arial", 24)
        self.big_font = pygame.font.SysFont("Arial", 40)

        self.sounds = {}
        self.load_sounds()

    def load_sounds(self):
        if not self.settings["sound"]:
            return

        try:
            pygame.mixer.init()

            if os.path.exists("assets/coin.wav"):
                self.sounds["coin"] = pygame.mixer.Sound("assets/coin.wav")

            if os.path.exists("assets/crash.wav"):
                self.sounds["crash"] = pygame.mixer.Sound("assets/crash.wav")

            if os.path.exists("assets/powerup.wav"):
                self.sounds["powerup"] = pygame.mixer.Sound("assets/powerup.wav")

        except Exception:
            self.sounds = {}

    def play_sound(self, name):
        if not self.settings["sound"]:
            return

        if name in self.sounds:
            self.sounds[name].play()

    def get_start_speed(self):
        difficulty = self.settings["difficulty"]

        if difficulty == "easy":
            return 4

        if difficulty == "hard":
            return 7

        return 5

    def get_spawn_modifier(self):
        difficulty = self.settings["difficulty"]

        if difficulty == "easy":
            return 1.3

        if difficulty == "hard":
            return 0.75

        return 1.0

    def move_left(self):
        if self.player_lane > 0:
            self.player_lane -= 1
            self.player_x = self.lanes[self.player_lane] - self.player_width // 2
            self.player_rect.x = self.player_x

    def move_right(self):
        if self.player_lane < self.lane_count - 1:
            self.player_lane += 1
            self.player_x = self.lanes[self.player_lane] - self.player_width // 2
            self.player_rect.x = self.player_x

    def safe_lane(self):
        possible = list(range(self.lane_count))

        if random.random() < 0.6:
            if self.player_lane in possible:
                possible.remove(self.player_lane)

        if len(possible) == 0:
            possible = list(range(self.lane_count))

        return random.choice(possible)

    def spawn_traffic(self):
        lane = self.safe_lane()
        x = self.lanes[lane] - 22
        y = -90

        colors = [
            (255, 80, 80),
            (180, 80, 255),
            (255, 160, 60),
            (70, 220, 220)
        ]

        car = {
            "rect": pygame.Rect(x, y, 44, 75),
            "speed": self.speed + random.randint(1, 3),
            "color": random.choice(colors)
        }

        self.traffic.append(car)

    def spawn_obstacle(self):
        lane = self.safe_lane()
        x = self.lanes[lane] - 25
        y = -60

        obstacle_type = random.choice([
            "barrier",
            "oil",
            "pothole",
            "slow_zone"
        ])

        obstacle = {
            "rect": pygame.Rect(x, y, 50, 35),
            "type": obstacle_type,
            "speed": self.speed
        }

        self.obstacles.append(obstacle)

    def spawn_coin(self):
        lane = random.randint(0, self.lane_count - 1)
        x = self.lanes[lane] - 15
        y = -30

        value = random.choice([1, 1, 1, 2, 3])

        coin = {
            "rect": pygame.Rect(x, y, 30, 30),
            "value": value,
            "speed": self.speed
        }

        self.coins.append(coin)

    def spawn_powerup(self):
        if self.active_powerup is not None or self.shield_active:
            return

        lane = random.randint(0, self.lane_count - 1)
        x = self.lanes[lane] - 18
        y = -40

        power_type = random.choice(["nitro", "shield", "repair"])

        powerup = {
            "rect": pygame.Rect(x, y, 36, 36),
            "type": power_type,
            "speed": self.speed,
            "life": 420
        }

        self.powerups.append(powerup)

    def spawn_road_event(self):
        event_type = random.choice([
            "moving_barrier",
            "speed_bump",
            "nitro_strip"
        ])

        if event_type == "moving_barrier":
            lane = random.randint(0, self.lane_count - 1)
            x = self.lanes[lane] - 35

            event = {
                "rect": pygame.Rect(x, -50, 70, 28),
                "type": event_type,
                "speed": self.speed,
                "direction": random.choice([-1, 1])
            }

        elif event_type == "speed_bump":
            lane = random.randint(0, self.lane_count - 1)
            x = self.lanes[lane] - 40

            event = {
                "rect": pygame.Rect(x, -40, 80, 22),
                "type": event_type,
                "speed": self.speed,
                "direction": 0
            }

        else:
            lane = random.randint(0, self.lane_count - 1)
            x = self.lanes[lane] - 35

            event = {
                "rect": pygame.Rect(x, -45, 70, 35),
                "type": event_type,
                "speed": self.speed,
                "direction": 0
            }

        self.road_events.append(event)

    def activate_powerup(self, power_type):
        if power_type == "nitro":
            if self.active_powerup is None and not self.shield_active:
                self.active_powerup = "nitro"
                self.powerup_timer = 300
                self.score += 100

        elif power_type == "shield":
            if self.active_powerup is None and not self.shield_active:
                self.shield_active = True
                self.active_powerup = "shield"
                self.score += 100

        elif power_type == "repair":
            if len(self.obstacles) > 0:
                self.obstacles.pop(0)

            self.score += 150

    def handle_collision(self):
        if self.shield_active:
            self.shield_active = False
            self.active_powerup = None
            self.play_sound("powerup")
            return

        self.play_sound("crash")
        self.game_over = True

    def update_powerup(self):
        if self.active_powerup == "nitro":
            self.speed = self.base_speed + 5
            self.powerup_timer -= 1

            if self.powerup_timer <= 0:
                self.active_powerup = None
                self.speed = self.base_speed

        elif self.active_powerup == "shield":
            self.speed = self.base_speed

        else:
            self.speed = self.base_speed

    def update_difficulty(self):
        progress_bonus = self.distance // 700

        if self.settings["difficulty"] == "easy":
            self.base_speed = 4 + progress_bonus * 0.4

        elif self.settings["difficulty"] == "hard":
            self.base_speed = 7 + progress_bonus * 0.7

        else:
            self.base_speed = 5 + progress_bonus * 0.5

    def update_spawns(self):
        modifier = self.get_spawn_modifier()
        progress = max(1, self.distance // 500)

        traffic_limit = max(25, int((90 - progress * 4) * modifier))
        obstacle_limit = max(35, int((120 - progress * 4) * modifier))
        coin_limit = 55
        powerup_limit = 420
        event_limit = max(130, int((260 - progress * 5) * modifier))

        self.spawn_timer_traffic += 1
        self.spawn_timer_obstacle += 1
        self.spawn_timer_coin += 1
        self.spawn_timer_powerup += 1
        self.spawn_timer_event += 1

        if self.spawn_timer_traffic >= traffic_limit:
            self.spawn_traffic()
            self.spawn_timer_traffic = 0

        if self.spawn_timer_obstacle >= obstacle_limit:
            self.spawn_obstacle()
            self.spawn_timer_obstacle = 0

        if self.spawn_timer_coin >= coin_limit:
            self.spawn_coin()
            self.spawn_timer_coin = 0

        if self.spawn_timer_powerup >= powerup_limit:
            self.spawn_powerup()
            self.spawn_timer_powerup = 0

        if self.spawn_timer_event >= event_limit:
            self.spawn_road_event()
            self.spawn_timer_event = 0

    def update_objects(self):
        for car in self.traffic[:]:
            car["rect"].y += int(car["speed"])

            if car["rect"].top > self.height:
                self.traffic.remove(car)

            elif car["rect"].colliderect(self.player_rect):
                self.handle_collision()
                self.traffic.remove(car)

        for obstacle in self.obstacles[:]:
            obstacle["rect"].y += int(self.speed)

            if obstacle["rect"].top > self.height:
                self.obstacles.remove(obstacle)

            elif obstacle["rect"].colliderect(self.player_rect):
                if obstacle["type"] in ["barrier", "pothole"]:
                    self.handle_collision()
                    self.obstacles.remove(obstacle)

                elif obstacle["type"] in ["oil", "slow_zone"]:
                    self.base_speed = max(3, self.base_speed - 1)
                    self.score = max(0, self.score - 50)
                    self.obstacles.remove(obstacle)

        for coin in self.coins[:]:
            coin["rect"].y += int(self.speed)

            if coin["rect"].top > self.height:
                self.coins.remove(coin)

            elif coin["rect"].colliderect(self.player_rect):
                self.coins_collected += coin["value"]
                self.score += coin["value"] * 50
                self.play_sound("coin")
                self.coins.remove(coin)

        for powerup in self.powerups[:]:
            powerup["rect"].y += int(self.speed)
            powerup["life"] -= 1

            if powerup["rect"].top > self.height or powerup["life"] <= 0:
                self.powerups.remove(powerup)

            elif powerup["rect"].colliderect(self.player_rect):
                self.activate_powerup(powerup["type"])
                self.play_sound("powerup")
                self.powerups.remove(powerup)

        for event in self.road_events[:]:
            event["rect"].y += int(self.speed)

            if event["type"] == "moving_barrier":
                event["rect"].x += event["direction"] * 3

                if event["rect"].left <= self.road_left:
                    event["direction"] = 1

                if event["rect"].right >= self.road_right:
                    event["direction"] = -1

            if event["rect"].top > self.height:
                self.road_events.remove(event)

            elif event["rect"].colliderect(self.player_rect):
                if event["type"] == "moving_barrier":
                    self.handle_collision()
                    self.road_events.remove(event)

                elif event["type"] == "speed_bump":
                    self.base_speed = max(3, self.base_speed - 1)
                    self.score = max(0, self.score - 30)
                    self.road_events.remove(event)

                elif event["type"] == "nitro_strip":
                    if self.active_powerup is None and not self.shield_active:
                        self.active_powerup = "nitro"
                        self.powerup_timer = 180
                    self.road_events.remove(event)

    def update(self):
        if self.game_over or self.finished:
            return

        self.update_difficulty()
        self.update_powerup()
        self.update_spawns()
        self.update_objects()

        self.distance += int(self.speed)
        self.score += int(self.speed // 2)

        self.road_offset += int(self.speed)

        if self.distance >= self.finish_distance:
            self.finished = True
            self.score += 1000

    def draw_road(self, screen):
        screen.fill((30, 140, 60))

        pygame.draw.rect(
            screen,
            (45, 45, 45),
            (self.road_left, 0, self.road_width, self.height)
        )

        for i in range(1, self.lane_count):
            x = self.road_left + i * self.lane_width
            pygame.draw.line(
                screen,
                (230, 230, 230),
                (x, 0),
                (x, self.height),
                2
            )

        dash_height = 40
        gap = 35

        for y in range(-dash_height, self.height, dash_height + gap):
            draw_y = y + self.road_offset % (dash_height + gap)
            pygame.draw.rect(
                screen,
                (255, 255, 255),
                (self.width // 2 - 4, draw_y, 8, dash_height)
            )

    def draw_player(self, screen):
        pygame.draw.rect(
            screen,
            self.player_color,
            self.player_rect,
            border_radius=8
        )

        pygame.draw.rect(
            screen,
            (0, 0, 0),
            self.player_rect,
            3,
            border_radius=8
        )

        window = pygame.Rect(
            self.player_rect.x + 10,
            self.player_rect.y + 10,
            25,
            18
        )

        pygame.draw.rect(
            screen,
            (180, 230, 255),
            window,
            border_radius=4
        )

        if self.shield_active:
            pygame.draw.circle(
                screen,
                (80, 200, 255),
                self.player_rect.center,
                50,
                4
            )

    def draw_traffic(self, screen):
        for car in self.traffic:
            pygame.draw.rect(
                screen,
                car["color"],
                car["rect"],
                border_radius=8
            )

            pygame.draw.rect(
                screen,
                (0, 0, 0),
                car["rect"],
                2,
                border_radius=8
            )

    def draw_obstacles(self, screen):
        for obstacle in self.obstacles:
            rect = obstacle["rect"]

            if obstacle["type"] == "barrier":
                pygame.draw.rect(screen, (230, 60, 40), rect)
                pygame.draw.line(
                    screen,
                    (255, 255, 255),
                    rect.topleft,
                    rect.bottomright,
                    4
                )

            elif obstacle["type"] == "oil":
                pygame.draw.ellipse(screen, (10, 10, 10), rect)

            elif obstacle["type"] == "pothole":
                pygame.draw.ellipse(screen, (80, 50, 30), rect)
                pygame.draw.ellipse(screen, (20, 20, 20), rect.inflate(-10, -10))

            elif obstacle["type"] == "slow_zone":
                pygame.draw.rect(
                    screen,
                    (200, 180, 80),
                    rect,
                    border_radius=8
                )

    def draw_coins(self, screen):
        for coin in self.coins:
            rect = coin["rect"]

            pygame.draw.circle(screen, (255, 215, 0), rect.center, 15)
            pygame.draw.circle(screen, (150, 100, 0), rect.center, 15, 2)

            text = self.font.render(str(coin["value"]), True, (0, 0, 0))
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)

    def draw_powerups(self, screen):
        for powerup in self.powerups:
            rect = powerup["rect"]

            if powerup["type"] == "nitro":
                color = (0, 200, 255)
                letter = "N"

            elif powerup["type"] == "shield":
                color = (120, 120, 255)
                letter = "S"

            else:
                color = (80, 255, 120)
                letter = "R"

            pygame.draw.rect(screen, color, rect, border_radius=8)
            pygame.draw.rect(screen, (0, 0, 0), rect, 2, border_radius=8)

            label = self.font.render(letter, True, (0, 0, 0))
            label_rect = label.get_rect(center=rect.center)
            screen.blit(label, label_rect)

    def draw_events(self, screen):
        for event in self.road_events:
            rect = event["rect"]

            if event["type"] == "moving_barrier":
                pygame.draw.rect(screen, (255, 80, 80), rect)
                pygame.draw.rect(screen, (0, 0, 0), rect, 2)

            elif event["type"] == "speed_bump":
                pygame.draw.rect(
                    screen,
                    (255, 180, 50),
                    rect,
                    border_radius=8
                )

            elif event["type"] == "nitro_strip":
                pygame.draw.rect(
                    screen,
                    (0, 220, 255),
                    rect,
                    border_radius=8
                )

                label = self.font.render("BOOST", True, (0, 0, 0))
                label_rect = label.get_rect(center=rect.center)
                screen.blit(label, label_rect)

    def draw_hud(self, screen):
        remaining = max(0, self.finish_distance - self.distance)

        hud_bg = pygame.Rect(10, 10, 190, 170)

        pygame.draw.rect(screen, (20, 20, 20), hud_bg, border_radius=10)
        pygame.draw.rect(screen, (255, 255, 255), hud_bg, 2, border_radius=10)

        lines = [
            f"Score: {self.score}",
            f"Coins: {self.coins_collected}",
            f"Distance: {self.distance}m",
            f"Remain: {remaining}m",
            f"Speed: {int(self.speed)}"
        ]

        y = 20

        for line in lines:
            text = self.font.render(line, True, (255, 255, 255))
            screen.blit(text, (20, y))
            y += 28

        if self.active_powerup == "nitro":
            power_text = f"Nitro: {self.powerup_timer // 60}s"

        elif self.active_powerup == "shield":
            power_text = "Shield: active"

        else:
            power_text = "Power: none"

        text = self.font.render(power_text, True, (255, 255, 0))
        screen.blit(text, (20, y))

        bar_x = 220
        bar_y = 15
        bar_w = 360
        bar_h = 15

        pygame.draw.rect(screen, (20, 20, 20), (bar_x, bar_y, bar_w, bar_h))

        progress = min(1, self.distance / self.finish_distance)

        pygame.draw.rect(
            screen,
            (0, 220, 120),
            (bar_x, bar_y, int(bar_w * progress), bar_h)
        )

        pygame.draw.rect(
            screen,
            (255, 255, 255),
            (bar_x, bar_y, bar_w, bar_h),
            2
        )

    def draw(self, screen):
        self.draw_road(screen)
        self.draw_coins(screen)
        self.draw_powerups(screen)
        self.draw_obstacles(screen)
        self.draw_events(screen)
        self.draw_traffic(screen)
        self.draw_player(screen)
        self.draw_hud(screen)