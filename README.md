[![Quality gate status](https://sonarcloud.io/api/project_badges/measure?project=mileevamaria_finance-accounting-exp&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=mileevamaria_finance-accounting-exp)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=mileevamaria_finance-accounting-exp&metric=coverage)](https://sonarcloud.io/summary/new_code?id=mileevamaria_finance-accounting-exp)
[![CI](https://github.com/mileevamaria/finance-accounting-exp/actions/workflows/python-app.yml/badge.svg)](https://github.com/mileevamaria/finance-accounting-exp/actions/workflows/python-app.yml)

# Finance Accounting Platform

Backend-платформа для управленческого финансового учета.

Приложение предназначено для учета финансовых операций компании, управления счетами, статьями операций и проектами, а также формирования управленческой отчетности.

Проект построен на асинхронном стеке Python и PostgreSQL с разделением приложения на API, сервисный и репозиторный слои.

---

## Возможности

### Пользователи и аутентификация

- регистрация пользователей;
- авторизация;
- JWT access и refresh токены;
- обновление access-токена;
- защищенные API-эндпоинты;
- хеширование паролей;
- dummy hash для защиты от определения существования пользователя по времени ответа.

### Управленческий учет

Платформа поддерживает:

- компании;
- финансовые счета;
- финансовые операции;
- статьи операций;
- группы статей;
- проекты;
- оплата подписки.

### Отчетность

- P&L по категориям;
- P&L по группам категорий;
- P&L по проектам;
- Cash Flow по месяцам.

### Платежи и подписки

Реализована интеграция с платежной системой YooKassa.

- создание платежей;
- обработка webhook-уведомлений;
- управление статусом подписки;
- синхронизация состояния подписки с платежной системой;
- защита от повторной обработки одного платежного события.

### WebSocket

Для передачи изменений в реальном времени.

Поддерживаются уведомления об изменении:

- операций;
- счетов;
- проектов;
- категорий;
- подписки.

---

## Установка

### Требования

Для запуска проекта необходимы:

- Python 3.13+
- PostgreSQL
- uv

### Клонирование репозитория

```bash
git clone <URL-репозитория>
cd finance-accounting-exp
```

### Установка зависимостей

```bash
make install
```

или:

```bash
uv sync
```

---

## Настройка окружения

Создайте файл `.env` в корне проекта. Пример переменных окружения в файле [`.env.example`](https://github.com/mileevamaria/finance-accounting-exp/blob/main/.env.example)

---

## База данных

Создайте базы данных PostgreSQL:

```sql
CREATE DATABASE finance;
CREATE DATABASE finance_test;
```

Примените миграции:

```bash
make migrate
```

или:

```bash
uv run alembic upgrade head
```

---

## Запуск

Запустите приложение в режиме разработки:

```bash
make run
```

или:

```bash
uv run uvicorn app.main:app --reload
```

После запуска API доступно по адресу:

```text
http://localhost:8000
```

Swagger UI:

```text
http://localhost:8000/docs
```
---

## Технологический стек

### Backend

- **Python 3.13**
- **FastAPI**
- **Pydantic v2**

### Работа с базой данных

- **PostgreSQL**
- **SQLAlchemy 2.0**
- **asyncpg**
- **Alembic**

### Асинхронность

Приложение использует асинхронную модель выполнения:

- `asyncio`;
- async endpoints FastAPI;
- `AsyncSession` SQLAlchemy;
- асинхронные репозитории и сервисы;
- `asyncpg` для взаимодействия с PostgreSQL.

### Аутентификация и безопасность

- JWT;
- `pwdlib`;
- хеширование паролей;
- access / refresh tokens;
- dummy hash.

### Тестирование

- pytest;
- pytest-asyncio;
- HTTPX;
- FastAPI TestClient;
- pytest-cov.

### Инструменты разработки

- uv;
- Makefile;
- Ruff;
- GitHub Actions;
- SonarQube.

---

## Архитектура

Проект построен по принципу разделения ответственности между слоями:

```text
                    ┌───────────────┐
                    │     Client    │
                    └───────┬───────┘
                            │
                            ▼
                    ┌───────────────┐
                    │   FastAPI     │
                    │    API        │
                    └───────┬───────┘
                            │
                            ▼
                    ┌───────────────┐
                    │    Services   │
                    │  бизнес-логика│
                    └───────┬───────┘
                            │
                            ▼
                    ┌───────────────┐
                    │ Repositories  │
                    │  работа с БД  │
                    └───────┬───────┘
                            │
                            ▼
                    ┌───────────────┐
                    │  PostgreSQL   │
                    └───────────────┘
