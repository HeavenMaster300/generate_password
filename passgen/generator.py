import random
import string
from utils import validate_length

def generate_password(length, use_special, use_digits, use_uppercase, use_lowercase):
    """
    Генерирует пароль на основе заданных параметров.
    """
    if not validate_length(length):
        raise ValueError("Длина пароля должна быть от 8 до 128 символов")

    chars = ""
    if use_lowercase:
        chars += string.ascii_lowercase
    if use_uppercase:
        chars += string.ascii_uppercase
    if use_digits:
        chars += string.digits
    if use_special:
        chars += string.punctuation

    if not chars:
        raise ValueError("Должен быть выбран хотя бы один тип символов")

    password = "".join(random.choice(chars) for _ in range(length))
    return password