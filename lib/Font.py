import pygame

class Font:
    @staticmethod
    def get_font(size):
        return pygame.font.Font(None, size)


class PixelTimes(Font):
    @staticmethod
    def get_font(size):
        return pygame.font.Font('assets/font/pixeltimes.ttf', size)
