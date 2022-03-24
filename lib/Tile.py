import pygame

from Constants import TILE_SIZE, SECOND_WIDTH
from .Font import PixelTimes

pixel_times = PixelTimes.get_font(TILE_SIZE[1] - 20)

class Tile:
    def __init__(self, start, duration, key):
        self.start = start
        self.duration = duration
        self.end = start + duration
        self.processed = False

        self.key = key

        self.render()

    def check_expired(self, timestamp):
        return timestamp > self.end and not self.processed

    def __str__(self):
        return chr(self.key)

    def render(self):
        surface = pygame.Surface((SECOND_WIDTH * self.duration, TILE_SIZE[1]), pygame.SRCALPHA)

        if self.processed:
            return surface

        pygame.draw.rect(surface, 'white', 
                         (0, 0, surface.get_width(), surface.get_height()), 
                         2, 10)
        
        text = pixel_times.render(str(self), 0, 'white')

        surface.blit(text, (13, 15))
        self.surface = surface
        return self.surface

    def process(self):
        self.processed = True
        return self

    def reset(self):
        self.processed = False
