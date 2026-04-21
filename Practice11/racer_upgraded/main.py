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
GOLD = (255, 215, 0)

# Настройка экрана
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pygame Racer: Upgraded")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Verdana", 24, bold=True)
score_font = pygame.font.SysFont("Verdana", 35, bold=True)
large_font = pygame.font.SysFont("Verdana", 60)
msg_font = pygame.font.SysFont("Verdana", 45, bold=True, italic=True)

# --- ЗАГРУЗКА РЕСУРСОВ ---

# 1. Загружаем и настраиваем фон
bg_original = pygame.image.load("racer_upgraded/assets/road.png").convert()
# Растягиваем под размер нашего окна
bg = pygame.transform.scale(bg_original, (SCREEN_WIDTH, SCREEN_HEIGHT))

bg_height = bg.get_height()

# Две переменные для координат Y
y1 = 0
y2 = -bg_height

# 2. Звуки
crash_sound = pygame.mixer.Sound("racer_upgraded/assets/crash.mp3")
coin_sound = pygame.mixer.Sound("racer_upgraded/assets/coin.mp3")
pygame.mixer.music.load("racer_upgraded/assets/wind warrior.mp3")
pygame.mixer.music.play(-1)

# 3. Картинка для счетчика (иконка)
coin_images = {
    1: pygame.transform.scale(pygame.image.load("racer_upgraded/assets/coin.png").convert_alpha(), (70, 70)),
    5: pygame.transform.scale(pygame.image.load("racer_upgraded/assets/big_coin.png").convert_alpha(), (75, 75)),
    10: pygame.transform.scale(pygame.image.load("racer_upgraded/assets/ultra_coin.png").convert_alpha(), (80, 80))
}
coin_icon = pygame.transform.scale(pygame.image.load("racer_upgraded/assets/counter.png").convert_alpha(), (70, 70))

# 4. Враги (Список разных машин)
enemy_files = ["racer_upgraded/assets/enemy1.png", "racer_upgraded/assets/enemy2.png", "racer_upgraded/assets/enemy3.png"]
enemy_imgs = [pygame.transform.scale(pygame.image.load(f).convert_alpha(), (100, 200)) for f in enemy_files]

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("racer_upgraded/assets/player.png").convert_alpha()
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
        self.spawn()

    def spawn(self):
        # Выбираем случайный вид машины
        self.image = random.choice(enemy_imgs)
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(60, SCREEN_WIDTH-60), -200)
        self.current_speed = enemy_speed 

    def move(self):
        self.rect.move_ip(0, self.current_speed)
        if self.rect.top > SCREEN_HEIGHT:
            self.spawn()

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.spawn()

    def spawn(self):
        # Шансы выпадения разных монет: 70% обычная, 20% серебро (+5), 10% золото (+10)
        chance = random.random()
        if chance < 0.7: self.value = 1
        elif chance < 0.9: self.value = 5
        else: self.value = 10
        
        self.image = coin_images[self.value]
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(60, SCREEN_WIDTH-60), -100)

    def move(self):
        self.rect.move_ip(0, bg_speed)
        if self.rect.top > SCREEN_HEIGHT:
            self.spawn()

# Сообщения
class FeedbackMessage:
    def __init__(self, text, color):
        self.text = msg_font.render(text, True, color)
        self.alpha = 255
        self.y = SCREEN_HEIGHT // 2
        self.x = SCREEN_WIDTH // 2 - self.text.get_width() // 2

    def draw(self, surface):
        if self.alpha > 0:
            self.text.set_alpha(self.alpha)
            surface.blit(self.text, (self.x, self.y))
            self.y -= 2 # Уплывает вверх
            self.alpha -= 5 # Исчезает

# Переменные для состояния
score = 0
bg_speed = 8  # Скорость движения фона
enemy_speed = 10
max_enemy_speed = 20 # Ограничение роста скорости
speed_up_step = 10 # Скорость растет каждые 10 монет
messages = []

# Создание объектов
P1 = Player()
E1 = Enemy()
C1 = Coin()

# Группы спрайтов
enemies = pygame.sprite.Group(E1)
coins = pygame.sprite.Group(C1)
all_sprites = pygame.sprite.Group(P1, E1, C1)

# Состояния
running = True
game_over = False

# Главный цикл
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

            # Если игра окончена, можно нажать 'q' для выхода или 'r' для рестарта
        if game_over and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                # 1. Обнуляем логические переменные
                score = 0
                enemy_speed = 10
                game_over = False
                
                # 2. Сбрасываем игрока на стартовую позицию
                P1.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 120)
                
                # 3. Сбрасываем врага (отправляем его наверх с новыми координатами)
                E1.spawn()
                
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
            old_score = score
            score += C1.value
            coin_sound.play()
            
            # Эффекты для жирных монет
            if C1.value == 5:
                messages.append(FeedbackMessage("AWESOME! +5", GOLD))
            elif C1.value == 10:
                messages.append(FeedbackMessage("AMAZING! +10", (0, 255, 255)))

            # Усложнение: проверяем, перешагнули ли мы порог очков
            if score // speed_up_step > old_score // speed_up_step:
                if enemy_speed < max_enemy_speed:
                    enemy_speed += 1
                    bg_speed += 0.5 # Плавно ускоряем и дорогу
            
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

        # Рисуем всплывающие сообщения
        for msg in messages[:]:
            msg.draw(screen)
            if msg.alpha <= 0: messages.remove(msg)

        # Отображение интерфейса (Иконка монетки + Число)
        screen.blit(coin_icon, (15, 15)) # Рисуем саму иконку
        scores_text = score_font.render(str(score), True, WHITE) # Рисуем только число
        screen.blit(scores_text, (95, 25)) # Ставим число правее иконки

    else:
        # Экран Game Over
        screen.fill(RED)
        over_text = large_font.render("GAME OVER", True, WHITE)
        instruction = font.render("Press 'q' to exit OR 'r' to restart", True, WHITE)
        screen.blit(over_text, (215, 300))
        screen.blit(instruction, (185, 440))

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()