from cryptography.fernet import Fernet
import json
import os

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


def save_password(password, service, username, filename="passwords.json"):
    """Сохраняет зашифрованный пароль с информацией о сервисе и пользователе.

    Args:
        password (str): Пароль для сохранения.
        service (str): Название сервиса (например, "GitHub", "Gmail").
        username (str): Имя пользователя для этого сервиса.
        filename (str, optional): Имя файла для хранения. По умолчанию "passwords.json".

    Returns:
        None
    """
    key = get_or_create_key()
    encrypted = encrypt_password(password, key)

    data = {}
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)

    # Используем уникальный ключ: service_username
    record_key = f"{service}_{username}"
    data[record_key] = {
        "service": service,
        "username": username,
        "password": encrypted
    }

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print(f"Пароль для {service} (пользователь: {username}) сохранён в {filename}")


def get_password(service, username, filename="passwords.json"):
    """Получает расшифрованный пароль по сервису и имени пользователя.

    Args:
        service (str): Название сервиса.
        username (str): Имя пользователя.
        filename (str, optional): Имя файла с данными. По умолчанию "passwords.json".

    Returns:
        dict or None: Словарь с данными о пароле, если найден, иначе None.
    """
    if not os.path.exists(filename):
        print(f"Файл {filename} не найден")
        return None

    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)

    record_key = f"{service}_{username}"
    if record_key in data:
        key = get_or_create_key()
        encrypted_password = data[record_key]["password"]
        decrypted_password = decrypt_password(encrypted_password, key)

        result = {
            "service": data[record_key]["service"],
            "username": data[record_key]["username"],
            "password": decrypted_password
        }
        print(f"Найден пароль для {service} (пользователь: {username})")
        return result
    else:
        print(f"Пароль для {service} (пользователь: {username}) не найден")
        return None


def list_all_passwords(filename="passwords.json"):
    """Выводит список всех сохранённых записей без паролей.

    Args:
        filename (str, optional): Имя файла с данными. По умолчанию "passwords.json".

    Returns:
        list: Список словарей с информацией о сервисах и пользователях.
    """
    if not os.path.exists(filename):
        print(f"Файл {filename} не найден")
        return []

    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)

    records = []
    for key, value in data.items():
        records.append({
            "service": value["service"],
            "username": value["username"]
        })

    return records
