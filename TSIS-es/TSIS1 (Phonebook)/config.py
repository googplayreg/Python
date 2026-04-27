import os
from dotenv import load_dotenv

def load_config():
    """Загружает параметры подключения из .env"""
    load_dotenv()
    return {
        "dbname": os.getenv("DB_NAME"),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASS"),
        "host": os.getenv("DB_HOST", "127.0.0.1"),
        "port": os.getenv("DB_PORT", "5432")
    }