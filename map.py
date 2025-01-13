import pygame

# Разрешение экрана
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


# Определяем классы для объектов
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Crystal(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Spike(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Drone(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Lever(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Barrier(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


# Функция для загрузки карты
def load_map():
    level_map = [
        "1111111111111111",
        "1P00000000000001",
        "1C11111111111101",
        "1S10000000000001",
        "1L11111111111101",
        "1C1000C000000001",
        "1S111S111S111111",
        "1D111R0000000011",
        "1C0000C0000B0011",
        "1L11111111111101",
        "1111111111111111"
    ]

    platforms = pygame.sprite.Group()
    crystals = pygame.sprite.Group()
    spikes = pygame.sprite.Group()
    drones = pygame.sprite.Group()
    levers = pygame.sprite.Group()
    barriers = pygame.sprite.Group()

    # Размер плитки
    tile_size = 40

    # Путь к изображениям
    image_paths = {
        '1': 'platform.png',
        'C': 'crystal.png',
        'S': 'spike.png',
        'D': 'drone.png',
        'R': 'lever.png',
        'B': 'barrier.png',
        'P': 'portal.png',  # Допустим, у вас есть изображение портала
        'L': 'laser.png'  # Лазер, если хотите добавить
    }

    # Перебор карты и создание объектов
    for row_index, row in enumerate(level_map):
        for col_index, tile in enumerate(row):
            x = col_index * tile_size
            y = row_index * tile_size

            # Определяем, какой объект добавлять
            if tile == '1':  # Платформа
                platforms.add(Platform(x, y, image_paths['1']))
            elif tile == 'C':  # Кристалл
                crystals.add(Crystal(x + 10, y + 10, image_paths['C']))  # Смещение для красоты
            elif tile == 'S':  # Шипы
                spikes.add(Spike(x + 10, y + 10, image_paths['S']))
            elif tile == 'D':  # Дрон
                drones.add(Drone(x, y, image_paths['D']))
            elif tile == 'R':  # Рычаг
                levers.add(Lever(x, y, image_paths['R']))
            elif tile == 'B':  # Энергетический барьер
                barriers.add(Barrier(x, y, image_paths['B']))
            # Добавление других объектов по мере необходимости

    return platforms, crystals, spikes, drones, levers, barriers


# Инициализация Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# Загрузка карты
platforms, crystals, spikes, drones, levers, barriers = load_map()

# Главный игровой цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))  # Очистка экрана

    # Отображение всех объектов
    platforms.draw(screen)
    crystals.draw(screen)
    spikes.draw(screen)
    drones.draw(screen)
    levers.draw(screen)
    barriers.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
