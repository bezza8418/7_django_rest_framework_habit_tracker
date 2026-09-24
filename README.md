# 7_django_rest_framework_habit_tracker

Курсовая работа. Трекер полезных привычек (Django REST Framework).

---

## Технологии

- Python 3.12+
- Django 6.x
- Django REST Framework
- PostgreSQL
- Redis + Celery
- JWT (djangorestframework-simplejwt)
- drf-spectacular (документация)
- django-cors-headers (CORS)
- pytelegrambotapi (Telegram-бот)

---

## Установка и запуск

1. Клонируйте репозиторий:

   git clone https://github.com/bezza8418/7_django_rest_framework_habit_tracker.git
   cd 7_django_rest_framework_habit_tracker

2. Создайте виртуальное окружение и активируйте его:

   python -m venv venv
   venv\Scripts\activate

3. Установите зависимости:

   pip install -r requirements.txt

4. Создайте файл `.env` по примеру `.env.example`:

   DB_NAME=habit_tracker_db
   DB_USER=postgres
   DB_PASSWORD=your_password
   DB_HOST=localhost
   DB_PORT=5432
   SECRET_KEY=your-secret-key
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   REDIS_HOST=localhost
   REDIS_PORT=6379
   REDIS_DB=0
   TELEGRAM_BOT_TOKEN=your_bot_token

5. Создайте базу данных PostgreSQL:

   CREATE DATABASE habit_tracker_db;

6. Примените миграции:

   python manage.py migrate

7. Создайте суперпользователя:

   python manage.py createsuperuser

8. Запустите сервер:

   python manage.py runserver

9. Запустите Celery worker:

   celery -A habit_tracker worker -l info -P solo

10. Запустите Celery beat:

    celery -A habit_tracker beat -l info

---

## API Эндпоинты

| Метод | URL | Описание |
|-------|-----|----------|
| POST | `/api/register/` | Регистрация |
| POST | `/api/token/` | Получение JWT-токенов |
| POST | `/api/token/refresh/` | Обновление токена |
| GET/POST | `/api/habits/` | Список своих привычек / создание |
| GET/PUT/PATCH/DELETE | `/api/habits/{id}/` | CRUD привычки |
| GET | `/api/public-habits/` | Список публичных привычек |
| GET | `/api/docs/` | Swagger UI |
| GET | `/api/redoc/` | ReDoc |
| GET | `/api/schema/` | OpenAPI схема |

---

## Модель Habit

- `user` — создатель привычки
- `place` — место
- `time` — время
- `action` — действие
- `is_pleasant` — признак приятной привычки
- `linked_habit` — связанная привычка
- `periodicity` — периодичность (1–7 дней)
- `reward` — вознаграждение
- `duration` — время на выполнение (≤ 120 сек)
- `is_public` — признак публичности

---

## Валидаторы

- Нельзя одновременно `reward` и `linked_habit`
- `duration` ≤ 120 секунд
- В `linked_habit` только приятные привычки
- У приятной привычки нет `reward` и `linked_habit`
- Периодичность от 1 до 7 дней

---

## Права доступа

- Пользователь видит только свои привычки (CRUD)
- Публичные привычки — только просмотр
- Регистрация и токены — без авторизации

---

## Пагинация

- 5 привычек на страницу
- Параметр `?page=N`
- Параметр `?page_size=N` (макс. 50)

---

## Celery-задачи

| Задача | Расписание | Описание |
|--------|-----------|----------|
| `check_habits_for_reminders` | Каждую минуту | Проверяет привычки и отправляет напоминания в Telegram |

---

## Telegram-бот

Для работы бота нужен токен от `@BotFather`. Токен добавляется в `.env`.

---

## Тесты

python manage.py test

Покрытие: 86%

coverage run --source='.' manage.py test
coverage report

Отчёт: `coverage.txt`

---

## 📄 Лицензия
Проект разработан в учебных целях.

## 📞 Контакты
Автор: bezza8418