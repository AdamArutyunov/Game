import pyglet

from Constants import TILE_SIZE, SECOND_WIDTH

class TileSprite:
    def __init__(self, width, height, key):
        self.batch = pyglet.graphics.Batch()

        self.rectangle = pyglet.shapes.BorderedRectangle(
            x = 0,
            y = 0,
            width=width,
            height=height,
            border=5,
            color=(0, 0, 0),
            border_color=(255, 255, 255),
            batch=self.batch,
        )

        self.label = pyglet.text.Label(
            chr(key),
            font_name='Pixel Times',
            font_size=36,
            x = 0,
            y = 0,
            batch=self.batch,
        )


    def move(self, x, dy):
        self.rectangle.x += dx
        self.rectangle.y += dy
        self.label.x += dx
        self.label.y += dy

    def moveTo(self, x, y):
        self.rectangle.x = x
        self.rectangle.y = y
        self.label.x = x + 10
        self.label.y = y + 10

    def draw(self):
        self.batch.draw()


class Tile:
    def __init__(self, start, duration, key):
        self.start = start
        self.duration = duration
        self.end = start + duration
        self.processed = False

        self.key = key

        self.sprite = TileSprite(SECOND_WIDTH * self.duration, TILE_SIZE[1], key)

    def check_expired(self, timestamp):
        return timestamp > self.end and not self.processed

    def __str__(self):
        return chr(self.key)

    def draw(self):
        if self.processed:
            return

        self.sprite.draw()

    def process(self):
        self.processed = True
        return self

    def reset(self):
        self.processed = False

    def is_processed(self):
        return self.processed
