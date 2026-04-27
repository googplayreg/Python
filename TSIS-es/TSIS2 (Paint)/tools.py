import pygame

def flood_fill(surface, start_pos, new_color):
    """
    Алгоритм заливки (Flood Fill) с использованием стека.
    Работает через get_at и set_at.
    """
    width, height = surface.get_size()
    target_color = surface.get_at(start_pos)
    
    # Если цвет в точке уже совпадает с нужным — ничего не делаем
    if target_color == new_color:
        return

    # Стек для хранения координат, которые нужно проверить
    stack = [start_pos]
    
    while stack:
        x, y = stack.pop()
        
        # Проверяем границы и совпадение цвета
        if 0 <= x < width and 0 <= y < height:
            if surface.get_at((x, y)) == target_color:
                surface.set_at((x, y), new_color)
                
                # Добавляем соседние пиксели в стек
                stack.append((x + 1, y))
                stack.append((x - 1, y))
                stack.append((x, y + 1))
                stack.append((x, y - 1))


# --- ФУНКЦИИ ГЕОМЕТРИИ ---

def draw_rect_shape(surface, color, start, end, width):
    r = pygame.Rect(start[0], start[1], end[0] - start[0], end[1] - start[1])
    r.normalize()
    pygame.draw.rect(surface, color, r, width)

def draw_circle_shape(surface, color, start, end, width):
    rad = int(((end[0] - start[0])**2 + (end[1] - start[1])**2)**0.5)
    if rad > 0:
        pygame.draw.circle(surface, color, start, rad, width)

def draw_square_shape(surface, color, start, end, width):
    side = max(abs(end[0] - start[0]), abs(end[1] - start[1]))
    dx = start[0] if end[0] > start[0] else start[0] - side
    dy = start[1] if end[1] > start[1] else start[1] - side
    if side > 0:
        pygame.draw.rect(surface, color, (dx, dy, side, side), width)

def draw_rtriangle_shape(surface, color, start, end, width):
    pygame.draw.polygon(surface, color, [start, (start[0], end[1]), end], width)

def draw_eqtriangle_shape(surface, color, start, end, width):
    w = end[0] - start[0]
    h = abs(w) * (3**0.5) / 2
    sy = 1 if end[1] > start[1] else -1
    pts = [
        (start[0] + w / 2, start[1]), 
        (start[0], start[1] + h * sy), 
        (end[0], start[1] + h * sy)
    ]
    pygame.draw.polygon(surface, color, pts, width)

def draw_rhombus_shape(surface, color, start, end, width):
    mx, my = (start[0] + end[0]) / 2, (start[1] + end[1]) / 2
    pts = [(mx, start[1]), (end[0], my), (mx, end[1]), (start[0], my)]
    pygame.draw.polygon(surface, color, pts, width)