import pygame

from blocks import Platform
from player import Player
from portal import Portal

FPS = 60
clock = pygame.time.Clock()


class Level:
    def __init__(self, level_number):
        self.level_data = self.read_level_data(level_number)  # Загрузка данных уровня
        self.size = self.width, self.height = 800, 600  # Размер экрана
        self.portals = []  # Список порталов на уровне
        self.platforms = []  # Список платформ на уровне
        self.entities = pygame.sprite.Group()  # Группа всех объектов на уровне

    def read_level_data(self, level_number):
        """
        Загружает данные уровня (например, из файла или базы данных).
        В данном примере просто возвращает фиктивные данные.
        """
        # Здесь может быть логика загрузки уровня из файла или базы данных
        return {
            "platforms": [(100, 300), (400, 500)],  # Координаты платформ
            "portals": [(100, 300), (600, 300)],  # Координаты порталов
        }

    def draw_level(self, screen):
        """
        Отрисовывает все объекты уровня на экране.
        """
        screen.fill((0, 0, 0))  # Очистка экрана (черный фон)

        # Отрисовка платформ
        for platform in self.platforms:
            screen.blit(platform.image, platform.rect)

        # Отрисовка порталов
        for portal in self.portals:
            screen.blit(portal.image, portal.rect)

    def start_level(self):
        """
        Запускает уровень.
        """
        pygame.init()
        screen = pygame.display.set_mode(self.size)  # Создание окна игры
        hero = Player(300, 55)  # Создание игрока
        left = right = up = False  # Флаги управления

        # Создание платформ
        for platform_data in self.level_data["platforms"]:
            x, y = platform_data
            platform = Platform(x, y)
            self.platforms.append(platform)
            self.entities.add(platform)

        # Создание порталов
        portal1 = Portal(100, 300, None)
        portal2 = Portal(600, 300, None)
        portal1.target_portal = portal2
        portal2.target_portal = portal1
        self.portals.extend([portal1, portal2])
        self.entities.add(portal1)
        self.entities.add(portal2)

        self.entities.add(hero)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        left = True
                    if event.key == pygame.K_RIGHT:
                        right = True
                    if event.key == pygame.K_UP:
                        up = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        left = False
                    if event.key == pygame.K_RIGHT:
                        right = False
                    if event.key == pygame.K_UP:
                        up = False

            hero.update(left, right, up, self.platforms, self.portals)

            self.draw_level(screen)
            self.entities.draw(screen)
            pygame.display.update()
            clock.tick(FPS)


if __name__ == "__main__":
    level = Level(1)
    level.start_level()
