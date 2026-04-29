import json
import os
from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()

# --- Параметры БД (Секретные) ---
DB_CONFIG = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASS"),
    "host": os.getenv("DB_HOST", "127.0.0.1"),
    "port": os.getenv("DB_PORT", "5432")
}

# --- Цвета ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (40, 40, 40)
DARK_GRAY = (20, 20, 20)
RED = (213, 50, 80)        # Еда +1
ORANGE = (255, 165, 0)     # Еда +2
GOLD = (255, 215, 0)       # Еда +3
DARK_RED = (139, 0, 0)     # Яд (Poison)
BLUE = (0, 100, 255)       # Power-up: Щит
CYAN = (0, 255, 255)       # Power-up: Ускорение
PURPLE = (128, 0, 128)     # Power-up: Замедление
BROWN = (139, 69, 19)      # Препятствия (Стены)
YELLOW = (255, 255, 102)

# --- Геометрия окна и поля ---
GRID_SIZE = 20
COLS, ROWS = 30, 30
PLAY_WIDTH = COLS * GRID_SIZE   # 600
PLAY_HEIGHT = ROWS * GRID_SIZE  # 600

PADDING = 20
SIDEBAR_WIDTH = 250

WINDOW_WIDTH = PLAY_WIDTH + SIDEBAR_WIDTH + (PADDING * 3) # 890
WINDOW_HEIGHT = PLAY_HEIGHT + (PADDING * 2)               # 640

FIELD_X = PADDING
FIELD_Y = PADDING

# --- Настройки пользователя (JSON) ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SETTINGS_FILE = os.path.join(BASE_DIR, "settings.json")

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, 'r') as f:
                return json.load(f)
        except:
            pass
    return {"snake_color": [0, 255, 0], "grid_overlay": True, "sound": True}

def save_settings(settings_dict):
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(settings_dict, f, indent=4)

USER_SETTINGS = load_settings()