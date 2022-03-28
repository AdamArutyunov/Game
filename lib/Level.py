import pygame

from Constants import TILE_SIZE, SECOND_WIDTH
from lib.Exceptions import TileExpiredException
from lib.Tile import Tile
from lib.Effect import EFFECTS


LETTER_ALIASES = {
    'space': ' ',
}

BEAT_ALIASES = {
    'b': 1,
    'h': 1 / 2,
    't': 1 / 3,
    'q': 1 / 4,
    'o': 1 / 8,
    'n': 1 / 9,
    's': 1 / 16,
}

class Level:
    def __init__(self, name='', music_src=''):
        self.tracks = []
        self.effects = []
        self.name = name
        self.music_src = music_src

    @classmethod
    def from_file(self, file_src):
        with open(file_src) as f:
            file = f.read().strip(' \n')

        sections = file.split('\n\n\n')
        if not sections:
            raise Exception('Level parse error: no level info.')

        level_info = sections[0].split('\n')
        level_name, level_music_src, bpm = level_info
        bpm = int(bpm)

        level = Level(level_name, level_music_src)

        for section in sections[1:-1]:
            lines = section.split('\n')

            track_start = int(lines[0]) * 60 / bpm
            track = Track(track_start)
            
            block_start = 0

            for line in lines[1:]:
                print(line)
                line = line.strip()
                if not line:
                    print('Line empty, block_start = 0')
                    block_start = 0
                    continue

                if line.startswith('#'):
                    print('Line is comment')
                    continue

                if line.startswith('BLOCK'):
                    block_start = int(line.split()[1])
                    print('Line is blockstart', block_start)
                    continue

                start_beat, duration_beat, letter = line.split()

                if letter in LETTER_ALIASES:
                    letter = LETTER_ALIASES[letter]

                start_beats = 0
                duration_beats = 0

                for beat_alias, beats in BEAT_ALIASES.items():
                    while beat_alias in start_beat:
                        start_beats += beats
                        start_beat = start_beat.replace(beat_alias, '', 1)

                    while beat_alias in duration_beat:
                        duration_beats += beats
                        duration_beat = duration_beat.replace(beat_alias, '', 1)

                start = (block_start + float(start_beat or '0') + start_beats) * 60 / bpm
                duration = (float(duration_beat or '0') + duration_beats) * 60 / bpm

                tile = Tile(start, duration, ord(letter))
                track.add_tile(tile)

            track.validate()
            level.add_track(track)


        current_effect = None
        for line in sections[-1].split('\n'):
            line = line.strip()
            if line.startswith('EFFECT'):
                _, slug, effect_start, effect_duration = line.split()
                start = float(effect_start)
                duration = float(effect_duration)

                effect = EFFECTS[slug](start, duration)
                current_effect = effect

                level.effects.append(effect)
            else:
                current_effect.update(*line.split())
        

        return level

    def add_track(self, track):
        self.tracks.append(track)

    def get_tracks(self):
        return self.tracks

    def update(self, timestamp):
        for track in self.tracks:
            track.check_expired(timestamp)

    def process_key(self, timestamp, key):
        processed_tiles = []
        for track in self.tracks:
            processed_tiles += track.process_key(timestamp, key)

        return processed_tiles

    def reset(self):
        for track in self.tracks:
            track.reset()

    def get_duration(self):
        return max(map(lambda x: x.end, self.tracks))

    def get_effects(self):
        return self.effects


class Track:
    def __init__(self, start):
        self.tiles = []
        self.start = start
        self.end = start

    def get_tiles(self):
        return self.tiles

    def add_tile(self, tile):
        self.tiles.append(tile)
        self.tiles.sort(key=lambda t: t.start)

        self.end = self.tiles[-1].end

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
                raise Exception()

        return True

    def get_tile(self, timestamp):
        if not self.tiles:
            return None

        left = 0
        right = len(self.tiles)
        
        while right - left > 1:
            middle = (left + right) // 2
            middle_tile = self.tiles[middle]

            if middle_tile.start <= timestamp + 0.1:
                left = middle
            else:
                right = middle

        tile = self.tiles[left]
        if tile.start <= timestamp + 0.1 and timestamp < tile.end:
            return tile

    def check_expired(self, timestamp):
        expired = list(filter(lambda t: t.check_expired(timestamp), self.tiles))

        if expired:
            raise TileExpiredException

    def process_key(self, timestamp, key):
        tile = self.get_tile(timestamp)

        if tile and tile.key == key and not tile.is_processed():
            return [tile.process()]

        return []

    def reset(self):
        for tile in self.tiles:
            tile.reset()

