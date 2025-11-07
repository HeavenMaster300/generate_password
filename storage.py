import hashlib
import json
import os


def hash_password(password):
    """Хэширует пароль с использованием алгоритма SHA-256.

    Args:
        password (str): Пароль в виде строки.

    Returns:
        str: Хэш пароля в шестнадцатеричном формате (64 символа).
    """
    return hashlib.sha256(password.encode()).hexdigest()


def save_password(password, label, filename="passwords.json"):
    """Сохраняет хэш пароля с меткой в JSON-файл.

    Если файл уже существует — обновляет его, добавляя новую запись.
    Если метка уже есть — перезаписывает её.

    Args:
        password (str): Пароль для сохранения.
        label (str): Метка (название сервиса, аккаунта и т.п.).
        filename (str, optional): Имя файла для хранения. По умолчанию "passwords.json".

    Returns:
        None

    Side Effects:
        Создаёт или обновляет JSON-файл с хэшами паролей.
        Выводит сообщение о сохранении в консоль.
    """
    hashed = hash_password(password)
    data = {}
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)

    data[label] = {"hash": hashed}
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"Пароль для {label} сохранён в {filename}")


def find_password(label, filename="passwords.json"):
    """Ищет хэш сохранённого пароля по метке.

    Args:
        label (str): Метка, по которой нужно найти пароль.
        filename (str, optional): Имя файла с данными. По умолчанию "passwords.json".

    Returns:
        str or None: Хэш пароля, если найден, иначе None.

    Side Effects:
        Выводит сообщение в консоль о результате поиска.
    """
    if not os.path.exists(filename):
        print(f"Файл {filename} не найден")
        return None

    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)

    if label in data:
        print(f"Найден хэш пароля для {label}: {data[label]['hash']}")
        return data[label]["hash"]
    else:
        print(f"Пароль с меткой {label} не найден")
        return None