import pyglet
import time

from Constants import TILE_SIZE, SECOND_WIDTH, LEFT_BORDER
from .Exceptions import TileExpiredException
from .Game import Game
from .Particle import CaptionParticle, ProcessedTileParticle
from .Utils import get_center


class State:
    def __init__(self, app):
        self.app = app
        self.particles = []
        self.effects = []

        self.data = {}

    def process_tick(self):
        pass

    def handle_event(self, event):
        pass

    def destroy(self):
        pass

    def add_particle(self, particle):
        self.particles.append(particle)

    def add_effect(self, effect):
        self.effects.append(effect)


class MenuState(State):
    def __init__(self, app, game):
        super().__init__(app)

        self.game = game

    def process_tick(self):
        screen = self.app.screen
        title = PixelTimes.get_font(300).render('Solo', 0, 'white')
        subtitle = PixelTimes.get_font(60).render('Press Enter to start', 0, 'white')

        screen.blit(title, (get_center(screen, title)[0], 200))
        screen.blit(subtitle, (get_center(screen, subtitle)[0], 500))


    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            self.app.set_state(ApplicationState.GAME, self.game, 0)


class GameState(State):
    ALPHABET_ORDS = list(map(lambda c: ord(c), 'qwertyuiopasdfghjklzxcvbnm ;,./1234567890'))

    def __init__(self, app, game, offset=0):
        super().__init__(app)

        self.game = game
        self.offset = offset
        #self.add_particle(CaptionParticle(1, (100, 50), 3, game.get_level().name))
        #self.effects = game.get_level().get_effects()

        for track in game.get_tracks():
            for tile in track.get_tiles():
                if tile.start + tile.duration < offset:
                    tile.process()


        #pygame.mixer.music.load(game.get_level().music_src)
        #pygame.mixer.music.play(0, offset)

    def destroy(self):
        #pygame.mixer.music.stop()
        #pygame.mixer.music.unload()
        pass

    def process_tick(self):
        tick = self.app.tick + self.offset
        dx = -tick * 60 * SECOND_WIDTH // 60

        #for effect in self.effects:
        #    self.data.update(effect.affect(tick))
        
        #self.app.screen.fill(self.data.get('background', (0, 0, 0)))

        for i, track in enumerate(self.game.get_tracks()):
            for tile in track.get_tiles():
                tile.sprite.moveTo(
                    dx + LEFT_BORDER + tile.start * SECOND_WIDTH,
                    (TILE_SIZE[1] + 5) * i + 200,
                )

                tile.draw()

            try:
                track.check_expired(tick)
            except TileExpiredException as e:
                if not self.data.get('godmode', False):
                    self.game.reset()
                    self.app.set_state(ApplicationState.GAME, self.game, self.offset)

            #pygame.draw.line(
            #    self.app.screen,
            #    'white', 
            #    (LEFT_BORDER, 200),
            #    (LEFT_BORDER, self.app.screen.get_height() - 50),
            #    width=2
            #)

            #self.particles = list(filter(lambda x: not x.is_expired(tick), self.particles))

            '''
            for particle in self.particles:
                tick = self.app.tick + self.offset
                if not particle.is_active(tick):
                    continue

                particle.update(tick)
                surface = particle.render(tick)
                self.app.screen.blit(surface, particle.coords)
            '''

    def handle_event(self, event):
        tick = self.app.tick + self.offset

        if event.type == pygame.KEYDOWN:
            if event.key in GameState.ALPHABET_ORDS:
                for i, track in enumerate(self.game.get_tracks()):
                    processed_tiles = track.process_key(tick, event.key)

                    for tile in processed_tiles:
                        dx = -tick * 60 * SECOND_WIDTH // 60
                        particle = ProcessedTileParticle(
                            tick, 
                            (dx + LEFT_BORDER + tile.start * SECOND_WIDTH, (TILE_SIZE[1] + 5) * i + 200),
                            tile,
                            (-SECOND_WIDTH, -TILE_SIZE[1] / 0.3),
                        )

                        self.add_particle(particle)

                right = 300
                for particle in self.particles:
                    if isinstance(particle, CaptionParticle):
                        right = max(right, particle.coords[0] + particle.width + 5)
                        while right > self.app.screen.get_size()[0]:
                            right -= self.app.screen.get_size()[0]

                particle = CaptionParticle(tick, (right, 650), 0.5, chr(event.key), 72, 'white', 0, 0.5)
                self.add_particle(particle)


class GameOverState(State):
    def process_tick(self):
        tick = self.app.tick

        self.app.screen.fill('red')

    def handle_event(self, event):
        pass


class ApplicationState:
    MENU = MenuState
    GAME = GameState
    GAME_OVER = GameOverState


class Application:
    def __init__(self, window):
        self.window = window

        self.state = None
        self.running = False
        self.start_tick = 0

    def set_state(self, state, *args, **kwargs):
        if self.state:
            self.state.destroy()

        self.state = state(self, *args, **kwargs)
        self.clear_ticker()

    def get_state(self):
        return self.state

    def clear_ticker(self):
        self.start_tick = time.time()
        self.tick = 0

    def run(self):
        self.running = True
        self.clear_ticker()

        def update(dt):
            #for event in pygame.event.get():
            #    if event.type == pygame.QUIT:
            #        self.stop()

            #    self.state.handle_event(event)

            self.tick += dt

            self.window.clear()

            self.state.process_tick()

        pyglet.clock.schedule_interval(update, 1 / 120.0)

    def stop(self):
        self.running = False
