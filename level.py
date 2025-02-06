import random
import sys
import os

from player import Player
from blocks import Platform
from crystal import Crystal
from portal import Portal
from spike import Spike

import pygame

FPS = 50
clock = pygame.time.Clock()


def load_image(name, colorkey=None):
    fullname = os.path.join('Images', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


player_x = 0
player_y = 0


def read_level_data(level_number):
    fullname = os.path.join('Levels', "level_" + str(level_number) + ".txt")

    if not os.path.isfile(fullname):
        print(f"Файл '{fullname}' не найден")
        sys.exit()

    level_file = open(fullname, 'r')
    level_data = []
    portals = {}
    pos_x = 0
    pos_y = 0

    lines = level_file.readlines()
    for lin in lines:
        line = lin.rstrip()
        row = []

        if '/' in line:
            player_x = int(line.split('/')[0])
            player_y = int(line.split('/')[1])
        for char in line:

            if char == 'p':  # Платформа
                platform = Platform(pos_x, pos_y)
                row.append(platform)
                print(f"✅ Платформа добавлена: ({pos_x}, {pos_y})")  # Отладка

            elif char == 'c':  # Кристалл
                row.append(Crystal(pos_x, pos_y))

            elif char == 's':  # Шипы (если есть)
                row.append(Spike(pos_x, pos_y + 50))  # Смещаем вниз

            elif char.isalpha():  # Порталы
                if char in portals:
                    target = portals[char]
                    portal = Portal(pos_x, pos_y, target_portal=target)
                    target.target_portal = portal
                    row.append(portal)
                else:
                    portal = Portal(pos_x, pos_y)
                    portals[char] = portal
                    row.append(portal)

            pos_x += 70  # Смещаемся вправо по карте

        pos_y += 70  # Смещаемся вниз по карте
        pos_x = 0
        level_data.append(row)

    return level_data


def show_text(some_text, screen):
    font = pygame.font.Font(None, 100)
    text_surface = font.render(some_text, True, (0, 255, 0))
    text_rect = text_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))

    screen.fill((0, 0, 0))  # Чёрный фон
    screen.blit(text_surface, text_rect)
    pygame.display.update()


class Level:
    def __init__(self, level_number):
        self.level_data = read_level_data(level_number)
        self.level_number = level_number
        self.count_of_crystals = 0
        self.size = self.width, self.height = 700, 630
        self.final_level_num = 2

    def display_text(self, screen, value):
        font = pygame.font.Font(None, 30)
        text_surface = font.render(f"Количество кристаллов: {value}", True, (255, 255, 255))
        text_rect = text_surface.get_rect()
        text_rect.x = screen.get_width() - 280  # Правый край экрана минус ширина текста
        text_rect.y = 10  # Верхний край экрана
        screen.blit(text_surface, text_rect)

    def draw_level(self, screen):
        screen.fill((0, 0, 0))
        fon = pygame.transform.scale(load_image('main_background.png'), (700, 630))
        screen.blit(fon, (0, 0))

    def start_level(self):
        pygame.init()
        screen = pygame.display.set_mode(self.size)
        hero = Player(player_x, player_y, self)  # создаем героя по (x,y) координатам
        left = right = up = False
        entities = pygame.sprite.Group()  # Все объекты

        platforms = []
        crystals = []
        portals = []
        spikes = []

        for row_data in self.level_data:
            for obj in row_data:
                if isinstance(obj, Platform):
                    platforms.append(obj)
                    entities.add(obj)
                elif isinstance(obj, Crystal):
                    crystals.append(obj)
                    entities.add(obj)
                elif isinstance(obj, Portal):
                    portals.append(obj)
                    entities.add(obj)
                elif isinstance(obj, Spike):
                    spikes.append(obj)
                    entities.add(obj)

        entities.add(hero)

        self.count_of_crystals = len(crystals)

        print('s')
        while True:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                if e.type == pygame.KEYDOWN and e.key == pygame.K_LEFT:
                    left = True
                if e.type == pygame.KEYDOWN and e.key == pygame.K_RIGHT:
                    right = True
                if e.type == pygame.KEYUP and e.key == pygame.K_RIGHT:
                    right = False
                if e.type == pygame.KEYUP and e.key == pygame.K_LEFT:
                    left = False
                if e.type == pygame.KEYDOWN and e.key == pygame.K_UP:
                    up = True
                if e.type == pygame.KEYUP and e.key == pygame.K_UP:
                    up = False

            if self.count_of_crystals == hero.count_of_crystals:
                if self.level_number + 1 < self.final_level_num + 1:
                    print(f"Уровень {self.level_number} пройден!")

                    show_text("Уровень пройден!", screen)

                    pygame.time.delay(2000)
                    self.level_number += 1
                    current_level = Level(self.level_number)
                    current_level.start_level()
                    return
                else:
                    print(f"Вы прошли все уровни!")

                    show_text("Вы прошли игру!", screen)

                    pygame.time.delay(2000)
                    pygame.quit()
            self.draw_level(screen)
            self.display_text(screen, hero.count_of_crystals)
            hero.update(left, right, up, platforms, crystals, portals, spikes, screen)  # 🔥 Добавляем screen
            entities.draw(screen)
            pygame.display.update()
            clock.tick(FPS)
