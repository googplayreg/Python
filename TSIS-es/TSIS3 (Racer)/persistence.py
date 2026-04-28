import json
import os

# Получаем путь к папке, где лежит этот main.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Теперь указываем пути к json относительно этой папки
# (Передай эти пути в функции загрузки/сохранения в persistence.py)
SETTINGS_FILE = os.path.join(BASE_DIR, "settings.json")
LEADERBOARD_FILE = os.path.join(BASE_DIR, "leaderboard.json")
# Пути к файлам данных
# SETTINGS_FILE = 'TSIS-es/TSIS3 (Racer)/settings.json'
# LEADERBOARD_FILE = 'TSIS-es/TSIS3 (Racer)/leaderboard.json'

# Настройки по умолчанию, если файлов еще нет
DEFAULT_SETTINGS = {
    "music_volume": 0.5,
    "music_track": "Track 1",
    "car_image": "TSIS-es/TSIS3 (Racer)/assets/player1.png",
    "difficulty": "Medium",
    "username": "Player"
}

def load_settings():
    """Загружает настройки из JSON или возвращает стандартные."""
    if not os.path.exists(SETTINGS_FILE):
        return DEFAULT_SETTINGS.copy()
    try:
        with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return DEFAULT_SETTINGS.copy()

def save_settings(settings):
    """Сохраняет текущие настройки в файл."""
    with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
        json.dump(settings, f, indent=4, ensure_ascii=False)

def load_leaderboard():
    """Загружает список рекордов."""
    if not os.path.exists(LEADERBOARD_FILE):
        return []
    try:
        with open(LEADERBOARD_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

def save_leaderboard(leaderboard_data):
    """
    Принимает список словарей, сортирует по очкам (score) 
    и сохраняет только ТОП-10.
    """
    # Сортировка по убыванию очков
    leaderboard_data.sort(key=lambda x: x.get('score', 0), reverse=True)
    top_10 = leaderboard_data[:10]
    
    with open(LEADERBOARD_FILE, 'w', encoding='utf-8') as f:
        json.dump(top_10, f, indent=4, ensure_ascii=False)

def add_new_score(username, score, distance):
    """Утилита для быстрого добавления нового результата."""
    data = load_leaderboard()
    data.append({
        "name": username,
        "score": score,
        "distance": int(distance)
    })
    save_leaderboard(data)