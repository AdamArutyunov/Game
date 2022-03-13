import pygame

from .Font import PixelTimes


class Particle:
    def __init__(self, start, coords, duration=0):
        self.start = start
        self.duration = duration
        self.coords = coords

    def render(self, time):
        return

    def is_active(self, time):
        return self.start <= time < self.start + self.duration


class CaptionParticle(Particle):
    def __init__(self, start, coords, duration, caption, font_size=72, color='white'):
        super().__init__(start, coords, duration)
        
        self.surface = PixelTimes.get_font(font_size).render(caption, 0, color)

    def render(self, time):
        if not self.is_active(time):
            return

        phase = (1 - (time - self.start) / self.duration) * 255
        self.surface.set_alpha(phase)
        return self.surface
