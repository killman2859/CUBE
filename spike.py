from pygame import *

class Spike(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((50, 20))  # Размер шипов
        self.image.fill(Color("#FF0000"))  # Красный цвет
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
