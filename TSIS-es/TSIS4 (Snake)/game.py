import pygame
import random
import time
from config import *
from db import save_score, get_personal_best

def draw_snake(screen, snake_list, color, has_shield):
    """Отрисовка змейки. Если есть щит — рисуем обводку."""
    for i, segment in enumerate(snake_list):
        # Рисуем сегмент (смещаем на FIELD_X/Y)
        rect = [segment[0] + FIELD_X, segment[1] + FIELD_Y, GRID_SIZE, GRID_SIZE]
        
        # Голова
        if i == len(snake_list) - 1:
            pygame.draw.rect(screen, color, rect)
            # Глаза
            eye_color = WHITE if has_shield else BLACK
            pygame.draw.rect(screen, eye_color, [rect[0] + 4, rect[1] + 4, 4, 4])
            pygame.draw.rect(screen, eye_color, [rect[0] + 12, rect[1] + 4, 4, 4])
        else:
            # Тело (чуть темнее основного цвета)
            body_color = [max(0, c - 50) for c in color]
            pygame.draw.rect(screen, body_color, rect)
        
        # Контур сегмента
        pygame.draw.rect(screen, BLACK, rect, 1)

def generate_item_pos(snake_list, walls, header_offset=0):
    """Генерирует свободную клетку (не на змейке и не в стене)"""
    while True:
        x = random.randrange(0, PLAY_WIDTH, GRID_SIZE)
        y = random.randrange(0, PLAY_HEIGHT, GRID_SIZE)
        if [x, y] not in snake_list and [x, y] not in walls:
            return [x, y]

def generate_walls(level, snake_list):
    """Создает стены, если уровень >= 3"""
    walls = []
    if level >= 3:
        # Количество блоков стены растет с уровнем
        num_walls = (level - 2) * 5 
        for _ in range(num_walls):
            while True:
                w = generate_item_pos(snake_list, walls)
                # Проверка: не ставим стену вплотную к голове (запас 3 клетки)
                head = snake_list[-1]
                dist = abs(w[0] - head[0]) + abs(w[1] - head[1])
                if dist > GRID_SIZE * 3:
                    walls.append(w)
                    break
    return walls

