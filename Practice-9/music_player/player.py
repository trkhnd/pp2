import os
import pygame


class MusicPlayer:
    def __init__(self, music_folder):
        self.music_folder = music_folder
        self.tracks = self.load_tracks()
        self.current_index = 0
        self.is_playing = False

        pygame.mixer.init()

        self.title_font = pygame.font.SysFont("Arial", 34, bold=True)
        self.info_font = pygame.font.SysFont("Arial", 24)
        self.small_font = pygame.font.SysFont("Arial", 20)

    def load_tracks(self):
        if not os.path.exists(self.music_folder):
            return []

        tracks = []
        for file_name in os.listdir(self.music_folder):
            if file_name.lower().endswith((".wav", ".mp3", ".ogg")):
                tracks.append(file_name)

        tracks.sort()
        return tracks

    def get_current_track_path(self):
        if not self.tracks:
            return None
        return os.path.join(self.music_folder, self.tracks[self.current_index])

    def get_current_track_name(self):
        if not self.tracks:
            return "No tracks found"
        return self.tracks[self.current_index]

    def play(self):
        if not self.tracks:
            return

        track_path = self.get_current_track_path()
        pygame.mixer.music.load(track_path)
        pygame.mixer.music.play()
        self.is_playing = True

    def stop(self):
        pygame.mixer.music.stop()
        self.is_playing = False

    def next_track(self):
        if not self.tracks:
            return

        self.current_index = (self.current_index + 1) % len(self.tracks)
        self.play()

    def previous_track(self):
        if not self.tracks:
            return

        self.current_index = (self.current_index - 1) % len(self.tracks)
        self.play()

    def get_position_seconds(self):
        pos_ms = pygame.mixer.music.get_pos()
        if pos_ms < 0:
            return 0
        return pos_ms // 1000

    def draw(self, screen):
        screen.fill((245, 245, 245))

        title_surface = self.title_font.render("Music Player", True, (0, 0, 0))
        screen.blit(title_surface, (220, 40))

        track_surface = self.info_font.render(
            f"Current Track: {self.get_current_track_name()}",
            True,
            (0, 0, 128)
        )
        screen.blit(track_surface, (60, 130))

        status_text = "Playing" if self.is_playing else "Stopped"
        status_surface = self.info_font.render(
            f"Status: {status_text}",
            True,
            (128, 0, 0)
        )
        screen.blit(status_surface, (60, 180))

        position_surface = self.info_font.render(
            f"Position: {self.get_position_seconds()} sec",
            True,
            (0, 100, 0)
        )
        screen.blit(position_surface, (60, 230))

        controls = [
            "Controls:",
            "P = Play",
            "S = Stop",
            "N = Next Track",
            "B = Previous Track",
            "Q = Quit"
        ]

        y = 320
        for line in controls:
            line_surface = self.small_font.render(line, True, (0, 0, 0))
            screen.blit(line_surface, (60, y))
            y += 35