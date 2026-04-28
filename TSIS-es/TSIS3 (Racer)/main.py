import pygame
import sys
import time
import random
import persistence
import ui
import racer
import os
import tkinter as tk
from tkinter import simpledialog

def ask_username():
    root = tk.Tk()
    root.withdraw() # Скрываем основное окно tkinter
    name = simpledialog.askstring("Username", "Enter your name:", initialvalue=user_settings["username"])
    if name:
        user_settings["username"] = name
        persistence.save_settings(user_settings)
    root.destroy()

# Инициализация
pygame.init()
pygame.mixer.init()

# Загрузка настроек
user_settings = persistence.load_settings()

# Параметры окна (Дорога 800 + Боковая панель 300)
SCREEN_WIDTH = 1100
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pygame Racer Advanced (TSIS Edition)")
clock = pygame.time.Clock()

# Шрифты и UI
game_ui = ui.UI()

# --- ЗАГРУЗКА РЕСУРСОВ ---
bg_img = pygame.image.load("TSIS-es/TSIS3 (Racer)/assets/road.png").convert()
bg_img = pygame.transform.scale(bg_img, (800, SCREEN_HEIGHT))

available_cars = [
    "TSIS-es/TSIS3 (Racer)/assets/player1.png", 
    "TSIS-es/TSIS3 (Racer)/assets/player2.png", 
    "TSIS-es/TSIS3 (Racer)/assets/player3.png"
]

coin_imgs = {
    1: pygame.image.load("TSIS-es/TSIS3 (Racer)/assets/coin.png").convert_alpha(),
    5: pygame.image.load("TSIS-es/TSIS3 (Racer)/assets/big_coin.png").convert_alpha(),
    10: pygame.image.load("TSIS-es/TSIS3 (Racer)/assets/ultra_coin.png").convert_alpha()
}

powerup_imgs = {
    "nitro": pygame.image.load("TSIS-es/TSIS3 (Racer)/assets/nitro.png").convert_alpha(),
    "repair": pygame.image.load("TSIS-es/TSIS3 (Racer)/assets/repair.png").convert_alpha(),
    "shield": None # Щит рисуем кодом
}

hazard_imgs = {
    "oil": pygame.image.load("TSIS-es/TSIS3 (Racer)/assets/oil_spill.png").convert_alpha(),
    "pothole": pygame.image.load("TSIS-es/TSIS3 (Racer)/assets/pothole.png").convert_alpha(),
    "wall": pygame.image.load("TSIS-es/TSIS3 (Racer)/assets/obstacle.png").convert_alpha(),
    "bump": None # Лежачий полицейский рисуется кодом
}

enemy_imgs = [
    pygame.image.load("TSIS-es/TSIS3 (Racer)/assets/enemy1.png").convert_alpha(),
    pygame.image.load("TSIS-es/TSIS3 (Racer)/assets/enemy2.png").convert_alpha(),
    pygame.image.load("TSIS-es/TSIS3 (Racer)/assets/enemy3.png").convert_alpha(),
    pygame.image.load("TSIS-es/TSIS3 (Racer)/assets/enemy4.png").convert_alpha(),
    pygame.image.load("TSIS-es/TSIS3 (Racer)/assets/enemy5.png").convert_alpha()
]

crash_sound = pygame.mixer.Sound("TSIS-es/TSIS3 (Racer)/assets/crash.mp3")
# Музыкальные треки
tracks = {
    "Track 1": "TSIS-es/TSIS3 (Racer)/assets/wind warrior.mp3",
    "Track 2": "TSIS-es/TSIS3 (Racer)/assets/Axel F.mp3",
    "OFF": None
}

# --- ГЛОБАЛЬНЫЕ ПЕРЕМЕННЫЕ ИГРЫ ---
current_state = "MENU"
score = 0
distance = 0
coins_collected = 0
highscores = persistence.load_leaderboard()

# Параметры сложности (пункт 3.5.2)
difficulty_mods = {
    "Easy": {"speed": 7, "spawn_rate": 0.05},
    "Medium": {"speed": 10, "spawn_rate": 0.08},
    "Hard": {"speed": 13, "spawn_rate": 0.12}
}

