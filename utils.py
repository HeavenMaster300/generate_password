def validate_length(length):
    """Проверяет, что длина пароля находится в допустимом диапазоне.

    Args:
        length (int): Длина пароля для проверки.

    Returns:
        bool: True, если длина от 8 до 128 включительно, иначе False.
    """
    return 8 <= length <= 128