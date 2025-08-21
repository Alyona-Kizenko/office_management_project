# Office Management Django Project

Проект для управления рабочими местами и сотрудниками.

## � Функциональность

- **Приложение workplaces**: Управление рабочими местами
- **Приложение employees**: Управление сотрудниками
- **Админ-панель**: Полное управление данными
- **Форматирование кода**: Black и Isort

## � Установка

1. Клонируйте репозиторий
2. Создайте виртуальное окружение:
   ```bash
   python -m venv venv
   source venv/Scripts/activate  # Git Bash
   ```
3. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```
4. Примените миграции:
   ```bash
   python manage.py migrate
   ```
5. Создайте суперпользователя:
   ```bash
   python manage.py createsuperuser
   ```
6. Запустите сервер:
   ```bash
   python manage.py runserver
   ```

## �️ Использованные инструменты

- **Django 4.2.7** - веб-фреймворк
- **Black** - форматирование кода
- **Isort** - сортировка импортов

## � Структура проекта

```
office_management_project/
├── office_management/     # Главный проект
├── workplaces/           # Рабочие места
├── employees/           # Сотрудники
├── manage.py           # Управляющий скрипт
├── requirements.txt    # Зависимости
├── .gitignore         # Игнорируемые файлы
└── README.md          # Документация
```

## � Команды разработки

```bash
# Форматирование кода
black .
isort .

# Проверка форматирования
black --check .
isort --check-only .

# Миграции
python manage.py makemigrations
python manage.py migrate
```

## � Доступ

- Главная страница: http://127.0.0.1:8000/
- Админ-панель: http://127.0.0.1:8000/admin/

