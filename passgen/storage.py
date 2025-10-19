import hashlib
import json
import os


def hash_password(password):
    """
    Хэширует пароль с использованием SHA-256.
    """
    return hashlib.sha256(password.encode()).hexdigest()


def save_password(password, label, filename="passwords.json"):
    """
    Сохраняет хэш пароля с меткой в JSON-файл.
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
    """
    Ищет хэш пароля по метке.
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