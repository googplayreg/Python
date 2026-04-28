import pygame

# Константы интерфейса
SIDEBAR_WIDTH = 300
ROAD_WIDTH = 800
TOTAL_WIDTH = ROAD_WIDTH + SIDEBAR_WIDTH
SCREEN_HEIGHT = 800

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)
RED = (200, 0, 0)
GOLD = (255, 215, 0)
CYAN = (0, 255, 255)

# Шрифты (инициализируются после pygame.init() в main.py)
# Здесь мы просто создаем обертку для удобства
class UI:
    def __init__(self):
        self.font_small = pygame.font.SysFont("Verdana", 20)
        self.font_medium = pygame.font.SysFont("Verdana", 35, bold=True)
        self.font_large = pygame.font.SysFont("Verdana", 60, bold=True)

    def draw_text(self, surface, text, pos, font, color=WHITE, center=False):
        """Утилита для отрисовки текста одной строкой."""
        text_obj = font.render(str(text), True, color)
        rect = text_obj.get_rect()
        if center:
            rect.center = pos
        else:
            rect.topleft = pos
        surface.blit(text_obj, rect)

class Button:
    """Класс для создания интерактивных кнопок."""
    def __init__(self, x, y, width, height, text, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False

    def draw(self, surface, font):
        # Меняем цвет при наведении
        current_color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, current_color, self.rect, border_radius=10)
        pygame.draw.rect(surface, WHITE, self.rect, width=2, border_radius=10)
        
        # Центрируем текст на кнопке
        text_obj = font.render(self.text, True, WHITE)
        text_rect = text_obj.get_rect(center=self.rect.center)
        surface.blit(text_obj, text_rect)

    def check_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def is_clicked(self, mouse_pos, mouse_up):
        return self.is_hovered and mouse_up

def draw_sidebar(surface, ui, score, distance, coins, powerup_status, leaderboard):
    """Отрисовка правой панели с данными и таблицей лидеров."""
    sidebar_rect = pygame.Rect(ROAD_WIDTH, 0, SIDEBAR_WIDTH, SCREEN_HEIGHT)
    pygame.draw.rect(surface, GRAY, sidebar_rect)
    pygame.draw.line(surface, WHITE, (ROAD_WIDTH, 0), (ROAD_WIDTH, SCREEN_HEIGHT), 3)

    # 1. Игровая статистика
    ui.draw_text(surface, "STATISTICS", (ROAD_WIDTH + 150, 40), ui.font_medium, GOLD, center=True)
    ui.draw_text(surface, f"Score: {score}", (ROAD_WIDTH + 20, 100), ui.font_small)
    ui.draw_text(surface, f"Distance: {int(distance)} m", (ROAD_WIDTH + 20, 140), ui.font_small)
    ui.draw_text(surface, f"Coins: {coins}", (ROAD_WIDTH + 20, 180), ui.font_small)
    
    # 2. Статус усилителя (пункт 3.3 и 3.4)
    status_color = CYAN if powerup_status["active"] else WHITE
    ui.draw_text(surface, f"Power-up: {powerup_status['name']}", (ROAD_WIDTH + 20, 240), ui.font_small, status_color)
    ui.draw_text(surface, f"Time: {powerup_status['time']}s", (ROAD_WIDTH + 20, 270), ui.font_small, status_color)

    # 3. Лидерборд (пункт 3.4.5)
    ui.draw_text(surface, "TOP 10 LOCAL", (ROAD_WIDTH + 150, 350), ui.font_medium, GOLD, center=True)
    
    y_offset = 400
    for i, entry in enumerate(leaderboard[:10]):
        color = GOLD if i == 0 else WHITE
        name = entry.get("name", "Unknown")
        pts = entry.get("score", 0)
        ui.draw_text(surface, f"{i+1}. {name}: {pts}", (ROAD_WIDTH + 20, y_offset), ui.font_small, color)
        y_offset += 30