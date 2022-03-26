import os

import pygame

pygame.init()

from lib.Application import Application, ApplicationState
from lib.Level import Level, Track
from lib.Tile import Tile
from lib.Game import Game
from lib.Effect import BackgroundColorEffect

os.environ['SDL_VIDEODRIVER'] = 'directx'

size = (1440, 800)
screen = pygame.display.set_mode(size, pygame.HWSURFACE | pygame.DOUBLEBUF)
pygame.display.set_caption('Solo')

MainLevel = Level.from_file('src/levels/dropout.lv')

CurrentGame = Game(MainLevel)

app = Application(screen)
app.set_state(ApplicationState.GAME, CurrentGame)
app.run()
