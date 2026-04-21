import pygame
import random

# Инициализация Pygame
pygame.init()

# Константы экрана и сетки
WIDTH, GAME_HEIGHT = 600, 600
HEADER_HEIGHT = 60 
SCREEN_HEIGHT = GAME_HEIGHT + HEADER_HEIGHT
GRID_SIZE = 20  # Размер одной ячейки (квадратика)

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
HEADER_COLOR = (45, 45, 45)
RED = (213, 50, 80)      # Для еды (+1)
ORANGE = (255, 165, 0)   # Для еды (+2)
GOLD = (255, 215, 0)     # Для еды (+3, исчезающая)
GREEN = (0, 255, 0)      # Для головы змейки
DARK_GREEN = (0, 180, 0) # Для змейки
YELLOW = (255, 255, 102) # Для текста счета
GRAY = (30, 30, 30)      # Для сетки

# Создание игрового окна
screen = pygame.display.set_mode((WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Pygame Snake: Upgraded')

# Настройка FPS (скорости игры)
clock = pygame.time.Clock()

# Шрифты для счета и сообщений
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

defeat_sound = pygame.mixer.Sound("snake_upgraded/assets/game over.mp3")

def draw_grid():
    """Отрисовка сетки"""
    # Вертикальные линии
    for x in range(0, WIDTH, GRID_SIZE):
        pygame.draw.line(screen, GRAY, (x, HEADER_HEIGHT), (x, SCREEN_HEIGHT))
    # Горизонтальные линии
    for y in range(HEADER_HEIGHT, SCREEN_HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, GRAY, (0, y), (WIDTH, y))

def show_interface(score, level):
    """Отрисовка верхней панели со счетом"""
    pygame.draw.rect(screen, HEADER_COLOR, [0, 0, WIDTH, HEADER_HEIGHT])
    pygame.draw.line(screen, WHITE, (0, HEADER_HEIGHT), (WIDTH, HEADER_HEIGHT), 2)
    val = score_font.render(f"SCORE: {score}   LEVEL: {level}", True, YELLOW)
    screen.blit(val, [20, 10])

def draw_snake(snake_list):
    """Отрисовка всех сегментов змейки"""
    for i, segment in enumerate(snake_list):
        # Проверяем является ли сегмент головой
        # Если да, отрисовываем голову, если нет — обычное тело
        if i == len(snake_list) - 1:
            pygame.draw.rect(screen, GREEN, [segment[0], segment[1], GRID_SIZE, GRID_SIZE])
            # Рисуем глаза на голове
            pygame.draw.rect(screen, BLACK, [segment[0] + 3, segment[1] + 5, 4, 4])
            pygame.draw.rect(screen, BLACK, [segment[0] + 13, segment[1] + 5, 4, 4])
            # Для контура клеток змейки
            pygame.draw.rect(screen, BLACK, [segment[0], segment[1], GRID_SIZE, GRID_SIZE], 1)

        else:
            pygame.draw.rect(screen, DARK_GREEN, [segment[0], segment[1], GRID_SIZE, GRID_SIZE])
            pygame.draw.rect(screen, BLACK, [segment[0], segment[1], GRID_SIZE, GRID_SIZE], 1)

def generate_food(snake_list):
    """Создание координат еды"""
    while True:  # задаем условия чтобы еда не попадала на саму змейку
        fx = round(random.randrange(0, WIDTH - GRID_SIZE) / 20.0) * 20.0
        fy = round(random.randrange(HEADER_HEIGHT, SCREEN_HEIGHT - GRID_SIZE) / 20.0) * 20.0
        if [fx, fy] not in snake_list:
            # Создаем еду случайного типа (с различной вероятностью появления)
            chance = random.random()
            if chance > 0.9: # 10% шанс на золотую
                f_type = 3
                timer = pygame.time.get_ticks() + 7000 # Исчезнет через 7 сек
            elif chance > 0.7: # 20% шанс на оранжевую
                f_type = 2
                timer = None
            else:
                f_type = 1
                timer = None
            return {"pos": [fx, fy], "type": f_type, "timer": timer}

def game_loop():
    game_over = False
    game_close = False
    pygame.mixer.music.load("snake_upgraded/assets/Axel F.mp3")
    pygame.mixer.music.play(-1)
    x1 = WIDTH / 2
    y1 = HEADER_HEIGHT + (GAME_HEIGHT / 2)
    x1_change = GRID_SIZE
    y1_change = 0

    # Переменные для тела змейки
    Length_of_snake = 3  # Начальная длина
    snake_List = []

    # Создаем начальное тело (горизонтально в ряд)
    for i in range(Length_of_snake):
        snake_List.append([x1 - (Length_of_snake - 1 - i) * GRID_SIZE, y1])

    # Переменные для счета и уровней
    score = 0
    level = 1
    current_speed = 7 # Используем локальную переменную скорости

    food = generate_food(snake_List)

    while not game_over:

        while game_close == True:
            screen.fill(BLACK)
            message = font_style.render("Game Over! Press Q to exit or R to restart", True, RED)
            screen.blit(message, [WIDTH / 9, SCREEN_HEIGHT / 3])
            pygame.mixer.music.stop()
            # defeat_sound.play()
            pygame.display.update()

            # Обработка действий для выхода и рестарта
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_r:
                        game_loop()
                if event.type == pygame.QUIT:
                    game_over = True
                    game_close = False

        # Управление
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change == 0:
                    x1_change = -GRID_SIZE
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change = GRID_SIZE
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change == 0:
                    y1_change = -GRID_SIZE
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    y1_change = GRID_SIZE
                    x1_change = 0

        # Логика движения
        x1 += x1_change
        y1 += y1_change

        # Проверка на столкновение с границами
        if x1 >= WIDTH or x1 < 0 or y1 >= SCREEN_HEIGHT or y1 < HEADER_HEIGHT:
            game_close = True

        # Проверка таймера еды
        if food["timer"] and pygame.time.get_ticks() > food["timer"]:
            food = generate_food(snake_List) # Еда испарилась!

        screen.fill(BLACK)
        draw_grid()

        # Логика роста хвоста
        snake_Head = [x1, y1]
        snake_List.append(snake_Head)
        # Если длина списка координат больше длины змеи, удаляем самый старый "хвост"
        if len(snake_List) > Length_of_snake:
            del snake_List[0]
        
        # Проверка столкновения с самим собой
        for segment in snake_List[:-1]: # Проверяем всё тело, кроме самой головы
            if segment == snake_Head and Length_of_snake > 1:
                game_close = True

        # Логика еды и уровней
        if x1 == food["pos"][0] and y1 == food["pos"][1]:
            val = food["type"]
            score += val * 10
            Length_of_snake += val # Растем на 1, 2 или 3 ячейки!
            food = generate_food(snake_List)
            
            if score % 50 == 0: # Повышаем скорость реже (каждые 50 очков)
                level += 1
                if current_speed < 15: current_speed += 1

        # Отрисовка еды (цвет зависит от типа)
        f_color = RED if food["type"] == 1 else (ORANGE if food["type"] == 2 else GOLD)
        pygame.draw.rect(screen, f_color, [food["pos"][0], food["pos"][1], GRID_SIZE, GRID_SIZE])
        
        draw_snake(snake_List)
        show_interface(score, level)
        
        pygame.display.update()
        clock.tick(current_speed)

    pygame.quit()
    quit()

if __name__ == "__main__":
    game_loop()