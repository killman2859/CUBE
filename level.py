import random
import sys
import os

from player import Player
from blocks import Platform
from crystal import Crystal
from portal import Portal

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


def read_level_data(level_number):
    fullname = os.path.join('Levels', "level_" + str(level_number) + ".txt")
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл '{fullname}' не найден")
        sys.exit()
    level_file = open(fullname, 'r')
    level_data = list()
    portals = dict()
    pos_x = 0
    pos_y = 0
    lines = level_file.readlines()
    for lin in lines:
        line = lin.rstrip()
        row = []
        for char in line:
            if char == 'p':
                row.append(Platform(pos_x, pos_y))
            elif char == 'c':
                row.append(Crystal(pos_x, pos_y))
            elif char != '-':
                portal = Portal(pos_x, pos_y)
                if char in portals.keys():
                    portals[char].target_portal = portal
                    portal.target_portal = portals[char]
                    row.append(portal)
                else:
                    portals[char] = portal
                    row.append(portal)
            pos_x += 70
        pos_y += 70
        pos_x = 0
        level_data.append(row)
    return level_data


class Level:
    def __init__(self, level_number):
        self.level_data = read_level_data(level_number)

        self.size = self.width, self.height = 700, 630

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
        hero = Player(300, 55)  # создаем героя по (x,y) координатам
        left = right = up = False
        entities = pygame.sprite.Group()  # Все объекты

        platforms = []  # то, во что мы будем врезаться или опиратьсяa
        crystals = []
        portals = []

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

        entities.add(hero)

        # pf = Platform(100, 300)
        # entities.add(pf)
        # platforms.append(pf)
        #
        # crystal_1 = Crystal(200, 200)
        # entities.add(crystal_1)
        # crystals.append(crystal_1)
        #
        # portal1 = Portal(100, 300, None)
        # portal2 = Portal(600, 300, None)
        # portal1.target_portal = portal2
        # portal2.target_portal = portal1
        # portals.extend([portal1, portal2])
        # entities.add(portal1)
        # entities.add(portal2)

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

            self.draw_level(screen)
            self.display_text(screen, hero.count_of_crystals)
            hero.update(left, right, up, platforms, crystals, portals)
            entities.draw(screen)  # отображение всего
            pygame.display.update()
            clock.tick(FPS)
