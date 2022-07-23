import os

import pyglet

from lib.Application import Application, ApplicationState
from lib.Level import Level, Track
from lib.Tile import Tile
from lib.Game import Game
from lib.Effect import BackgroundColorEffect


window = pyglet.window.Window(
    #fullscreen=True
)
window.set_vsync(True)

# pygame.display.set_caption('Solo')

MainLevel = Level.from_file('src/levels/dropout.lv')

CurrentGame = Game(MainLevel)

app = Application(window)
app.set_state(ApplicationState.GAME, CurrentGame)
app.run()

pyglet.app.run()
