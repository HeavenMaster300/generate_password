def validate_length(length):
    """
    Проверяет, что длина пароля находится в допустимом диапазоне (8-128).
    """
    return 8 <= length <= 128