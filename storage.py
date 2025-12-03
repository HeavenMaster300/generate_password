"""Модуль для работы с хранением паролей в PostgreSQL."""

from cryptography.fernet import Fernet
import os
from db import get_db_connection, init_database


def get_or_create_key(key_file="secret.key"):
    """Получает или создаёт ключ шифрования.

    Args:
        key_file (str): Имя файла с ключом шифрования.

    Returns:
        bytes: Ключ шифрования.
    """
    if os.path.exists(key_file):
        with open(key_file, "rb") as f:
            return f.read()
    else:
        key = Fernet.generate_key()
        with open(key_file, "wb") as f:
            f.write(key)
        return key


def encrypt_password(password, key):
    """Шифрует пароль с использованием Fernet.

    Args:
        password (str): Пароль в виде строки.
        key (bytes): Ключ шифрования.

    Returns:
        str: Зашифрованный пароль в base64.
    """
    fernet = Fernet(key)
    encrypted = fernet.encrypt(password.encode())
    return encrypted.decode()


def decrypt_password(encrypted_password, key):
    """Расшифровывает пароль.

    Args:
        encrypted_password (str): Зашифрованный пароль в base64.
        key (bytes): Ключ шифрования.

    Returns:
        str: Расшифрованный пароль.
    """
    fernet = Fernet(key)
    decrypted = fernet.decrypt(encrypted_password.encode())
    return decrypted.decode()


def save_password(password, service, username):
    """Сохраняет зашифрованный пароль в PostgreSQL.

    Args:
        password (str): Пароль для сохранения.
        service (str): Название сервиса (например, "GitHub", "Gmail").
        username (str): Имя пользователя для этого сервиса.

    Returns:
        None
    """
    # Инициализация БД (если таблицы нет)
    init_database()

    key = get_or_create_key()
    encrypted = encrypt_password(password, key)

    conn = get_db_connection()
    cur = conn.cursor()

    try:
        # Попытка вставки или обновления (UPSERT)
        cur.execute("""
            INSERT INTO passwords (service, username, password)
            VALUES (%s, %s, %s)
            ON CONFLICT (service, username) 
            DO UPDATE SET 
                password = EXCLUDED.password,
                updated_at = NOW();
        """, (service, username, encrypted))

        conn.commit()
        print(f"Пароль для {service} (пользователь: {username}) сохранён в базе данных")
    except Exception as e:
        conn.rollback()
        print(f"Ошибка сохранения: {e}")
    finally:
        cur.close()
        conn.close()


def get_password(service, username):
    """Получает расшифрованный пароль из PostgreSQL.

    Args:
        service (str): Название сервиса.
        username (str): Имя пользователя.

    Returns:
        dict or None: Словарь с данными о пароле, если найден, иначе None.
    """
    conn = get_db_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            SELECT service, username, password 
            FROM passwords 
            WHERE service = %s AND username = %s;
        """, (service, username))

        row = cur.fetchone()

        if row:
            key = get_or_create_key()
            encrypted_password = row[2]
            decrypted_password = decrypt_password(encrypted_password, key)

            result = {
                "service": row[0],
                "username": row[1],
                "password": decrypted_password
            }
            print(f"\n🔓 Найден пароль для {service} (пользователь: {username})")
            print(f"   Пароль: {decrypted_password}")
            return result
        else:
            print(f"Пароль для {service} (пользователь: {username}) не найден")
            return None
    except Exception as e:
        print(f"Ошибка получения пароля: {e}")
        return None
    finally:
        cur.close()
        conn.close()


def list_all_passwords():
    """Выводит список всех сохранённых записей из PostgreSQL без паролей.

    Returns:
        list: Список словарей с информацией о сервисах и пользователях.
    """
    conn = get_db_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            SELECT service, username, created_at 
            FROM passwords 
            ORDER BY created_at DESC;
        """)

        rows = cur.fetchall()

        if not rows:
            print("Нет сохранённых паролей")
            return []

        print("\nСохранённые пароли:")
        print("-" * 50)
        records = []
        for row in rows:
            record = {
                "service": row[0],
                "username": row[1]
            }
            records.append(record)
            print(f"  📌 {row[0]} | Пользователь: {row[1]}")

        print("-" * 50)
        print(f"Всего записей: {len(records)}")
        return records
    except Exception as e:
        print(f"Ошибка получения списка: {e}")
        return []
    finally:
        cur.close()
        conn.close()
