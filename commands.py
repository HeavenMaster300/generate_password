"""Модуль для обработки командной строки и взаимодействия с генератором и хранилищем."""

import argparse
from generator import generate_password
from storage import save_password, get_password, list_all_passwords


def setup_parser():
    """Создаёт и настраивает парсер аргументов командной строки.

    Returns:
        argparse.ArgumentParser: Настроенный парсер с поддержкой всех флагов.
    """
    parser = argparse.ArgumentParser(description="Генератор безопасных паролей")
    parser.add_argument("--length", type=int, default=12, help="Длина пароля (8-128)")
    parser.add_argument("--special", action="store_true", help="Использовать спецсимволы")
    parser.add_argument("--digits", action="store_true", help="Использовать цифры")
    parser.add_argument("--uppercase", action="store_true", help="Использовать заглавные буквы")
    parser.add_argument("--lowercase", action="store_true", help="Использовать строчные буквы")
    parser.add_argument("--save", action="store_true", help="Сохранить сгенерированный пароль")
    parser.add_argument("--service", type=str, help="Название сервиса для сохранения/поиска пароля")
    parser.add_argument("--username", type=str, help="Имя пользователя для сервиса")
    parser.add_argument("--find", action="store_true", help="Найти пароль по сервису и пользователю")
    parser.add_argument("--list", action="store_true", help="Показать список всех сохранённых паролей")
    return parser


def run_cli():
    """Запускает CLI: обрабатывает аргументы и выполняет нужные действия.

    Поддерживает:
    - Генерацию пароля с кастомизацией символов
    - Сохранение пароля по сервису и имени пользователя
    - Поиск сохранённого пароля по сервису и пользователю
    - Вывод списка всех сохранённых паролей

    Returns:
        None
    """
    parser = setup_parser()
    args = parser.parse_args()

    # Показать список всех паролей
    if args.list:
        list_all_passwords()
        return

    # Найти пароль
    if args.find:
        if not args.service or not args.username:
            print("Ошибка: для поиска пароля необходимо указать --service и --username")
            return
        get_password(args.service, args.username)
        return

    # Генерация пароля
    try:
        password = generate_password(
            args.length,
            args.special,
            args.digits,
            args.uppercase,
            args.lowercase
        )
        print(f"Сгенерирован пароль: {password}")

        # Сохранение пароля
        if args.save:
            if not args.service or not args.username:
                print("Ошибка: для сохранения пароля необходимо указать --service и --username")
                return
            save_password(password, args.service, args.username)
    except ValueError as e:
        print(f"Ошибка: {str(e)}")
