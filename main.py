import pygame

pygame.init()

from lib.Application import Application, ApplicationState
from lib.Level import Level, Track
from lib.Tile import Tile
from lib.Game import Game

size = (1280, 720)
screen = pygame.display.set_mode(size, pygame.DOUBLEBUF, vsync=1)
pygame.display.set_caption('Solo')

MainLevel = Level('First Level')

FirstTrack = Track(0)
SecondTrack = Track(0)
ThirdTrack = Track(0)

FirstTrack.add_tile(Tile(3, 0.2, ord('a')))
FirstTrack.add_tile(Tile(4, 0.2, ord('d')))
FirstTrack.add_tile(Tile(5, 0.2, ord('g')))

SecondTrack.add_tile(Tile(3.2, 0.2, ord('b')))
SecondTrack.add_tile(Tile(4.2, 0.2, ord('e')))
SecondTrack.add_tile(Tile(5.2, 0.2, ord('h')))

ThirdTrack.add_tile(Tile(3.4, 0.2, ord('c')))
ThirdTrack.add_tile(Tile(4.4, 0.2, ord('f')))
ThirdTrack.add_tile(Tile(5.4, 0.2, ord('i')))

MainLevel.add_track(FirstTrack)
MainLevel.add_track(SecondTrack)
MainLevel.add_track(ThirdTrack)

CurrentGame = Game(MainLevel)


app = Application(screen)
app.set_state(ApplicationState.GAME, CurrentGame)
app.run()
