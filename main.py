import os

import pygame

pygame.init()

from lib.Application import Application, ApplicationState
from lib.Level import Level, Track
from lib.Tile import Tile
from lib.Game import Game
from lib.Effect import BackgroundColorEffect

os.environ['SDL_VIDEODRIVER'] = 'directx'

size = (0, 0)
screen = pygame.display.set_mode(size, pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.FULLSCREEN)
pygame.display.set_caption('Solo')

MainLevel = Level.from_file('src/levels/dropout.lv')

CurrentGame = Game(MainLevel)

app = Application(screen)
app.set_state(ApplicationState.GAME, CurrentGame, 61.7)
app.run()