def start_new_game():
    global score, distance, coins_collected, manager, player, bg_y1, bg_y2, enemy_speed, target_speed
    score = 0
    distance = 0
    coins_collected = 0
    bg_y1 = 0
    bg_y2 = -SCREEN_HEIGHT
    
    # Настройка скорости от сложности
    diff = user_settings["difficulty"]
    target_speed = difficulty_mods[diff]["speed"] # Запоминаем скорость (до ускорения или замедления)
    enemy_speed = difficulty_mods[diff]["speed"]
    
    manager = racer.EntityManager()
    player = racer.Player(user_settings["car_image"])
    manager.all_sprites.add(player)
    
    # Сразу создаем одну машину врага
    manager.create_enemy(enemy_imgs)
    
    # Музыка
    if user_settings["music_track"] != "OFF":
        pygame.mixer.music.load(tracks.get(user_settings["music_track"], "TSIS-es/TSIS3 (Racer)/assets/wind warrior.mp3"))
        pygame.mixer.music.play(-1)

# --- ОСНОВНОЙ ЦИКЛ ---
running = True
while running:
    mouse_pos = pygame.mouse.get_pos()
    events = pygame.event.get()
    mouse_up = False
    
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_up = True

    screen.fill((0, 0, 0))

    if current_state == "MENU":
        # Название
        game_ui.draw_text(screen, "SUPER RACER", (550, 120), game_ui.font_large, ui.GOLD, center=True)
        
        # Кнопки
        btn_name = ui.Button(425, 220, 250, 50, f"NAME: {user_settings['username']}", ui.GRAY, ui.GOLD)
        btn_play = ui.Button(425, 300, 250, 50, "PLAY", ui.GRAY, ui.RED)
        btn_leader = ui.Button(425, 380, 250, 50, "LEADERBOARD", ui.GRAY, ui.GOLD)
        btn_settings = ui.Button(425, 460, 250, 50, "SETTINGS", ui.GRAY, ui.RED)
        btn_exit = ui.Button(425, 540, 250, 50, "EXIT", ui.GRAY, ui.RED)
        
        # 2. Отрисовка и проверка наведения
        for btn in [btn_name, btn_play, btn_leader, btn_settings, btn_exit]:
            btn.check_hover(mouse_pos)
            btn.draw(screen, game_ui.font_small)
            
        # 3. Логика нажатий
        if btn_name.is_clicked(mouse_pos, mouse_up):
            ask_username() # Вызываем окно ввода, которое мы создали ранее
            
        if btn_play.is_clicked(mouse_pos, mouse_up):
            start_new_game()
            current_state = "PLAYING"

        if btn_leader.is_clicked(mouse_pos, mouse_up):
            current_state = "LEADERBOARD"
            
        if btn_settings.is_clicked(mouse_pos, mouse_up):
            current_state = "SETTINGS"
            
        if btn_exit.is_clicked(mouse_pos, mouse_up):
            running = False

    elif current_state == "PLAYING":
        base_diff_speed = difficulty_mods[user_settings["difficulty"]]["speed"]
        target_speed = base_diff_speed + (distance // 100) * 0.5
    
        # Чтобы игра не стала непроходимой, ставим лимит, например, 25
        target_speed = min(target_speed, 25)

        # 0. Плавное восстановление скорости (если наехали на кочку)
        if enemy_speed < target_speed:
            enemy_speed += 0.05
        elif enemy_speed > target_speed + 2: # Если мы летим на нитро
            pass # Не трогаем, пусть нитро само кончится
            
        # 1. Движение фона
        bg_y1 += enemy_speed * 0.8
        bg_y2 += enemy_speed * 0.8
        if bg_y1 >= SCREEN_HEIGHT: bg_y1 = bg_y2 - SCREEN_HEIGHT
        if bg_y2 >= SCREEN_HEIGHT: bg_y2 = bg_y1 - SCREEN_HEIGHT
        
        screen.blit(bg_img, (0, bg_y1))
        screen.blit(bg_img, (0, bg_y2))

        # 2. Обновление объектов
        distance += (enemy_speed / 60)
        player.move()
        manager.enemies.update(enemy_speed)
        manager.coins.update(enemy_speed * 0.8)
        manager.hazards.update(enemy_speed * 0.8)
        manager.powerups.update(enemy_speed * 0.8)
        
        # Спавн новых объектов (Вернули монеты в лимиты!)
        current_enemies = len(manager.enemies)
        current_hazards = len(manager.hazards)
        current_powerups = len(manager.powerups)
        current_coins = len(manager.coins)
        
        chance = random.random()
        if chance < 0.04: # Общий шанс появления чего-либо на кадр
            # Определяем, ЧТО именно может появиться, используя веса
            # Веса: Монеты(30), Враги(50), Препятствия(15), Бонусы(5)
            rand_val = random.randint(1, 100)

            if rand_val <= 50 and current_enemies < 2:
                # Спавн врага
                manager.create_enemy(enemy_imgs)
            
            elif 50 <= rand_val <= 80 and current_coins < 1:
                # Спавн монеты
                val = random.choice([1, 5, 10])
                img = coin_imgs.get(val)
                c = racer.RoadObject(img, "coin")
                c.value = val
                manager.coins.add(c)
                manager.all_sprites.add(c)
                
            elif 80 < rand_val <= 95 and current_hazards < 1:
                # Спавн препятствия (масло, яма и т.д.)
                h_type = random.choice(["oil", "pothole", "wall", "bump"])
                img = hazard_imgs.get(h_type)
                h = racer.RoadObject(img, h_type)
                manager.hazards.add(h)
                manager.all_sprites.add(h)
                
            elif rand_val > 95 and current_powerups < 1:
                # Спавн бонуса (самый редкий — всего 5% шанс из общих 4%)
                p_type = random.choice(["nitro", "shield", "repair"])
                img = powerup_imgs.get(p_type)
                p = racer.RoadObject(img, p_type)
                manager.powerups.add(p)
                manager.all_sprites.add(p)

        # 3. Обработка столкновений
        # С монетами
        collided_coin = pygame.sprite.spritecollideany(player, manager.coins)
        if collided_coin:
            score += collided_coin.value
            coins_collected += 1
            collided_coin.kill()
            
        # С усилителями
        collided_powerup = pygame.sprite.spritecollideany(player, manager.powerups)
        if collided_powerup:
            # Проверяем, свободен ли "слот" усилителя
            # Усилитель считается активным, если работает Нитро, есть Щит или Ремонт
            can_pickup = not (player.nitro_timer > time.time() or player.has_shield or player.has_repair)
            
            if can_pickup:
                if collided_powerup.type == "nitro":
                    player.apply_nitro()
                elif collided_powerup.type == "shield":
                    player.has_shield = True
                elif collided_powerup.type == "repair":
                    player.has_repair = True
                collided_powerup.kill() # Удаляем с дороги только если подобрали
            else:
                # Если слот занят, мы просто проезжаем сквозь него (или можно оставить на дороге)
                pass
            
        # С опасностями (масло, ямы, кочки)
        hazard = pygame.sprite.spritecollideany(player, manager.hazards)
        if hazard:
            if hazard.type == "oil":
                player.is_sliding = True
                player.slide_timer = time.time() + 1.5
            elif hazard.type == "bump":
                # Резкое замедление (эффект толчка). Скорость потом плавно восстановится (пункт 0)
                enemy_speed = 5 
            else: # wall или pothole
                if player.has_shield or player.has_repair:
                    if player.has_repair:
                        player.has_repair = False
                    else:
                        player.has_shield = False
                    hazard.kill()
                else:
                    current_state = "GAME_OVER"
                    crash_sound.play()

        # С врагами
        if pygame.sprite.spritecollideany(player, manager.enemies):
            if player.has_shield or player.has_repair:
                player.has_shield = False
                player.has_repair = False
                for e in manager.enemies: e.spawn() 
            else:
                current_state = "GAME_OVER"
                crash_sound.play()
                pygame.mixer.music.stop()
                persistence.add_new_score(user_settings["username"], score, distance)
                highscores = persistence.load_leaderboard()

        # 4. Отрисовка
        for sprite in manager.all_sprites:
            if hasattr(sprite, 'draw'):
                sprite.draw(screen)
            else:
                screen.blit(sprite.image, sprite.rect)

        player.draw_effects(screen)
        
        # Боковая панель
        status_name = "None"
        is_active = False
        timer_val = 0
        
        if player.nitro_timer > time.time():
            status_name = "NITRO"
            is_active = True
            timer_val = int(player.nitro_timer - time.time())
        elif player.has_shield:
            status_name = "SHIELD"
            is_active = True
        elif player.has_repair:
            status_name = "REPAIR (Life)"
            is_active = True
            
        p_status = {"active": is_active, "name": status_name, "time": timer_val}
        ui.draw_sidebar(screen, game_ui, score, distance, coins_collected, p_status, highscores)

    elif current_state == "LEADERBOARD":
        game_ui.draw_text(screen, "TOP 10 RACERS", (550, 80), game_ui.font_large, ui.GOLD, center=True)
        
        # Отображаем заголовки
        game_ui.draw_text(screen, "NAME          SCORE          DIST", (550, 160), game_ui.font_small, ui.WHITE, center=True)
        
        # Рисуем топ-10
        for i, entry in enumerate(highscores[:10]):
            txt = f"{i+1}. {entry['name'][:10]:<10} {int(entry['score']):<10} {int(entry['distance'])}m"
            game_ui.draw_text(screen, txt, (550, 200 + i*40), game_ui.font_small, ui.WHITE, center=True)
            
        btn_back = ui.Button(425, 650, 250, 50, "BACK", ui.GRAY, ui.RED)
        btn_back.check_hover(mouse_pos)
        btn_back.draw(screen, game_ui.font_small)
        
        if btn_back.is_clicked(mouse_pos, mouse_up):
            current_state = "MENU"

    elif current_state == "SETTINGS":
        # Экран настроек - упрощенная логика переключения
        game_ui.draw_text(screen, "SETTINGS", (550, 100), game_ui.font_large, ui.GOLD, center=True)
        
        # Сохраняем имена файлов
        current_car_name = os.path.basename(user_settings['car_image'])
        current_track_name = os.path.basename(user_settings['music_track'])
        
        btn_diff = ui.Button(425, 220, 250, 50, f"Diff: {user_settings['difficulty']}", ui.GRAY, ui.GOLD)
        btn_car  = ui.Button(425, 300, 250, 50, f"Car: {current_car_name}", ui.GRAY, ui.GOLD)
        btn_mus  = ui.Button(425, 380, 250, 50, f"Music: {current_track_name}", ui.GRAY, ui.GOLD)
        btn_back = ui.Button(425, 550, 250, 50, "SAVE & BACK", ui.GRAY, ui.RED)
        
        for btn in [btn_diff, btn_car, btn_mus, btn_back]:
            btn.check_hover(mouse_pos)
            btn.draw(screen, game_ui.font_small)

        if btn_diff.is_clicked(mouse_pos, mouse_up):
            # Переключение сложности по кругу
            levels = ["Easy", "Medium", "Hard"]
            idx = (levels.index(user_settings["difficulty"]) + 1) % 3
            user_settings["difficulty"] = levels[idx]

        if btn_car.is_clicked(mouse_pos, mouse_up):
            # Находим индекс текущей машины и переключаем на следующую
            current_idx = available_cars.index(user_settings["car_image"])
            next_idx = (current_idx + 1) % len(available_cars)
            user_settings["car_image"] = available_cars[next_idx]

        if btn_mus.is_clicked(mouse_pos, mouse_up):
            # Переключение треков: Track 1 -> Track 2 -> OFF
            track_list = ["Track 1", "Track 2", "OFF"]
            curr_mus = user_settings["music_track"]
            idx = (track_list.index(curr_mus) + 1) % 3
            user_settings["music_track"] = track_list[idx]
            # Сразу применяем музыку (стоп или смена)
            if user_settings["music_track"] == "OFF":
                pygame.mixer.music.stop()
            else:
                pygame.mixer.music.load(tracks[user_settings["music_track"]])
                pygame.mixer.music.play(-1)
            
        if btn_back.is_clicked(mouse_pos, mouse_up):
            persistence.save_settings(user_settings)
            pygame.mixer.music.stop()
            current_state = "MENU"

    elif current_state == "GAME_OVER":
        game_ui.draw_text(screen, "GAME OVER", (400, 200), game_ui.font_large, ui.RED, center=True)
        
        # Отрисовка статистики справа
        ui.draw_sidebar(screen, game_ui, score, distance, coins_collected, {"active":False, "name":"-", "time":0}, highscores)
        
        btn_retry = ui.Button(300, 350, 250, 50, "RETRY", ui.GRAY, ui.GOLD)
        btn_menu = ui.Button(300, 430, 250, 50, "MAIN MENU", ui.GRAY, ui.GOLD)
        
        for btn in [btn_retry, btn_menu]:
            btn.check_hover(mouse_pos)
            btn.draw(screen, game_ui.font_small)
        
        if btn_retry.is_clicked(mouse_pos, mouse_up):
            start_new_game()
            current_state = "PLAYING"
            
        if btn_menu.is_clicked(mouse_pos, mouse_up):
            pygame.mixer.music.stop()
            current_state = "MENU"

    pygame.display.update()
    clock.tick(60)

pygame.quit()