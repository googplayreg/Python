import pygame
import random
import sys

# Инициализация Pygame
pygame.init()

# Константы
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
FPS = 60
WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLACK = (0, 0, 0)

# Настройка экрана
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pygame Racer")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Verdana", 24, bold=True)
score_font = pygame.font.SysFont("Verdana", 35, bold=True)
large_font = pygame.font.SysFont("Verdana", 60)

# --- ЗАГРУЗКА РЕСУРСОВ ---

# 1. Загружаем и настраиваем фон
bg_original = pygame.image.load("racer/assets/road.png").convert()
# Растягиваем под размер нашего окна
bg = pygame.transform.scale(bg_original, (SCREEN_WIDTH, SCREEN_HEIGHT))

bg_height = bg.get_height()

# Две переменные для координат Y
y1 = 0
y2 = -bg_height

# 2. Звуки
crash_sound = pygame.mixer.Sound("racer/assets/crash.mp3")
coin_sound = pygame.mixer.Sound("racer/assets/coin.mp3")
pygame.mixer.music.load("racer/assets/wind warrior.mp3")
pygame.mixer.music.play(-1)

# 3. Картинка для счетчика (иконка)
coin_icon_img = pygame.image.load("racer/assets/coin.png").convert_alpha()
coin_icon = pygame.transform.scale(coin_icon_img, (70, 70))

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("racer/assets/player.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 200))
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 120)
        self.speed = 13

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0:
            if pressed_keys[pygame.K_LEFT]:
                self.rect.move_ip(-self.speed, 0)
        if self.rect.right < SCREEN_WIDTH:
            if pressed_keys[pygame.K_RIGHT]:
                self.rect.move_ip(self.speed, 0)

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("racer/assets/enemy3.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 200))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), -100)
        self.speed = 15

    def move(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.top = -100
            self.rect.center = (random.randint(40, SCREEN_WIDTH-40), -100)

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("racer/assets/coin.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (80, 80))
        self.rect = self.image.get_rect()
        self.spawn()

    def spawn(self):
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), -50)

    def move(self):
        self.rect.move_ip(0, 10)
        if self.rect.top > SCREEN_HEIGHT:
            self.spawn()

# Создание объектов
P1 = Player()
E1 = Enemy()
C1 = Coin()

# Группы спрайтов
enemies = pygame.sprite.Group()
enemies.add(E1)
coins = pygame.sprite.Group()
coins.add(C1)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(C1)

# Переменные для состояния
score = 0
bg_speed = 10  # Скорость движения фона
running = True
game_over = False

# Главный цикл
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if game_over:
            pygame.mixer.music.stop()

            # Если игра окончена, можно нажать 'q' для выхода или 'r' для рестарта
        if game_over and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                # 1. Обнуляем логические переменные
                score = 0
                game_over = False
                
                # 2. Сбрасываем игрока на стартовую позицию
                P1.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)
                
                # 3. Сбрасываем врага (отправляем его наверх с новыми координатами)
                E1.rect.center = (random.randint(40, SCREEN_WIDTH-40), -100)
                
                # 4. Сбрасываем монетку
                C1.spawn()
                
                # 5. Сбрасываем фон (чтобы дорога не дергалась при старте)
                y1 = 0
                y2 = -bg_height
                
                # 6. Снова запускаем музыку
                pygame.mixer.music.play(-1)
            elif event.key == pygame.K_q:
                running = False

    if not game_over:
        # 1. Логика движения фона
        y1 += bg_speed
        y2 += bg_speed

        if y1 >= bg_height:
            y1 = -bg_height
        if y2 >= bg_height:
            y2 = -bg_height

        # 2. Обновление позиций
        P1.move()
        E1.move()
        C1.move()

        # 3. Проверка столкновений с монеткой
        if pygame.sprite.spritecollideany(P1, coins):
            score += 1
            # coin_sound.play() 
            C1.spawn()

        # 4. Проверка столкновения с врагом
        if pygame.sprite.spritecollideany(P1, enemies):
            crash_sound.play() 
            pygame.mixer.music.stop()
            game_over = True

        # 5. Отрисовка фона
        screen.blit(bg, (0, y1))
        screen.blit(bg, (0, y2))

        # Отрисовка всех объектов поверх фона
        for entity in all_sprites:
            screen.blit(entity.image, entity.rect)

        # Отображение интерфейса (Иконка монетки + Число)
        screen.blit(coin_icon, (15, 15)) # Рисуем саму иконку
        scores_text = score_font.render(str(score), True, WHITE) # Рисуем только число
        screen.blit(scores_text, (95, 25)) # Ставим число правее иконки

    else:
        # Экран Game Over
        screen.fill(RED)
        over_text = large_font.render("GAME OVER", True, WHITE)
        instruction = font.render("Press X (or \"q\") to exit OR \"r\" to restart", True, WHITE)
        screen.blit(over_text, (215, 300))
        screen.blit(instruction, (135, 440))

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()