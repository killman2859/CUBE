from pygame import *

class Portal(sprite.Sprite):
    def __init__(self, x, y, target_portal=None):
        sprite.Sprite.__init__(self)
        self.image = Surface((50, 50))  # Размер портала
        self.image.fill(Color("#00FF00"))  # Зеленый цвет для портала
        self.rect = Rect(x, y, 50, 50)
        self.target_portal = target_portal  # Связанный портал
        self.animation_frames = []  # Анимация портала
        self.current_frame = 0

    def teleport(self, player):
        if self.target_portal is None:
            print(f"⚠️ Ошибка: целевой портал не задан! ({self.rect.x}, {self.rect.y})")
            return

        print(f"✅ Телепорт из ({player.rect.x}, {player.rect.y}) в ({self.target_portal.rect.x}, {self.target_portal.rect.y})")

        new_x = self.target_portal.rect.x + 55  # Сдвигаем вправо
        if new_x > 700:  # Если выходит за границы экрана
            new_x = self.target_portal.rect.x - 55  # Сдвигаем влево

        player.rect.x = new_x
        player.rect.y = self.target_portal.rect.y