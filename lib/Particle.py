import pygame

from .Font import PixelTimes


class Particle:
    def __init__(self, start, coords, duration=0):
        self.start = start
        self.duration = duration
        self.end = start + duration
        self.coords = coords

        self.width = 0
        self.height = 0

    def render(self, time):
        return

    def is_active(self, time):
        return self.start <= time < self.end

    def is_expired(self, time):
        return time >= self.end


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
        
        self.surface = PixelTimes.get_font(font_size).render(caption, 0, color)
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
    def __init__(self, start, coords, tile):
        super().__init__(start, coords, 10)

        self.surface = pygame.Surface.copy(tile.surface)

    def render(self, time):
        phase = 1 - (time - self.start) / self.duration
        self.surface.set_alpha(32)
        print(self.surface.get_alpha())

        return self.surface
