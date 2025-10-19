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