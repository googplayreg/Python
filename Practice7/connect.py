import psycopg2
from config import load_config

def get_connection():
    # Устанавливает и возвращает активное соединение с базой данных 
    try:
        # Получаем словарик с настройками из файла config.py 
        db_config = load_config()

        # Распаковываем словарь и подключаемся
        conn = psycopg2.connect(**db_config)
        return conn

    except Exception as e:
        print(f"Ошибка подключения к БД: {e}")
        return None