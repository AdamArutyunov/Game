from easing_functions import CubicEaseOut
import pygame

from .Font import PixelTimes
from Constants import TILE_SIZE


class Particle:
    def __init__(self, start, start_coords, duration=0, speed=(0, 0)):
        self.start = start
        self.duration = duration
        self.end = start + duration

        self.start_coords = self.coords = start_coords

        self.speed = speed

        self.width = 0
        self.height = 0

    def render(self, time):
        return

    def is_active(self, time):
        return self.start <= time < self.end

    def is_expired(self, time):
        return time >= self.end

    def update(self, time):
        self.coords = (
            self.start_coords[0] + self.speed[0] * (time - self.start),
            self.start_coords[1] + self.speed[1] * (time - self.start),
        )


class CaptionParticle(Particle):
    def __init__(
            self,
            start,
            coords,
            duration,
            caption,
            font_size=72, 
            color='white',
            transition_in=0.5,
            transition_out=0.5):
        super().__init__(start, coords, duration)
        
        self.surface = PixelTimes.get_font(font_size).render(caption, 0, color).convert_alpha()
        self.width, self.height = self.surface.get_size()

        self.transition_in = transition_in
        self.transition_out = transition_out

    def render(self, time):
        if not self.is_active(time):
            return

        if time < self.start + self.transition_in and self.transition_in > 0:
            alpha = (time - self.start) / self.transition_in
        elif time > self.end - self.transition_out and self.transition_out > 0:
            alpha = 1 - (time - (self.end - self.transition_out)) / self.transition_out
        else:
            alpha = 1
        
        self.surface.set_alpha(alpha * 255)
        return self.surface


class ProcessedTileParticle(Particle):
    def __init__(self, start, coords, tile, speed):
        duration = 0.15

        super().__init__(start, coords, duration, speed)

        self.surface = pygame.Surface.copy(tile.surface).convert_alpha()
        self.initial_coords = coords
        self.easing_function = CubicEaseOut()

    def render(self, time):
        phase = (time - self.start) / self.duration

        easing_phase = self.easing_function(phase)
        self.surface.set_alpha((1 - phase) * 128)

        return self.surface
