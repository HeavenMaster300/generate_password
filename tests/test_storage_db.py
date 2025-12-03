import unittest

from db import get_db_connection, init_database
from storage import (
    get_or_create_key,
    encrypt_password,
    decrypt_password,
    save_password,
    get_password,
    list_all_passwords,
)

# Тестовые значения, чтобы не мешать реальным данным
TEST_SERVICE = "test_service"
TEST_USER = "test_user"


class TestDatabaseAndStorage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Один раз перед всеми тестами: гарантируем, что таблица passwords создана
        init_database()

    def setUp(self):
        # Перед каждым тестом чистим только нашу тестовую запись
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "DELETE FROM passwords WHERE service = %s AND username = %s",
            (TEST_SERVICE, TEST_USER),
        )
        conn.commit()
        cur.close()
        conn.close()

    # Проверяем, что ключ шифрования создаётся один раз и дальше возвращается тот же самый
    def test_get_or_create_key_idempotent(self):
        key1 = get_or_create_key()
        key2 = get_or_create_key()
        self.assertEqual(key1, key2)

    # Проверяем, что после шифрования и расшифровки получаем исходный пароль
    def test_encrypt_decrypt_roundtrip(self):
        key = get_or_create_key()
        original = "MyS3cret_Pass!"
        encrypted = encrypt_password(original, key)
        self.assertIsInstance(encrypted, str)  # шифр хранится как строка
        decrypted = decrypt_password(encrypted, key)
        self.assertEqual(original, decrypted)

    # Проверяем полную цепочку: сохранение пароля в БД и чтение обратно
    def test_save_and_get_password(self):
        original_password = "TestPass123!"
        save_password(original_password, TEST_SERVICE, TEST_USER)
        result = get_password(TEST_SERVICE, TEST_USER)

        self.assertIsNotNone(result)                      # запись найдена
        self.assertEqual(result["service"], TEST_SERVICE)
        self.assertEqual(result["username"], TEST_USER)
        self.assertEqual(result["password"], original_password)  # пароль совпадает

    # Проверяем, что сохранение с теми же service/username перезаписывает пароль
    def test_save_overwrites_existing(self):
        save_password("old_pass", TEST_SERVICE, TEST_USER)
        save_password("new_pass", TEST_SERVICE, TEST_USER)

        result = get_password(TEST_SERVICE, TEST_USER)
        self.assertEqual(result["password"], "new_pass")

    # Проверяем, что наша тестовая запись попадает в список list_all_passwords
    def test_list_all_passwords_contains_test_record(self):
        save_password("TestPass123!", TEST_SERVICE, TEST_USER)
        records = list_all_passwords()

        self.assertTrue(
            any(
                r["service"] == TEST_SERVICE and r["username"] == TEST_USER
                for r in records
            )
        )


if __name__ == "__main__":
    # Точка входа для отдельного запуска тестов хранилища/БД
    unittest.main()
