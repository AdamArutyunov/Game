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


TestEffect = BackgroundColorEffect(0, MainLevel.get_duration())
TestEffect.add_colorpoint(3, (0, 0, 0))
TestEffect.add_colorpoint(10+2/3, (127, 0, 0))
TestEffect.add_colorpoint(21+1/3, (0, 0, 127))
TestEffect.add_colorpoint(50, (0, 127, 0))

app = Application(screen)
app.set_state(ApplicationState.GAME, CurrentGame)
app.get_state().add_effect(TestEffect)
app.run()
