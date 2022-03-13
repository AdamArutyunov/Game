class Game:
    def __init__(self, level):
        self.level = level

    def get_tracks(self):
        return self.level.tracks

    def get_level(self):
        return self.level

    def reset(self):
        self.level.reset()
