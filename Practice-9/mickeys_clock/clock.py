import pygame
import datetime
import math

class MickeyClock:
    def __init__(self, screen, hand_image):
        self.screen = screen
        self.hand_image = hand_image
        self.center = (screen.get_width() // 2, screen.get_height() // 2)

    def get_time_angles(self):
        now = datetime.datetime.now()

        seconds = now.second
        minutes = now.minute

        sec_angle = -seconds * 6   # clockwise
        min_angle = -minutes * 6

        return sec_angle, min_angle

    def draw_hand(self, image, angle):
        rotated = pygame.transform.rotate(image, angle)
        rect = rotated.get_rect(center=self.center)
        self.screen.blit(rotated, rect)

    def draw_numbers(self):
        radius = 220

        for num in range(1, 13):
            # Bigger font for main numbers
            if num in [12, 3, 6, 9]:
                font = pygame.font.SysFont(None, 50)
            else:
                font = pygame.font.SysFont(None, 35)

            angle = math.radians((num - 3) * 30)

            x = self.center[0] + radius * math.cos(angle)
            y = self.center[1] + radius * math.sin(angle)

            text = font.render(str(num), True, (0, 0, 0))
            rect = text.get_rect(center=(x, y))

            self.screen.blit(text, rect)

    def draw_ticks(self):
        for i in range(60):
            angle = math.radians(i * 6)

            if i % 5 == 0:
                inner = 230
                outer = 250
                width = 3
            else:
                inner = 240
                outer = 250
                width = 1

            x1 = self.center[0] + inner * math.cos(angle)
            y1 = self.center[1] + inner * math.sin(angle)

            x2 = self.center[0] + outer * math.cos(angle)
            y2 = self.center[1] + outer * math.sin(angle)

            pygame.draw.line(self.screen, (0, 0, 0), (x1, y1), (x2, y2), width)

    def draw_clock_face(self):
        # Outer circle
        pygame.draw.circle(self.screen, (0, 0, 0), self.center, 260, 3)

        # Draw ticks and numbers
        self.draw_ticks()
        self.draw_numbers()

    def draw(self):
        # Draw clock face first
        self.draw_clock_face()

        sec_angle, min_angle = self.get_time_angles()

        # Seconds = left hand
        self.draw_hand(self.hand_image, sec_angle)

        # Minutes = right hand
        self.draw_hand(self.hand_image, min_angle)