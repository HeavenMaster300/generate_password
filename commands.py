"""Модуль для обработки командной строки и взаимодействия с генератором и хранилищем."""

import argparse
from generator import generate_password
from storage import save_password, find_password


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
    parser.add_argument("--save", type=str, help="Сохранить пароль с указанной меткой")
    parser.add_argument("--find", type=str, help="Найти пароль по метке")
    return parser


def run_cli():
    """Запускает CLI: обрабатывает аргументы и выполняет нужные действия.

    Поддерживает:
    - Генерацию пароля с кастомизацией символов
    - Сохранение пароля по метке
    - Поиск сохранённого пароля по метке

    Returns:
        None
    """
    parser = setup_parser()
    args = parser.parse_args()

    if args.find:
        find_password(args.find)
        return

    try:
        password = generate_password(
            args.length,
            args.special,
            args.digits,
            args.uppercase,
            args.lowercase
        )
        print(f"Сгенерирован пароль: {password}")

        if args.save:
            save_password(password, args.save)
    except ValueError as e:
        print(f"Ошибка: {str(e)}")