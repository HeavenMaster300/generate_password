import string
import unittest

from utils import validate_length
from generator import generate_password


class TestUtils(unittest.TestCase):
    # Проверяем, что валидные длины (границы и середина диапазона) проходят
    def test_validate_length_valid(self):
        self.assertTrue(validate_length(8))      # нижняя граница
        self.assertTrue(validate_length(16))     # типичное значение
        self.assertTrue(validate_length(128))    # верхняя граница

    # Проверяем, что невалидные длины корректно отклоняются
    def test_validate_length_invalid(self):
        self.assertFalse(validate_length(0))     # совсем маленькое
        self.assertFalse(validate_length(7))     # на 1 меньше нижней границы
        self.assertFalse(validate_length(129))   # на 1 больше верхней границы


class TestGeneratePassword(unittest.TestCase):
    # Проверяем, что длина сгенерированного пароля совпадает с запрошенной
    def test_password_length(self):
        pwd = generate_password(16, True, True, True, True)
        self.assertEqual(len(pwd), 16)

    # Проверяем, что при отсутствии выбранных наборов символов выбрасывается ValueError
    def test_password_requires_at_least_one_charset(self):
        with self.assertRaises(ValueError):
            generate_password(16, False, False, False, False)

    # Проверяем, что все символы пароля принадлежат допустимому набору
    def test_password_uses_only_allowed_characters(self):
        length = 20
        pwd = generate_password(length, True, True, True, True)
        allowed = (
            string.ascii_lowercase
            + string.ascii_uppercase
            + string.digits
            + string.punctuation
        )
        self.assertEqual(len(pwd), length)
        self.assertTrue(all(ch in allowed for ch in pwd))

    # Проверяем, что при включении цифр и строчных букв они реально присутствуют в пароле
    def test_password_contains_required_types(self):
        pwd = generate_password(20, False, True, False, True)
        self.assertTrue(any(ch in string.digits for ch in pwd))           # есть цифры
        self.assertTrue(any(ch in string.ascii_lowercase for ch in pwd))  # есть строчные


if __name__ == "__main__":
    # Точка входа для запуска только этого файла тестов
    unittest.main()
