import pygame
from datetime import datetime
import tools # Импортируем файл с инструментами
import os

# Инициализация
pygame.init()
WIDTH, HEIGHT = 1250, 850
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Paint Advanced (TSIS Edition)")

# Цвета
WHITE, BLACK = (255, 255, 255), (0, 0, 0)
PANEL_GRAY = (210, 210, 210)
NOTIFY_COLOR = (50, 50, 50)  # Для уведомления
COLORS = [(0, 0, 0), (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (0, 255, 255), (255, 0, 255)]

# Настройки
PANEL_HEIGHT = 160
current_color = BLACK
current_tool = 'pencil'
BRUSH_SIZES = [2, 5, 10, 20, 35, 50]
brush_size = BRUSH_SIZES[1]
drawing = False
start_pos = (0, 0)
last_pos = None

# Текст
active_text, is_typing, text_pos = "", False, (0, 0)

canvas = pygame.Surface((WIDTH, HEIGHT - PANEL_HEIGHT))
canvas.fill(WHITE)
main_font = pygame.font.SysFont("Arial", 36)
font = pygame.font.SysFont("Arial", 22)
ui_font = pygame.font.SysFont("Arial", 20, bold=True)

save_notify_time = 0   # Время для сообщения

def draw_button(surf, rect, text, is_active, color=PANEL_GRAY):
    pygame.draw.rect(surf, color, rect, border_radius=8)
    b_color = BLACK if is_active else (140, 140, 140)
    pygame.draw.rect(surf, b_color, rect, 3 if is_active else 1, border_radius=8)
    if text:
        text_surf = font.render(text, True, BLACK)
        surf.blit(text_surf, text_surf.get_rect(center=rect.center))

# Разметка кнопок
shapes_and_tools = ['pencil', 'line', 'rect', 'circle', 'square', 'rtriangle', 'eqtriangle', 'rhombus', 'fill', 'text', 'eraser']
tool_btns = {name: pygame.Rect(10 + i*75, 45, 70, 40) for i, name in enumerate(shapes_and_tools)}
size_btns = {BRUSH_SIZES[i]: pygame.Rect(10 + i*55, 110, 45, 35) for i in range(len(BRUSH_SIZES))}
color_btns = {color: pygame.Rect(850 + i*50, 45, 40, 40) for i, color in enumerate(COLORS)}

running = True
clock = pygame.time.Clock()

while running:
    mouse_pos = pygame.mouse.get_pos()
    current_time = pygame.time.get_ticks()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if is_typing:
                if event.key == pygame.K_RETURN:
                    txt_img = main_font.render(active_text, True, current_color)
                    canvas.blit(txt_img, text_pos)
                    active_text, is_typing = "", False
                elif event.key == pygame.K_ESCAPE:
                    active_text, is_typing = "", False
                elif event.key == pygame.K_BACKSPACE: 
                    active_text = active_text[:-1]
                else: 
                    active_text += event.unicode
            else:
                if pygame.K_1 <= event.key <= pygame.K_6:
                    brush_size = BRUSH_SIZES[event.key - pygame.K_1]
                if event.key == pygame.K_s and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                    # 1. Получаем путь к папке, в которой лежит этот запущенный файл
                    project_folder = os.path.dirname(os.path.abspath(__file__))
    
                    # 2. Формируем имя файла
                    filename = f"paint_{datetime.now().strftime('%H-%M-%S_%d-%m-%Y')}.png"
    
                    # 3. Соединяем путь к папке и имя файла в один полный путь
                    full_path = os.path.join(project_folder, filename)
    
                    # 4. Сохраняем по полному пути
                    pygame.image.save(canvas, full_path)
    
                    save_notify_time = current_time + 2000 # Уведомление

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.pos[1] < PANEL_HEIGHT:
                for n, r in tool_btns.items():
                    if r.collidepoint(event.pos): current_tool = n
                for s, r in size_btns.items():
                    if r.collidepoint(event.pos): brush_size = s
                for c, r in color_btns.items():
                    if r.collidepoint(event.pos): current_color = c
            else:
                drawing = True
                start_pos = (event.pos[0], event.pos[1] - PANEL_HEIGHT)
                last_pos = start_pos
                if current_tool == 'fill': tools.flood_fill(canvas, start_pos, current_color)
                if current_tool == 'text': is_typing, text_pos = True, start_pos

        if event.type == pygame.MOUSEBUTTONUP and drawing:
            drawing = False
            end_pos = (event.pos[0], event.pos[1] - PANEL_HEIGHT)
            
            # ФИНАЛЬНАЯ ОТРИСОВКА (используем функции из tools.py)
            if current_tool == 'line': pygame.draw.line(canvas, current_color, start_pos, end_pos, brush_size)
            elif current_tool == 'rect': tools.draw_rect_shape(canvas, current_color, start_pos, end_pos, brush_size)
            elif current_tool == 'circle': tools.draw_circle_shape(canvas, current_color, start_pos, end_pos, brush_size)
            elif current_tool == 'square': tools.draw_square_shape(canvas, current_color, start_pos, end_pos, brush_size)
            elif current_tool == 'rtriangle': tools.draw_rtriangle_shape(canvas, current_color, start_pos, end_pos, brush_size)
            elif current_tool == 'eqtriangle': tools.draw_eqtriangle_shape(canvas, current_color, start_pos, end_pos, brush_size)
            elif current_tool == 'rhombus': tools.draw_rhombus_shape(canvas, current_color, start_pos, end_pos, brush_size)

        if event.type == pygame.MOUSEMOTION and drawing:
            curr = (event.pos[0], event.pos[1] - PANEL_HEIGHT)
            if curr[1] >= 0:
                if current_tool == 'pencil':
                    pygame.draw.line(canvas, current_color, last_pos, curr, brush_size)
                    pygame.draw.circle(canvas, current_color, curr, brush_size // 2)
                    last_pos = curr
                elif current_tool == 'eraser':
                    pygame.draw.line(canvas, WHITE, last_pos, curr, brush_size * 2)
                    pygame.draw.circle(canvas, WHITE, curr, brush_size)
                    last_pos = curr

    # Рендеринг интерфейса и фона
    screen.fill(PANEL_GRAY)
    screen.blit(canvas, (0, PANEL_HEIGHT))

    # Предпросмотр для всех фигур
    if drawing and current_tool in ['line', 'rect', 'circle', 'square', 'rtriangle', 'eqtriangle', 'rhombus']:
        temp = pygame.Surface((WIDTH, HEIGHT - PANEL_HEIGHT), pygame.SRCALPHA)
        cur_m = (mouse_pos[0], mouse_pos[1] - PANEL_HEIGHT)
        col = (*current_color, 130) # Прозрачный цвет
        
        # Вызываем те же функции, что и выше, но рисуем на temp поверхности
        if current_tool == 'line': pygame.draw.line(temp, col, start_pos, cur_m, brush_size)
        elif current_tool == 'rect': tools.draw_rect_shape(temp, col, start_pos, cur_m, brush_size)
        elif current_tool == 'circle': tools.draw_circle_shape(temp, col, start_pos, cur_m, brush_size)
        elif current_tool == 'square': tools.draw_square_shape(temp, col, start_pos, cur_m, brush_size)
        elif current_tool == 'rtriangle': tools.draw_rtriangle_shape(temp, col, start_pos, cur_m, brush_size)
        elif current_tool == 'eqtriangle': tools.draw_eqtriangle_shape(temp, col, start_pos, cur_m, brush_size)
        elif current_tool == 'rhombus': tools.draw_rhombus_shape(temp, col, start_pos, cur_m, brush_size)
        
        screen.blit(temp, (0, PANEL_HEIGHT))

    if is_typing:
        t_img = main_font.render(active_text + "|", True, current_color)
        screen.blit(t_img, (text_pos[0], text_pos[1] + PANEL_HEIGHT))

    # Панель интерфейса
    pygame.draw.line(screen, BLACK, (0, PANEL_HEIGHT), (WIDTH, PANEL_HEIGHT), 2)
    screen.blit(ui_font.render("Tools:", True, BLACK), (15, 15))
    for n, r in tool_btns.items(): draw_button(screen, r, n.replace('rtriangle','R-Tri').replace('eqtriangle','Eq-Tri').capitalize(), current_tool == n)
    
    screen.blit(ui_font.render(f"Brush Size (1-6):", True, BLACK), (15, 88))
    for s, r in size_btns.items(): 
        label = str(list(BRUSH_SIZES).index(s) + 1)
        draw_button(screen, r, label, brush_size == s)
        
    screen.blit(ui_font.render("Palette:", True, BLACK), (850, 15))
    for c, r in color_btns.items(): draw_button(screen, r, "", current_color == c, c)

    # Отрисовка уведомления о сохранении картинки
    if current_time < save_notify_time:
        notify_rect = pygame.Rect(WIDTH - 180, HEIGHT - 60, 160, 40)
        pygame.draw.rect(screen, NOTIFY_COLOR, notify_rect, border_radius=10)
        msg = ui_font.render("Image Saved!", True, WHITE)
        screen.blit(msg, msg.get_rect(center=notify_rect.center))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()