import math
import datetime
import pygame


class MickeyClock:
    def __init__(self, screen):
        self.screen = screen
        self.width, self.height = self.screen.get_size()
        self.center = (self.width // 2, self.height // 2 + 20)

        self.bg_color = (245, 245, 245)
        self.outline_color = (0, 0, 0)
        self.text_color = (0, 0, 0)

        self.clock_radius = 210

        self.title_font = pygame.font.SysFont("Arial", 30, bold=True)
        self.time_font = pygame.font.SysFont("Arial", 40, bold=True)

        # load hand image
        original = pygame.image.load("images/mickey_hand.png").convert_alpha()

        # resize image
        self.right_hand = pygame.transform.smoothscale(original, (70, 170))
        self.left_hand = pygame.transform.flip(self.right_hand, True, False)

    def draw_clock_face(self):
        self.screen.fill(self.bg_color)

        title = self.title_font.render("Mickey's Clock", True, self.text_color)
        title_rect = title.get_rect(center=(self.width // 2, 55))
        self.screen.blit(title, title_rect)

        # big circle
        pygame.draw.circle(self.screen, self.outline_color, self.center, self.clock_radius, 4)

        # ears
        left_ear = (self.center[0] - 105, self.center[1] - 185)
        right_ear = (self.center[0] + 105, self.center[1] - 185)
        pygame.draw.circle(self.screen, self.outline_color, left_ear, 45, 4)
        pygame.draw.circle(self.screen, self.outline_color, right_ear, 45, 4)

        # minute/second marks
        for i in range(60):
            angle = math.radians(i * 6 - 90)

            outer_x = self.center[0] + self.clock_radius * math.cos(angle)
            outer_y = self.center[1] + self.clock_radius * math.sin(angle)

            if i % 5 == 0:
                inner_r = self.clock_radius - 25
                width = 4
            else:
                inner_r = self.clock_radius - 12
                width = 2

            inner_x = self.center[0] + inner_r * math.cos(angle)
            inner_y = self.center[1] + inner_r * math.sin(angle)

            pygame.draw.line(
                self.screen,
                self.outline_color,
                (inner_x, inner_y),
                (outer_x, outer_y),
                width
            )

    def blit_rotate_pivot(self, image, angle, pivot):
        """
        Rotate image around its bottom-center point and place that pivot at 'pivot'.
        """
        image_rect = image.get_rect()
        pivot_offset = pygame.math.Vector2(0, image_rect.height // 2 - 10)

        rotated_offset = pivot_offset.rotate(-angle)
        rotated_image = pygame.transform.rotozoom(image, angle, 1.0)
        rotated_rect = rotated_image.get_rect(center=(pivot[0] - rotated_offset.x,
                                                      pivot[1] - rotated_offset.y))
        self.screen.blit(rotated_image, rotated_rect)

    def draw_hands(self, now):
        minute = now.minute
        second = now.second

        # 360/60 = 6 degrees each
        minute_angle = -(minute * 6)
        second_angle = -(second * 6)

        # minute hand = right hand
        self.blit_rotate_pivot(self.right_hand, minute_angle, self.center)

        # second hand = left hand
        self.blit_rotate_pivot(self.left_hand, second_angle, self.center)

        pygame.draw.circle(self.screen, self.outline_color, self.center, 10)

    def draw_time_text(self, now):
        text = now.strftime("%M:%S")
        surf = self.time_font.render(text, True, self.text_color)
        rect = surf.get_rect(center=(self.width // 2, self.height - 55))
        self.screen.blit(surf, rect)

    def draw(self):
        now = datetime.datetime.now()

        self.draw_clock_face()
        self.draw_hands(now)
        self.draw_time_text(now)