import pygame
import random

# Инициализация Pygame
pygame.init()

# Константы экрана и сетки
WIDTH, HEIGHT = 600, 400
GRID_SIZE = 20  # Размер одной ячейки (квадратика)

# Цвета (RGB)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (213, 50, 80)      # Для еды
GREEN = (0, 255, 0)      # Для головы змейки
DARK_GREEN = (0, 180, 0) # Для змейки
YELLOW = (255, 255, 102) # Для текста счета
GRAY = (30, 30, 30)      # Для сетки

# Создание игрового окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Pygame Snake')

# Настройка FPS (скорости игры)
clock = pygame.time.Clock()

# Шрифты для счета и сообщений
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

defeat_sound = pygame.mixer.Sound("snake/assets/game over.mp3")

def draw_grid():
    """Отрисовка сетки"""
    # Вертикальные линии
    for x in range(0, WIDTH, GRID_SIZE):
        pygame.draw.line(screen, GRAY, (x, 0), (x, HEIGHT))
    # Горизонтальные линии
    for y in range(0, HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, GRAY, (0, y), (WIDTH, y))

def show_score(score, level):
    """Функция для отображения счета и уровня на экране"""
    value = score_font.render(f"Счет: {score}  Уровень: {level}", True, YELLOW)
    screen.blit(value, [5, 5])

def draw_snake(snake_list, x_change, y_change):
    """Отрисовка всех сегментов змейки"""
    for i, segment in enumerate(snake_list):
        # Проверяем является ли сегмент головой
        # Если да, отрисовываем голову, если нет — обычное тело
        if i == len(snake_list) - 1:
            pygame.draw.rect(screen, GREEN, [segment[0], segment[1], GRID_SIZE, GRID_SIZE])
            # Рисуем глаза на голове
            pygame.draw.rect(screen, BLACK, [segment[0] + 3, segment[1] + 5, 4, 4])
            pygame.draw.rect(screen, BLACK, [segment[0] + 13, segment[1] + 5, 4, 4])

        else:
            pygame.draw.rect(screen, DARK_GREEN, [segment[0], segment[1], GRID_SIZE, GRID_SIZE])

def generate_food(snake_list):
    """Создание координат еды, которые не попадают на змейку"""
    while True:
        fx = round(random.randrange(0, WIDTH - GRID_SIZE) / float(GRID_SIZE)) * GRID_SIZE
        fy = round(random.randrange(0, HEIGHT - GRID_SIZE) / float(GRID_SIZE)) * GRID_SIZE
        if [fx, fy] not in snake_list:
            return fx, fy

def game_loop():
    game_over = False
    game_close = False
    pygame.mixer.music.load("snake/assets/Axel F.mp3")
    pygame.mixer.music.play(-1)
    x1 = WIDTH / 2
    y1 = HEIGHT / 2
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

    foodx, foody = generate_food(snake_List)

    while not game_over:

        while game_close == True:
            screen.fill(BLACK)
            message = font_style.render("Game Over! Press Q to exit or R to restart", True, RED)
            screen.blit(message, [WIDTH / 9, HEIGHT / 3])
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

        # Проверка на столкновение с границами
        if x1 >= WIDTH or x1 < 0 or y1 >= HEIGHT or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change
        screen.fill(BLACK)

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
        if x1 == foodx and y1 == foody:
            score += 10
            Length_of_snake += 1
            foodx, foody = generate_food(snake_List) # Новое яблоко будет не на змейке
            
            # Повышение уровня каждые 3 яблока (30 очков)
            if score % 30 == 0:
                level += 1
                # Увеличиваем скорость только если она еще не достигла 15
                if current_speed < 15:
                    current_speed += 2

        # Отрисовка
        draw_grid()
        pygame.draw.rect(screen, RED, [foodx, foody, GRID_SIZE, GRID_SIZE])
        draw_snake(snake_List, x1_change, y1_change)
        show_score(score, level)
        
        pygame.display.update()
        clock.tick(current_speed)

    pygame.quit()
    quit()

if __name__ == "__main__":
    game_loop()