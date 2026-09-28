# 7_django_rest_framework_habit_tracker

Курсовая работа. Трекер полезных привычек (Django REST Framework).

---

## Приложение доступно

- **Swagger**: http://158.160.85.251/api/docs/
- **Админка**: http://158.160.85.251/admin/

---

## Запуск через Docker

1. Создайте `.env` по примеру `.env.template`

2. Запустите:

   docker compose up -d --build

3. Приложение доступно:

   - **Swagger**: http://localhost/api/docs/
   - **Админка**: http://localhost/admin/

4. Создайте суперпользователя:

   docker compose exec web python manage.py createsuperuser

5. Остановка:

   docker compose down

---

## Локальный запуск

1. Установите зависимости:

   pip install -r requirements.txt

2. Примените миграции:

   python manage.py migrate

3. Запустите сервер:

   python manage.py runserver

4. Celery worker:

   celery -A habit_tracker worker -l info -P solo

5. Celery beat:

   celery -A habit_tracker beat -l info

---

## CI/CD

При push в `develop` GitHub Actions:

1. Запускает тесты
2. Запускает flake8
3. Собирает Docker-образ
4. Деплоит на сервер

### Секреты GitHub:

- `SERVER_IP`
- `SERVER_USER`
- `SSH_PRIVATE_KEY`

---

## Документация API

Полная документация — в Swagger:

**http://158.160.85.251/api/docs/**

---

## Тесты

python manage.py test

---

## Автор

bezza8418