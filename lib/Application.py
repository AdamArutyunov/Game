import pygame

from Constants import TILE_SIZE, SECOND_WIDTH, LEFT_BORDER
from .Exceptions import TileExpiredException
from .Game import Game
from .Font import PixelTimes
from .Particle import CaptionParticle


class State:
    def __init__(self, app):
        self.app = app
        self.particles = []

    def process_tick(self):
        pass

    def handle_event(self, event):
        pass

    def destroy(self):
        pass


class MenuState(State):
    def process_tick(self):
        self.app.screen.fill('black')

    def handle_event(self, event):
        pass


class GameState(State):
    ALPHABET_ORDS = list(map(lambda c: ord(c), 'qwertyuiopasdfghjklzxcvbnm '))

    def __init__(self, app, game):
        super().__init__(app)

        self.game = game
        self.particles.append(CaptionParticle(1, (100, 50), 3, game.get_level().name))

        self.screen_font = PixelTimes.get_font(72)

        pygame.mixer.music.load(game.get_level().music_src)
        pygame.mixer.music.play()

    def destroy(self):
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()

    def process_tick(self):
        tick = self.app.tick
        dx = -self.app.tick * 60 * SECOND_WIDTH // 60

        for i, track in enumerate(self.game.get_tracks()):
            self.app.screen.blit(
                track.surface, 
                (dx + LEFT_BORDER, (TILE_SIZE[1] + 5) * i + 200)
            )

            try:
                track.check_expired(tick)
            except TileExpiredException as e:
                self.game.reset()
                self.app.set_state(ApplicationState.GAME, self.game)

            pygame.draw.line(
                self.app.screen,
                'white', 
                (LEFT_BORDER, 200),
                (LEFT_BORDER, self.app.screen.get_height() - 50),
                width=2
            )

            particles = filter(lambda x: x.is_active(tick), self.particles)

            for particle in particles:
                surface = particle.render(tick)
                self.app.screen.blit(surface, particle.coords)

    def handle_event(self, event):
        tick = self.app.tick

        if event.type == pygame.KEYDOWN:
            if event.key in GameState.ALPHABET_ORDS:
                for track in self.game.get_tracks():
                    track.process_key(tick, event.key)

                particle = CaptionParticle(tick, (500, 600), 0.5, chr(event.key))
                self.particles.append(particle)


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
    def __init__(self, screen):
        self.screen = screen

        self.state = ApplicationState.MENU(self)
        self.running = False
        self.start_tick = 0

    def set_state(self, state, *args, **kwargs):
        if self.state:
            self.state.destroy()

        self.state = state(self, *args, **kwargs)
        self.clear_ticker()

    def clear_ticker(self):
        self.start_tick = pygame.time.get_ticks() / 1000

    def get_state(self):
        return self.state

    def run(self):
        from time import time
        clock = pygame.time.Clock()

        self.running = True
        self.clear_ticker()

        last_time = time()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.stop()

                self.state.handle_event(event)

            self.screen.fill('black')

            self.state.process_tick()

            pygame.display.flip()
            clock.tick(60)

            new_time = time()
            last_time = new_time
                
    def stop(self):
        self.running = False

    @property
    def tick(self):
        return pygame.time.get_ticks() / 1000 - self.start_tick
