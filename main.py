import pygame

pygame.init()

from lib.Application import Application, ApplicationState
from lib.Level import Level, Track
from lib.Tile import Tile
from lib.Game import Game

size = (1280, 720)
screen = pygame.display.set_mode(size, pygame.DOUBLEBUF, vsync=1)
pygame.display.set_caption('Solo')

MainLevel = Level.from_file('src/levels/test.lv')

CurrentGame = Game(MainLevel)


app = Application(screen)
app.set_state(ApplicationState.GAME, CurrentGame)
app.run()
