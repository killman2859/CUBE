from pygame import *

PLATFORM_WIDTH = 500
PLATFORM_HEIGHT = 100
PLATFORM_COLOR = "#FF6262"


class Platform(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = image.load("Images/platform.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
