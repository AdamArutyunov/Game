import pygame

from Constants import TILE_SIZE, SECOND_WIDTH
from lib.Exceptions import TileExpiredException
from lib.Tile import Tile


LETTER_ALIASES = {
    'space': ' ',
}

BEAT_ALIASES = {
    'b': 1,
    'h': 1 / 2,
    't': 1 / 3,
    'q': 1 / 4,
    'o': 1 / 8,
    's': 1 / 16,
}

class Level:
    def __init__(self, name='', music_src=''):
        self.tracks = []
        self.name = name
        self.music_src = music_src

    @classmethod
    def from_file(self, file_src):
        with open(file_src) as f:
            file = f.read().strip(' \n')

        blocks = file.split('\n\n')
        if len(blocks) == 0:
            raise Exception('Level parse error: no level info.')

        level_info = blocks[0].split('\n')
        level_name, level_music_src, bpm = level_info
        bpm = int(bpm)

        level = Level(level_name, level_music_src)

        for block in blocks[1:]:
            block_lines = block.split('\n')

            track_start = int(block_lines[0]) * 60 / bpm
            track = Track(track_start)
            
            for tile_line in block_lines[1:]:
                start_beat, duration_beat, letter = tile_line.split()

                if letter in LETTER_ALIASES:
                    letter = LETTER_ALIASES[letter]

                start_beats = 0
                start_beat_parts = start_beat.split('+')
                duration_beats = 0
                duration_beat_parts = duration_beat.split('+')

                for part in start_beat_parts:
                    try:
                        start_beats += float(part)
                    except Exception:
                        start_beats += BEAT_ALIASES[part]

                for part in duration_beat_parts:
                    try:
                        duration_beats += float(part)
                    except Exception:
                        duration_beats += BEAT_ALIASES[part]

                start = start_beats * 60 / bpm - 0.1
                duration = duration_beats * 60 / bpm

                tile = Tile(start, duration, ord(letter))
                track.add_tile(tile)

            track.validate()
            level.add_track(track)

        return level

    def add_track(self, track):
        self.tracks.append(track)

    def update(self, timestamp):
        for track in self.tracks:
            track.check_expired(timestamp)

    def reset(self):
        for track in self.tracks:
            track.reset()


class Track:
    def __init__(self, start):
        self.tiles = []
        self.start = start
        self.end = start

        self.surface = pygame.Surface((0, TILE_SIZE[1]))

    def add_tile(self, tile):
        self.tiles.append(tile)
        self.tiles.sort(key=lambda t: t.start)

        self.end = self.tiles[-1].end

        self.render()

    def validate(self):
        stamps = []

        for tile in self.tiles:
            stamps.append((tile.start, 1))
            stamps.append((tile.end, 0))

        stamps.sort()

        d = 0
        for stamp in stamps:
            if stamp[1] == 0:
                d -= 1
            elif stamp[1] == 1:
                d += 1

            if d > 1:
                return False

        return True

    def get_tile(self, timestamp):
        if not self.tiles:
            return None

        left = 0
        right = len(self.tiles)
        
        while right - left > 1:
            middle = (left + right) // 2
            middle_tile = self.tiles[middle]

            if middle_tile.start <= timestamp:
                left = middle
            else:
                right = middle

        tile = self.tiles[left]
        if tile.start <= timestamp < tile.end:
            return tile

    def check_expired(self, timestamp):
        expired = list(filter(lambda t: t.check_expired(timestamp), self.tiles))

        if expired:
            raise TileExpiredException

    def render(self):
        surface = pygame.Surface((SECOND_WIDTH * self.end, TILE_SIZE[1]))

        for tile in self.tiles:
            tile_surface = tile.render()
            surface.blit(tile_surface, (tile.start * SECOND_WIDTH, 0))

        self.surface = surface
        return surface

    def process_key(self, timestamp, key):
        tile = self.get_tile(timestamp)

        if tile and tile.key == key:
            tile.process()

        self.render()

    def reset(self):
        for tile in self.tiles:
            tile.reset()

        self.render()

