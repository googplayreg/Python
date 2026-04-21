import pygame

# Инициализация Pygame
pygame.init()

# Настройки экрана (делаем большой холст)
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Paint")

# Базовые цвета + 3 новых
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PANEL_GRAY = (220, 220, 220)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)

# Настройки интерфейса
PANEL_HEIGHT = 100
current_color = RED
current_tool = 'rect' # Доступны: 'rect', 'circle', 'square', 'rtriangle', 'eqtriangle', 'rhombus', 'eraser'
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
    
    # Если передан текст, центрируем и рисуем его
    if text:
        text_surf = font.render(text, True, BLACK)
        text_rect = text_surf.get_rect(center=rect.center)
        surface.blit(text_surf, text_rect)

# Размечаем области кнопок инструментов (x, y, ширина, высота)
btn_rect       = pygame.Rect(10, 30, 80, 50)
btn_circle     = pygame.Rect(100, 30, 80, 50)
btn_square     = pygame.Rect(190, 30, 90, 50)
btn_rtriangle  = pygame.Rect(290, 30, 90, 50)
btn_eqtriangle = pygame.Rect(390, 30, 90, 50)
btn_rhombus    = pygame.Rect(490, 30, 100, 50)
btn_eraser     = pygame.Rect(600, 30, 80, 50)

# Кнопки выбора цвета (уменьшены, чтобы быть похожими на палитру)
color_start_x = 750
btn_red     = pygame.Rect(color_start_x, 35, 40, 40)
btn_green   = pygame.Rect(color_start_x + 50, 35, 40, 40)
btn_blue    = pygame.Rect(color_start_x + 100, 35, 40, 40)
btn_yellow  = pygame.Rect(color_start_x + 150, 35, 40, 40)
btn_cyan    = pygame.Rect(color_start_x + 200, 35, 40, 40)
btn_magenta = pygame.Rect(color_start_x + 250, 35, 40, 40)

