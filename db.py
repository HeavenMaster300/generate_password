"""Модуль для работы с PostgreSQL."""

import psycopg2


def get_db_connection():
    """Создаёт подключение к базе PostgreSQL."""
    conn = psycopg2.connect(
        host="localhost",
        port="5432",
        database="passgen",   # только что созданная БД
        user="postgres",      # используем суперпользователя
        password="10022005b777b"  # ЗАМЕНИТЕ НА РЕАЛЬНЫЙ ПАРОЛЬ
    )
    return conn


def init_database():
    """Инициализирует базу данных: создаёт таблицу если её нет."""
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS passwords (
            id SERIAL PRIMARY KEY,
            service TEXT NOT NULL,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),
            updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),
            UNIQUE(service, username)
        );
    """)

    conn.commit()
    cur.close()
    conn.close()
