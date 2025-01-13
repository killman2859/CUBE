from pygame import *

MOVE_SPEED = 7
WIDTH = 22
HEIGHT = 32
COLOR = "#888888"
JUMP_POWER = 10
GRAVITY = 0.8  # Сила, которая будет тянуть нас вниз


class Player(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.count_of_crystals = 0
        self.xvel = 0
        self.X = x
        self.Y = y
        self.image = image.load("Images/Hero.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.yvel = 0  # скорость вертикального перемещения
        self.onGround = False  # На земле ли я?

    def update(self, left, right, up, platforms, crystals):
        if up:
            if self.onGround:  # прыгаем, только когда можем оттолкнуться от земли
                self.yvel = -JUMP_POWER

        if left:
            self.xvel = -MOVE_SPEED  # Лево = x- n

        if right:
            self.xvel = MOVE_SPEED  # Право = x + n

        if not (left or right):  # стоим, когда нет указаний идти
            self.xvel = 0

        if not self.onGround:
            self.yvel += GRAVITY

        self.onGround = False

        self.rect.y += self.yvel
        self.collide(0, self.yvel, platforms, crystals)

        self.rect.x += self.xvel  # переносим свои положение на xvel
        self.collide(self.xvel, 0, platforms, crystals)

    # def draw(self, screen):  # Выводим себя на экран
    #     screen.blit(self.image, (self.rect.x, self.rect.y))

    def collide(self, xvel, yvel, platforms, crystals):
        for c in crystals:
            if sprite.collide_rect(self, c):  # если есть пересечение кристалла с игроком
                self.count_of_crystals += 1
                crystals.remove(c)
                c.kill()
        for p in platforms:
            if sprite.collide_rect(self, p):  # если есть пересечение платформы с игроком

                if xvel > 0:  # если движется вправо
                    self.rect.right = p.rect.left  # то не движется вправо

                if xvel < 0:  # если движется влево
                    self.rect.left = p.rect.right  # то не движется влево

                if yvel > 0:  # если падает вниз
                    self.rect.bottom = p.rect.top  # то не падает вниз
                    self.onGround = True  # и становится на что-то твердое
                    self.yvel = 0  # и энергия падения пропадает

                if yvel < 0:  # если движется вверх
                    self.rect.top = p.rect.bottom  # то не движется вверх
                    self.yvel = 0  # и энергия прыжка пропадает