# Текст над цветами
colors_label = font.render("Colors", True, BLACK)

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
                    # Инструменты
                    if btn_rect.collidepoint(mouse_x, mouse_y): current_tool = 'rect'
                    elif btn_circle.collidepoint(mouse_x, mouse_y): current_tool = 'circle'
                    elif btn_square.collidepoint(mouse_x, mouse_y): current_tool = 'square'
                    elif btn_rtriangle.collidepoint(mouse_x, mouse_y): current_tool = 'rtriangle'
                    elif btn_eqtriangle.collidepoint(mouse_x, mouse_y): current_tool = 'eqtriangle'
                    elif btn_rhombus.collidepoint(mouse_x, mouse_y): current_tool = 'rhombus'
                    elif btn_eraser.collidepoint(mouse_x, mouse_y): current_tool = 'eraser'
                    
                    # Цвета
                    elif btn_red.collidepoint(mouse_x, mouse_y): current_color = RED
                    elif btn_green.collidepoint(mouse_x, mouse_y): current_color = GREEN
                    elif btn_blue.collidepoint(mouse_x, mouse_y): current_color = BLUE
                    elif btn_yellow.collidepoint(mouse_x, mouse_y): current_color = YELLOW
                    elif btn_cyan.collidepoint(mouse_x, mouse_y): current_color = CYAN
                    elif btn_magenta.collidepoint(mouse_x, mouse_y): current_color = MAGENTA
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

                elif current_tool == 'square':
                    # Квадрат: стороны всегда равны по максимальному смещению
                    r_width = end_pos[0] - start_pos[0]
                    r_height = end_pos[1] - start_pos[1]
                    side = max(abs(r_width), abs(r_height))
                    draw_x = start_pos[0] if r_width > 0 else start_pos[0] - side
                    draw_y = start_pos[1] if r_height > 0 else start_pos[1] - side
                    if side > 0:
                        pygame.draw.rect(canvas, current_color, (draw_x, draw_y, side, side))

                elif current_tool == 'rtriangle':
                    # Прямоугольный треугольник (прямой угол в точке старта)
                    p1 = start_pos
                    p2 = (start_pos[0], end_pos[1])
                    p3 = end_pos
                    pygame.draw.polygon(canvas, current_color, [p1, p2, p3])

                elif current_tool == 'eqtriangle':
                    # Равносторонний треугольник (считаем высоту математически)
                    width = end_pos[0] - start_pos[0]
                    side = abs(width)
                    height = side * (3 ** 0.5) / 2
                    sign_y = 1 if end_pos[1] >= start_pos[1] else -1
                    
                    p1 = (start_pos[0] + width / 2, start_pos[1])
                    p2 = (start_pos[0], start_pos[1] + height * sign_y)
                    p3 = (end_pos[0], start_pos[1] + height * sign_y)
                    pygame.draw.polygon(canvas, current_color, [p1, p2, p3])

                elif current_tool == 'rhombus':
                    # Ромб (вершины по серединам сторон описывающего прямоугольника)
                    mid_x = (start_pos[0] + end_pos[0]) / 2
                    mid_y = (start_pos[1] + end_pos[1]) / 2
                    p1 = (mid_x, start_pos[1])
                    p2 = (end_pos[0], mid_y)
                    p3 = (mid_x, end_pos[1])
                    p4 = (start_pos[0], mid_y)
                    pygame.draw.polygon(canvas, current_color, [p1, p2, p3, p4])

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
    if drawing and current_tool in ['rect', 'circle', 'square', 'rtriangle', 'eqtriangle', 'rhombus']:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if mouse_y > PANEL_HEIGHT:
            # Создаем временную прозрачную поверхность для предпросмотра
            temp_surface = pygame.Surface((WIDTH, HEIGHT - PANEL_HEIGHT), pygame.SRCALPHA)
            end_pos = (mouse_x, mouse_y - PANEL_HEIGHT)
            color_with_alpha = (*current_color, 120)
            
            if current_tool == 'rect':
                r_w = end_pos[0] - start_pos[0]
                r_h = end_pos[1] - start_pos[1]
                d_x = start_pos[0] if r_w > 0 else end_pos[0]
                d_y = start_pos[1] if r_h > 0 else end_pos[1]
                pygame.draw.rect(temp_surface, color_with_alpha, (d_x, d_y, abs(r_w), abs(r_h)))
                
            elif current_tool == 'circle':
                rad = max(abs(end_pos[0] - start_pos[0]), abs(end_pos[1] - start_pos[1])) // 2
                c_x = min(start_pos[0], end_pos[0]) + rad
                c_y = min(start_pos[1], end_pos[1]) + rad
                if rad > 0:
                    pygame.draw.circle(temp_surface, color_with_alpha, (c_x, c_y), rad)

            elif current_tool == 'square':
                r_w = end_pos[0] - start_pos[0]
                r_h = end_pos[1] - start_pos[1]
                side = max(abs(r_w), abs(r_h))
                d_x = start_pos[0] if r_w > 0 else start_pos[0] - side
                d_y = start_pos[1] if r_h > 0 else start_pos[1] - side
                if side > 0:
                    pygame.draw.rect(temp_surface, color_with_alpha, (d_x, d_y, side, side))

            elif current_tool == 'rtriangle':
                p1 = start_pos
                p2 = (start_pos[0], end_pos[1])
                p3 = end_pos
                pygame.draw.polygon(temp_surface, color_with_alpha, [p1, p2, p3])

            elif current_tool == 'eqtriangle':
                width = end_pos[0] - start_pos[0]
                side = abs(width)
                height = side * (3 ** 0.5) / 2
                sign_y = 1 if end_pos[1] >= start_pos[1] else -1
                p1 = (start_pos[0] + width / 2, start_pos[1])
                p2 = (start_pos[0], start_pos[1] + height * sign_y)
                p3 = (end_pos[0], start_pos[1] + height * sign_y)
                pygame.draw.polygon(temp_surface, color_with_alpha, [p1, p2, p3])

            elif current_tool == 'rhombus':
                mid_x = (start_pos[0] + end_pos[0]) / 2
                mid_y = (start_pos[1] + end_pos[1]) / 2
                p1 = (mid_x, start_pos[1])
                p2 = (end_pos[0], mid_y)
                p3 = (mid_x, end_pos[1])
                p4 = (start_pos[0], mid_y)
                pygame.draw.polygon(temp_surface, color_with_alpha, [p1, p2, p3, p4])
                    
            screen.blit(temp_surface, (0, PANEL_HEIGHT))
            
    # 4. Отрисовка элементов панели поверх всего
    pygame.draw.line(screen, BLACK, (0, PANEL_HEIGHT), (WIDTH, PANEL_HEIGHT), 2) # Линия-разделитель
    
    # Кнопки инструментов
    draw_button(screen, btn_rect, "Rect", current_tool == 'rect')
    draw_button(screen, btn_circle, "Circle", current_tool == 'circle')
    draw_button(screen, btn_square, "Square", current_tool == 'square')
    draw_button(screen, btn_rtriangle, "R-Tri", current_tool == 'rtriangle')
    draw_button(screen, btn_eqtriangle, "Eq-Tri", current_tool == 'eqtriangle')
    draw_button(screen, btn_rhombus, "Rhombus", current_tool == 'rhombus')
    draw_button(screen, btn_eraser, "Eraser", current_tool == 'eraser')
    
    # Текст над палитрой
    screen.blit(colors_label, (color_start_x + 85, 10))
    
    # Кнопки цветов (без текста, пустая строка)
    draw_button(screen, btn_red, "", current_color == RED, RED)
    draw_button(screen, btn_green, "", current_color == GREEN, GREEN)
    draw_button(screen, btn_blue, "", current_color == BLUE, BLUE)
    draw_button(screen, btn_yellow, "", current_color == YELLOW, YELLOW)
    draw_button(screen, btn_cyan, "", current_color == CYAN, CYAN)
    draw_button(screen, btn_magenta, "", current_color == MAGENTA, MAGENTA)

    pygame.display.flip()
    clock.tick(120)

pygame.quit()