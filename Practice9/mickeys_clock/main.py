import pygame
import sys
# Импортируем наш класс из соседнего файла clock.py
from clock import Clock 

def main():
    # 1. ИНИЦИАЛИЗАЦИЯ
    pygame.init()

    # Настройки окна
    # Можешь изменить эти числа под размер твоего циферблата
    WIDTH, HEIGHT = 686, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Интерактивные часы")

    # Таймер для контроля частоты кадров
    fps_controller = pygame.time.Clock()

    # 2. СОЗДАНИЕ ОБЪЕКТА ЧАСОВ
    # Передаем размеры экрана, чтобы часы знали, где их центр
    my_clock = Clock(WIDTH, HEIGHT)

    # Попробуем загрузить фон, если он у тебя есть
    # Если файла нет, программа просто пропустит этот шаг (благодаря try/except)
    background = None
    try:
        background = pygame.image.load('mickeys_clock/images/clock_face.png').convert()
        background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    except Exception as e:
        print(f"Фон не найден, ошибка: {e}")
        background = None # Чтобы программа знала, что рисовать нечего

    # 3. ГЛАВНЫЙ ЦИКЛ
    running = True
    while running:
        
        # --- Обработка событий ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # --- Логика (Update) ---
        # Здесь наш объект Clock лезет в систему, берет время и считает углы
        my_clock.update()

        # --- Отрисовка (Draw) ---
        if background:
            screen.blit(background, (0, 0))
        else:
            screen.fill((230, 230, 230)) # Светло-серый фон, если нет картинки

        # Рисуем стрелки поверх фона
        my_clock.draw(screen)

        # Обновляем экран
        pygame.display.flip()

        # Ограничиваем цикл (30 кадров в секунду для часов — идеально)
        fps_controller.tick(30)

    # ВЫХОД
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()