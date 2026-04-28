import pygame
import random
import time

# Константы для логики
SCREEN_WIDTH = 1100
ROAD_WIDTH = 800
SCREEN_HEIGHT = 800
LANES = [66, 200, 333, 466, 600, 733] # Центры 6-ти полос

# Цвета для графики pygame
OIL_COLOR = (30, 30, 30)
BUMP_COLOR = (100, 100, 100)
BOOST_COLOR = (0, 255, 0)

class Player(pygame.sprite.Sprite):
    def __init__(self, image_path):
        super().__init__()
        # Загрузка и настройка игрока
        self.original_image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.original_image, (60, 120))
        self.rect = self.image.get_rect()
        self.rect.center = (ROAD_WIDTH // 2, SCREEN_HEIGHT - 100)
        
        self.speed = 10
        self.base_speed = 10
        self.is_sliding = False
        self.slide_timer = 0
        
        # Статусы усилителей
        self.has_shield = False
        self.shield_timer = 0
        self.has_repair = False
        self.nitro_timer = 0

    def apply_nitro(self):
        self.nitro_timer = time.time() + 5 # Нитро на 5 секунд
        self.speed = self.base_speed * 2

    def move(self):
        # Если нитро закончилось, возвращаем скорость
        if self.nitro_timer > 0 and time.time() > self.nitro_timer:
            self.speed = self.base_speed
            self.nitro_timer = 0

        # Эффект масла: рандомное смещение
        if self.is_sliding:
            if time.time() < self.slide_timer:
                self.rect.x += random.choice([-10, 10])
            else:
                self.is_sliding = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < ROAD_WIDTH:
            self.rect.x += self.speed

    def draw_effects(self, surface):
        # Отрисовка щита (пункт 3.3.5)
        if self.has_shield:
            pygame.draw.circle(surface, (0, 200, 255), self.rect.center, 70, 3)
            if time.time() > self.shield_timer:
                self.has_shield = False

class Enemy(pygame.sprite.Sprite):
    def __init__(self, images):
        super().__init__()
        self.images = images # Список из 5 картинок машин
        self.spawn()

    def spawn(self):
        self.image = random.choice(self.images)
        self.image = pygame.transform.scale(self.image, (60, 120))
        self.rect = self.image.get_rect()
        # Выбираем случайную полосу из 6
        self.rect.center = (random.choice(LANES), -150)

    def update(self, speed):
        self.rect.y += speed
        if self.rect.top > SCREEN_HEIGHT:
            self.spawn()

class RoadObject(pygame.sprite.Sprite):
    """Общий класс для монет, препятствий и бустов."""
    def __init__(self, image=None, type="coin"):
        super().__init__()
        self.type = type
        if image:
            self.image = pygame.transform.scale(image, (50, 50))
        else:
            # Если нет картинки, рисуем прямоугольник (для бустов/препятствий pygame)
            self.image = pygame.Surface((60, 60), pygame.SRCALPHA)
            if type == "bump": pygame.draw.rect(self.image, BUMP_COLOR, (0, 20, 60, 20))
            if type == "boost": pygame.draw.polygon(self.image, BOOST_COLOR, [(30,0), (60,60), (0,60)])
        
        self.rect = self.image.get_rect()
        self.spawn()

    def spawn(self):
        self.rect.center = (random.choice(LANES), -100)

        if self.type == "coin":
            # Выбираем случайную ценность
            self.value = random.choice([1, 5, 10])
        else:
            self.value = 0 # Для всех остальных объектов (ямы, бусты) ценность 0

    def update(self, speed):
        self.rect.y += speed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill() # Объекты удаляются, если улетели за экран

    def draw(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        else:
            # Логика для объектов без картинки
            if self.type == "bump":
                # Ярко-желтый "лежачий полицейский"
                pygame.draw.rect(screen, (255, 215, 0), self.rect)
                # Добавляем черные диагональные полоски для заметности
                for i in range(0, self.rect.width, 20):
                    pygame.draw.line(screen, (0, 0, 0), 
                                     (self.rect.x + i, self.rect.y), 
                                     (self.rect.x + i + 10, self.rect.y + self.rect.height), 4)
            
            elif self.type == "shield":
                # Отрисовка бонуса "Щит" на дороге (если нет картинки)
                # Рисуем синий светящийся ромб или круг
                pygame.draw.circle(screen, (0, 191, 255), self.rect.center, 20)
                pygame.draw.circle(screen, (255, 255, 255), self.rect.center, 20, 2) # Ободок

class EntityManager:
    """Управляет всеми группами спрайтов и их появлением."""
    def __init__(self):
        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        self.hazards = pygame.sprite.Group() # Масло, препятствия
        self.powerups = pygame.sprite.Group()

    def create_enemy(self, images):
        e = Enemy(images)
        self.enemies.add(e)
        self.all_sprites.add(e)

    def spawn_random_event(self, coin_imgs, powerup_imgs, hazard_imgs):
        """Логика плотности трафика (3.2.4)."""
        chance = random.random()
        
        # 1. Монеты (всегда высокий шанс)
        if chance < 0.05:
            c = RoadObject(random.choice(list(coin_imgs.values())), "coin")
            # Назначаем ценность монеты для счета
            self.coins.add(c)
            self.all_sprites.add(c)
            
        # 2. Препятствия (3.1.1 и 3.2.2)
        elif chance < 0.07:
            h_type = random.choice(["oil", "pothole", "wall", "bump"])
            img = hazard_imgs.get(h_type)
            h = RoadObject(img, h_type)
            self.hazards.add(h)
            self.all_sprites.add(h)

        # 3. Усилители (3.3)
        elif chance < 0.08:
            p_type = random.choice(["nitro", "shield", "repair"])
            img = powerup_imgs.get(p_type)
            p = RoadObject(img, p_type)
            self.powerups.add(p)
            self.all_sprites.add(p)