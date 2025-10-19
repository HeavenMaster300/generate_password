# Генератор паролей CLI

Утилита для генерации безопасных паролей с поддержкой настройки длины, типов символов и сохранения хэшей паролей в файл.

## Установка
```bash
git clone https://github.com/HeavenMaster300/generate_password.git
cd password-generator
python -m passgen.main


python -m passgen.main --length 12 --special --digits --uppercase --lowercase
python -m passgen.main --save mypassword
python -m passgen.main --find mypassword