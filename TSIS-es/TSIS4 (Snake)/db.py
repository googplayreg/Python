import psycopg2
from config import DB_CONFIG

def get_connection():
    """Создает подключение, используя данные из config.py"""
    try:
        conn = psycopg2.connect(**DB_CONFIG) # Распаковываем словарь с данными
        return conn
    except Exception as e:
        print(f"Ошибка подключения к БД: {e}")
        return None

def init_db():
    """Создает таблицы согласно ТЗ"""
    conn = get_connection()
    if not conn: return
    
    try:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS players (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL
                );
                CREATE TABLE IF NOT EXISTS game_sessions (
                    id SERIAL PRIMARY KEY,
                    player_id INTEGER REFERENCES players(id),
                    score INTEGER NOT NULL,
                    level_reached INTEGER NOT NULL,
                    played_at TIMESTAMP DEFAULT NOW()
                );
            """)
        conn.commit()
    except Exception as e:
        print(f"Ошибка инициализации БД: {e}")
    finally:
        conn.close()

def save_score(username, score, level_reached):
    conn = get_connection()
    if not conn: return
    try:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO players (username) VALUES (%s) ON CONFLICT (username) DO UPDATE SET username = EXCLUDED.username RETURNING id;", (username,))
            player_id = cur.fetchone()[0]
            cur.execute("INSERT INTO game_sessions (player_id, score, level_reached) VALUES (%s, %s, %s);", (player_id, score, level_reached))
        conn.commit()
    except Exception as e:
        print(f"Ошибка сохранения: {e}")
    finally:
        conn.close()

def get_personal_best(username):
    conn = get_connection()
    if not conn: return 0
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT MAX(s.score) FROM game_sessions s
                JOIN players p ON s.player_id = p.id
                WHERE p.username = %s;
            """, (username,))
            res = cur.fetchone()
            return res[0] if res and res[0] else 0
    finally:
        conn.close()

def get_top_10():
    conn = get_connection()
    if not conn: return []
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT p.username, s.score, s.level_reached, s.played_at::date
                FROM game_sessions s
                JOIN players p ON s.player_id = p.id
                ORDER BY s.score DESC LIMIT 10;
            """)
            return cur.fetchall()
    finally:
        conn.close()