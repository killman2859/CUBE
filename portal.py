from pygame import *

class Portal(sprite.Sprite):
    def __init__(self, x, y, target_portal):
        sprite.Sprite.__init__(self)
        self.image = Surface((50, 50))  # Размер портала
        self.image.fill(Color("#00FF00"))  # Зеленый цвет для портала
        self.rect = Rect(x, y, 50, 50)
        self.target_portal = target_portal  # Связанный портал
        self.animation_frames = []  # Анимация портала
        self.current_frame = 0

    def update(self):
        # Анимация портала (можно добавить смену кадров)
        pass

    def teleport(self, player):
        # Телепортация игрока на целевой портал
        player.rect.x = self.target_portal.rect.x
        player.rect.y = self.target_portal.rect.y