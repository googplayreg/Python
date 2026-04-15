import pygame
from player import MusicPlayer  # Импортируем класс из соседнего файла

# 1. Инициализация Pygame
pygame.init()

# Настройки окна
WIDTH, HEIGHT = 600, 450
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Music Player with Keyboard Controller")

# Цвета
WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
GREEN = (0, 255, 127)
GRAY = (150, 150, 150)

# Шрифты (используем стандартный системный шрифт)
font_large = pygame.font.SysFont("Arial", 28, bold=True)
font_medium = pygame.font.SysFont("Arial", 20)
font_small = pygame.font.SysFont("Arial", 16)

def draw_text(text, font, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

# 2. Создаем экземпляр плеера
# Передаем название папки с музыкой
player = MusicPlayer("music")

clock = pygame.time.Clock()
running = True

# --- ГЛАВНЫЙ ЦИКЛ ---
while running:
    screen.fill(BLACK)
    
    # А. Обработка событий (Клавиатура)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                # Если музыка еще не запускалась — запускаем
                if not player.is_playing:
                    player.play()
                else:
                    # Если уже играет или на паузе — переключаем состояние
                    player.toggle_pause()
            elif event.key == pygame.K_s: # Stop
                player.stop()
            elif event.key == pygame.K_RIGHT: # Next
                player.next_track()
            elif event.key == pygame.K_LEFT: # Back (Previous)
                player.previous_track()
            elif event.key == pygame.K_UP:
                player.change_volume(0.05) # Прибавляем 5%
            elif event.key == pygame.K_DOWN:
                player.change_volume(-0.05) # Убавляем 5%
            elif event.key == pygame.K_q: # Quit
                running = False

    # Б. Получение данных для отображения
    current_track = player.get_current_track_name()
    status_text = "Playing" if player.is_playing else "Stoped"
    
    # Получаем текущую позицию (в секундах)
    # get_pos() дает мс с начала текущего трека
    pos_ms = pygame.mixer.music.get_pos()
    pos_sec = max(0, pos_ms // 1000) 

    # В. Отрисовка UI
    # Заголовок
    draw_text("MUSIC PLAYER", font_large, GREEN, 200, 30)
    
    # Информация о треке
    pygame.draw.rect(screen, (40, 40, 40), (40, 90, 520, 100), border_radius=10)
    draw_text(f"Now playing:", font_small, GRAY, 60, 105)
    draw_text(current_track, font_medium, WHITE, 60, 135)
    
    # Статус и время
    draw_text(f"Status: {status_text}", font_small, GREEN if player.is_playing else GRAY, 60, 210)
    draw_text(f"Time: {pos_sec} sec.", font_small, WHITE, 450, 210)

    # Параметры полоски громкости
    vol_bar_x = 400
    vol_bar_y = 330
    vol_bar_width = 150
    vol_bar_height = 15
    
    # Рисуем блок громкости
    draw_text(f"Громкость: {round(player.volume * 100)}%", font_small, GRAY, vol_bar_x, vol_bar_y - 25)
    # Рисуем фон полоски (серый)
    pygame.draw.rect(screen, (60, 60, 60), (vol_bar_x, vol_bar_y, vol_bar_width, vol_bar_height), border_radius=5)
    
    # Рисуем заполненную часть (зеленый)
    # Ширина заполнения зависит от текущей громкости
    current_vol_width = vol_bar_width * player.volume
    pygame.draw.rect(screen, GREEN, (vol_bar_x, vol_bar_y, current_vol_width, vol_bar_height), border_radius=5)
    
    # Панель управления (подсказки)
    y_hint = 260
    hints = [
        "P - Play/Pause (Играть/Пауза)",
        "S - Stop (Стоп)", 
        "Right - Next (Следующий)", 
        "Left - Back (Предыдущий)",
        "Up - Louder (Громче)",
        "Down - Quieter (Тише)",
        "Q - Quit (Выход)"
    ]
    
    for hint in hints:
        draw_text(hint, font_small, GRAY, 60, y_hint)
        y_hint += 25

    pygame.display.flip()
    clock.tick(30) # 30 кадров в секунду

pygame.quit()