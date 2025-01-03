import random

from player import Player
from blocks import Platform

import pygame

FPS = 50
clock = pygame.time.Clock()


def read_level_data(level_number):
    return "some"


class Level:
    def __init__(self, level_number):
        self.level_data = read_level_data(level_number)

        self.size = self.width, self.height = 800, 600

    def draw_level(self, screen):
        screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 50)
        text = font.render("Hello, Pygame!", True, (100, 255, 100))
        text_x = self.width // 2 - text.get_width() // 2
        text_y = self.height // 2 - text.get_height() // 2
        text_w = text.get_width()
        text_h = text.get_height()
        screen.blit(text, (text_x, text_y))
        pygame.draw.rect(screen, (0, 255, 0), (text_x - 10, text_y - 10,
                                               text_w + 20, text_h + 20), 1)

    def start_level(self):
        pygame.init()
        screen = pygame.display.set_mode(self.size)
        hero = Player(300, 55)  # создаем героя по (x,y) координатам
        left = right = up = False
        entities = pygame.sprite.Group()  # Все объекты
        platforms = []  # то, во что мы будем врезаться или опираться
        entities.add(hero)
        pf = Platform(100, 300)
        entities.add(pf)
        platforms.append(pf)
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
            hero.update(left, right, up, platforms)
            entities.draw(screen)  # отображение всего
            pygame.display.update()
            clock.tick(FPS)
