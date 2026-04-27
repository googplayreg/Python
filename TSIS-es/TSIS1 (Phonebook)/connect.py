import psycopg2
from config import load_config

def get_connection():
    """Создает объект соединения с БД"""
    try:
        config = load_config()
        return psycopg2.connect(**config)
    except Exception as e:
        print(f"Ошибка подключения: {e}")
        return None