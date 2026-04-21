import pygame

# Инициализация Pygame
pygame.init()

# Настройки экрана (делаем большой холст)
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Paint")

# Базовые цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PANEL_GRAY = (220, 220, 220)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Настройки интерфейса
PANEL_HEIGHT = 100
current_color = RED
current_tool = 'rect' # 'rect', 'circle', 'eraser'
drawing = False
start_pos = (0, 0)
last_pos = None # Для ластика

# Создаем отдельную поверхность для холста
# Высота холста = общая высота минус высота панели инструментов
canvas = pygame.Surface((WIDTH, HEIGHT - PANEL_HEIGHT))
canvas.fill(WHITE)

font = pygame.font.SysFont(None, 30)

def draw_button(surface, rect, text, is_active, color=PANEL_GRAY):
    """Вспомогательная функция для отрисовки кнопок"""
    pygame.draw.rect(surface, color, rect, border_radius=5)
    # Если кнопка активна, рисуем толстую черную рамку, иначе тонкую серую
    border_color = BLACK if is_active else (150, 150, 150)
    border_width = 3 if is_active else 1
    pygame.draw.rect(surface, border_color, rect, border_width, border_radius=5)
    
    text_surf = font.render(text, True, BLACK)
    text_rect = text_surf.get_rect(center=rect.center)
    surface.blit(text_surf, text_rect)

# Размечаем области кнопок (x, y, ширина, высота)
btn_rect   = pygame.Rect(20, 25, 100, 50)
btn_circle = pygame.Rect(130, 25, 100, 50)
btn_eraser = pygame.Rect(240, 25, 100, 50)

# Кнопки выбора цвета
btn_red    = pygame.Rect(400, 25, 60, 50)
btn_green  = pygame.Rect(470, 25, 60, 50)
btn_blue   = pygame.Rect(540, 25, 60, 50)

running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # Левый клик
                mouse_x, mouse_y = event.pos
                
                # Проверяем клики по панели инструментов
                if mouse_y <= PANEL_HEIGHT:
                    if btn_rect.collidepoint(mouse_x, mouse_y): current_tool = 'rect'
                    elif btn_circle.collidepoint(mouse_x, mouse_y): current_tool = 'circle'
                    elif btn_eraser.collidepoint(mouse_x, mouse_y): current_tool = 'eraser'
                    
                    elif btn_red.collidepoint(mouse_x, mouse_y): current_color = RED
                    elif btn_green.collidepoint(mouse_x, mouse_y): current_color = GREEN
                    elif btn_blue.collidepoint(mouse_x, mouse_y): current_color = BLUE
                else:
                    # Начинаем рисовать на холсте
                    drawing = True
                    # Корректируем координату Y, так как холст начинается ниже панели
                    start_pos = (mouse_x, mouse_y - PANEL_HEIGHT)
                    last_pos = start_pos # Запоминаем точку старта для ластика
                    
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and drawing:
                drawing = False
                mouse_x, mouse_y = event.pos
                end_pos = (mouse_x, mouse_y - PANEL_HEIGHT)
                
                # Финальная отрисовка фигур при отпускании кнопки
                if current_tool == 'rect':
                    r_width = end_pos[0] - start_pos[0]
                    r_height = end_pos[1] - start_pos[1]
                    # Обработка ситуаций, когда мышь тянут влево или вверх
                    draw_x = start_pos[0] if r_width > 0 else end_pos[0]
                    draw_y = start_pos[1] if r_height > 0 else end_pos[1]
                    pygame.draw.rect(canvas, current_color, (draw_x, draw_y, abs(r_width), abs(r_height)))
                    
                elif current_tool == 'circle':
                    # Считаем радиус и центр
                    radius = max(abs(end_pos[0] - start_pos[0]), abs(end_pos[1] - start_pos[1])) // 2
                    center_x = min(start_pos[0], end_pos[0]) + radius
                    center_y = min(start_pos[1], end_pos[1]) + radius
                    if radius > 0:
                        pygame.draw.circle(canvas, current_color, (center_x, center_y), radius)

                last_pos = None

        elif event.type == pygame.MOUSEMOTION:
            if drawing:
                mouse_x, mouse_y = event.pos
                current_pos = (mouse_x, mouse_y - PANEL_HEIGHT)
                
                # Блокируем рисование, если курсор ушел на панель инструментов
                if current_pos[1] < 0:
                    continue
                    
                # Ластик стирает в реальном времени при движении
                if current_tool == 'eraser':
                    pygame.draw.line(canvas, WHITE, last_pos, current_pos, 50)
                    pygame.draw.circle(canvas, WHITE, current_pos, 25)
                    last_pos = current_pos

    # 1. Заливаем основной экран фоном панели
    screen.fill(PANEL_GRAY)
    
    # 2. Рисуем холст со всеми сохраненными рисунками
    screen.blit(canvas, (0, PANEL_HEIGHT))
    
    # 3. Отрисовка "предпросмотра" фигур во время перетаскивания
    if drawing and current_tool in ['rect', 'circle']:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if mouse_y > PANEL_HEIGHT:
            # Создаем временную прозрачную поверхность для предпросмотра
            temp_surface = pygame.Surface((WIDTH, HEIGHT - PANEL_HEIGHT), pygame.SRCALPHA)
            end_pos = (mouse_x, mouse_y - PANEL_HEIGHT)
            
            if current_tool == 'rect':
                r_w = end_pos[0] - start_pos[0]
                r_h = end_pos[1] - start_pos[1]
                d_x = start_pos[0] if r_w > 0 else end_pos[0]
                d_y = start_pos[1] if r_h > 0 else end_pos[1]
                pygame.draw.rect(temp_surface, (*current_color, 120), (d_x, d_y, abs(r_w), abs(r_h)))
                
            elif current_tool == 'circle':
                rad = max(abs(end_pos[0] - start_pos[0]), abs(end_pos[1] - start_pos[1])) // 2
                c_x = min(start_pos[0], end_pos[0]) + rad
                c_y = min(start_pos[1], end_pos[1]) + rad
                if rad > 0:
                    pygame.draw.circle(temp_surface, (*current_color, 120), (c_x, c_y), rad)
                    
            screen.blit(temp_surface, (0, PANEL_HEIGHT))
            
    # 4. Отрисовка элементов панели поверх всего
    pygame.draw.line(screen, BLACK, (0, PANEL_HEIGHT), (WIDTH, PANEL_HEIGHT), 2) # Линия-разделитель
    
    draw_button(screen, btn_rect, "Rect", current_tool == 'rect')
    draw_button(screen, btn_circle, "Circle", current_tool == 'circle')
    draw_button(screen, btn_eraser, "Eraser", current_tool == 'eraser')
    
    draw_button(screen, btn_red, "R", current_color == RED, RED)
    draw_button(screen, btn_green, "G", current_color == GREEN, GREEN)
    draw_button(screen, btn_blue, "B", current_color == BLUE, BLUE)

    pygame.display.flip()
    clock.tick(120)

pygame.quit()