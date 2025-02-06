import pygame
from pygame import *

MOVE_SPEED = 7
WIDTH = 22
HEIGHT = 32
COLOR = "#888888"
JUMP_POWER = 10
GRAVITY = 0.8  # Сила, которая будет тянуть нас вниз

import time


class Player(sprite.Sprite):
    def __init__(self, x, y, level):
        sprite.Sprite.__init__(self)
        self.count_of_crystals = 0
        self.curr_level = level
        self.xvel = 0
        self.X = x
        self.Y = y
        self.images = list()
        self.cur_sprite = 0
        image_1 = image.load("Images/Hero/Hero_1.png").convert_alpha()
        image_2 = image.load("Images/Hero/Hero_2.png").convert_alpha()
        image_3 = image.load("Images/Hero/Hero_3.png").convert_alpha()
        image_4 = image.load("Images/Hero/Hero_4.png").convert_alpha()
        image_5 = image.load("Images/Hero/Hero_5.png").convert_alpha()
        self.images.append(image_1)
        self.images.append(image_2)
        self.images.append(image_3)
        self.images.append(image_4)
        self.images.append(image_5)

        self.image = self.images[0]  # начальное изображение
        self.rect = self.images[0].get_rect()
        self.rect.x = x
        self.rect.y = y
        self.yvel = 0  # скорость вертикального перемещения
        self.onGround = False  # На земле ли я?
        self.last_teleport_time = 0  # Время последней телепортации (чтобы не застревать)

    def update(self, left, right, up, platforms, crystals, portals, spikes, screen):

        self.cur_sprite = (self.cur_sprite + 1) % len(self.images)
        self.image = self.images[self.cur_sprite]

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

        # Обработка вертикальных столкновений
        self.rect.y += self.yvel
        self.collide(0, self.yvel, platforms, crystals, portals, spikes, screen)

        # Обработка горизонтальных столкновений
        self.rect.x += self.xvel
        self.collide(self.xvel, 0, platforms, crystals, portals, spikes, screen)

    def collide(self, xvel, yvel, platforms, crystals, portals, spikes, screen):
        for p in platforms:
            if sprite.collide_rect(self, p):  # Проверяем столкновение с платформой
                if xvel > 0:  # Если движется вправо
                    self.rect.right = p.rect.left
                if xvel < 0:  # Если движется влево
                    self.rect.left = p.rect.right
                if yvel > 0:  # Если падает вниз
                    self.rect.bottom = p.rect.top
                    self.onGround = True
                    self.yvel = 0  # Обнуляем вертикальную скорость при столкновении с платформой
                if yvel < 0:  # Если движется вверх (прыгает)
                    self.rect.top = p.rect.bottom
                    self.yvel = 0

        for s in spikes:
            if sprite.collide_rect(self, s):
                print("💀 Игрок погиб!")
                self.respawn(screen)  # Передаём экран для отображения надписи

        for portal in portals:
            if sprite.collide_rect(self, portal):
                portal.teleport(self)

        for crystal in crystals:
            if sprite.collide_rect(self, crystal):
                self.count_of_crystals += 1
                crystals.remove(crystal)
                crystal.kill()  # Удаляем кристалл из списка
                print(f"��� Количество кристаллов: {self.count_of_crystals}")
                return

        if self.rect.y > 700:
            print("💀 Игрок погиб!")
            self.respawn(screen)  # Передаём экран для отображения надписи

    def respawn(self, screen):
        """Респавн игрока после смерти"""
        print("🔄 Перезапуск уровня...")

        # Отображаем экран поражения
        font = pygame.font.Font(None, 100)
        text_surface = font.render("ПОРАЖЕНИЕ", True, (255, 0, 0))
        text_rect = text_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))

        screen.fill((0, 0, 0))  # Чёрный фон
        screen.blit(text_surface, text_rect)
        pygame.display.update()

        pygame.time.delay(2000)  # Ждём 2 секунды перед рестартом

        new_level = self.curr_level
        new_level.start_level()
        self.kill()