def run_game(screen, username, settings):
    """Основной цикл игры"""
    clock = pygame.time.Clock()
    
    # Состояние змейки
    x1, y1 = PLAY_WIDTH // 2, PLAY_HEIGHT // 2
    x1_change, y1_change = GRID_SIZE, 0
    snake_list = []
    snake_len = 3
    for i in range(snake_len):
        snake_list.append([x1 - (snake_len - 1 - i) * GRID_SIZE, y1])

    # Игровые параметры
    score = 0
    level = 1
    base_speed = 7
    speed_modifier = 0 # Для баффов
    personal_best = get_personal_best(username)
    
    # Эффекты
    has_shield = False
    powerup_timer = 0 # Когда закончится эффект
    
    # Объекты на поле
    walls = []
    
    # Еда (Type: 1-RED, 2-ORANGE, 3-GOLD, 4-POISON)
    def create_food():
        pos = generate_item_pos(snake_list, walls)
        r = random.random()
        if r > 0.9: return {"pos": pos, "type": 3, "expires": pygame.time.get_ticks() + 7000}
        if r > 0.7: return {"pos": pos, "type": 2, "expires": None}
        if r > 0.5: return {"pos": pos, "type": 4, "expires": None} # Яд
        return {"pos": pos, "type": 1, "expires": None}

    # Power-ups (Type: 1-Speed, 2-Slow, 3-Shield)
    def create_powerup():
        pos = generate_item_pos(snake_list, walls)
        p_type = random.randint(1, 3)
        return {"pos": pos, "type": p_type, "expires": pygame.time.get_ticks() + 8000}

    food = create_food()
    active_powerup = None
    next_powerup_spawn = pygame.time.get_ticks() + random.randint(5000, 15000)

    running = True
    while running:
        # 1. Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change == 0:
                    x1_change, y1_change = -GRID_SIZE, 0
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change, y1_change = GRID_SIZE, 0
                elif event.key == pygame.K_UP and y1_change == 0:
                    x1_change, y1_change = 0, -GRID_SIZE
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    x1_change, y1_change = 0, GRID_SIZE

        # 2. Логика движения
        x1 += x1_change
        y1 += y1_change
        head = [x1, y1]

        # 3. Проверка столкновений
        collision = False
        # Стены или границы
        if x1 < 0 or x1 >= PLAY_WIDTH or y1 < 0 or y1 >= PLAY_HEIGHT or head in walls or head in snake_list[:-1]:
            if has_shield:
                has_shield = False # Щит спасает один раз
                # Откатываем голову назад, чтобы не застрять в стене
                x1 -= x1_change
                y1 -= y1_change
                head = [x1, y1]
            else:
                collision = True

        if collision:
            save_score(username, score, level)
            return "GAMEOVER", score, level, personal_best

        snake_list.append(head)
        if len(snake_list) > snake_len:
            del snake_list[0]

        # 4. Поедание предметов
        # Еда
        if x1 == food["pos"][0] and y1 == food["pos"][1]:
            if food["type"] == 4: # ЯД
                snake_len -= 2
                if snake_len <= 1:
                    save_score(username, score, level)
                    return "GAMEOVER", score, level, personal_best
                # При похудении удаляем лишние сегменты из списка
                snake_list = snake_list[-snake_len:]
            else:
                score += food["type"] * 10
                snake_len += food["type"]
            
            # Рост уровня
            new_level = (score // 50) + 1
            if new_level > level:
                level = new_level
                walls = generate_walls(level, snake_list)
                base_speed = min(20, 7 + level)
            
            food = create_food()

        # Power-ups
        if active_powerup and x1 == active_powerup["pos"][0] and y1 == active_powerup["pos"][1]:
            if active_powerup["type"] == 1: # Скорость
                speed_modifier = 5
                powerup_timer = pygame.time.get_ticks() + 5000
            elif active_powerup["type"] == 2: # Замедление
                speed_modifier = -3
                powerup_timer = pygame.time.get_ticks() + 5000
            elif active_powerup["type"] == 3: # Щит
                has_shield = True
            active_powerup = None
            next_powerup_spawn = pygame.time.get_ticks() + random.randint(10000, 20000)

        # 5. Таймеры и спавн
        now = pygame.time.get_ticks()
        # Проверка исчезновения еды/баффов
        if food["expires"] and now > food["expires"]: food = create_food()
        if active_powerup and now > active_powerup["expires"]: active_powerup = None
        
        # Сброс эффектов скорости
        if now > powerup_timer: speed_modifier = 0
        
        # Спавн нового баффа
        if not active_powerup and now > next_powerup_spawn:
            active_powerup = create_powerup()

        # 6. Отрисовка
        screen.fill(DARK_GRAY)
        # Игровая область (черный квадрат)
        pygame.draw.rect(screen, BLACK, [FIELD_X, FIELD_Y, PLAY_WIDTH, PLAY_HEIGHT])
        
        if settings["grid_overlay"]:
            for x in range(0, PLAY_WIDTH + GRID_SIZE, GRID_SIZE):
                pygame.draw.line(screen, GRAY, (x + FIELD_X, FIELD_Y), (x + FIELD_X, PLAY_HEIGHT + FIELD_Y))
            for y in range(0, PLAY_HEIGHT + GRID_SIZE, GRID_SIZE):
                pygame.draw.line(screen, GRAY, (FIELD_X, y + FIELD_Y), (PLAY_WIDTH + FIELD_X, y + FIELD_Y))

        # Стены
        for w in walls:
            pygame.draw.rect(screen, BROWN, [w[0] + FIELD_X, w[1] + FIELD_Y, GRID_SIZE, GRID_SIZE])

        # Еда
        f_colors = {1: RED, 2: ORANGE, 3: GOLD, 4: DARK_RED}
        pygame.draw.ellipse(screen, f_colors[food["type"]], [food["pos"][0] + FIELD_X, food["pos"][1] + FIELD_Y, GRID_SIZE, GRID_SIZE])

        # Power-up
        if active_powerup:
            p_colors = {1: CYAN, 2: PURPLE, 3: BLUE}
            pygame.draw.rect(screen, p_colors[active_powerup["type"]], [active_powerup["pos"][0] + FIELD_X, active_powerup["pos"][1] + FIELD_Y, GRID_SIZE, GRID_SIZE])

        draw_snake(screen, snake_list, settings["snake_color"], has_shield)
        
        # Sidebar (Интерфейс справа)
        side_x = PLAY_WIDTH + (PADDING * 2)
        font = pygame.font.SysFont("comicsansms", 25)
        
        screen.blit(font.render(f"Player: {username}", True, WHITE), [side_x, 50])
        screen.blit(font.render(f"Score: {score}", True, YELLOW), [side_x, 90])
        screen.blit(font.render(f"Level: {level}", True, WHITE), [side_x, 130])
        screen.blit(font.render(f"Best: {personal_best}", True, GOLD), [side_x, 170])
        
        if has_shield:
            screen.blit(font.render("SHIELD ACTIVE", True, BLUE), [side_x, 250])
        if speed_modifier > 0:
            screen.blit(font.render("SPEED BOOST", True, CYAN), [side_x, 290])
        elif speed_modifier < 0:
            screen.blit(font.render("SLOW MOTION", True, PURPLE), [side_x, 290])

        pygame.display.update()
        clock.tick(base_speed + speed_modifier)