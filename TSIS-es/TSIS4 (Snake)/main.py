import pygame
import sys
from config import *
from db import init_db, get_top_10, save_score
from game import run_game

# Инициализация
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Pygame Snake Advanced (TSIS Edition)")
clock = pygame.time.Clock()

# Шрифты
font_main = pygame.font.SysFont("bahnschrift", 40)
font_sub = pygame.font.SysFont("bahnschrift", 25)
font_button = pygame.font.SysFont("bahnschrift", 30)

class Button:
    """Класс для создания интерактивных кнопок"""
    def __init__(self, text, x, y, w, h, color, hover_color):
        self.text = text
        self.rect = pygame.Rect(x, y, w, h)
        self.color = color
        self.hover_color = hover_color

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        current_color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color
        pygame.draw.rect(screen, current_color, self.rect, border_radius=10)
        pygame.draw.rect(screen, WHITE, self.rect, 2, border_radius=10)
        
        text_surf = font_button.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False

def draw_text(text, font, color, x, y, center=False):
    surf = font.render(text, True, color)
    rect = surf.get_rect(center=(x, y) if center else (x, y))
    screen.blit(surf, rect)

def input_username():
    """Экран ввода имени пользователя"""
    username = ""
    active = True
    while active:
        screen.fill(DARK_GRAY)
        draw_text("ENTER YOUR NAME:", font_main, GOLD, WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 50, True)
        
        # Поле ввода
        input_rect = pygame.Rect(WINDOW_WIDTH//2 - 150, WINDOW_HEIGHT//2, 300, 50)
        pygame.draw.rect(screen, BLACK, input_rect)
        pygame.draw.rect(screen, WHITE, input_rect, 2)
        
        draw_text(username, font_button, WHITE, input_rect.centerx, input_rect.centery, True)
        draw_text("Press ENTER to start", font_sub, GRAY, WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 80, True)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and username.strip():
                    active = False
                elif event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                else:
                    if len(username) < 15 and event.unicode.isalnum():
                        username += event.unicode

        pygame.display.update()
        clock.tick(30)
    return username

def leaderboard_screen():
    """Экран Топ-10 из базы данных"""
    running = True
    back_btn = Button("BACK", WINDOW_WIDTH//2 - 100, WINDOW_HEIGHT - 80, 200, 50, GRAY, BLACK)
    top_data = get_top_10() # Запрос к БД

    while running:
        screen.fill(DARK_GRAY)
        draw_text("LEADERBOARD (TOP 10)", font_main, GOLD, WINDOW_WIDTH//2, 50, True)
        
        # Заголовки таблицы
        headers = ["RANK", "PLAYER", "SCORE", "LVL", "DATE"]
        header_x = [100, 250, 450, 550, 700]
        for h, x in zip(headers, header_x):
            draw_text(h, font_sub, YELLOW, x, 120)

        # Данные
        for i, row in enumerate(top_data):
            y = 170 + i * 35
            draw_text(str(i+1), font_sub, WHITE, header_x[0], y)
            draw_text(str(row[0]), font_sub, WHITE, header_x[1], y)
            draw_text(str(row[1]), font_sub, WHITE, header_x[2], y)
            draw_text(str(row[2]), font_sub, WHITE, header_x[3], y)
            draw_text(str(row[3]), font_sub, WHITE, header_x[4], y)

        back_btn.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if back_btn.is_clicked(event): running = False
        
        pygame.display.update()
        clock.tick(30)

def settings_screen():
    """Экран настроек (JSON)"""
    global USER_SETTINGS
    running = True
    
    # Кнопки цветов
    colors = {"GREEN": [0, 255, 0], "CYAN": [0, 255, 255], "MAGENTA": [255, 0, 255]}
    color_btns = []
    for i, (name, val) in enumerate(colors.items()):
        color_btns.append((Button(name, 150 + i*200, 250, 150, 50, DARK_GRAY, val), val))

    grid_btn = Button(f"GRID: {'ON' if USER_SETTINGS['grid_overlay'] else 'OFF'}", WINDOW_WIDTH//2 - 150, 350, 300, 50, GRAY, BLACK)
    save_btn = Button("SAVE & BACK", WINDOW_WIDTH//2 - 150, 500, 300, 60, (0, 100, 0), (0, 150, 0))

    while running:
        screen.fill(DARK_GRAY)
        draw_text("SETTINGS", font_main, WHITE, WINDOW_WIDTH//2, 80, True)
        draw_text("Pick Snake Color:", font_sub, WHITE, WINDOW_WIDTH//2, 200, True)

        for btn, val in color_btns:
            btn.draw(screen)
        grid_btn.draw(screen)
        save_btn.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            
            for btn, val in color_btns:
                if btn.is_clicked(event): USER_SETTINGS["snake_color"] = val
            
            if grid_btn.is_clicked(event):
                USER_SETTINGS["grid_overlay"] = not USER_SETTINGS["grid_overlay"]
                grid_btn.text = f"GRID: {'ON' if USER_SETTINGS['grid_overlay'] else 'OFF'}"
            
            if save_btn.is_clicked(event):
                save_settings(USER_SETTINGS)
                running = False

        pygame.display.update()
        clock.tick(30)

def game_over_screen(score, lvl, best):
    """Экран окончания игры"""
    running = True
    retry_btn = Button("RETRY", WINDOW_WIDTH//2 - 150, 400, 300, 50, (0, 100, 0), (0, 150, 0))
    menu_btn = Button("MAIN MENU", WINDOW_WIDTH//2 - 150, 470, 300, 50, GRAY, BLACK)

    while running:
        screen.fill(BLACK)
        draw_text("GAME OVER", font_main, RED, WINDOW_WIDTH//2, 100, True)
        draw_text(f"SCORE: {score}", font_button, WHITE, WINDOW_WIDTH//2, 200, True)
        draw_text(f"LEVEL: {lvl}", font_sub, WHITE, WINDOW_WIDTH//2, 250, True)
        draw_text(f"PERSONAL BEST: {best}", font_sub, GOLD, WINDOW_WIDTH//2, 300, True)

        retry_btn.draw(screen)
        menu_btn.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if retry_btn.is_clicked(event): return "RETRY"
            if menu_btn.is_clicked(event): return "MENU"

        pygame.display.update()
        clock.tick(30)

def main_menu():
    """Главное меню"""
    init_db() # Создаем таблицы при запуске
    username = input_username()
    
    play_btn = Button("PLAY", WINDOW_WIDTH//2 - 150, 200, 300, 60, (0, 150, 0), (0, 200, 0))
    lb_btn = Button("LEADERBOARD", WINDOW_WIDTH//2 - 150, 280, 300, 60, GRAY, BLACK)
    set_btn = Button("SETTINGS", WINDOW_WIDTH//2 - 150, 360, 300, 60, GRAY, BLACK)
    quit_btn = Button("QUIT", WINDOW_WIDTH//2 - 150, 440, 300, 60, (150, 0, 0), (200, 0, 0))

    while True:
        screen.fill(DARK_GRAY)
        draw_text(f"WELCOME, {username}!", font_main, GOLD, WINDOW_WIDTH//2, 100, True)
        
        play_btn.draw(screen)
        lb_btn.draw(screen)
        set_btn.draw(screen)
        quit_btn.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            
            if play_btn.is_clicked(event):
                result = run_game(screen, username, USER_SETTINGS)
                while result[0] == "GAMEOVER":
                    choice = game_over_screen(result[1], result[2], result[3])
                    if choice == "RETRY":
                        result = run_game(screen, username, USER_SETTINGS)
                    else:
                        break
            
            if lb_btn.is_clicked(event): leaderboard_screen()
            if set_btn.is_clicked(event): settings_screen()
            if quit_btn.is_clicked(event): pygame.quit(); sys.exit()

        pygame.display.update()
        clock.tick(30)

if __name__ == "__main__":
    main_menu()