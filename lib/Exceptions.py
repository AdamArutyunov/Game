class TileExpiredException(Exception):
    def __init__(self, tile=None, message=''):
        self.tile = tile
        super().__init__(message)

    def __str__(self):
        return 'Tile is expired.'
