import os
import sys

import pygame
from level import Level

# Изображение не получится загрузить
# без предварительной инициализации pygame
pygame.init()
size = width, height = 500, 500
screen = pygame.display.set_mode(size)
FPS = 60
clock = pygame.time.Clock()
current_level = None


def load_image(name, colorkey=None):
    fullname = os.path.join('Images', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["CUBE", "",
                  "Добро пожаловать!",
                  "Правила игры:",
                  "1. Основной задачей игры является",
                  " сбор кристаллов",
                  "2. Игрок может двигаться влево(A) и вправо(D),",
                  " также присутствует прыжок(SPACE, W)",
                  "3.В игре присутствуют препятствия,",
                  " которые могут убить игрока", "", "", "",
                  "Для продолжения нажмите любую клавишу"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('red'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                current_level = Level(0)
                current_level.start_level()
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    start_screen()
