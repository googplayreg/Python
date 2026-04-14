import pygame
from ball import Ball  # Импортируем класс

# 1. Инициализация Pygame
pygame.init()

# Настройки окна (как в задании: белый фон, красный шарик)
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Moving Ball Game")

# Цвета
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# 2. Создаем объект шарика
# Ставим его в центр экрана
# Параметры: x, y, radius, color, step
ball = Ball(WIDTH // 2, HEIGHT // 2, 25, RED, 20)

clock = pygame.time.Clock()
running = True

# --- ГЛАВНЫЙ ЦИКЛ ---
while running:
    # 1. Обработка системных событий (выход из программы)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Здесь больше не проверяем стрелки через KEYDOWN

    # 2. Проверка зажатых клавиш (Continuous movement)
    keys = pygame.key.get_pressed()

    if keys[pygame.K_UP]:
        ball.move("UP", WIDTH, HEIGHT)
    if keys[pygame.K_DOWN]:
        ball.move("DOWN", WIDTH, HEIGHT)
    if keys[pygame.K_LEFT]:
        ball.move("LEFT", WIDTH, HEIGHT)
    if keys[pygame.K_RIGHT]:
        ball.move("RIGHT", WIDTH, HEIGHT)

    # Отрисовка
    screen.fill(WHITE) # Заливаем фон белым
    
    ball.draw(screen)  # Рисуем шарик

    # Обновление экрана
    pygame.display.flip()
    
    # Ограничиваем FPS
    clock.tick(60)

pygame.quit()