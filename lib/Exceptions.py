class TileExpiredException(Exception):
    def __str__(self):
        return 'Tile is expired.'
